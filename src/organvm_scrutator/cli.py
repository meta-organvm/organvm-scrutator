"""
organvm-scrutator CLI — Self-Auditing Governance System

Usage:
    organvm-scrutator scan          # Scan all plans
    organvm-scrutator questions    # Question analysis
    organvm-scrutator suggestions  # Suggestion analysis  
    organvm-scrutator atoms        # Atom tracking
    organvm-scrutator energy       # Energy metrics
    organvm-scrutator gaps         # Gap analysis
    organvm-scrutator dispatch     # Dispatch gaps to research
    organvm-scrutator stats        # Full system stats
    organvm-scrutator dashboard   # Start dashboard
"""

import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from organvm_scrutator.scanner.plan_scanner import PlanScanner
from organvm_scrutator.scanner.question_counter import QuestionCounter
from organvm_scrutator.scanner.atom_tracker import AtomTracker
from organvm_scrutator.governance.suggestion_ledger import SuggestionLedger
from organvm_scrutator.governance.energy_ledger import EnergyLedger
from organvm_scrutator.research.gap_identifier import GapIdentifier
from organvm_scrutator.research.inquiry_dispatcher import InquiryDispatcher


console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """organvm-scrutator — Self-Auditing Governance System
    
    Law of the Land: If there's no data or statistics to prove whichever
    answer is the best one, then it's an opportunity for studying and figuring it out.
    """
    pass


@main.command()
def scan():
    """Scan all .claude/plans/ directories across the workspace"""
    console.print("[bold blue]Scanning plans...[/bold blue]")
    
    scanner = PlanScanner()
    plans = scanner.scan_all()
    
    console.print(f"[green]Found {len(plans)} plans[/green]")
    
    # Generate and save index
    output = scanner.save_index()
    console.print(f"[green]Index saved to {output}[/green]")


@main.command()
def questions():
    """Analyze questions asked by agents"""
    console.print("[bold blue]Analyzing questions...[/bold blue]")
    
    qc = QuestionCounter()
    analysis = qc.analyze()
    
    table = Table(title="Question Analysis")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Questions", str(analysis['total_questions']))
    table.add_row("Answered", str(analysis['answered']))
    table.add_row("Unanswered", str(analysis['unanswered']))
    table.add_row("Answer Rate", f"{analysis['answer_rate']:.1%}")
    
    console.print(table)
    
    # Export
    output = qc.export_to_yaml()
    console.print(f"[green]Exported to {output}[/green]")


@main.command()
def suggestions():
    """Analyze agent suggestions and acceptance rates"""
    console.print("[bold blue]Analyzing suggestions...[/bold blue]")
    
    ledger = SuggestionLedger()
    analysis = ledger.analyze()
    
    table = Table(title="Suggestion Analysis")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Suggestions", str(analysis['total_suggestions']))
    table.add_row("Accepted", str(analysis['accepted']))
    table.add_row("Rejected", str(analysis['rejected']))
    table.add_row("Modified", str(analysis['modified']))
    table.add_row("Acceptance Rate", f"{analysis['acceptance_rate']:.1%}")
    
    console.print(table)
    
    # Show by agent
    if analysis.get('by_agent'):
        agent_table = Table(title="By Agent")
        agent_table.add_column("Agent", style="cyan")
        agent_table.add_column("Total", style="magenta")
        agent_table.add_column("Accepted", style="green")
        agent_table.add_column("Rate", style="yellow")
        
        for agent, stats in analysis['by_agent'].items():
            agent_table.add_row(
                agent,
                str(stats['total']),
                str(stats['accepted']),
                f"{stats['acceptance_rate']:.1%}"
            )
        
        console.print(agent_table)


@main.command()
def atoms():
    """Analyze atom (work item) creation and completion"""
    console.print("[bold blue]Analyzing atoms...[/bold blue]")
    
    tracker = AtomTracker()
    analysis = tracker.analyze()
    
    table = Table(title="Atom Analysis")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Atoms", str(analysis['total_atoms']))
    table.add_row("Open", str(analysis['open']))
    table.add_row("In Progress", str(analysis['in_progress']))
    table.add_row("Completed", str(analysis['completed']))
    table.add_row("Blocked", str(analysis['blocked']))
    table.add_row("Completion Rate", f"{analysis['completion_rate']:.1%}")
    
    console.print(table)
    
    # Export
    output = tracker.export_metrics()
    console.print(f"[green]Exported to {output}[/green]")


