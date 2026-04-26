# AGENTS.md — organvm-scrutator

## System Context

**Purpose:** Self-auditing governance system that scrutinizes itself
**Law of the Land:** Every unknown is a research opportunity

## Key Concepts

### Metabolic Model
- **Input Energy** = Questions + Suggestions
- **Output Energy** = Atoms + Completions
- **Efficiency** = Output / Input
- **States:** CATABOLIC (≥1.0), BALANCED (0.5-1.0), ANABOLIC (0-0.5), EXPLORING (0)

### Evidence Hierarchy
- **PROVEN** — Verified with data/sources
- **STUDIED** — Analyzed but unverified  
- **HYPOTHESIZED** — Theoretical, untested
- **UNKNOWN** — No data exists → Research commission

## Commands

```bash
# Scan and analyze
organvm-scrutator scan          # Scan all plans
organvm-scrutator questions     # Question analysis
organvm-scrutator suggestions   # Suggestion analysis
organvm-scrutator atoms         # Atom tracking
organvm-scrutator energy        # Metabolic metrics
organvm-scrutator gaps          # Gap identification
organvm-scrutator dispatch      # Dispatch to praxis-perpetua
organvm-scrutator stats         # Full overview

# Session tracking
source .env                     # Load environment
scrutator-session-start         # Start new session
scrutator-session-end 5 3 8 2   # End session (questions, suggestions, atoms, completions)
```

## Data Storage

| File | Purpose |
|------|---------|
| `data/raw/questions.jsonl` | Every question asked |
| `data/raw/suggestions.jsonl` | Every recommendation |
| `data/raw/atoms.jsonl` | Every work item |
| `data/raw/energy.jsonl` | Session metabolic records |
| `data/research/gaps.jsonl` | Identified gaps |
| `data/research/dispatches.jsonl` | Research dispatches |
| `data/indices/*.yaml` | Aggregated metrics |

## Integration Points

- **praxis-perpetua:** Writes research inquiries to `commissions/inquiry-log.yaml`
- **IRF:** Reads DONE-ID counter from `organvm-corpvs-testamentvm/data/done-id-counter.json`
- **seed.yaml:** Scans across all workspace repos

## Workflow

1. **Session Start:** `scrutator-session-start` → sets session ID + timestamp
2. **During Session:** Track questions, suggestions, atoms as they occur
3. **Session End:** Run `organvm-scrutator stats` → updates all indices
4. **Gap Analysis:** Run `organvm-scrutator gaps` → identifies research opportunities
5. **Dispatch:** Run `organvm-scrutator dispatch` → sends gaps to praxis-perpetua

## Priority Guidelines

- **P0 (Critical):** Security, blockers, emergencies — Immediate
- **P1 (High):** Significant impact — 24 hours
- **P2 (Medium):** Enhancement — 1 week
- **P3 (Low):** Future work — 1 month

---

*Every gap is a research opportunity. The system measures its own ignorance.*