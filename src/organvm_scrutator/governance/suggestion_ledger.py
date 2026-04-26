"""
Suggestion Ledger — Tracks recommendations made by agents and their acceptance rate

Every suggestion is a hypothesis about what should be done. This module
tracks acceptance, rejection, and modification rates to build a model
of agent-human collaboration effectiveness.
"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Suggestion:
    """Represents a single suggestion/recommendation"""
    id: str
    session_id: str
    timestamp: str
    suggestion_text: str
    context: Optional[str] = None
    status: str = 'pending'  # pending, accepted, rejected, modified
    outcome: Optional[str] = None
    modified_from: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)


class SuggestionLedger:
    """
    Tracks every suggestion made by agents.
    
    Suggestions are the primary mechanism of value transfer from agent to human.
    High acceptance rates indicate alignment. High rejection rates indicate
    either misunderstanding or creative tension (which is productive).
    
    Law of the Land: Every rejected suggestion is a data point about
    what the system doesn't understand about human preferences.
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or os.environ.get(
            'SCRUTATOR_DATA',
            str(Path(__file__).parent.parent.parent.parent / 'data')
        ) / 'raw')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.suggestions_file = self.data_dir / 'suggestions.jsonl'
        self.suggestions: list[Suggestion] = []
        
    def load_suggestions(self) -> list[Suggestion]:
        """Load existing suggestions from storage"""
        self.suggestions = []
        
        if self.suggestions_file.exists():
            with open(self.suggestions_file, 'r') as f:
                for line in f:
                    if line.strip():
                        self.suggestions.append(Suggestion(**json.loads(line)))
        
        return self.suggestions
    
    def add_suggestion(self, session_id: str, suggestion_text: str,
                      context: Optional[str] = None) -> Suggestion:
        """Add a new suggestion to the ledger"""
        suggestion = Suggestion(
            id=f"SUG-{len(self.suggestions)+1:05d}",
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            suggestion_text=suggestion_text,
            context=context,
            status='pending'
        )
        
        self.suggestions.append(suggestion)
        self._persist_suggestion(suggestion)
        
        return suggestion
    
    def accept_suggestion(self, suggestion_id: str, outcome: Optional[str] = None):
        """Mark a suggestion as accepted"""
        for s in self.suggestions:
            if s.id == suggestion_id:
                s.status = 'accepted'
                s.outcome = outcome
                break
        
        self._rewrite_ledger()
    
    def reject_suggestion(self, suggestion_id: str, reason: Optional[str] = None):
        """Mark a suggestion as rejected"""
        for s in self.suggestions:
            if s.id == suggestion_id:
                s.status = 'rejected'
                s.outcome = reason
                break
        
        self._rewrite_ledger()
    
    def modify_suggestion(self, suggestion_id: str, modified_from: str,
                         outcome: Optional[str] = None):
        """Mark a suggestion as modified (partial acceptance)"""
        for s in self.suggestions:
            if s.id == suggestion_id:
                s.status = 'modified'
                s.modified_from = modified_from
                s.outcome = outcome
                break
        
        self._rewrite_ledger()
    
    def _persist_suggestion(self, suggestion: Suggestion):
        """Append suggestion to JSONL storage"""
        with open(self.suggestions_file, 'a') as f:
            f.write(json.dumps(suggestion.to_dict()) + '\n')
    
    def _rewrite_ledger(self):
        """Rewrite entire ledger"""
        with open(self.suggestions_file, 'w') as f:
            for s in self.suggestions:
                f.write(json.dumps(s.to_dict()) + '\n')
    
    def analyze(self) -> dict:
        """Generate suggestion analysis"""
        if not self.suggestions:
            self.load_suggestions()
            
        total = len(self.suggestions)
        accepted = sum(1 for s in self.suggestions if s.status == 'accepted')
        rejected = sum(1 for s in self.suggestions if s.status == 'rejected')
        modified = sum(1 for s in self.suggestions if s.status == 'modified')
        pending = sum(1 for s in self.suggestions if s.status == 'pending')
        
        # By agent type (extract from session_id)
        by_agent = {}
        for s in self.suggestions:
            agent = s.session_id.split('-')[0] if '-' in s.session_id else 'unknown'
            if agent not in by_agent:
                by_agent[agent] = {'total': 0, 'accepted': 0, 'rejected': 0, 'modified': 0}
            by_agent[agent]['total'] += 1
            if s.status == 'accepted':
                by_agent[agent]['accepted'] += 1
            elif s.status == 'rejected':
                by_agent[agent]['rejected'] += 1
            elif s.status == 'modified':
                by_agent[agent]['modified'] += 1
        
        # Calculate acceptance rates
        for agent in by_agent:
            total_agent = by_agent[agent]['total']
            accepted_agent = by_agent[agent]['accepted']
            by_agent[agent]['acceptance_rate'] = accepted_agent / total_agent if total_agent > 0 else 0
        
        return {
            'total_suggestions': total,
            'accepted': accepted,
            'rejected': rejected,
            'modified': modified,
            'pending': pending,
            'acceptance_rate': accepted / total if total > 0 else 0,
            'rejection_rate': rejected / total if total > 0 else 0,
            'modification_rate': modified / total if total > 0 else 0,
            'by_agent': by_agent,
            'rejected_suggestions': [
                s.to_dict() for s in self.suggestions if s.status == 'rejected'
            ]
        }
    
    def get_research_opportunities(self) -> list[dict]:
        """Identify patterns in rejected suggestions as research opportunities"""
        opportunities = []
        
        # Analyze rejection patterns
        rejected = [s for s in self.suggestions if s.status == 'rejected']
        
        # Group by common themes (simple keyword matching)
        themes = {}
        for s in rejected:
            # Extract key terms (simple approach)
            words = s.suggestion_text.lower().split()
            key_words = [w for w in words if len(w) > 5][:2]
            theme_key = ','.join(key_words) if key_words else 'unknown'
            
            if theme_key not in themes:
                themes[theme_key] = []
            themes[theme_key].append(s.suggestion_text)
        
        for theme, items in themes.items():
            opportunities.append({
                'theme': theme,
                'count': len(items),
                'examples': items[:3],
                'status': 'research_opportunity',
                'hypothesis': f"Why do {len(items)} suggestions about '{theme}' get rejected?"
            })
        
        return opportunities