# ORGANVM SCRUTATOR — Core Research Document

**Document ID:** RESEARCH-001
**Created:** 2026-04-26
**Status:** FOUNDATIONAL
**Author:** Claude (Hokage)

---

## THE CORE PRINCIPLE (Law of the Land)

> **If there is no data or statistics to prove whichever answer is the best one, then it is an opportunity for studying and figuring it out.**

This is not a gap. This is a **research opportunity**. Every unknown is a commission. Every untested hypothesis is a pending inquiry.

---

## THEORETICAL FOUNDATION

### 1. Epistemology of Self-Governance

The ORGANVM Scrulator operates on a fundamental insight: **a self-governing system must measure its own ignorance**.

Traditional governance assumes knowledge. The Scrulator assumes ignorance—and builds measurement infrastructure around that assumption.

**Core Axioms:**

1. **Ignorance is Observable** — Every unknown manifests as a pattern (question, gap, unverified claim)
2. **Ignorance is Quantifiable** — Questions can be counted, gaps catalogued, claims classified
3. **Ignorance is Actionable** — Every unknown can become a research commission
4. **Research Closes Ignorance** — Systematic investigation converts unknowns to knowns

### 2. The Metabolic Model

The system is a metabolic organism. It consumes uncertainty (questions, suggestions) and produces clarity (atoms, completions).

```
Input Energy = Questions + Suggestions
Output Energy = Atoms + Completions

Efficiency = Output / Input

Metabolic States:
- CATABOLIC: Efficiency ≥ 1.0 (output > input, highly productive)
- BALANCED: 0.5 ≤ Efficiency < 1.0 (healthy learning)
- ANABOLIC: 0 < Efficiency < 0.5 (building phase)
- EXPLORING: Efficiency = 0 (pure discovery)
```

**Insight:** High input with low output is NOT failure. It's learning. The ratio reveals the system's learning rate.

### 3. Evidence Hierarchy

Every claim in the system must be classified by evidence level:

| Level | Definition | System Response |
|-------|------------|-----------------|
| **PROVEN** | Verified with data/sources | Trust, use |
| **STUDIED** | Analyzed but unverified | Flag for verification |
| **HYPOTHESIZED** | Theoretical, untested | Test, experiment |
| **UNKNOWN** | No data exists | Convert to research |

**Law Enforcement:** Every UNKNOWN becomes a research task. Every STUDIED claim is verified or archived.

---

## SYSTEM ARCHITECTURE

### The Four Ledgers

1. **Question Ledger** — Tracks every question asked
   - Count, text, context, answer status
   - Patterns reveal boundary conditions

2. **Suggestion Ledger** — Tracks recommendations
   - Acceptance, rejection, modification rates
   - By-agent analysis reveals alignment

3. **Atom Tracker** — Tracks work items
   - Creation, completion, blocking
   - Priority distribution

4. **Energy Ledger** — Tracks metabolic rate
   - Input vs output over time
   - System efficiency

### The Research Pipeline

```
GAP IDENTIFICATION → CLASSIFICATION → PRIORITIZATION → DISPATCH → TRACKING
      ↓                    ↓                  ↓               ↓           ↓
  Pattern Scan       Category Assign    Score Calc    praxis-perpetua  Commission
  Evidence Verify    Severity Level    Threshold      inquiry-log     Status
```

### The Feedback Loop

```
Research Commission → Investigation → Results → Evidence Update → Gap Resolution
                                                            ↓
                                                      System Learning
                                                            ↓
                                                      New Questions (cycle)
```

---

## INNOVATIVE MECHANISMS

### 1. Vacuum Radiation Detection

Every completion "radiates vacuums in all directions." When work completes:

- What adjacent work is now visible?
- What dependencies are unblocked?
- What questions does this answer?

**Implementation:** Post-completion scan for emergent gaps.

### 2. The Evidence Gap Index (EGI)

A composite score of system knowledge:

```
EGI = (Proven Claims / Total Claims) × 1.0
    + (Studied Claims / Total Claims) × 0.5
    + (Hypothesized Claims / Total Claims) × 0.25
    + (Unknowns → Research / Total Unknowns) × 0.5
```

EGI approaches 1.0 as system approaches omniscience. EGI of 0.5 = 50% of unknowns being studied.

### 3. Metabolic Drift Detection

Track efficiency over time:

- **Increasing efficiency:** System learning (good)
- **Stable efficiency:** Steady state (ok)
- **Decreasing efficiency:** System stress (investigate)

### 4. The Question Origination Index

Not all questions are equal. Track which questions lead to:
- Research dispatches
- System changes
- Knowledge creation

Questions that spawn research are high-value. Questions that don't may indicate misalignment.

---

## RESEARCH QUESTIONS (For Praxis Perpetua)

### RQ-1: Metabolic Baseline
**Question:** What is the natural metabolic rate of the ORGANVM system?
**Method:** Measure energy efficiency over 30 sessions
**Expected Output:** Baseline efficiency ratio + confidence interval

### RQ-2: Question Taxonomy
**Question:** Can questions be categorized by outcome?
**Method:** Cluster questions by what happens after they're asked
**Expected Output:** Question type → outcome mapping

### RQ-3: Suggestion Alignment
**Question:** Do acceptance rates vary by agent type?
**Method:** Compare acceptance rates across Claude, Codex, Gemini
**Expected Output:** Agent alignment profiles

### RQ-4: Gap Lifecycle
**Question:** How long does a gap take to resolve?
**Method:** Track time from gap detection to research completion
**Expected Output:** Gap resolution time distribution

### RQ-5: Evidence Velocity
**Question:** How fast does the EGI improve?
**Method:** Track EGI changes over time
**Expected Output:** Evidence accumulation rate

---

## IMPLEMENTATION STATUS

| Component | Status | Notes |
|-----------|--------|-------|
| Plan Scanner | IMPLEMENTED | Scans all .claude/plans/ |
| Question Counter | IMPLEMENTED | JSONL storage |
| Suggestion Ledger | IMPLEMENTED | Acceptance tracking |
| Atom Tracker | IMPLEMENTED | DONE-ID integration |
| Energy Ledger | IMPLEMENTED | Metabolic computation |
| Gap Identifier | IMPLEMENTED | Pattern scanning |
| Inquiry Dispatcher | IMPLEMENTED | praxis-perpetua write |
| CLI | IMPLEMENTED | Full command suite |
| Dashboard | PARTIAL | TUI + HTML export |
| Pre-commit Hook | PENDING | Session close automation |
| CI Pipeline | PENDING | Daily scans |

---

## EXTENSION POINTS

### Potential Innovations

1. **Semantic Gap Detection** — Use embeddings to find thematic gaps, not just pattern matches

2. **Predictive Gap Analysis** — ML model that predicts which areas will produce gaps

3. **Cross-System Comparison** — Compare metabolic rates across similar systems

4. **Gap Network Analysis** — Map gap relationships (this gap blocks that gap)

5. **Autonomous Investigation** — Agent that investigates gaps without human commission

---

## CONCLUSION

The ORGANVM Scrulator is not merely a governance tool. It is an embodiment of the epistemological principle: **the acknowledgment of ignorance is the beginning of wisdom**.

Every question is data. Every gap is opportunity. Every research commission is the system choosing to learn rather than to assume.

This is the law of the land. It is not a suggestion. It is the fundamental operating principle of a self-measuring, self-improving governance system.

---

**Next Steps:**
1. Deploy organvm-scrutator to workspace
2. Run first full scan
3. Dispatch first research inquiries
4. Establish weekly review cadence

---

*This document is a living artifact. It evolves as the system learns about itself.*