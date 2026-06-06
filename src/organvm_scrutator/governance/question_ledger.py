"""
Question Ledger — Tracks questions (imported from scanner for re-export compatibility)
"""

from organvm_scrutator.scanner.question_counter import Question, QuestionCounter


class QuestionLedger(QuestionCounter):
    """Governance-facing compatibility wrapper for question storage."""


__all__ = ["QuestionLedger", "QuestionCounter", "Question"]
