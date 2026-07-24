from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unicodedata
import unittest
from pathlib import Path

import yaml

from scripts.validation import portability

REPO_ROOT = Path(__file__).resolve().parents[1]
P10_MODULE_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260722-002/artifacts/artifact_identity.py"
)
P10_SPEC = importlib.util.spec_from_file_location(
    "p10_t07_artifact_identity_compatibility",
    P10_MODULE_PATH,
)
assert P10_SPEC and P10_SPEC.loader
p10_artifact_identity = importlib.util.module_from_spec(P10_SPEC)
P10_SPEC.loader.exec_module(p10_artifact_identity)


class ValidationPortabilityTests(unittest.TestCase):
    def test_portable_paths_pass(self) -> None:
        paths = (
            "scripts/validation/api.py",
            "research_control/tasks/RT-20260723-020/artifacts/quality-requirements.lock",
        )
        self.assertEqual(
            [portability.lint_relative_path(path) for path in paths],
            [(), ()],
        )
        self.assertEqual(portability.evaluate_paths(paths)["status"], "PASS")

    def test_p10_t07_negative_fixtures_preserve_exact_findings(self) -> None:
        fixtures = (
            "/tmp/a.json",
            r"artifacts\a.json",
            "artifacts/Con.md",
            "artifacts/name. ",
            "artifacts/../name.md",
            "artifacts/cafe\u0301.md",
            f"artifacts/{'x' * 97}.md",
            f"{'segment/' * 30}result.json",
            "artifacts/bad?.json",
        )
        self.assertNotEqual(fixtures[5], unicodedata.normalize("NFC", fixtures[5]))
        for path in fixtures:
            with self.subTest(path=path):
                actual = [
                    finding.to_dict()
                    for finding in portability.lint_relative_path(path)
                ]
                self.assertEqual(actual, p10_artifact_identity.lint_relative_path(path))

    def test_casefold_collisions_preserve_p10_t07_behavior(self) -> None:
        paths = ("artifacts/Report.md", "artifacts/report.md")
        actual = [
            collision.to_dict()
            for collision in portability.casefold_collisions(paths)
        ]
        self.assertEqual(actual, p10_artifact_identity.casefold_collisions(paths))
        self.assertEqual(portability.evaluate_paths(paths)["exit_code"], 1)

    def test_receipt_is_deterministic_and_prospective_only(self) -> None:
        paths = ("b/file.md", "a/file.md", "b/file.md")
        first = portability.evaluate_paths(paths)
        second = portability.evaluate_paths(reversed(paths))
        self.assertEqual(first, second)
        self.assertTrue(first["authority"]["prospective_only"])
        self.assertFalse(first["authority"]["historical_paths_changed"])
        self.assertFalse(first["authority"]["physics_claim_authority"])

    def test_cli_exit_codes_and_json(self) -> None:
        passing = subprocess.run(
            [
                sys.executable,
                "-m",
                "scripts.validation.portability",
                "--path",
                "scripts/validation/api.py",
                "--json",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(passing.returncode, 0, passing.stderr)
        self.assertEqual(json.loads(passing.stdout)["status"], "PASS")

        failing = subprocess.run(
            [
                sys.executable,
                "-m",
                "scripts.validation.portability",
                "--path",
                "artifacts/Con.md",
                "--json",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(failing.returncode, 1, failing.stderr)
        self.assertEqual(json.loads(failing.stdout)["status"], "FAIL")

    def test_ci_matrix_declares_supported_platform_cells(self) -> None:
        workflow_path = REPO_ROOT / ".github/workflows/project-control-validation.yml"
        workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        job = workflow["jobs"]["quality_portability_matrix"]
        matrix = job["strategy"]["matrix"]
        self.assertEqual(matrix["os"], ["ubuntu-latest", "macos-latest"])
        self.assertEqual(matrix["python-version"], ["3.12"])
        self.assertEqual(job["runs-on"], "${{ matrix.os }}")

    def test_makefile_declares_bounded_quality_target(self) -> None:
        makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("validate-quality:", makefile)
        self.assertIn("scripts/validation/api.py", makefile)
        self.assertIn("scripts.validation.portability", makefile)


if __name__ == "__main__":
    unittest.main()
