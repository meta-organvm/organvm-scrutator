# SOP-2026-04-26: Inquiry Dispatch Protocol

**SOP ID:** SOP-SCRUTATOR-003
**Effective Date:** 2026-04-26
**Status:** ACTIVE
**Version:** 1.0

---

## Purpose

This SOP establishes the protocol for dispatching identified gaps as formal research inquiries to praxis-perpetua. Every gap becomes a commission.

## Scope

Applies to all gaps identified through Gap Analysis Protocol (SOP-SCRUTATOR-002) that meet dispatch thresholds.

## Dispatch Criteria

| Condition | Action |
|-----------|--------|
| Gap severity = Critical | Dispatch immediately |
| Gap severity = High | Dispatch within 24h |
| Occurrences ≥ 3 | Dispatch regardless of severity |
| Gap has clear research question | Dispatch |

## Procedure

### Step 1: Prepare Inquiry

Generate inquiry ID: `INQ-YYYY-NNN`

Where:
- YYYY = current year
- NNN = sequential number (padded to 3 digits)

### Step 2: Format Inquiry

Create structured inquiry document:

```yaml
id: INQ-2026-001
title: "Investigation: [gap statement truncated to 80 chars]"
description: |
  Research Inquiry generated from Gap Analysis
  
  Source Gap: GAP-00123
  Category: UNKNOWN
  Severity: high
  Occurrences: 3
  
  Statement: [full gap statement]
  
  Evidence Sources:
  - [source 1]
  - [source 2]
  
  Research Question: [transformed from statement]
  
  Law of the Land: If there's no data or statistics to prove
  whichever answer is the best one, then it's an opportunity for
  studying and figuring it out.

priority: P1
status: proposed
source: organvm-scrutator
gap_id: GAP-00123
created_at: 2026-04-26T14:30:00Z
```

### Step 3: Write to Praxis Perpetua

Append to `praxis-perpetua/commissions/inquiry-log.yaml`:

```yaml
inquiries:
  - id: INQ-2026-001
    title: "Investigation: ..."
    description: |
      ...
    priority: P1
    status: proposed
    created_at: 2026-04-26T14:30:00Z
    source: organvm-scrutator
    gap_id: GAP-00123
```

### Step 4: Update Local Tracker

Append to `data/research/dispatches.jsonl`:

```json
{
  "id": "INQ-2026-001",
  "gap_id": "GAP-00123",
  "created_at": "2026-04-26T14:30:00Z",
  "status": "proposed"
}
```

### Step 5: Confirm Dispatch

- Log dispatch confirmation
- Update gap status to `dispatched`
- Set `commission_id` field

## Follow-Up

### Commission Status Tracking

| Status | Meaning |
|--------|---------|
| proposed | Created, awaiting review |
| commissioned | Accepted by SGO |
| in_progress | Active research |
| completed | Results delivered |
| archived | No longer active |

### Resolution Flow

1. **SGO accepts commission** → status = `commissioned`
2. **Research begins** → status = `in_progress`
3. **Results delivered** → status = `completed`
4. **Results integrated** → gap marked `RESOLVED`

## Quality Standards

- **No gap orphaned** — Every dispatched gap has a commission ID
- **Traceability** — gap_id → commission_id linkage maintained
- **Timeliness** — Critical gaps dispatch within 24 hours

## Batch Dispatch

For efficiency, batch dispatches can run weekly:

1. Collect all qualifying gaps
2. Generate batch inquiry package
3. Write all to inquiry-log.yaml
4. Update all gap statuses

---

**Author:** Claude (Hokage)
**Review Cycle:** Quarterly
**Next Review:** 2026-07-26