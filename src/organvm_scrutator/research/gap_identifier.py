"""
Gap Identifier — Identifies what the system doesn't know

Every gap is a research opportunity. This module scans the governance
system for unanswered questions, unverified claims, and unknown unknowns.
"""

import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Gap:
    """Represents a single knowledge gap"""
    id: str
    discovered_at: str
    statement: str
    category: str  # unknown, unverified, unexplored
    severity: str  # critical, high, medium, low
    occurrences: int = 1
    evidence_sources: list[str] = None
    related_gaps: list[str] = None
    
    def __post_init__(self):
        if self.evidence_sources is None:
            self.evidence_sources = []
        if self.related_gaps is None:
            self.related_gaps = []
    
    def to_dict(self) -> dict:
        return asdict(self)


class GapIdentifier:
    """
    Identifies gaps in system knowledge.
    
    Gap categories:
    - UNKNOWN: The system doesn't know this exists
    - UNVERIFIED: Known but not proven
    - UNEXPLORED: Known to exist but not studied
    
    Law of the Land: Every gap is a research opportunity. The system
    must actively seek its own ignorance.
    """
    
    # Patterns that indicate gaps
    VACUUM_PATTERNS = [
        re.compile(r'VACUUM:\s*(.+)', re.IGNORECASE),
        re.compile(r'\?{3,}(.+)', re.IGNORECASE),
        re.compile(r'unknown\s+unknown', re.IGNORECASE),
        re.compile(r'tbd|to be determined', re.IGNORECASE),
        re.compile(r'not\s+(?:yet\s+)?(?:implemented|done|tested|verified)', re.IGNORECASE),
    ]
    
    # Claim patterns for evidence verification
    CLAIM_PATTERNS = [
        re.compile(r'(\d+)\s+(?:repos|files|items|atoms|plans|sessions)', re.IGNORECASE),
        re.compile(r'(?:total|sum|count|number)\s+(?:of\s+)?(\w+)', re.IGNORECASE),
        re.compile(r'(\w+)\s*%\s+(?:complete|done|coverage)', re.IGNORECASE),
    ]
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or os.environ.get(
            'SCRUTATOR_DATA',
            str(Path(__file__).parent.parent.parent.parent / 'data')
        ) / 'research')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.gaps_file = self.data_dir / 'gaps.jsonl'
        self.gaps: list[Gap] = []
    
    def load_gaps(self) -> list[Gap]:
        """Load existing gaps from storage"""
        self.gaps = []
        
        if self.gaps_file.exists():
            with open(self.gaps_file, 'r') as f:
                for line in f:
                    if line.strip():
                        self.gaps.append(Gap(**json.loads(line)))
        
        return self.gaps
    
    def scan_for_gaps(self, sources: list[str] = None) -> list[Gap]:
        """Scan source files for gaps"""
        if sources is None:
            sources = self._default_sources()
        
        new_gaps = []
        
        for source_path in sources:
            path = Path(source_path)
            if not path.exists():
                continue
            
            try:
                content = path.read_text()
                gaps_found = self._extract_gaps(content, str(path))
                new_gaps.extend(gaps_found)
            except Exception as e:
                print(f"Warning: Failed to scan {source_path}: {e}")
        
        # Deduplicate and merge
        self._merge_gaps(new_gaps)
        
        return self.gaps
    
    def _default_sources(self) -> list[str]:
        """Get default sources for gap scanning"""
        home = Path.home()
        return [
            str(home / 'Workspace' / 'organvm' / 'organvm-corpvs-testamentvm' / 'INST-INDEX-RERUM-FACIENDARUM.md'),
            str(home / 'Workspace' / 'organvm' / 'organvm-corpvs-testamentvm' / 'data'),
            str(home / '.claude' / 'plans'),
            str(home / 'Workspace' / 'organvm' / 'praxis-perpetua' / 'commissions' / 'inquiry-log.yaml'),
        ]
    
    def _extract_gaps(self, content: str, source: str) -> list[Gap]:
        """Extract gaps from content"""
        gaps = []
        
        for pattern in self.VACUUM_PATTERNS:
            for match in pattern.finditer(content):
                statement = match.group(1).strip()
                
                # Determine category
                if 'vacuum' in statement.lower():
                    category = 'UNEXPLORED'
                elif '?' in statement:
                    category = 'UNKNOWN'
                else:
                    category = 'UNVERIFIED'
                
                gap = Gap(
                    id=f"GAP-{len(self.gaps) + len(gaps) + 1:05d}",
                    discovered_at=datetime.now().isoformat(),
                    statement=statement[:200],  # Truncate for sanity
                    category=category,
                    severity=self._assess_severity(statement),
                    evidence_sources=[source]
                )
                gaps.append(gap)
        
        return gaps
    
    def _assess_severity(self, statement: str) -> str:
        """Assess gap severity based on content"""
        text = statement.lower()
        
        if any(word in text for word in ['critical', 'blocker', 'p0', 'emergency', 'security']):
            return 'critical'
        if any(word in text for word in ['important', 'p1', 'priority', 'significant']):
            return 'high'
        if any(word in text for word in ['should', 'would be nice', 'eventually']):
            return 'medium'
        
        return 'low'
    
    def _merge_gaps(self, new_gaps: list[Gap]):
        """Merge new gaps with existing, deduplicating similar statements"""
        for new_gap in new_gaps:
            # Check for similar existing gap
            similar = None
            for existing in self.gaps:
                if self._statements_similar(new_gap.statement, existing.statement):
                    similar = existing
                    break
            
            if similar:
                # Update occurrence count and sources
                similar.occurrences += 1
                if new_gap.evidence_sources[0] not in similar.evidence_sources:
                    similar.evidence_sources.append(new_gap.evidence_sources[0])
            else:
                self.gaps.append(new_gap)
                self._persist_gap(new_gap)
    
    def _statements_similar(self, a: str, b: str) -> bool:
        """Check if two statements are similar enough to be considered the same gap"""
        # Simple word overlap check
        words_a = set(a.lower().split())
        words_b = set(b.lower().split())
        
        overlap = len(words_a & words_b)
        total = len(words_a | words_b)
        
        return overlap / total > 0.5 if total > 0 else False
    
    def _persist_gap(self, gap: Gap):
        """Append gap to JSONL storage"""
        with open(self.gaps_file, 'a') as f:
            f.write(json.dumps(gap.to_dict()) + '\n')
    
    def get_research_queue(self) -> list[dict]:
        """Get gaps ranked by research priority"""
        if not self.gaps:
            self.load_gaps()
        
        # Sort by severity and occurrences
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        sorted_gaps = sorted(
            self.gaps,
            key=lambda g: (severity_order.get(g.severity, 4), -g.occurrences)
        )
        
        return [
            {
                'gap_id': g.id,
                'statement': g.statement,
                'category': g.category,
                'severity': g.severity,
                'occurrences': g.occurrences,
                'evidence_sources': g.evidence_sources[:3],
                'research_priority': self._compute_research_priority(g)
            }
            for g in sorted_gaps[:50]  # Top 50
        ]
    
    def _compute_research_priority(self, gap: Gap) -> str:
        """Compute research priority for a gap"""
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        score = severity_order.get(gap.severity, 3) * 10 + (10 - min(gap.occurrences * 2, 10))
        
        if score < 15:
            return 'P0'
        elif score < 25:
            return 'P1'
        elif score < 35:
            return 'P2'
        else:
            return 'P3'
    
    def export_gap_queue(self, output_path: Optional[str] = None) -> str:
        """Export gap queue to YAML"""
        import yaml
        
        queue = self.get_research_queue()
        
        if output_path is None:
            output_path = str(self.data_dir / 'gap-queue.yaml')
        
        with open(output_path, 'w') as f:
            yaml.dump({'gaps': queue, 'total': len(queue)}, f, default_flow_style=False)
        
        return output_path