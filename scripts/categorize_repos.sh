#!/usr/bin/env bash
# categorize_repos.sh — assign an `action` to each repo in the inventory.
#
# Reads:  ${SCRUTATOR_DATA:-data}/inventory/repos.jsonl
# Writes: ${SCRUTATOR_DATA:-data}/inventory/repos.categorized.jsonl
#
# Buckets (first match wins):
#   skip_already_target   - owner == "meta-organvm"
#   skip_no_admin         - admin != true
#   keep_on_profile       - personal repo matching profile-keep heuristic
#   defer_fork            - fork == true
#   rename_then_transfer  - basename collides with an existing meta-organvm/* repo
#   transfer_archived     - archived
#   transfer_private      - private, not archived
#   transfer_public       - public, not archived

set -euo pipefail

DATA_DIR="${SCRUTATOR_DATA:-data}/inventory"
IN="${DATA_DIR}/repos.jsonl"
OUT="${DATA_DIR}/repos.categorized.jsonl"
KEEP_FILE="${SCRUTATOR_PROFILE_KEEP:-scripts/profile_keep.txt}"

[[ -f "$IN" ]] || { echo "error: $IN not found; run scripts/inventory_repos.sh first" >&2; exit 1; }
[[ -f "$KEEP_FILE" ]] || { echo "error: $KEEP_FILE not found" >&2; exit 1; }

VIEWER=$(gh api /user --jq .login)

# Load profile-keep allowlist (newline-delimited basenames; ignore # comments and blanks).
KEEP_BASENAMES=$(grep -v '^[[:space:]]*#' "$KEEP_FILE" | grep -v '^[[:space:]]*$' | tr '\n' ',' | sed 's/,$//')

# Build the set of basenames already in meta-organvm (collision detection).
COLLIDE_SET=$(jq -rs '[.[] | select(.owner == "meta-organvm") | .full_name | split("/")[1]] | unique | join(",")' "$IN")

jq -c \
  --arg viewer "$VIEWER" \
  --arg keep_csv "$KEEP_BASENAMES" \
  --arg collide_csv "$COLLIDE_SET" \
  '
  ($keep_csv | split(",") | map(select(length>0))) as $keep
  | ($collide_csv | split(",") | map(select(length>0))) as $collide
  | (.full_name | split("/")[1]) as $base
  | . + {
      action: (
        if .owner == "meta-organvm" then "skip_already_target"
        elif (.admin // false) != true then "skip_no_admin"
        elif (.owner == $viewer)
             and (
               ($base == $viewer)
               or ($base == ($viewer + ".github.io"))
               or ($keep | index($base))
             )
          then "keep_on_profile"
        elif .fork == true then "defer_fork"
        elif ($collide | index($base)) then "rename_then_transfer"
        elif .archived == true then "transfer_archived"
        elif .private == true then "transfer_private"
        else "transfer_public"
        end
      )
    }
  ' "$IN" > "$OUT"

echo "Categorized $(wc -l < "$OUT" | tr -d ' ') repos -> $OUT" >&2
echo "" >&2
echo "Bucket counts:" >&2
jq -r '.action' "$OUT" | sort | uniq -c | sort -rn >&2
