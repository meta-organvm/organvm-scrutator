"""
Energy Ledger — Tracks input/output energy of sessions

Energy = questions + suggestions (input) vs atoms + completions (output)
This module provides the fundamental metric of session productivity and
captures the system's metabolic rate.
"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from .question_ledger import QuestionLedger
from .suggestion_ledger import SuggestionLedger
from ..scanner.atom_tracker import AtomTracker


@dataclass
class SessionEnergy:
    """Energy metrics for a single session"""
    session_id: str
    timestamp: str
    
    # Input energy
    questions_asked: int = 0
    suggestions_made: int = 0
    
    # Output energy
    atoms_created: int = 0
    completions: int = 0
    
    # Derived metrics
    total_input: int = 0
    total_output: int = 0
    efficiency_ratio: float = 0.0
    
    def to_dict(self) -> dict:
        return asdict(self)


class EnergyLedger:
    """
    Tracks the metabolic energy of sessions.
    
    The fundamental insight: every session has an energy budget.
    Input energy (questions + suggestions) represents uncertainty and
    hypothesis generation. Output energy (atoms + completions) represents
    value delivery.
    
    Law of the Land: High input with low output is not failure — it's
    learning. The ratio between them reveals the system's learning rate.
    
    The system is a metabolic organism. This module measures its pulse.
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or os.environ.get(
            'SCRUTATOR_DATA',
            str(Path(__file__).parent.parent.parent.parent / 'data')
        ) / 'raw')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize sub-ledgers
        self.question_ledger = QuestionLedger(data_dir)
        self.suggestion_ledger = SuggestionLedger(data_dir)
        self.atom_tracker = AtomTracker(data_dir)
        
        self.energy_file = self.data_dir / 'energy.jsonl'
        self.energy_records: list[SessionEnergy] = []
    
    def load_energy_records(self) -> list[SessionEnergy]:
        """Load existing energy records"""
        self.energy_records = []
        
        if self.energy_file.exists():
            with open(self.energy_file, 'r') as f:
                for line in f:
                    if line.strip():
                        self.energy_records.append(SessionEnergy(**json.loads(line)))
        
        return self.energy_records
    
    def record_session(self, session_id: str,
                      questions_asked: int,
                      suggestions_made: int,
                      atoms_created: int,
                      completions: int) -> SessionEnergy:
        """Record energy metrics for a session"""
        total_input = questions_asked + suggestions_made
        total_output = atoms_created + completions
        efficiency = total_output / total_input if total_input > 0 else 0.0
        
        energy = SessionEnergy(
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            questions_asked=questions_asked,
            suggestions_made=suggestions_made,
            atoms_created=atoms_created,
            completions=completions,
            total_input=total_input,
            total_output=total_output,
            efficiency_ratio=efficiency
        )
        
        self.energy_records.append(energy)
        self._persist_energy(energy)
        
        return energy
    
    def compute_current_session_energy(self, session_id: str) -> SessionEnergy:
        """Compute energy for the current session from sub-ledgers"""
        # Get current session's questions
        all_questions = self.question_ledger.load_questions()
        session_questions = [q for q in all_questions if q.session_id == session_id]
        
        # Get current session's suggestions
        all_suggestions = self.suggestion_ledger.load_suggestions()
        session_suggestions = [s for s in all_suggestions if s.session_id == session_id]
        
        # Get current session's atoms
        all_atoms = self.atom_tracker.load_atoms()
        session_atoms = [a for a in all_atoms if a.session_id == session_id]
        
        # Count completions
        session_completions = sum(1 for a in session_atoms if a.status == 'completed')
        
        return self.record_session(
            session_id=session_id,
            questions_asked=len(session_questions),
            suggestions_made=len(session_suggestions),
            atoms_created=len(session_atoms),
            completions=session_completions
        )
    
    def _persist_energy(self, energy: SessionEnergy):
        """Append energy record to JSONL storage"""
        with open(self.energy_file, 'a') as f:
            f.write(json.dumps(energy.to_dict()) + '\n')
    
    def analyze(self) -> dict:
        """Generate energy analysis"""
        if not self.energy_records:
            self.load_energy_records()
        
        if not self.energy_records:
            return {
                'total_sessions': 0,
                'message': 'No energy records yet. Run a session to collect data.'
            }
        
        total_sessions = len(self.energy_records)
        
        total_questions = sum(e.questions_asked for e in self.energy_records)
        total_suggestions = sum(e.suggestions_made for e in self.energy_records)
        total_atoms = sum(e.atoms_created for e in self.energy_records)
        total_completions = sum(e.completions for e in self.energy_records)
        
        total_input = total_questions + total_suggestions
        total_output = total_atoms + total_completions
        
        avg_efficiency = sum(e.efficiency_ratio for e in self.energy_records) / total_sessions
        
        # Efficiency distribution
        efficient_sessions = sum(1 for e in self.energy_records if e.efficiency_ratio >= 1.0)
        learning_sessions = sum(1 for e in self.energy_records if 0 < e.efficiency_ratio < 1.0)
       Exploring_sessions = sum(1 for e in self.energy_records if e.efficiency_ratio == 0.0)
        
        return {
            'total_sessions': total_sessions,
            'total_input_energy': total_input,
            'total_output_energy': total_output,
            'total_questions': total_questions,
            'total_suggestions': total_suggestions,
            'total_atoms': total_atoms,
            'total_completions': total_completions,
            'system_efficiency': total_output / total_input if total_input > 0 else 0,
            'average_session_efficiency': avg_efficiency,
            'efficiency_distribution': {
                'efficient': efficient_sessions,  # output >= input
                'learning': learning_sessions,    # 0 < output < input
                'exploring': Exploring_sessions   # output = 0
            },
            'metabolic_state': self._classify_metabolic_state(avg_efficiency)
        }
    
    def _classify_metabolic_state(self, efficiency: float) -> str:
        """Classify the system's metabolic state based on efficiency"""
        if efficiency >= 1.0:
            return "CATABOLIC"  # Outputting more than inputting — highly productive
        elif efficiency >= 0.5:
            return "BALANCED"   # Healthy learning-to-output ratio
        elif efficiency > 0:
            return "ANABOLIC"   # Inputting more than output — building/learning phase
        else:
            return "EXPLORING"  # No output yet — pure exploration/discovery
    
    def export_metrics(self, output_path: Optional[str] = None) -> str:
        """Export energy metrics to YAML"""
        import yaml
        
        analysis = self.analyze()
        
        if output_path is None:
            output_path = str(self.data_dir.parent / 'indices' / 'energy-metrics.yaml')
        
        with open(output_path, 'w') as f:
            yaml.dump(analysis, f, default_flow_style=False, sort_keys=False)
        
        return output_path