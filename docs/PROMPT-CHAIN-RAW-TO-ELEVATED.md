# PROMPT CHAIN: RAW → CLEANED → ELEVATED
## The Mutiversal Atomization Protocol

---

## STAGE 0: RAW INPUT

**State:** Unprocessed, noisy, full of context
**Metaphor:** Crude ore straight from the mine
**Question:** What is ALL of this?

```
You have been given a session transcript (or raw content). Your task is to receive it
without judgment, without filtering, without interpretation. Simply acknowledge what
is here.

Do not analyze. Do not summarize. Do not act.
Simply witness the full text and report:
- Total character count
- Total token estimate
- Number of distinct speakers/voices
- Apparent topics (list without elaboration)
- Apparent intent (one sentence)
- Emotional tenor (one adjective)

Output in JSON:
{
  "raw_metrics": { ... },
  "raw_witness": "I have witnessed X characters of content from Y speakers about Z"
}
```

---

## STAGE 1: CLEANED

**State:** Noise removed, structure emerging
**Metaphor:** Ore refined to metal
**Question:** What remains when noise is gone?

```
Take the raw content and perform the following operations:

1. REMOVE NOISE
   - Strip formatting artifacts (```, ---, etc.)
   - Remove repeated whitespace
   - Collapse redundant phrases
   - Extract unique sentences only

2. IDENTIFY STRUCTURE
   - Detect conversation turns
   - Identify explicit commands vs. questions vs. statements
   - Find topic boundaries
   - Locate decision points

3. EXTRACT ATOMS (First Pass - Surface Level)
   - Each actionable unit becomes ONE atom
   - Atoms have: content, type (task/suggestion/idea/fact), speaker

4. INDEX
   - Number each atom
   - Tag with domain if obvious
   - Flag if atom implies another atom

Output: "cleaned_atoms.jsonl"
- One line per atom
- Fields: id, content_cleaned, type, domain_hint, implied_by, implies
```

---

## STAGE 2: ELEVATED

**State:** Atomic decomposition complete, multiversal exploration ready
**Metaphor:** Metal forged into precision instruments
**Question:** What is this REALLY about across all possible realities?

### Stage 2a: ATOMIC DECOMPOSITION

```
For each atom from Stage 1, perform EXHAUSTIVE decomposition:

CONTENT ANALYSIS:
- What is explicitly stated?
- What is implied but not said?
- What is assumed as background?
- What is the emotional charge?

ENTITY EXTRACTION:
- Who is mentioned? (characters)
- What is mentioned? (objects/concepts)
- What actions occur? (verbs)
- What relationships exist? (connections)

DOMAIN MAPPING:
- Which organ/realm does this touch?
- Which IRF category applies?
- Which governance layer is affected?

SUBATOMIC SPLIT:
Each atom contains micro-elements. Extract them:
- ENTITY: A person, place, thing
- ACTION: What happens/is proposed
- DOMAIN: The field of concern
- REFERENCE: What this connects to
- TIMESTAMP: When this matters
- PRIORITY: If explicit, else unknown

Output: "atoms_decomposed.jsonl"
- Each atom expanded to 3-7 subatomic elements
```

### Stage 2b: MULTIVERSAL EXPLORATION

```
For each SUBATOMIC element, explore across logic instances:

MULTIVERSAL LOGIC INSTANCES:
1. If this is TRUE, what follows?
2. If this is FALSE, what follows?
3. If this is UNKNOWN, what research is needed?
4. If this is IMPOSSIBLE, what替代 exists? (alternatives)
5. If this is ALWAYS, what's the exception?
6. If this is NEVER, when does it start?

REALITY BRANCHING:
For each element, consider:
- Best-case scenario
- Worst-case scenario  
- Most-likely scenario
- Most-interesting scenario (even if unlikely)

IMPLICATION CHAIN:
Element A → implies B → implies C → implies D
Map forward 3 steps and backward 3 steps

GAP RADIATION:
After each completion, NEW questions emerge. Capture:
- What does this ELEMENT make visible?
- What does this ELEMENT make possible?
- What does this ELEMENT make urgent?

