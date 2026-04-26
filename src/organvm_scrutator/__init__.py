"""
organvm-scrutator — Self-Auditing Governance System

Law of the Land: If there's no data or statistics to prove whichever
answer is the best one, then it's an opportunity for studying and figuring it out.

This system scrutinizes itself: it watches the watchers, measures the measurers,
and tracks every gap between what is known and what remains unknown.
"""

__version__ = "0.1.0"
__author__ = "ORGANVM System"

from organvm_scrutator.scanner.plan_scanner import PlanScanner
from organvm_scrutator.scanner.question_counter import QuestionCounter
from organvm_scrutator.scanner.atom_tracker import AtomTracker
from organvm_scrutator.governance.question_ledger import QuestionLedger
from organvm_scrutator.governance.suggestion_ledger import SuggestionLedger
from organvm_scrutator.governance.energy_ledger import EnergyLedger
from organvm_scrutator.research.gap_identifier import GapIdentifier
from organvm_scrutator.research.inquiry_dispatcher import InquiryDispatcher
from organvm_scrutator.viz.index_generator import IndexGenerator
from organvm_scrutator.viz.dashboard import Dashboard

__all__ = [
    "PlanScanner",
    "QuestionCounter", 
    "AtomTracker",
    "QuestionLedger",
    "SuggestionLedger",
    "EnergyLedger",
    "GapIdentifier",
    "InquiryDispatcher",
    "IndexGenerator",
    "Dashboard",
]