"""
Question Counter — Tracks every question asked by agents

Every question is a data point about uncertainty. This module captures
the quantity, type, and context of all questions to build a governance metric.
"""

import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Question:
    """Represents a single question asked"""
    id: str
    session_id: str
    timestamp: str
    question_text: str
    context: Optional[str] = None
    answered: bool = False
    answer_source: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)


class QuestionCounter:
    """
    Counts and analyzes questions asked across sessions.
    
    Questions are the primary mechanism of uncertainty transfer from
    agent to human. High question rates indicate:
    - Boundary conditions not captured in training
    - Ambiguous instructions requiring clarification
    - Learning opportunities for the system
    
    Law of the Land applies: every unanswered question is a research opportunity.
    """
    
    QUESTION_TOOL_PATTERN = re.compile(r'"question":\s*\{.*?"questions":\s*\[(.*?)\]', re.DOTALL)
    QUOTED_QUESTION_PATTERN = re.compile(r'"header":\s*"([^"]+)"')
    
    def __init__(self, data_dir: Optional[str] = None):
        data_root = Path(data_dir or os.environ.get(
            'SCRUTATOR_DATA',
            str(Path(__file__).parent.parent.parent.parent / 'data')
        ))
        self.data_dir = data_root / 'raw'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.questions_file = self.data_dir / 'questions.jsonl'
        self.questions: list[Question] = []
        
    def load_questions(self) -> list[Question]:
        """Load existing questions from storage"""
        self.questions = []
        
        if self.questions_file.exists():
            with open(self.questions_file, 'r') as f:
                for line in f:
                    if line.strip():
                        self.questions.append(Question(**json.loads(line)))
        
        return self.questions
    
    def add_question(self, session_id: str, question_text: str, 
                    context: Optional[str] = None) -> Question:
        """Add a new question to the ledger"""
        question = Question(
            id=f"Q-{len(self.questions)+1:05d}",
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            question_text=question_text,
            context=context,
            answered=False
        )
        
        self.questions.append(question)
        self._persist_question(question)
        
        return question
    
    def mark_answered(self, question_id: str, answer_source: str):
        """Mark a question as answered"""
        for q in self.questions:
            if q.id == question_id:
                q.answered = True
                q.answer_source = answer_source
                break
        
        self._rewrite_ledger()
    
    def _persist_question(self, question: Question):
        """Append question to JSONL storage"""
        with open(self.questions_file, 'a') as f:
            f.write(json.dumps(question.to_dict()) + '\n')
    
    def _rewrite_ledger(self):
        """Rewrite entire ledger (for updates)"""
        with open(self.questions_file, 'w') as f:
            for q in self.questions:
                f.write(json.dumps(q.to_dict()) + '\n')
    
    def analyze(self) -> dict:
        """Generate question analysis"""
        if not self.questions:
            self.load_questions()
            
        total = len(self.questions)
        answered = sum(1 for q in self.questions if q.answered)
        unanswered = total - answered
        
        # Group by session
        by_session = {}
        for q in self.questions:
            by_session[q.session_id] = by_session.get(q.session_id, 0) + 1
        
        # Find common question patterns
        question_words = []
        for q in self.questions:
            words = q.question_text.lower().split()
            question_words.extend([w for w in words if len(w) > 3])
        
        from collections import Counter
        word_freq = Counter(question_words)
        
        return {
            'total_questions': total,
            'answered': answered,
            'unanswered': unanswered,
            'answer_rate': answered / total if total > 0 else 0,
            'by_session': by_session,
            'common_words': dict(word_freq.most_common(20)),
            'unanswered_questions': [
                q.to_dict() for q in self.questions if not q.answered
            ]
        }
    
    def get_research_opportunities(self) -> list[dict]:
        """Identify unanswered questions as research opportunities"""
        opportunities = []
        
        for q in self.questions:
            if not q.answered:
                opportunities.append({
                    'question_id': q.id,
                    'question': q.question_text,
                    'session': q.session_id,
                    'status': 'unanswered',
                    'priority': self._assess_priority(q.question_text)
                })
        
        return opportunities
    
    def _assess_priority(self, question_text: str) -> str:
        """Assess research priority based on question content"""
        text = question_text.lower()
        
        # High priority indicators
        if any(word in text for word in ['blocker', 'blocking', 'critical', 'urgent', 'p0']):
            return 'P0'
        if any(word in text for word in ['design', 'architecture', 'spec', 'protocol']):
            return 'P1'
        if any(word in text for word in ['what is', 'how does', 'explain']):
            return 'P2'
        
        return 'P3'  # Default
    
    def export_to_yaml(self, output_path: Optional[str] = None) -> str:
        """Export analysis to YAML for human review"""
        import yaml
        
        analysis = self.analyze()
        
        if output_path is None:
            output_path = str(self.data_dir.parent / 'indices' / 'question-metrics.yaml')
        
        # Convert to serializable format
        analysis['unanswered_questions'] = analysis['unanswered_questions'][:50]  # Limit
        
        with open(output_path, 'w') as f:
            yaml.dump(analysis, f, default_flow_style=False, sort_keys=False)
        
        return output_path
