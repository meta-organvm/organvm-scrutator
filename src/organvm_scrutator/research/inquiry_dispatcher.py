"""
Inquiry Dispatcher — Converts gaps to research commissions

When gaps are identified, they need to become research inquiries.
This module dispatches gaps to praxis-perpetua as formal research commissions.
"""

import json
import os
import yaml
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Inquiry:
    """Represents a research inquiry"""
    id: str
    gap_id: str
    created_at: str
    title: str
    description: str
    priority: str
    status: str  # proposed, commissioned, in_progress, completed, archived
    commission_id: Optional[str] = None
    results: Optional[dict] = None
    
    def to_dict(self) -> dict:
        return asdict(self)


class InquiryDispatcher:
    """
    Dispatches identified gaps as research inquiries to praxis-perpetua.
    
    The dispatcher acts as the bridge between the governance system
    and the formal research apparatus. It:
    1. Takes gaps from the gap identifier
    2. Formats them as research inquiries
    3. Writes them to praxis-perpetua's commission log
    4. Tracks commission status
    
    Law of the Land: Every gap becomes a commission. The system
    must formalize its ignorance into actionable research.
    """
    
    def __init__(self, praxis_endpoint: Optional[str] = None):
        self.praxis_endpoint = Path(praxis_endpoint or os.environ.get(
            'SCRUTATOR_PRAXIS_ENDPOINT',
            str(Path.home() / 'Workspace' / 'organvm' / 'praxis-perpetua')
        ))
        
        self.inquiry_log = self.praxis_endpoint / 'commissions' / 'inquiry-log.yaml'
        self.dispatcher_log = Path(__file__).parent.parent.parent.parent / 'data' / 'research' / 'dispatches.jsonl'
        self.dispatcher_log.parent.mkdir(parents=True, exist_ok=True)
        
        self.inquiries: list[Inquiry] = []
    
    def load_inquiry_log(self) -> list[dict]:
        """Load existing inquiries from praxis-perpetua"""
        if not self.inquiry_log.exists():
            return []
        
        with open(self.inquiry_log, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('inquiries', []) if data else []
    
    def dispatch_gap(self, gap: dict, priority: str = 'P2') -> Inquiry:
        """Dispatch a single gap as a research inquiry"""
        # Generate inquiry ID
        existing_count = len(self.load_inquiry_log())
        inquiry_id = f"INQ-2026-{existing_count+1:03d}"
        
        inquiry = Inquiry(
            id=inquiry_id,
            gap_id=gap.get('gap_id', 'UNKNOWN'),
            created_at=datetime.now().isoformat(),
            title=self._generate_title(gap),
            description=self._generate_description(gap),
            priority=priority,
            status='proposed',
        )
        
        # Persist locally
        self.inquiries.append(inquiry)
        self._persist_dispatch(inquiry)
        
        # Attempt to write to praxis-perpetua
        self._write_to_praxis(inquiry)
        
        return inquiry
    
    def dispatch_batch(self, gaps: list[dict], threshold: int = 3) -> list[Inquiry]:
        """Dispatch multiple gaps, filtering by occurrence threshold"""
        inquiries = []
        
        for gap in gaps:
            if gap.get('occurrences', 0) >= threshold:
                inquiry = self.dispatch_gap(gap, gap.get('research_priority', 'P2'))
                inquiries.append(inquiry)
        
        return inquiries
    
    def _generate_title(self, gap: dict) -> str:
        """Generate a research title from gap statement"""
        statement = gap.get('statement', '')
        
        # Truncate and clean
        title = statement[:80].strip()
        if len(statement) > 80:
            title += '...'
        
        # Capitalize
        title = title[0].upper() + title[1:] if title else 'Unnamed Research'
        
        return f"Investigation: {title}"
    
    def _generate_description(self, gap: dict) -> str:
        """Generate research description from gap data"""
        return f"""
Research Inquiry generated from Gap Analysis

**Source Gap:** {gap.get('gap_id', 'UNKNOWN')}
**Category:** {gap.get('category', 'UNKNOWN')}
**Severity:** {gap.get('severity', 'unknown')}
**Occurrences:** {gap.get('occurrences', 1)}
**Priority:** {gap.get('research_priority', 'P2')}

**Statement:**
{gap.get('statement', 'No statement')}

**Evidence Sources:**
{chr(10).join(f'- {s}' for s in gap.get('evidence_sources', [])[:5])}

**Research Question:**
{self._generate_research_question(gap)}

**Law of the Land:** If there's no data or statistics to prove
whichever answer is the best one, then it's an opportunity for
studying and figuring it out.
""".strip()
    
    def _generate_research_question(self, gap: dict) -> str:
        """Generate the core research question from gap"""
        statement = gap.get('statement', '')
        
        # Transform statement into research question
        if '?' in statement:
            return statement
        
        # Add appropriate question prefix
        text = statement.lower()
        
        if any(word in text for word in ['number', 'count', 'total', 'how many']):
            return f"What is the precise count of {statement}?"
        elif any(word in text for word in ['missing', 'vacuum', 'none']):
            return f"Why is there nothing known about {statement}?"
        elif any(word in text for word in ['unverified', 'unproven']):
            return f"How can we verify {statement}?"
        else:
            return f"What do we need to know about {statement}?"
    
    def _persist_dispatch(self, inquiry: Inquiry):
        """Persist dispatch to local log"""
        with open(self.dispatcher_log, 'a') as f:
            f.write(json.dumps(inquiry.to_dict()) + '\n')
    
    def _write_to_praxis(self, inquiry: Inquiry):
        """Write inquiry to praxis-perpetua (append mode)"""
        if not self.inquiry_log.exists():
            # Create genesis log
            self.inquiry_log.parent.mkdir(parents=True, exist_ok=True)
            initial_data = {
                'inquiries': [],
                'last_updated': datetime.now().isoformat()
            }
            with open(self.inquiry_log, 'w') as f:
                yaml.dump(initial_data, f)
        
        # Read existing
        with open(self.inquiry_log, 'r') as f:
            data = yaml.safe_load(f) or {'inquiries': []}
        
        # Append new inquiry
        inquiry_dict = {
            'id': inquiry.id,
            'title': inquiry.title,
            'description': inquiry.description,
            'priority': inquiry.priority,
            'status': inquiry.status,
            'created_at': inquiry.created_at,
            'source': 'organvm-scrutator',
            'gap_id': inquiry.gap_id
        }
        
        data['inquiries'].append(inquiry_dict)
        data['last_updated'] = datetime.now().isoformat()
        
        # Write back
        with open(self.inquiry_log, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    
    def get_dispatch_status(self) -> dict:
        """Get status of all dispatched inquiries"""
        local_inquiries = []
        
        if self.dispatcher_log.exists():
            with open(self.dispatcher_log, 'r') as f:
                for line in f:
                    if line.strip():
                        local_inquiries.append(json.loads(line))
        
        praxis_inquiries = self.load_inquiry_log()
        
        return {
            'local_dispatches': len(local_inquiries),
            'praxis_commissions': len(praxis_inquiries),
            'by_status': self._count_by_status(local_inquiries, praxis_inquiries)
        }
    
    def _count_by_status(self, local: list, praxis: list) -> dict:
        counts = {}
        for inquiry in local + praxis:
            status = inquiry.get('status', 'unknown')
            counts[status] = counts.get(status, 0) + 1
        return counts