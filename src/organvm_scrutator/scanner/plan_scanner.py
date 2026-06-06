"""
Plan Scanner — Scans all .claude/plans/ directories across the workspace

Discovers, parses, and indexes every plan file to build the master visibility index.
"""

import json
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class PlanMetadata:
    """Represents a single plan file's metadata"""
    plan_id: str
    file_path: str
    repo: str
    created: str
    modified: str
    status: str
    author: Optional[str] = None
    parent_irf: Optional[str] = None
    lines: int = 0
    words: int = 0
    
    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


class PlanScanner:
    """
    Scans all .claude/plans/ directories across configured workspaces.
    
    Discovery patterns:
    - ~/Workspace/organvm/*/.claude/plans/
    - ~/.claude/plans/
    - ~/Workspace/4444J99/*/.claude/plans/
    """
    
    # Patterns for extracting metadata from plan filenames and content
    DATE_PATTERN = re.compile(r'(\d{4}-\d{2}-\d{2})')
    PLAN_ID_PATTERN = re.compile(r'\*\*Plan ID:\*\*\s*(\S+)')
    STATUS_PATTERN = re.compile(r'\*\*Status:\*\*\s*(\S+)')
    AUTHOR_PATTERN = re.compile(r'\*\*Author:\*\*\s*(.+)')
    PARENT_IRF_PATTERN = re.compile(r'\*\*Parent IRF:\*\*\s*(\S+)')
    
    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = Path(workspace_root or os.environ.get(
            'SCRUTATOR_WORKSPACE_ROOT', 
            str(Path.home() / 'Workspace')
        ))
        self.exclude_patterns = ['contrib--', 'bench/', '.git', 'node_modules']
        self.plans: list[PlanMetadata] = []
        
    def scan_all(self) -> list[PlanMetadata]:
        """Run full scan across all configured plan directories"""
        self.plans = []
        
        # Scan global plans (~/.claude/plans/)
        global_plans = self._scan_directory(Path.home() / '.claude' / 'plans')
        self.plans.extend(global_plans)
        
        # Scan organvm workspace plans
        organvm_root = self.workspace_root / 'organvm'
        if organvm_root.exists():
            for repo_dir in organvm_root.iterdir():
                if repo_dir.is_dir() and not self._is_excluded(repo_dir.name):
                    plan_dir = repo_dir / '.claude' / 'plans'
                    if plan_dir.exists():
                        repo_plans = self._scan_directory(plan_dir, repo_dir.name)
                        self.plans.extend(repo_plans)
        
        # Scan 4444J99 workspace
        j99_root = self.workspace_root / '4444J99'
        if j99_root.exists():
            for repo_dir in j99_root.iterdir():
                if repo_dir.is_dir() and not self._is_excluded(repo_dir.name):
                    plan_dir = repo_dir / '.claude' / 'plans'
                    if plan_dir.exists():
                        repo_plans = self._scan_directory(plan_dir, repo_dir.name)
                        self.plans.extend(repo_plans)
        
        return self.plans
    
    def _scan_directory(self, plan_dir: Path, repo: str = 'global') -> list[PlanMetadata]:
        """Scan a single plan directory"""
        plans = []
        
        for plan_file in plan_dir.glob('*.md'):
            try:
                metadata = self._parse_plan_file(plan_file, repo)
                if metadata:
                    plans.append(metadata)
            except Exception as e:
                print(f"Warning: Failed to parse {plan_file}: {e}")
                
        return plans
    
    def _parse_plan_file(self, file_path: Path, repo: str) -> Optional[PlanMetadata]:
        """Extract metadata from a plan file"""
        content = file_path.read_text()
        
        # Extract from filename
        filename = file_path.stem
        date_match = self.DATE_PATTERN.search(filename)
        
        # Extract from content
        plan_id_match = self.PLAN_ID_PATTERN.search(content)
        status_match = self.STATUS_PATTERN.search(content)
        author_match = self.AUTHOR_PATTERN.search(content)
        parent_irf_match = self.PARENT_IRF_PATTERN.search(content)
        
        # Get file stats
        stat = file_path.stat()
        
        return PlanMetadata(
            plan_id=plan_id_match.group(1) if plan_id_match else filename,
            file_path=str(file_path),
            repo=repo,
            created=datetime.fromtimestamp(stat.st_ctime).isoformat()[:10],
            modified=datetime.fromtimestamp(stat.st_mtime).isoformat()[:10],
            status=status_match.group(1) if status_match else 'UNKNOWN',
            author=author_match.group(1).strip() if author_match else None,
            parent_irf=parent_irf_match.group(1) if parent_irf_match else None,
            lines=len(content.splitlines()),
            words=len(content.split())
        )
    
    def _is_excluded(self, name: str) -> bool:
        """Check if directory should be excluded"""
        for pattern in self.exclude_patterns:
            if pattern in name:
                return True
        return False
    
    def generate_index(self) -> dict:
        """Generate the master visibility index"""
        return {
            'generated_at': datetime.now().isoformat(),
            'total_plans': len(self.plans),
            'by_repo': self._group_by_repo(),
            'by_status': self._group_by_status(),
            'by_date': self._group_by_date(),
            'plans': [p.to_dict() for p in self.plans]
        }
    
    def _group_by_repo(self) -> dict:
        groups = {}
        for plan in self.plans:
            groups[plan.repo] = groups.get(plan.repo, 0) + 1
        return groups
    
    def _group_by_status(self) -> dict:
        groups = {}
        for plan in self.plans:
            groups[plan.status] = groups.get(plan.status, 0) + 1
        return groups
    
    def _group_by_date(self) -> dict:
        groups = {}
        for plan in self.plans:
            date = plan.created[:7]  # YYYY-MM
            groups[date] = groups.get(date, 0) + 1
        return groups
    
    def save_index(self, output_path: Optional[str] = None):
        """Save index to file"""
        index = self.generate_index()
        
        if output_path is None:
            output_dir = Path(os.environ.get(
                'SCRUTATOR_INDICES',
                str(Path(__file__).parent.parent.parent.parent / 'data' / 'indices')
            ))
            output_path = str(output_dir / 'visibility-index.md')
        
        # Generate markdown index
        md = self._render_markdown(index)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(md)
        
        # Also save JSON for programmatic access
        json_path = output_path.replace('.md', '.json')
        Path(json_path).write_text(json.dumps(index, indent=2))
        
        return output_path
    
    def _render_markdown(self, index: dict) -> str:
        """Render index as markdown"""
        lines = [
            "# Visibility Index — Plan Registry",
            f"",
            f"**Generated:** {index['generated_at']}",
            f"**Total Plans:** {index['total_plans']}",
            f"",
            "## By Repository",
            f""
        ]
        
        for repo, count in sorted(index['by_repo'].items(), key=lambda x: -x[1]):
            lines.append(f"- `{repo}`: {count} plans")
        
        lines.extend(["", "## By Status", ""])
        for status, count in sorted(index['by_status'].items(), key=lambda x: -x[1]):
            lines.append(f"- `{status}`: {count}")
        
        lines.extend(["", "## By Month", ""])
        for date, count in sorted(index['by_date'].items(), reverse=True):
            lines.append(f"- {date}: {count}")
        
        lines.extend(["", "---", "", "## Full Registry", ""])
        
        for plan in sorted(index['plans'], key=lambda x: x['modified'], reverse=True)[:50]:
            lines.append(f"### {plan['plan_id']}")
            lines.append(f"- **Repo:** `{plan['repo']}`")
            lines.append(f"- **Status:** {plan['status']}")
            lines.append(f"- **Created:** {plan['created']}")
            lines.append(f"- **Modified:** {plan['modified']}")
            lines.append(f"- **Words:** {plan['words']}")
            lines.append(f"- **Path:** `{plan['file_path']}`")
            lines.append("")
        
        return "\n".join(lines)
