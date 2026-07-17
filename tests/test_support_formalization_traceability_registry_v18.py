from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

from scripts.research_control import strict_yaml
from scripts.research_control.support_formalization import (
    validate_traceability_registry_v18 as validator,
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
    / "validate_traceability_registry_v18.py"
)
REGISTRY_PATH = (
    REPO_ROOT
    / "research_control"
    / "design"
    / "support_formalization_traceability_registry_v18.yaml"
)
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "support_traceability_v18"
FIXTURE_REGISTRY_PATH = FIXTURE_ROOT / REGISTRY_PATH.relative_to(REPO_ROOT)
EXPECTED_PLAN_TASK_IDS = ["P7-T02", "P7-T03", "P7-T04", "P7-T05", "P7-T06"]
FIRST_ENTRY_ID = "SFR-V18-P7-T02-TYPED-EQSRC-ORBIT-CHECKER"


def validate_fixture_registry(registry: dict[str, Any]) -> dict[str, Any]:
    return validator.validate_registry(
        dependencies=TraceabilityInputs(repo_root=FIXTURE_ROOT, registry=registry)
    )


class SupportFormalizationTraceabilityRegistryV18Tests(unittest.TestCase):
    def test_registry_validates_all_v18_support_tools(self) -> None:
        receipt = validator.validate_registry()
        self.assertEqual(receipt["status"], "PASS")
        self.assertFalse(receipt["proof_authority"])
        self.assertTrue(receipt["support_only"])
        self.assertEqual(receipt["entry_count"], 5)
        self.assertEqual(
            [entry["plan_task_id"] for entry in receipt["entries"]],
            EXPECTED_PLAN_TASK_IDS,
        )

        fixture_receipt = validator.validate_registry(repo_root=FIXTURE_ROOT)
        self.assertEqual(fixture_receipt["status"], "PASS")
        self.assertEqual(fixture_receipt["entry_count"], 5)
        self.assertEqual(
            [entry["plan_task_id"] for entry in fixture_receipt["entries"]],
            EXPECTED_PLAN_TASK_IDS,
        )

    def test_cli_writes_json_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.json"
            markdown_path = Path(temp_dir) / "index.md"
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--json-output",
                    str(report_path),
                    "--markdown-output",
                    str(markdown_path),
                    "--json",
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            parsed = json.loads(report_path.read_text(encoding="utf-8"))
            markdown = markdown_path.read_text(encoding="utf-8")
        self.assertEqual(parsed["entry_count"], 5)
        self.assertIn("Proof authority | false", markdown)
        self.assertIn("detector_placeholder_collapse_checker", markdown)

    def test_registry_fails_closed_when_proof_authority_is_enabled(self) -> None:
        registry = copy.deepcopy(strict_yaml.load(FIXTURE_REGISTRY_PATH))
        registry["entries"][0]["authority_boundary"]["proof_authority"] = True

        with self.assertRaisesRegex(
            validator.V18TraceabilityError,
            rf"^{FIRST_ENTRY_ID} boundary proof_authority is not false$",
        ):
            validate_fixture_registry(registry)

    def test_registry_fails_closed_when_pnf_row_is_missing(self) -> None:
        registry = copy.deepcopy(strict_yaml.load(FIXTURE_REGISTRY_PATH))
        registry["entries"][0]["proof_normal_form_row_id"] = "PNF-MISSING"

        with self.assertRaisesRegex(
            validator.V18TraceabilityError,
            rf"^{FIRST_ENTRY_ID} missing proof-normal-form row: PNF-MISSING$",
        ):
            validate_fixture_registry(registry)

    def test_registry_fails_closed_when_report_hash_is_changed(self) -> None:
        registry = copy.deepcopy(strict_yaml.load(FIXTURE_REGISTRY_PATH))
        registry["entries"][0]["report_hash"] = "0" * 64

        with self.assertRaisesRegex(
            validator.V18TraceabilityError,
            rf"^{FIRST_ENTRY_ID} report_hash mismatch$",
        ):
            validate_fixture_registry(registry)

    def test_registry_fails_closed_when_source_hash_is_changed(self) -> None:
        registry = copy.deepcopy(strict_yaml.load(FIXTURE_REGISTRY_PATH))
        source_artifact = registry["entries"][0]["source_artifacts"][0]
        source_artifact["source_hash"] = "0" * 64
        source_path = re.escape(source_artifact["path"])

        with self.assertRaisesRegex(
            validator.V18TraceabilityError,
            (
                rf"^{FIRST_ENTRY_ID} source_artifacts hash mismatch for "
                rf"{source_path}: [0-9a-f]{{64}} != {'0' * 64}$"
            ),
        ):
            validate_fixture_registry(registry)


if __name__ == "__main__":
    unittest.main()
