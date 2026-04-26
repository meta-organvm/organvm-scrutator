# SOP-2026-04-26: Session Metrics Collection Protocol

**SOP ID:** SOP-SCRUTATOR-001
**Effective Date:** 2026-04-26
**Status:** ACTIVE
**Version:** 1.0

---

## Purpose

This SOP establishes the protocol for collecting session metrics during AI agent sessions. Every session produces data about uncertainty, hypothesis generation, and value delivery. This protocol ensures consistent, comprehensive capture.

## Scope

Applies to all AI agent sessions (Claude, Codex, Gemini, etc.) operating in the ORGANVM workspace.

## Procedure

### Pre-Session

1. **Initialize session context**
   ```bash
   export SCRUTATOR_SESSION_ID="$(date +%Y-%m-%d)-$(whoami)-$(head -c 4 /dev/urandom | xxd -p)"
   export SCRUTATOR_START_TIME=$(date -Iseconds)
   ```

2. **Clear previous session flags** (if any)

### During Session

3. **Track questions** — When using the `question` tool, append to session notes:
   - Question text
   - Context
   - Whether answered

4. **Track suggestions** — When making recommendations:
   - Suggestion text
   - Human response (accepted/rejected/modified)

5. **Track atoms created** — When work items emerge:
   - Atom type (plan, task, IRF item)
   - Priority
   - Link to source

### Post-Session (Close-Out)

6. **Calculate session energy**
   ```bash
   # Input: questions + suggestions
   # Output: atoms created + completions
   
   questions_asked=$(grep -c "question:" session.md 2>/dev/null || echo 0)
   suggestions_made=$(grep -c "suggestion:" session.md 2>/dev/null || echo 0)
   atoms_created=$(grep -c "atom:" session.md 2>/dev/null || echo 0)
   ```

7. **Record to ledgers**
   - Write to `questions.jsonl`
   - Write to `suggestions.jsonl`
   - Write to `atoms.jsonl`
   - Write to `energy.jsonl`

8. **Update governance-metrics.yaml**

9. **Check for research opportunities**
   - Any unanswered question with 3+ occurrences → gap
   - Gap with evidence → dispatch to praxis-perpetua

## Metrics Collected

| Metric | Description | Storage |
|--------|-------------|---------|
| Questions Asked | Count + text | questions.jsonl |
| Suggestions Made | Count + text + outcome | suggestions.jsonl |
| Atoms Created | Count + type + priority | atoms.jsonl |
| Completions | Count + atom IDs | completions.jsonl |
| Session Energy | Input/Output ratio | energy.jsonl |

## Quality Standards

- **Completeness:** All metrics MUST be captured
- **Accuracy:** Use exact counts, not estimates
- **Timeliness:** Record within 5 minutes of session end
- **Traceability:** Link to session ID

## Exceptions

- Brief status-check sessions (<5 min): Skip detailed tracking
- Emergency sessions: Capture minimal metrics, document reason

## Related SOPs

- SOP-SCRUTATOR-002: Gap Analysis Protocol
- SOP-SCRUTATOR-003: Inquiry Dispatch Protocol
- SOP-SCRUTATOR-004: Evidence Hierarchy Maintenance

---

**Author:** Claude (Hokage)
**Review Cycle:** Quarterly
**Next Review:** 2026-07-26