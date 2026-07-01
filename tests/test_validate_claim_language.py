from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_claim_language", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ClaimLanguageLinterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.linter = load_module()
        cls.taxonomy = cls.linter.load_taxonomy(TAXONOMY_PATH)

    def scan_one(self, path: str, text: str):
        return self.linter.report_dict(
            self.linter.scan_text_map(
                {path: text},
                taxonomy=self.taxonomy,
                reviewed_contexts=[],
                active_handoffs={"research_control/handoffs/handoff-active.yaml"},
            ),
            scanned_paths=[path],
        )

    def test_public_overclaim_hard_fails(self) -> None:
        report = self.scan_one("README.md", "The project has GR derived from the substrate.\n")
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["hard_fail_count"], 1)
        self.assertEqual(report["findings"][0]["class_id"], "einstein_equation_overclaim")
        self.assertEqual(report["findings"][0]["severity"], "hard_fail_current_public")

    def test_historical_artifact_overclaim_is_warning_only(self) -> None:
        report = self.scan_one(
            "research_control/tasks/RT-TEST/artifacts/legacy_note.md",
            "Historical note says benchmark recovered.\n",
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["hard_fail_count"], 0)
        self.assertEqual(report["warning_count"], 1)
        self.assertEqual(report["findings"][0]["severity"], "warn_historical")

    def test_scoped_positive_wording_passes(self) -> None:
        report = self.scan_one(
            "research_control/current_frontier.md",
            "matter_coupling status: accepted only as scoped source-extension evidence/precondition.\n",
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["finding_count"], 0)

    def test_accepted_as_scoped_evidence_precondition_passes(self) -> None:
        report = self.scan_one(
            "research_control/current_frontier.md",
            "matter_coupling control_status: accepted_as_scoped_evidence_precondition.\n",
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["finding_count"], 0)

    def test_bare_accepted_near_high_risk_row_fails(self) -> None:
        report = self.scan_one(
            "research_control/current_frontier.md",
            "matter_coupling: accepted\n",
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["findings"][0]["class_id"], "bare_high_risk_accepted")

    def test_active_handoff_overclaim_hard_fails_as_control(self) -> None:
        report = self.scan_one(
            "research_control/handoffs/handoff-active.yaml",
            'summary: "GR derived."\n',
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["findings"][0]["severity"], "hard_fail_current_control")

    def test_explicit_denial_context_passes(self) -> None:
        report = self.scan_one(
            "research_control/current_frontier.md",
            "This row records no benchmark Gate Chair closure and no global theory rejection.\n",
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["finding_count"], 0)

    def test_no_target_certificate_overread_fails(self) -> None:
        report = self.scan_one(
            "research_control/current_frontier.md",
            "A no-target certificate supplies matter semantics.\n",
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["findings"][0]["class_id"], "no_target_certificate_as_positive_semantics")

    def test_rr_e_transport_law_adoption_overread_fails(self) -> None:
        report = self.scan_one(
            "research_control/current_frontier.md",
            "RR_ETransportCompletenessOrInvarianceLaw_v1 adopted.\n",
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["findings"][0]["class_id"], "rr_e_transport_source_law_overclaim")

    def test_validator_as_proof_overread_fails(self) -> None:
        report = self.scan_one(
            "research_control/current_frontier.md",
            "The validator proves the physics.\n",
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["findings"][0]["class_id"], "validator_as_proof")

    def test_reviewed_context_downgrades_route_context(self) -> None:
        contexts = [
            {
                "entry_id": "ALLOW-TEST",
                "path": "implementations_plans/test.md",
                "class_ids": ["*"],
                "surface_class_override": "intentional_bad_example_surfaces",
                "severity_override": "warn_intentional_example",
                "reviewed_by_task_id": "RT-TEST",
                "reviewed_by_role": "validator-engineer@0.2.0",
                "scope_rationale": "Synthetic route context.",
            }
        ]
        findings = self.linter.scan_text_map(
            {"implementations_plans/test.md": "The bad example says GR derived.\n"},
            taxonomy=self.taxonomy,
            reviewed_contexts=contexts,
            active_handoffs=set(),
        )
        report = self.linter.report_dict(findings, scanned_paths=["implementations_plans/test.md"])
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["warning_count"], 1)
        self.assertEqual(report["findings"][0]["context"], "ALLOW-TEST")

    def test_json_cli_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("GR derived.\n", encoding="utf-8")
            command = [
                sys.executable,
                SCRIPT_PATH.as_posix(),
                "--json",
                "--repo-root",
                root.as_posix(),
                "--taxonomy",
                TAXONOMY_PATH.as_posix(),
                "--reviewed-contexts",
                (REPO_ROOT / "research_control/design/claim_language_linter_reviewed_contexts.yaml").as_posix(),
                "--paths",
                "README.md",
            ]
            result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 1)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["status"], "FAIL")
        self.assertEqual(parsed["hard_fail_count"], 1)

    def test_changed_gate_selects_only_claim_language_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Project overview.\n", encoding="utf-8")
            (root / "scripts/project_control").mkdir(parents=True)
            (root / "scripts/project_control/README.md").write_text(
                "Tool documentation.\n",
                encoding="utf-8",
            )
            (root / "research_control/handoffs").mkdir(parents=True)
            (root / "research_control/program_state.yaml").write_text(
                'latest_handoff_id: "handoff-9999"\n',
                encoding="utf-8",
            )
            (root / "research_control/handoffs/handoff-9999.yaml").write_text(
                'handoff_id: "handoff-9999"\n',
                encoding="utf-8",
            )

            selected = self.linter.claim_language_gate_paths(
                [
                    "README.md",
                    "scripts/project_control/README.md",
                    "research_control/handoffs/handoff-9999.yaml",
                ],
                repo_root=root,
            )

        self.assertEqual(
            selected,
            ["README.md", "research_control/handoffs/handoff-9999.yaml"],
        )

    def test_changed_gate_public_overclaim_fails(self) -> None:
        fixture_text = (
            REPO_ROOT / "tests/fixtures/claim_language/public_overclaim.md"
        ).read_text(encoding="utf-8")
        report = self.scan_one("README.md", fixture_text)

        self.assertEqual(report["status"], "FAIL")
        self.assertGreaterEqual(report["hard_fail_count"], 1)


if __name__ == "__main__":
    unittest.main()
