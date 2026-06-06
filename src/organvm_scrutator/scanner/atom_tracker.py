"""
Atom Tracker — Tracks tasks, atoms, and work items created during sessions

Atoms are the fundamental units of work in ORGANVM. This module tracks
every atom created, its source session, and its completion status.
"""

import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Atom:
    """Represents a single work atom"""
    id: str
    session_id: str
    created_at: str
    title: str
    type: str  # plan, task, item, suggestion
    status: str  # open, in_progress, completed, blocked
    priority: str  # P0, P1, P2, P3
    source: Optional[str] = None
    completed_at: Optional[str] = None
    blocker: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)


class AtomTracker:
    """
    Tracks atoms (work items) across all sessions.
    
    Atoms are created from:
    - Plans (planning phase outputs)
    - Suggestions (recommendations made by agents)
    - Questions (unanswered queries that become tasks)
    - IRF items (governance work items)
    
    Law of the Land: Every atom that cannot be completed is an opportunity
    to understand why, not a failure to report.
    """
    
    ATOM_ID_PATTERN = re.compile(r'(DONE-\d+|IRF-[A-Z]+-\d+|ATM-\d+|VSS-\d+)')
    PRIORITY_PATTERN = re.compile(r'\*\*([P0-3])\*\*')
    STATUS_PATTERN = re.compile(r'\*\*Status:\*\*\s*(\S+)')
    
    def __init__(self, data_dir: Optional[str] = None):
        data_root = Path(data_dir or os.environ.get(
            'SCRUTATOR_DATA',
            str(Path(__file__).parent.parent.parent.parent / 'data')
        ))
        self.data_dir = data_root / 'raw'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.atoms_file = self.data_dir / 'atoms.jsonl'
        self.completions_file = self.data_dir / 'completions.jsonl'
        
        self.atoms: list[Atom] = []
        self.completions: list[dict] = []
    
    def load_atoms(self) -> list[Atom]:
        """Load existing atoms from storage"""
        self.atoms = []
        
        if self.atoms_file.exists():
            with open(self.atoms_file, 'r') as f:
                for line in f:
                    if line.strip():
                        self.atoms.append(Atom(**json.loads(line)))
        
        return self.atoms
    
    def load_completions(self) -> list[dict]:
        """Load completion records"""
        self.completions = []
        
        if self.completions_file.exists():
            with open(self.completions_file, 'r') as f:
                for line in f:
                    if line.strip():
                        self.completions.append(json.loads(line))
        
        return self.completions
    
    def create_atom(self, session_id: str, title: str, 
                   atom_type: str = 'task',
                   priority: str = 'P2',
                   source: Optional[str] = None) -> Atom:
        """Create a new atom"""
        # Generate ID
        existing_ids = [a.id for a in self.atoms]
        
        if atom_type == 'done':
            # Find next DONE-ID from IRF
            next_id = self._get_next_done_id()
            atom_id = f"DONE-{next_id}"
        elif atom_type.startswith('IRF-'):
            atom_id = atom_type
        else:
            atom_id = f"ATM-{len(self.atoms)+1:06d}"
        
        atom = Atom(
            id=atom_id,
            session_id=session_id,
            created_at=datetime.now().isoformat(),
            title=title,
            type=atom_type,
            status='open',
            priority=priority,
            source=source
        )
        
        self.atoms.append(atom)
        self._persist_atom(atom)
        
        return atom
    
    def complete_atom(self, atom_id: str, notes: Optional[str] = None):
        """Mark an atom as completed"""
        for atom in self.atoms:
            if atom.id == atom_id:
                atom.status = 'completed'
                atom.completed_at = datetime.now().isoformat()
                
                # Record completion
                completion = {
                    'atom_id': atom_id,
                    'completed_at': atom.completed_at,
                    'session_id': atom.session_id,
                    'title': atom.title,
                    'notes': notes
                }
                self.completions.append(completion)
                self._persist_completion(completion)
                break
        
        self._rewrite_atoms()
    
    def block_atom(self, atom_id: str, blocker: str):
        """Mark an atom as blocked"""
        for atom in self.atoms:
            if atom.id == atom_id:
                atom.status = 'blocked'
                atom.blocker = blocker
                break
        
        self._rewrite_atoms()
    
    def _get_next_done_id(self) -> int:
        """Get next available DONE-ID from IRF counter"""
        irf_counter = Path.home() / 'Workspace' / 'organvm' / 'organvm-corpvs-testamentvm' / 'data' / 'done-id-counter.json'
        
        if irf_counter.exists():
            data = json.loads(irf_counter.read_text())
            return data.get('next_id', 480)
        
        return 480
    
    def _persist_atom(self, atom: Atom):
        """Append atom to JSONL storage"""
        with open(self.atoms_file, 'a') as f:
            f.write(json.dumps(atom.to_dict()) + '\n')
    
    def _persist_completion(self, completion: dict):
        """Append completion to JSONL storage"""
        with open(self.completions_file, 'a') as f:
            f.write(json.dumps(completion) + '\n')
    
    def _rewrite_atoms(self):
        """Rewrite entire atoms ledger"""
        with open(self.atoms_file, 'w') as f:
            for atom in self.atoms:
                f.write(json.dumps(atom.to_dict()) + '\n')
    
    def analyze(self) -> dict:
        """Generate atom analysis"""
        if not self.atoms:
            self.load_atoms()
        
        if not self.completions:
            self.load_completions()
        
        total = len(self.atoms)
        open_count = sum(1 for a in self.atoms if a.status == 'open')
        in_progress = sum(1 for a in self.atoms if a.status == 'in_progress')
        completed = sum(1 for a in self.atoms if a.status == 'completed')
        blocked = sum(1 for a in self.atoms if a.status == 'blocked')
        
        # By priority
        by_priority = {}
        for a in self.atoms:
            by_priority[a.priority] = by_priority.get(a.priority, 0) + 1
        
        # By type
        by_type = {}
        for a in self.atoms:
            by_type[a.type] = by_type.get(a.type, 0) + 1
        
        # By session
        by_session = {}
        for a in self.atoms:
            by_session[a.session_id] = by_session.get(a.session_id, 0) + 1
        
        # Completion rate
        completion_rate = completed / total if total > 0 else 0
        
        return {
            'total_atoms': total,
            'open': open_count,
            'in_progress': in_progress,
            'completed': completed,
            'blocked': blocked,
            'completion_rate': completion_rate,
            'by_priority': by_priority,
            'by_type': by_type,
            'by_session': by_session,
            'blocked_atoms': [a.to_dict() for a in self.atoms if a.status == 'blocked']
        }
    
    def get_energy_output(self) -> dict:
        """Calculate energy output (atoms created/completed)"""
        if not self.atoms:
            self.load_atoms()
        
        return {
            'total_created': len(self.atoms),
            'total_completed': sum(1 for a in self.atoms if a.status == 'completed'),
            'creation_rate': len(self.atoms) / 30 if self.atoms else 0,  # per day (approx)
            'completion_rate': sum(1 for a in self.atoms if a.status == 'completed') / len(self.atoms) if self.atoms else 0
        }
    
    def export_metrics(self, output_path: Optional[str] = None) -> str:
        """Export metrics to YAML"""
        import yaml
        
        analysis = self.analyze()
        
        if output_path is None:
            output_path = str(self.data_dir.parent / 'indices' / 'atom-metrics.yaml')
        
        with open(output_path, 'w') as f:
            yaml.dump(analysis, f, default_flow_style=False, sort_keys=False)
        
        return output_path
