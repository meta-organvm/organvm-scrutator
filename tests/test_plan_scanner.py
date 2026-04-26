import pytest
from pathlib import Path
from organvm_scrutator.scanner.plan_scanner import PlanScanner, PlanMetadata


class TestPlanScanner:
    """Tests for the PlanScanner module"""
    
    def test_scanner_initialization(self):
        scanner = PlanScanner()
        assert scanner.workspace_root == scanner.workspace_root
        assert scanner.plans == []
    
    def test_is_excluded(self):
        scanner = PlanScanner()
        assert scanner._is_excluded('contrib--some-repo') == True
        assert scanner._is_excluded('bench/some-repo') == True
        assert scanner._is_excluded('normal-repo') == False
    
    def test_plan_metadata_to_dict(self):
        plan = PlanMetadata(
            plan_id="TEST-001",
            file_path="/test/path.md",
            repo="test-repo",
            created="2026-04-26",
            modified="2026-04-26",
            status="DRAFT"
        )
        d = plan.to_dict()
        assert d['plan_id'] == "TEST-001"
        assert d['repo'] == "test-repo"
        assert d['status'] == "DRAFT"