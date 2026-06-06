from organvm_scrutator.governance.energy_ledger import EnergyLedger
from organvm_scrutator.governance.question_ledger import QuestionLedger
from organvm_scrutator.research.gap_identifier import GapIdentifier
from organvm_scrutator.scanner.question_counter import QuestionCounter


def test_question_ledger_reexports_scanner_counter(tmp_path):
    ledger = QuestionLedger(str(tmp_path))

    assert isinstance(ledger, QuestionCounter)
    assert ledger.data_dir == tmp_path / "raw"


def test_scrutator_data_env_builds_expected_subdirectories(tmp_path, monkeypatch):
    monkeypatch.setenv("SCRUTATOR_DATA", str(tmp_path))

    energy = EnergyLedger()
    gaps = GapIdentifier()

    assert energy.data_dir == tmp_path / "raw"
    assert gaps.data_dir == tmp_path / "research"
    assert energy.analyze()["total_sessions"] == 0