Output: "multiversal_map.json"
- Graph structure of elements × logic instances × reality branches
```

### Stage 2c: ATOM-TO-WORK MAPPING

```
Transform the multiversal map into actionable form:

TASK ATOMS:
- What needs to be DONE?
- Who would do it?
- What's the blocking dependency?

SUGGESTION ATOMS:
- What was RECOMMENDED?
- What's the acceptance likelihood?
- What's the rejection reason?

IDEA ATOMS:
- What needs further THOUGHT?
- What research commission does this spawn?
- What's the confidence level?

FACT ATOMS:
- What is VERIFIED?
- What's the evidence source?
- What's the confidence level?

UNKNOWN ATOMS:
- What is NOT KNOWN?
- What's the evidence gap?
- What's the research priority?

Output: "work_queue.yaml"
- Fully atomic, fully categorized, multi-version tracked
- Ready for IRF ingestion
```

---

## COMPLETE CHAIN FLOW

```
[RAW INPUT]
     ↓
Stage 0: Witness (metrics only)
     ↓
[WITNESSED CONTENT]
     ↓
Stage 1: Clean & Extract
     ↓
[SURFACE ATOMS]
     ↓
Stage 2a: Decompose
     ↓
[SUBATOMIC ELEMENTS]
     ↓
Stage 2b: Multiversal Map
     ↓
[MULTIVERSAL GRAPH]
     ↓
Stage 2c: Work Queue
     ↓
[IRF-READY ATOMS]
```

---

## EXAMPLE OUTPUT

### Input (Raw 2,000 chars):
```
Hey, we need to build that thing we talked about. 
The thing with the stuff. Also, Rob said to check 
the IRF and see if there's anything P0. And Maddie 
mentioned the spiral needs work.
```

### Stage 0 Output:
```json
{
  "raw_metrics": {
    "characters": 247,
    "estimated_tokens": 62,
    "speakers": 1,
    "topics": ["build thing", "IRF check", "spiral work"],
    "intent": "multi-part action request",
    "emotional_tenor": "casual, forward-looking"
  }
}
```

### Stage 1 Output:
```
ATOM-001: we need to build that thing we talked about [TASK]
ATOM-002: check the IRF for P0 items [TASK]
ATOM-003: spiral needs work [IDEA]
```

### Stage 2a Output (subatomic):
```
ATOM-001:
  - ENTITY: "we" (speaker + implicit team)
  - ACTION: "build" + "that thing we talked about"
  - DOMAIN: infrastructure/construction
  - REFERENCE: prior conversation (un-indexed)
  - TIMESTAMP: now
  - PRIORITY: unknown

ATOM-002:
  - ENTITY: "IRF" + "P0 items"
  - ACTION: "check" + "see if"
  - DOMAIN: governance/tracking
  - REFERENCE: organvm-corpvs-testamentvm
  - TIMESTAMP: when IRF is checked
  - PRIORITY: P0 (explicit)

ATOM-003:
  - ENTITY: "Maddie" + "spiral"
  - ACTION: "mentioned" + "needs work"
  - DOMAIN: creative/product
  - REFERENCE: person: Maddie, artifact: spiral
  - TIMESTAMP: during conversation
  - PRIORITY: unknown
```

### Stage 2b Output (multiversal):
```
ATOM-001 × IF-TRUE: building proceeds, resources needed
ATOM-001 × IF-FALSE: conversation stalled, re-prioritize
ATOM-001 × IF-UNKNOWN: need context on "thing we talked about"

ATOM-002 × IMPLIES: IRF check → P0 items → action items → completion
ATOM-002 × GAP: What IS in the IRF? Need snapshot.
ATOM-002 × RADIATION: New questions: Are there P1s? P2s?

ATOM-003 × BRANCH-BEST: Maddie leads spiral improvement
ATOM-003 × BRANCH-WORST: Spiral blocked, no resources
ATOM-003 × BRANCH-MOST-LIKELY: Work scheduled for later
```

### Stage 2c Output (work queue):
```yaml
- id: TASK-001
  type: task
  content: "Build the thing from prior conversation"
  domain: infrastructure
  priority: unknown
  blocker: "What thing? Context not captured"
  action: "Request clarification on 'the thing'"

