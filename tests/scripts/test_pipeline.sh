#!/usr/bin/env bash
# test_pipeline.sh — end-to-end test of categorize_repos.sh, render_transfer_plan.sh,
# and execute_transfers.sh (dry-run only). Uses a fixture inventory; no GitHub access.
#
# Run from repo root: bash tests/scripts/test_pipeline.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIXTURE="${REPO_ROOT}/tests/scripts/fixtures/repos.jsonl"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

export SCRUTATOR_DATA="$WORK/data"
export SCRUTATOR_PROFILE_KEEP="${REPO_ROOT}/scripts/profile_keep.txt"
export SCRUTATOR_VIEWER="ajp41890"        # bypass `gh api /user`
export SCRUTATOR_TARGET_ORG="meta-organvm"

mkdir -p "$SCRUTATOR_DATA/inventory"
cp "$FIXTURE" "$SCRUTATOR_DATA/inventory/repos.jsonl"

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "PASS: $*"; }

# --- categorize ---
bash "${REPO_ROOT}/scripts/categorize_repos.sh" >/dev/null 2>&1 || fail "categorize_repos.sh exited non-zero"

CATEGORIZED="$SCRUTATOR_DATA/inventory/repos.categorized.jsonl"
[[ -f "$CATEGORIZED" ]] || fail "categorized output not written"

assert_action() {
  local full_name="$1" expected="$2" got
  got=$(jq -r --arg n "$full_name" 'select(.full_name == $n) | .action' "$CATEGORIZED")
  [[ "$got" == "$expected" ]] || fail "$full_name: expected $expected, got $got"
}

assert_action "meta-organvm/organvm-scrutator" "skip_already_target"
assert_action "organvm/organvm-engine"         "transfer_public"
assert_action "organvm/a-organvm"              "transfer_archived"
assert_action "ajp41890/ajp41890"              "keep_on_profile"
assert_action "ajp41890/resume"                "keep_on_profile"
assert_action "ajp41890/ajp41890.github.io"    "keep_on_profile"
assert_action "ajp41890/some-fork"             "defer_fork"
assert_action "organvm/organvm-scrutator"      "rename_then_transfer"
assert_action "someorg/observer-only"          "skip_no_admin"
pass "categorize_repos.sh: all 9 rows resolved to expected buckets"

# --- render ---
bash "${REPO_ROOT}/scripts/render_transfer_plan.sh" >/dev/null 2>&1 || fail "render_transfer_plan.sh exited non-zero"
PLAN="$SCRUTATOR_DATA/inventory/transfer-plan.md"
[[ -f "$PLAN" ]] || fail "transfer-plan.md not written"

grep -q "Target org:.*meta-organvm" "$PLAN" || fail "plan missing target org"
grep -q "Total repos inventoried:.*9" "$PLAN" || fail "plan missing total count"
grep -q "Rename-then-transfer" "$PLAN" || fail "plan missing rename section"
grep -q "Transfer — archived" "$PLAN" || fail "plan missing archived section"
grep -q "Keep on personal profile" "$PLAN" || fail "plan missing keep_on_profile section"
grep -q "organvm/organvm-scrutator" "$PLAN" || fail "plan missing collision row"
pass "render_transfer_plan.sh: all required sections + rows present"

# --- execute (dry-run only) ---
DRY_OUT=$(bash "${REPO_ROOT}/scripts/execute_transfers.sh" 2>&1)
echo "$DRY_OUT" | grep -q "DRY-RUN: gh repo rename organvm-scrutator-legacy --repo organvm/organvm-scrutator" \
  || fail "dry-run missing rename for collision row"
echo "$DRY_OUT" | grep -q "DRY-RUN: gh repo transfer organvm/organvm-scrutator-legacy meta-organvm" \
  || fail "dry-run missing transfer of renamed source"
echo "$DRY_OUT" | grep -q "DRY-RUN: gh repo transfer organvm/organvm-engine meta-organvm" \
  || fail "dry-run missing public transfer"
echo "$DRY_OUT" | grep -q "DRY-RUN: gh repo transfer organvm/a-organvm meta-organvm" \
  || fail "dry-run missing archived transfer"
# Sanity: skip buckets must NOT appear
if echo "$DRY_OUT" | grep -q "DRY-RUN.*ajp41890/ajp41890 "; then
  fail "dry-run wrongly included keep_on_profile row"
fi
if echo "$DRY_OUT" | grep -q "DRY-RUN.*some-fork"; then
  fail "dry-run wrongly included defer_fork row"
fi
pass "execute_transfers.sh: dry-run output matches expectations"

# --- transfer-log.jsonl integrity ---
LOG="$SCRUTATOR_DATA/inventory/transfer-log.jsonl"
[[ -f "$LOG" ]] || fail "transfer-log.jsonl not written"
DRY_COUNT=$(jq -c 'select(.outcome == "dry_run")' "$LOG" | wc -l | tr -d ' ')
# Expected: 1 rename + 1 transfer (for rename_then_transfer) + 1 archived + 0 private + 1 public = 4
[[ "$DRY_COUNT" == "4" ]] || fail "expected 4 dry_run log entries, got $DRY_COUNT"
pass "transfer-log.jsonl: 4 dry_run entries recorded"

# --- --only filter ---
LOG_BEFORE=$(wc -l < "$LOG" | tr -d ' ')
bash "${REPO_ROOT}/scripts/execute_transfers.sh" --only transfer_archived >/dev/null 2>&1
LOG_AFTER=$(wc -l < "$LOG" | tr -d ' ')
[[ $((LOG_AFTER - LOG_BEFORE)) == "1" ]] || fail "--only transfer_archived should add exactly 1 row, added $((LOG_AFTER - LOG_BEFORE))"
pass "execute_transfers.sh --only transfer_archived: filter respected"

echo ""
echo "All tests passed."
