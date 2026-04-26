# SOP-2026-04-26: Gap Analysis Protocol

**SOP ID:** SOP-SCRUTATOR-002
**Effective Date:** 2026-04-26
**Status:** ACTIVE
**Version:** 1.0

---

## Purpose

This SOP establishes the protocol for identifying, categorizing, and prioritizing knowledge gaps in the ORGANVM system. Every gap is a research opportunity.

## Scope

Applies to all governance components that may contain unknown or unverified information.

## Gap Categories

| Category | Definition | Example |
|----------|------------|---------|
| **UNKNOWN** | System doesn't know this exists | "What is the blocking constraint on Stream Ω?" |
| **UNVERIFIED** | Known but not proven | "951 IRF items" (need verification) |
| **UNEXPLORED** | Known to exist but not studied | "2,834 unclassified documents" |

## Severity Levels

| Level | Criteria | Response Time |
|-------|----------|---------------|
| **Critical** | Security, blocking, P0 | Immediate |
| **High** | Significant system impact | 24 hours |
| **Medium** | Enhancement, P2 | 1 week |
| **Low** | Curiosity, P3 | 1 month |

## Procedure

### Step 1: Gap Detection

Gaps are identified through:

1. **Pattern scanning** — Regex search for:
   - `VACUUM:` markers
   - `???` unanswered questions
   - `TBD`, `to be determined`
   - `not yet implemented`

2. **Evidence verification** — Claims without sources

3. **Session analysis** — Unanswered questions from QuestionLedger

4. **Human report** — Explicit gap reporting

### Step 2: Gap Classification

For each detected gap:

1. **Extract statement** — What is unknown?
2. **Determine category** — UNKNOWN / UNVERIFIED / UNEXPLORED
3. **Assess severity** — Critical / High / Medium / Low
4. **Count occurrences** — How many times seen?
5. **Gather evidence** — List all sources

### Step 3: Gap Registration

Record in `data/research/gaps.jsonl`:

```json
{
  "id": "GAP-00123",
  "discovered_at": "2026-04-26T14:30:00Z",
  "statement": "What blocks Stream Ω execution?",
  "category": "UNKNOWN",
  "severity": "high",
  "occurrences": 1,
  "evidence_sources": ["session-2026-04-26.md"]
}
```

### Step 4: Research Priority Calculation

Priority = (severity_weight × 10) + (10 - min(occurrences × 2, 10))

| Priority | Score Range |
|----------|-------------|
| P0 | 0-14 |
| P1 | 15-24 |
| P2 | 25-34 |
| P3 | 35+ |

### Step 5: Research Dispatch

For P0/P1 gaps with ≥3 occurrences:

1. Generate research inquiry
2. Write to `praxis-perpetua/commissions/inquiry-log.yaml`
3. Update gap with `commission_id`

## Quality Standards

- **No gap left untriaged** — Every detected gap must be classified
- **Evidence required** — At least one source per gap
- **Timely dispatch** — P0 gaps dispatch within 24 hours

## Exceptions

- Duplicate gaps: Merge with existing, increment occurrence count
- False positives: Mark as `EXCLUDED` with reason

## Metrics

- Total gaps identified
- Gaps by category
- Gaps by severity
- Research dispatch rate
- Gap resolution rate

---

**Author:** Claude (Hokage)
**Review Cycle:** Quarterly
**Next Review:** 2026-07-26