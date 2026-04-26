"""
Index Generator — Generates markdown indices from scan data

Produces the master visibility index and derived indices for human review.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml


class IndexGenerator:
    """
    Generates various indices from scan data.
    
    Indices produced:
    - visibility-index.md: Master plan registry
    - session-chronology.md: Chronological session manifest
    - governance-metrics.yaml: Aggregated metrics
    - evidence-hierarchy.md: Claims and their evidence levels
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or Path(__file__).parent.parent.parent / 'data')
        self.indices_dir = self.data_dir / 'indices'
        self.indices_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_visibility_index(self, scanner) -> str:
        """Generate the master visibility index"""
        index = scanner.generate_index()
        
        md = f"""# Visibility Index — Plan Registry

**Generated:** {index['generated_at']}
**Total Plans:** {index['total_plans']}

---

## Summary

| Metric | Value |
|--------|-------|
| Total Plans | {index['total_plans']} |
| Repositories | {len(index['by_repo'])} |
| Statuses | {len(index['by_status'])} |

---

## By Repository

"""
        
        for repo, count in sorted(index['by_repo'].items(), key=lambda x: -x[1]):
            md += f"- `{repo}`: {count} plans\n"
        
        md += "\n## By Status\n\n"
        
        for status, count in sorted(index['by_status'].items(), key=lambda x: -x[1]):
            md += f"- `{status}`: {count}\n"
        
        md += "\n## By Month\n\n"
        
        for date, count in sorted(index['by_date'].items(), reverse=True):
            md += f"- {date}: {count}\n"
        
        md += f"""
---

## Plan Details

Showing most recently modified plans.

"""
        
        for plan in sorted(index['plans'], key=lambda x: x['modified'], reverse=True)[:50]:
            md += f"""### {plan['plan_id']}

| Field | Value |
|-------|-------|
| Repository | `{plan['repo']}` |
| Status | {plan['status']} |
| Created | {plan['created']} |
| Modified | {plan['modified']} |
| Lines | {plan['lines']} |
| Words | {plan['words']} |

**Path:** `{plan['file_path']}`

---
"""
        
        output_path = self.indices_dir / 'visibility-index.md'
        output_path.write_text(md)
        
        return str(output_path)
    
    def generate_session_chronology(self, energy_ledger) -> str:
        """Generate chronological session manifest"""
        energy_ledger.load_energy_records()
        
        md = f"""# Session Chronology

**Generated:** {datetime.now().isoformat()}
**Total Sessions:** {len(energy_ledger.energy_records)}

---

## Sessions by Date

"""
        
        # Group by date
        by_date = {}
        for record in energy_ledger.energy_records:
            date = record.timestamp[:10]
            if date not in by_date:
                by_date[date] = []
            by_date[date].append(record)
        
        for date in sorted(by_date.keys(), reverse=True):
            md += f"### {date}\n\n"
            for record in by_date[date]:
                md += f"""**{record.session_id}**

| Metric | Value |
|--------|-------|
| Questions | {record.questions_asked} |
| Suggestions | {record.suggestions_made} |
| Atoms | {record.atoms_created} |
| Completions | {record.completions} |
| Input | {record.total_input} |
| Output | {record.total_output} |
| Efficiency | {record.efficiency_ratio:.2f} |

"""
        
        output_path = self.indices_dir / 'session-chronology.md'
        output_path.write_text(md)
        
        return str(output_path)
    
    def generate_governance_metrics(self, **analyses) -> str:
        """Generate aggregated governance metrics"""
        
        metrics = {
            'generated_at': datetime.now().isoformat(),
            'plans': analyses.get('plans', {}),
            'questions': analyses.get('questions', {}),
            'suggestions': analyses.get('suggestions', {}),
            'atoms': analyses.get('atoms', {}),
            'energy': analyses.get('energy', {}),
            'gaps': analyses.get('gaps', {})
        }
        
        output_path = self.indices_dir / 'governance-metrics.yaml'
        
        with open(output_path, 'w') as f:
            yaml.dump(metrics, f, default_flow_style=False, sort_keys=False)
        
        return str(output_path)
    
    def generate_evidence_hierarchy(self, claims: list[dict]) -> str:
        """Generate evidence hierarchy for claims"""
        
        # Categorize by evidence level
        by_level = {'proven': [], 'studied': [], 'hypothesized': [], 'unknown': []}
        
        for claim in claims:
            level = claim.get('evidence_level', 'unknown')
            if level not in by_level:
                level = 'unknown'
            by_level[level].append(claim)
        
        md = f"""# Evidence Hierarchy

**Generated:** {datetime.now().isoformat()}

This document tracks every claim made in the system and its evidence level.

---

## Proven (Verifiable Data)

{len(by_level['proven'])} claims with verified evidence

"""
        
        for claim in by_level['proven']:
            md += f"""### {claim.get('statement', 'Unknown')}

**Evidence:** {claim.get('evidence_source', 'N/A')}

"""
        
        md += "\n## Studied (Analyzed, Unverified)\n\n"
        
        for claim in by_level['studied']:
            md += f"""### {claim.get('statement', 'Unknown')}

**Status:** {claim.get('status', 'studied')}

"""
        
        md += "\n## Hypothesized (Theoretical)\n\n"
        
        for claim in by_level['hypothesized']:
            md += f"""### {claim.get('statement', 'Unknown')}

"""
        
        md += "\n## Unknown (Research Opportunities)\n\n"
        
        for claim in by_level['unknown']:
            md += f"""### {claim.get('statement', 'Unknown')}

**Category:** {claim.get('category', 'unknown')}

"""
        
        output_path = self.indices_dir / 'evidence-hierarchy.md'
        output_path.write_text(md)
        
        return str(output_path)