- id: TASK-002
  type: task
  content: "Check IRF for P0 items"
  domain: governance
  priority: P0
  action: "Query IRF: organvm irf list --priority P0"
  
- id: TASK-003
  type: idea
  content: "Spiral needs work (via Maddie)"
  domain: creative
  priority: unknown
  action: "Tag Maddie for clarification session"
  research_commission: true
```

---

## IMPLEMENTATION

```python
#!/usr/bin/env python3
"""
prompt_atomizer.py — Raw to Elevated Pipeline

Usage:
    python prompt_atomizer.py raw_input.txt
    python prompt_atomizer.py --stage 1 cleaned_atoms.jsonl
    python prompt_atomizer.py --stage 2 atoms_decomposed.jsonl
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class SubatomicElement:
    """Single irreducible element from decomposition"""
    parent_atom_id: str
    element_type: str  # ENTITY, ACTION, DOMAIN, REFERENCE, TIMESTAMP, PRIORITY
    content: str
    confidence: float  # 0-1
    multiversal_states: dict  # TRUE, FALSE, UNKNOWN, etc.

@dataclass 
class Atom:
    """Surface-level atom extracted from raw content"""
    id: str
    raw_content: str
    cleaned_content: str
    atom_type: str  # task, suggestion, idea, fact, unknown
    domain_hint: Optional[str]
    implied_by: Optional[str]
    implies: List[str]
    subatoms: List[SubatomicElement]
    multiversal_map: dict
    work_ready: bool

class PromptAtomizer:
    """Complete RAW → CLEANED → ELEVATED pipeline"""
    
    def __init__(self, input_path: str):
        self.input_path = Path(input_path)
        self.raw_content = ""
        self.atoms: List[Atom] = []
        
    def stage_0_witness(self) -> dict:
        """Witness raw content without interpretation"""
        self.raw_content = self.input_path.read_text()
        return {
            "characters": len(self.raw_content),
            "estimated_tokens": len(self.raw_content) // 4,
            "speakers": self._count_speakers(),
            "topics": self._extract_topics(),
            "intent": self._extract_intent(),
            "emotional_tenor": self._extract_tenor()
        }
    
    def stage_1_clean(self) -> List[Atom]:
        """Clean content and extract surface atoms"""
        cleaned = self._remove_noise(self.raw_content)
        self.atoms = self._extract_atoms(cleaned)
        return self.atoms
    
    def stage_2a_decompose(self) -> List[Atom]:
        """Atomic decomposition of each atom"""
        for atom in self.atoms:
            atom.subatoms = self._decompose_atom(atom)
        return self.atoms
    
    def stage_2b_multiverse(self) -> List[Atom]:
        """Explore across logic instances"""
        for atom in self.atoms:
            atom.multiversal_map = self._build_multiverse_map(atom)
        return self.atoms
    
    def stage_2c_workqueue(self) -> dict:
        """Transform to IRF-ready work queue"""
        return self._build_work_queue(self.atoms)
    
    def run_full_pipeline(self) -> dict:
        """Execute complete RAW → ELEVATED chain"""
        witness = self.stage_0_witness()
        atoms = self.stage_1_clean()
        atoms = self.stage_2a_decompose()
        atoms = self.stage_2b_multiverse()
        workqueue = self.stage_2c_workqueue()
        
        return {
            "witness": witness,
            "atoms": [asdict(a) for a in atoms],
            "workqueue": workqueue
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prompt_atomizer.py <input_file>")
        sys.exit(1)
    
    atomizer = PromptAtomizer(sys.argv[1])
    result = atomizer.run_full_pipeline()
    print(json.dumps(result, indent=2))
```

---

## KEY PRINCIPLES

1. **Every prompt is a multiverse** — One prompt implies countless logic instances
2. **Atoms are permanent** — Never delete, only mark as processed
3. **Gaps radiate** — Every answer creates new questions
4. **Subatomic is the unit of work** — Not tasks, but the elements that compose tasks
5. **Nothing is lost** — RAW → CLEANED → ELEVATED preserves everything

---

*This chain converts conversation into navigable structure. The multiversal map ensures no implication is lost.*