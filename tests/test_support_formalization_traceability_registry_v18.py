from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.research_control import strict_yaml
from scripts.research_control.support_formalization import (
    validate_traceability_registry_v18 as validator,
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


class SupportFormalizationTraceabilityRegistryV18Tests(unittest.TestCase):
    def test_registry_validates_all_v18_support_tools(self) -> None:
        receipt = validator.validate_registry()
        self.assertEqual(receipt["status"], "PASS")
        self.assertFalse(receipt["proof_authority"])
        self.assertTrue(receipt["support_only"])
        self.assertEqual(receipt["entry_count"], 5)
        self.assertEqual(
            [entry["plan_task_id"] for entry in receipt["entries"]],
            ["P7-T02", "P7-T03", "P7-T04", "P7-T05", "P7-T06"],
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
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            shutil.copytree(REPO_ROOT, temp_root / "repo", ignore=shutil.ignore_patterns(".git"))
            copied_registry = (
                temp_root
                / "repo"
                / "research_control"
                / "design"
                / "support_formalization_traceability_registry_v18.yaml"
            )
            data = strict_yaml.load(copied_registry)
            data["entries"][0]["authority_boundary"]["proof_authority"] = True
            copied_registry.write_text(strict_yaml.dumps(data), encoding="utf-8")

            with self.assertRaises(validator.V18TraceabilityError):
                validator.validate_registry(repo_root=temp_root / "repo")

    def test_registry_fails_closed_when_pnf_row_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            shutil.copytree(REPO_ROOT, temp_root / "repo", ignore=shutil.ignore_patterns(".git"))
            copied_registry = (
                temp_root
                / "repo"
                / "research_control"
                / "design"
                / "support_formalization_traceability_registry_v18.yaml"
            )
            data = strict_yaml.load(copied_registry)
            data["entries"][0]["proof_normal_form_row_id"] = "PNF-MISSING"
            copied_registry.write_text(strict_yaml.dumps(data), encoding="utf-8")

            with self.assertRaises(validator.V18TraceabilityError):
                validator.validate_registry(repo_root=temp_root / "repo")


if __name__ == "__main__":
    unittest.main()
