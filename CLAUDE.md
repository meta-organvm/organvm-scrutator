# organvm-scrutator

**Status:** ACTIVE (Under Construction)
**Created:** 2026-04-26
**Purpose:** Self-auditing governance system that scrutinizes itself

---

## Core Principle (Law of the Land)

> If there is no data or statistics to prove whichever answer is the best one, then it is an opportunity for studying and figuring it out.

This system tracks every question asked, every suggestion made, every atom created, and every gap identified. Every unknown becomes a research opportunity.

---

## Architecture

```
organvm-scrutator/
├── src/organvm_scrutator/
│   ├── scanner/           # Data collection
│   │   ├── plan_scanner.py
│   │   ├── question_counter.py
│   │   └── atom_tracker.py
│   ├── governance/        # Metric computation
│   │   ├── question_ledger.py
│   │   ├── suggestion_ledger.py
│   │   └── energy_ledger.py
│   ├── research/          # Gap analysis
│   │   ├── gap_identifier.py
│   │   └── inquiry_dispatcher.py
│   └── viz/               # Output generation
│       ├── index_generator.py
│       └── dashboard.py
├── data/
│   ├── indices/           # Generated indices
│   ├── raw/               # JSONL data stores
│   └── research/          # Gap/dispatch logs
├── docs/
│   ├── RESEARCH-001.md    # Core theory
│   └── SOP-*.md           # Procedures
└── scripts/               # Automation
```

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `organvm-scrutator scan` | Scan all .claude/plans/ directories |
| `organvm-scrutator questions` | Analyze questions |
| `organvm-scrutator suggestions` | Analyze suggestions + acceptance |
| `organvm-scrutator atoms` | Track work items |
| `organvm-scrutator energy` | Compute metabolic metrics |
| `organvm-scrutator gaps` | Identify knowledge gaps |
| `organvm-scrutator dispatch` | Send gaps to praxis-perpetua |
| `organvm-scrutator stats` | Full system overview |

---

## Data Schemas

### Questions (questions.jsonl)
```json
{
  "id": "Q-00001",
  "session_id": "2026-04-26-hokage-001",
  "timestamp": "2026-04-26T14:30:00Z",
  "question_text": "What's the blocking constraint?",
  "answered": false
}
```

### Suggestions (suggestions.jsonl)
```json
{
  "id": "SUG-00001", 
  "session_id": "2026-04-26-hokage-001",
  "suggestion_text": "Create the repository structure",
  "status": "accepted"
}
```

### Atoms (atoms.jsonl)
```json
{
  "id": "DONE-480",
  "session_id": "2026-04-26-hokage-001",
  "title": "Create organvm-scrutator",
  "type": "done",
  "status": "completed"
}
```

### Energy (energy.jsonl)
```json
{
  "session_id": "2026-04-26-hokage-001",
  "questions_asked": 5,
  "suggestions_made": 3,
  "atoms_created": 8,
  "completions": 2,
  "efficiency_ratio": 1.25
}
```

---

## Key Metrics

| Metric | Description |
|--------|-------------|
| **Metabolic State** | CATABOLIC / BALANCED / ANABOLIC / EXPLORING |
| **System Efficiency** | Output energy / Input energy |
| **Acceptance Rate** | Suggestions accepted / Total suggestions |
| **Completion Rate** | Atoms completed / Atoms created |
| **Evidence Gap Index (EGI)** | Composite knowledge score |

---

## Development

### Setup
```bash
cd organvm-scrutator
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest tests -v
```

### Run CLI
```bash
organvm-scrutator stats
```

---

## Related Systems

- **IRF** — Index Rerum Faciendarum (work registry)
- **praxis-perpetua** — SGO research apparatus
- **organvm-engine** — Core CLI infrastructure
- **a-organvm** — Biological reference implementation

---

## Governance

- **Law of the Land:** Every unknown is a research opportunity
- **Evidence Hierarchy:** PROVEN → STUDIED → HYPOTHESIZED → UNKNOWN
- **Metabolic Model:** Input (Q+S) vs Output (A+C) = Efficiency
- **Gap Lifecycle:** Detection → Classification → Dispatch → Resolution

---

*This system measures its own measurement gaps.*