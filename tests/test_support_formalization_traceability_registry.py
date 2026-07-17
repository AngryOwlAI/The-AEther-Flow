from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

from scripts.research_control import strict_yaml
from scripts.research_control.support_formalization import (
    validate_traceability_registry as validator,
)
from scripts.research_control.support_formalization.traceability_io import (
    TraceabilityInputs,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / "scripts"
    / "research_control"
    / "support_formalization"
    / "validate_traceability_registry.py"
)
REGISTRY_PATH = (
    REPO_ROOT
    / "research_control"
    / "design"
    / "support_formalization_traceability_registry_v1.yaml"
)
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "support_traceability_v1"
FIXTURE_REGISTRY_PATH = FIXTURE_ROOT / REGISTRY_PATH.relative_to(REPO_ROOT)


def validate_fixture_registry(registry: dict[str, Any]) -> dict[str, Any]:
    return validator.validate_registry(
        dependencies=TraceabilityInputs(
            repo_root=FIXTURE_ROOT,
            registry=registry,
        )
    )


class SupportFormalizationTraceabilityRegistryTests(unittest.TestCase):
    def test_registry_validates_current_support_formalizations(self) -> None:
        receipt = validator.validate_registry()
        self.assertEqual(receipt["status"], "PASS")
        self.assertFalse(receipt["proof_authority"])
        self.assertTrue(receipt["support_only"])
        self.assertEqual(receipt["checked_entry_count"], 3)
        self.assertEqual(
            {entry["checker_id"] for entry in receipt["entries"]},
            {
                "finite_toy_tag_removal_support_formalization",
                "finite_local_witness_schema_support_formalization",
                "fail_closed_certificate_evaluation_support_formalization",
            },
        )
        fixture_receipt = validator.validate_registry(repo_root=FIXTURE_ROOT)
        self.assertEqual(fixture_receipt["status"], "PASS")
        self.assertEqual(fixture_receipt["checked_entry_count"], 1)
        self.assertEqual(
            fixture_receipt["entries"][0]["entry_id"],
            "SFR-V12-P6-T02-FINITE-TOY-TAG-REMOVAL",
        )
        fixture_files = {
            path.relative_to(FIXTURE_ROOT).as_posix()
            for path in FIXTURE_ROOT.rglob("*")
            if path.is_file()
        }
        self.assertEqual(len(fixture_files), 6)
        self.assertNotIn("README.md", fixture_files)

    def test_cli_json_output_is_deterministic(self) -> None:
        command = [sys.executable, str(SCRIPT_PATH), "--json"]
        first = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        second = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        self.assertEqual(first.stdout, second.stdout)
        parsed = json.loads(first.stdout)
        self.assertEqual(parsed["status"], "PASS")

    def test_cli_json_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "traceability_registry_report.json"
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
        self.assertEqual(parsed["checked_entry_count"], 3)
        self.assertEqual(parsed["authority_boundary_status"], "proof_authority_false_preserved")

    def test_registry_fails_closed_when_proof_authority_is_enabled(self) -> None:
        registry = copy.deepcopy(strict_yaml.load(FIXTURE_REGISTRY_PATH))
        registry["entries"][0]["proof_authority"] = True

        with self.assertRaisesRegex(
            validator.TraceabilityRegistryError,
            (
                r"^SFR-V12-P6-T02-FINITE-TOY-TAG-REMOVAL "
                r"proof_authority is not false$"
            ),
        ):
            validate_fixture_registry(registry)

    def test_registry_rejects_generated_path_as_canonical_source_authority(self) -> None:
        registry = copy.deepcopy(strict_yaml.load(FIXTURE_REGISTRY_PATH))
        artifact = registry["entries"][0]["canonical_source_artifacts"][0]
        artifact["path"] = ".local/content_semantics/forbidden.txt"
        artifact["source_hash"] = "not_used_because_path_prefix_fails_first"

        with self.assertRaisesRegex(
            validator.TraceabilityRegistryError,
            (
                r"^SFR-V12-P6-T02-FINITE-TOY-TAG-REMOVAL uses generated or "
                r"local path as authority: \.local/content_semantics/forbidden\.txt$"
            ),
        ):
            validate_fixture_registry(registry)


if __name__ == "__main__":
    unittest.main()
