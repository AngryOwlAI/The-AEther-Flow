from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from scripts.research_control import validate_red_team_review_artifact as validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "research_control" / "validate_red_team_review_artifact.py"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "research_control" / "red_team_review"


class RedTeamReviewArtifactValidatorTests(unittest.TestCase):
    def test_minimal_fixture_passes(self) -> None:
        receipt = validator.validate_review_file(FIXTURE_DIR / "valid_minimal.yaml")
        self.assertEqual(receipt["verdict"], "no_blocking_defect_found_as_written")
        self.assertFalse(receipt["physics_promotion_authorized"])

    def test_missing_required_field_fails(self) -> None:
        with self.assertRaises(validator.RedTeamReviewValidationError) as context:
            validator.validate_review_file(FIXTURE_DIR / "missing_required_field.yaml")
        self.assertIn("verdict", str(context.exception))

    def test_physics_promotion_true_fails(self) -> None:
        with self.assertRaises(validator.RedTeamReviewValidationError) as context:
            validator.validate_review_file(FIXTURE_DIR / "physics_promotion_true.yaml")
        self.assertIn("physics_promotion_authorized", str(context.exception))

    def test_invalid_verdict_fails(self) -> None:
        with self.assertRaises(validator.RedTeamReviewValidationError) as context:
            validator.validate_review_file(FIXTURE_DIR / "invalid_verdict.yaml")
        self.assertIn("verdict", str(context.exception))

    def test_cli_json_success_receipt(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--json",
                str(FIXTURE_DIR / "valid_minimal.yaml"),
            ],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["status"], "PASS")
        self.assertFalse(parsed["physics_promotion_authorized"])

    def test_cli_json_failure_receipt(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--json",
                str(FIXTURE_DIR / "physics_promotion_true.yaml"),
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["status"], "FAIL")
        self.assertFalse(parsed["physics_promotion_authorized"])


if __name__ == "__main__":
    unittest.main()
