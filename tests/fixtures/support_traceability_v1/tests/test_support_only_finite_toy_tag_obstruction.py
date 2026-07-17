from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.research_control.support_formalization import (
    finite_toy_tag_obstruction as formalization,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / "scripts"
    / "research_control"
    / "support_formalization"
    / "finite_toy_tag_obstruction.py"
)


class FiniteToyTagObstructionTests(unittest.TestCase):
    def test_finite_family_matches_refuter_artifact_objects(self) -> None:
        family = formalization.finite_toy_family()
        self.assertEqual(
            [item.object_id for item in family],
            ["X_plus", "X_flip", "X_scale", "X_token", "X_empty"],
        )
        self.assertEqual(len(formalization.tagged_objects(family)), 4)

    def test_partial_response_is_defined_only_on_tagged_objects(self) -> None:
        for source_object in formalization.tagged_objects():
            response = formalization.partial_response_relation(source_object)
            self.assertIsNotNone(response)
            self.assertEqual(response.orientation, source_object.tag.orientation)
            self.assertEqual(response.normalization, source_object.tag.normalization)
            self.assertEqual(response.token_semantics, source_object.tag.token_semantics)
        self.assertIsNone(
            formalization.partial_response_relation(formalization.untagged_object())
        )

    def test_tag_erasure_makes_response_undefined(self) -> None:
        result = formalization.tag_erasure_makes_response_undefined()
        self.assertEqual(result.status, "pass")
        self.assertFalse(result.proof_authority)
        self.assertEqual(
            result.evidence["checked_tagged_object_ids"],
            ["X_plus", "X_flip", "X_scale", "X_token"],
        )

    def test_no_new_source_data_totalization_obstruction(self) -> None:
        result = formalization.no_new_source_data_totalization_obstruction()
        self.assertEqual(result.status, "pass")
        self.assertEqual(result.evidence["fixed_orientation_count"], 0)
        self.assertEqual(result.evidence["fixed_token_map_count"], 0)
        self.assertTrue(result.evidence["untagged_object_fixed_under_relabeling"])

    def test_report_is_support_only_and_blocks_authority_overread(self) -> None:
        report = formalization.run_formalization()
        output = report.to_dict()
        self.assertEqual(output["status"], "pass_support_only")
        self.assertTrue(output["support_only"])
        self.assertFalse(output["proof_authority"])
        self.assertEqual(output["source_artifact_hash"], formalization.SOURCE_ARTIFACT_HASH)
        self.assertTrue(output["forbidden_authority_flags"])
        self.assertFalse(any(output["forbidden_authority_flags"].values()))
        self.assertIn("proof_authority=false", output["boundary_statement"])

    def test_cli_json_output_is_deterministic(self) -> None:
        command = [sys.executable, str(SCRIPT_PATH), "--json"]
        first = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        second = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        self.assertEqual(first.stdout, second.stdout)
        parsed = json.loads(first.stdout)
        self.assertEqual(parsed["status"], "pass_support_only")

    def test_cli_json_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.json"
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--json-output",
                    str(report_path),
                    "--json",
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            parsed = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(parsed["checker_id"], formalization.CHECKER_ID)
        self.assertEqual(parsed["status"], "pass_support_only")

    def test_source_artifact_hash_matches_registry_value(self) -> None:
        self.assertEqual(
            formalization.source_artifact_sha256(REPO_ROOT),
            formalization.SOURCE_ARTIFACT_HASH,
        )


if __name__ == "__main__":
    unittest.main()
