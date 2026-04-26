"""
Dashboard — Visual dashboard for governance metrics

Provides a TUI or web-based interface for viewing governance metrics.
"""

from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text


class Dashboard:
    """
    Interactive dashboard for governance metrics.
    
    Provides multiple view modes:
    - TUI: Terminal-based using Rich
    - HTML: Web dashboard (future)
    - JSON: API endpoint (future)
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or Path(__file__).parent.parent.parent / 'data')
        self.console = Console()
    
    def render_tui(self, **analyses):
        """Render TUI dashboard"""
        self.console.clear()
        
        # Header
        header = Text("ORGANVM SCRUTATOR", justify="center", style="bold cyan")
        self.console.print(Panel(header, style="on blue"))
        
        # Top-level metrics
        self._render_metrics_grid(analyses)
        
        # Detailed sections
        self._render_questions(analyses.get('questions', {}))
        self._render_suggestions(analyses.get('suggestions', {}))
        self._render_energy(analyses.get('energy', {}))
        self._render_gaps(analyses.get('gaps', []))
    
    def _render_metrics_grid(self, analyses: dict):
        """Render top metrics grid"""
        
        plans = analyses.get('plans', {})
        questions = analyses.get('questions', {})
        suggestions = analyses.get('suggestions', {})
        atoms = analyses.get('atoms', {})
        energy = analyses.get('energy', {})
        
        grid = Table(show_header=False, pad=False)
        grid.add_column(width=20)
        grid.add_column(width=20)
        grid.add_column(width=20)
        grid.add_column(width=20)
        
        grid.add_row(
            self._metric_cell("Plans", plans.get('total_plans', 0)),
            self._metric_cell("Questions", questions.get('total_questions', 0)),
            self._metric_cell("Suggestions", suggestions.get('total_suggestions', 0)),
            self._metric_cell("Atoms", atoms.get('total_atoms', 0))
        )
        
        grid.add_row(
            self._metric_cell("Accept Rate", f"{suggestions.get('acceptance_rate', 0):.1%}"),
            self._metric_cell("Completion", f"{atoms.get('completion_rate', 0):.1%}"),
            self._metric_cell("Efficiency", f"{energy.get('system_efficiency', 0):.2f}"),
            self._metric_cell("State", energy.get('metabolic_state', 'N/A'))
        )
        
        self.console.print(grid)
    
    def _metric_cell(self, label: str, value) -> Panel:
        """Create a metric cell"""
        return Panel(
            f"[bold]{value}[/bold]\n[dim]{label}[/dim]",
            style="on black"
        )
    
    def _render_questions(self, questions: dict):
        """Render questions section"""
        if not questions:
            return
        
        table = Table(title="Question Analysis", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Total", str(questions.get('total_questions', 0)))
        table.add_row("Answered", str(questions.get('answered', 0)))
        table.add_row("Unanswered", str(questions.get('unanswered', 0)))
        table.add_row("Rate", f"{questions.get('answer_rate', 0):.1%}")
        
        self.console.print(table)
    
    def _render_suggestions(self, suggestions: dict):
        """Render suggestions section"""
        if not suggestions:
            return
        
        table = Table(title="Suggestion Analysis", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Total", str(suggestions.get('total_suggestions', 0)))
        table.add_row("Accepted", str(suggestions.get('accepted', 0)))
        table.add_row("Rejected", str(suggestions.get('rejected', 0)))
        table.add_row("Rate", f"{suggestions.get('acceptance_rate', 0):.1%}")
        
        self.console.print(table)
    
    def _render_energy(self, energy: dict):
        """Render energy section"""
        if not energy:
            return
        
        table = Table(title="Energy Analysis", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Sessions", str(energy.get('total_sessions', 0)))
        table.add_row("Input", str(energy.get('total_input_energy', 0)))
        table.add_row("Output", str(energy.get('total_output_energy', 0)))
        table.add_row("State", energy.get('metabolic_state', 'UNKNOWN'))
        
        self.console.print(table)
    
    def _render_gaps(self, gaps: list):
        """Render gaps section"""
        if not gaps:
            return
        
        table = Table(title="Top Research Gaps", show_header=True)
        table.add_column("ID", style="cyan")
        table.add_column("Category", style="magenta")
        table.add_column("Severity", style="yellow")
        table.add_column("Priority", style="green")
        
        for gap in gaps[:10]:
            table.add_row(
                gap.get('gap_id', 'N/A'),
                gap.get('category', 'N/A'),
                gap.get('severity', 'N/A'),
                gap.get('research_priority', 'N/A')
            )
        
        self.console.print(table)
    
    def export_html(self, output_path: Optional[str] = None) -> str:
        """Export dashboard as HTML"""
        
        if output_path is None:
            output_path = str(self.data_dir / 'indices' / 'dashboard.html')
        
        html = """<!DOCTYPE html>
<html>
<head>
    <title>ORGANVM Scrutator Dashboard</title>
    <style>
        body { font-family: system-ui; max-width: 1200px; margin: 0 auto; padding: 20px; }
        .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 20px 0; }
        .metric { background: #1a1a2e; color: #eee; padding: 20px; border-radius: 8px; text-align: center; }
        .metric-value { font-size: 2em; font-weight: bold; }
        .metric-label { color: #888; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #1a1a2e; color: white; }
    </style>
</head>
<body>
    <h1>ORGANVM Scrutator Dashboard</h1>
    <p>Self-auditing governance metrics</p>
    
    <h2>System Overview</h2>
    <div class="metric-grid">
        <div class="metric">
            <div class="metric-value">--</div>
            <div class="metric-label">Plans</div>
        </div>
        <div class="metric">
            <div class="metric-value">--</div>
            <div class="metric-label">Questions</div>
        </div>
        <div class="metric">
            <div class="metric-value">--</div>
            <div class="metric-label">Suggestions</div>
        </div>
        <div class="metric">
            <div class="metric-value">--</div>
            <div class="metric-label">Atoms</div>
        </div>
    </div>
    
    <h2>Research Gaps</h2>
    <p>Run <code>organvm-scrutator gaps</code> to populate</p>
</body>
</html>"""
        
        Path(output_path).write_text(html)
        return output_path