@main.command()
def energy():
    """Analyze session energy (input vs output)"""
    console.print("[bold blue]Analyzing energy...[/bold blue]")
    
    ledger = EnergyLedger()
    analysis = ledger.analyze()
    
    table = Table(title="Energy Analysis (Metabolic State)")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Sessions", str(analysis.get('total_sessions', 0)))
    table.add_row("Total Input Energy", str(analysis.get('total_input_energy', 0)))
    table.add_row("Total Output Energy", str(analysis.get('total_output_energy', 0)))
    table.add_row("System Efficiency", f"{analysis.get('system_efficiency', 0):.2f}")
    table.add_row("Metabolic State", analysis.get('metabolic_state', 'UNKNOWN'))
    
    console.print(table)
    
    # Efficiency distribution
    if analysis.get('efficiency_distribution'):
        dist = analysis['efficiency_distribution']
        dist_table = Table(title="Efficiency Distribution")
        dist_table.add_column("State", style="cyan")
        dist_table.add_column("Sessions", style="magenta")
        
        dist_table.add_row("Efficient (≥1.0)", str(dist.get('efficient', 0)))
        dist_table.add_row("Learning (0-1.0)", str(dist.get('learning', 0)))
        dist_table.add_row("Exploring (0)", str(dist.get('exploring', 0)))
        
        console.print(dist_table)
    
    # Export
    output = ledger.export_metrics()
    console.print(f"[green]Exported to {output}[/green]")


@main.command()
def gaps():
    """Identify and analyze knowledge gaps"""
    console.print("[bold blue]Identifying gaps...[/bold blue]")
    
    identifier = GapIdentifier()
    identifier.scan_for_gaps()
    
    queue = identifier.get_research_queue()
    
    console.print(f"[green]Found {len(queue)} research opportunities[/green]")
    
    # Show top gaps
    if queue:
        gap_table = Table(title="Top Research Gaps")
        gap_table.add_column("Gap ID", style="cyan")
        gap_table.add_column("Category", style="magenta")
        gap_table.add_column("Severity", style="yellow")
        gap_table.add_column("Priority", style="green")
        
        for gap in queue[:10]:
            gap_table.add_row(
                gap['gap_id'],
                gap['category'],
                gap['severity'],
                gap['research_priority']
            )
        
        console.print(gap_table)
    
    # Export
    output = identifier.export_gap_queue()
    console.print(f"[green]Exported to {output}[/green]")


@main.command()
@click.option('--threshold', default=3, help='Minimum occurrences to dispatch')
def dispatch(threshold):
    """Dispatch gaps as research inquiries to praxis-perpetua"""
    console.print(f"[bold blue]Dispatching gaps (threshold={threshold})...[/bold blue]")
    
    identifier = GapIdentifier()
    identifier.scan_for_gaps()
    
    queue = identifier.get_research_queue()
    
    dispatcher = InquiryDispatcher()
    inquiries = dispatcher.dispatch_batch(queue, threshold)
    
    console.print(f"[green]Dispatched {len(inquiries)} inquiries[/green]")


@main.command()
def stats():
    """Show full system statistics"""
    console.print("[bold blue]Gathering system stats...[/bold blue]")
    
    # Plans
    scanner = PlanScanner()
    scanner.scan_all()
    plan_index = scanner.generate_index()
    
    # Questions
    qc = QuestionCounter()
    q_analysis = qc.analyze()
    
    # Suggestions
    sl = SuggestionLedger()
    s_analysis = sl.analyze()
    
    # Atoms
    at = AtomTracker()
    a_analysis = at.analyze()
    
    # Energy
    el = EnergyLedger()
    e_analysis = el.analyze()
    
    # Gaps
    gi = GapIdentifier()
    gi.scan_for_gaps()
    gap_queue = gi.get_research_queue()
    
    # Print summary
    console.print("\n[bold inverse]ORGANVM SCRUTATOR — SYSTEM OVERVIEW[/bold inverse]\n")
    
    summary_table = Table(show_header=False)
    summary_table.add_column("Component", style="cyan")
    summary_table.add_column("Value", style="magenta")
    
    summary_table.add_row("Plans Scanned", str(plan_index['total_plans']))
    summary_table.add_row("Questions Asked", str(q_analysis['total_questions']))
    summary_table.add_row("Suggestions Made", str(s_analysis['total_suggestions']))
    summary_table.add_row("Acceptance Rate", f"{s_analysis['acceptance_rate']:.1%}")
    summary_table.add_row("Atoms Created", str(a_analysis['total_atoms']))
    summary_table.add_row("Completion Rate", f"{a_analysis['completion_rate']:.1%}")
    summary_table.add_row("Sessions Tracked", str(e_analysis.get('total_sessions', 0)))
    summary_table.add_row("Metabolic State", e_analysis.get('metabolic_state', 'UNKNOWN'))
    summary_table.add_row("Research Gaps", str(len(gap_queue)))
    
    console.print(summary_table)


@main.command()
def dashboard():
    """Start the web dashboard (placeholder)"""
    console.print("[yellow]Dashboard not yet implemented[/yellow]")
    console.print("Run 'organvm-scrutator stats' for CLI stats")


if __name__ == '__main__':
    main()