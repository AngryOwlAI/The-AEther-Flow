from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ResearchControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.strict_yaml = load_module("strict_yaml", "strict_yaml.py")
        cls.validator = load_module("validate_research_control", "validate_research_control.py")
        cls.resolver = load_module("resolve_latest_handoff", "resolve_latest_handoff.py")
        cls.continue_research = load_module("continue_research", "continue_research.py")
        cls.checkpoint = load_module("checkpoint_research_transaction", "checkpoint_research_transaction.py")

    def test_strict_yaml_parses_nested_maps_and_lists(self) -> None:
        parsed = self.strict_yaml.loads(
            'name: "demo"\n'
            "enabled: true\n"
            "items:\n"
            '  - "alpha"\n'
            "nested:\n"
            '  child: "value"\n'
        )
        self.assertEqual(parsed["name"], "demo")
        self.assertTrue(parsed["enabled"])
        self.assertEqual(parsed["items"], ["alpha"])
        self.assertEqual(parsed["nested"]["child"], "value")

    def test_strict_yaml_rejects_anchors(self) -> None:
        with self.assertRaises(self.strict_yaml.StrictYamlError):
            self.strict_yaml.loads('name: &bad "demo"\n')

    def test_static_research_control_validation_passes(self) -> None:
        report = self.validator.validate_all()
        self.assertEqual(report.errors, [])

    def test_role_registry_accepts_distinct_role_versions(self) -> None:
        report = self.validator.ValidationReport()
        rows_by_registry = {
            "AGENT_ROLE_REGISTRY.csv": [
                {
                    "role_id": "documentation-curator",
                    "version": "0.1.0",
                    "status": "superseded",
                    "may_execute_autonomously": "true",
                    "may_create_outputs": "true",
                    "may_modify_sources": "true",
                    "may_promote_claims": "false",
                    "requires_human_gate": "false",
                },
                {
                    "role_id": "documentation-curator",
                    "version": "0.2.0",
                    "status": "active",
                    "may_execute_autonomously": "true",
                    "may_create_outputs": "true",
                    "may_modify_sources": "true",
                    "may_promote_claims": "false",
                    "requires_human_gate": "false",
                },
            ]
        }
        self.validator.validate_registry_values(report, rows_by_registry)
        self.assertEqual(report.errors, [])

    def test_resolve_latest_handoff(self) -> None:
        program_state = self.strict_yaml.loads(
            (REPO_ROOT / "research_control" / "program_state.yaml").read_text(
                encoding="utf-8"
            )
        )
        latest = self.resolver.resolve_latest()
        self.assertEqual(latest["handoff_id"], program_state["latest_handoff_id"])
        self.assertEqual(latest["task_id"], program_state["active_task_id"])

    def test_write_path_diff_rejects_undeclared_path(self) -> None:
        report = self.validator.ValidationReport()
        jobs = {
            "AJ-TEST": {
                "job_id": "AJ-TEST",
                "status": "completed",
                "created_at": "2026-06-08T00:00:00Z",
                "allowed_write_paths": "research_control/**",
                "output_paths": "",
            }
        }
        with mock.patch.object(self.validator, "changed_paths", return_value=["wiki/changed.md"]):
            self.validator.validate_diff(report, jobs, "HEAD", False)
        self.assertTrue(any("not allowed" in error for error in report.errors))

    def test_write_path_diff_accepts_declared_path(self) -> None:
        report = self.validator.ValidationReport()
        jobs = {
            "AJ-TEST": {
                "job_id": "AJ-TEST",
                "status": "completed",
                "created_at": "2026-06-08T00:00:00Z",
                "allowed_write_paths": "research_control/tasks/RT-TEST/**",
                "output_paths": "",
            }
        }
        with mock.patch.object(
            self.validator,
            "changed_paths",
            return_value=["research_control/tasks/RT-TEST/example.yaml"],
        ):
            self.validator.validate_diff(report, jobs, "HEAD", False)
        self.assertEqual(report.errors, [])

    def test_write_path_diff_rejects_broad_wiki_allowlist(self) -> None:
        report = self.validator.ValidationReport()
        jobs = {
            "AJ-TEST": {
                "job_id": "AJ-TEST",
                "status": "completed",
                "created_at": "2026-06-08T00:00:00Z",
                "allowed_write_paths": "wiki/**",
                "output_paths": "",
            }
        }
        with mock.patch.object(
            self.validator,
            "changed_paths",
            return_value=["wiki/tex/example.md"],
        ):
            self.validator.validate_diff(report, jobs, "HEAD", False)
        self.assertTrue(any("overly broad allowlist" in error for error in report.errors))

    def test_markdown_authority_parser_is_deterministic(self) -> None:
        authorities = self.validator.markdown_authority_by_line(
            "Intro\n"
            "<!-- authority: explanatory -->\n"
            "Explanation\n"
            "<!-- authority: control -->\n"
            "Rule\n"
        )
        self.assertEqual(authorities[1], "unmarked")
        self.assertEqual(authorities[2], "explanatory")
        self.assertEqual(authorities[3], "explanatory")
        self.assertEqual(authorities[4], "control")
        self.assertEqual(authorities[5], "control")

    def validate_authority_fixture(
        self,
        *,
        role_id: str,
        path_text: str,
        text: str,
    ):
        report = self.validator.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            path = root / path_text
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            with mock.patch.object(self.validator, "REPO_ROOT", root):
                self.validator.validate_markdown_authority_boundaries(
                    report,
                    {"job_id": "AJ-TEST", "role_id": role_id},
                    [path_text],
                    "HEAD",
                    False,
                )
        return report

    def test_documentation_curator_rejects_control_marked_section(self) -> None:
        report = self.validate_authority_fixture(
            role_id="documentation-curator",
            path_text="README.md",
            text="<!-- authority: control -->\n# Rule\n",
        )
        self.assertTrue(any("documentation-curator cannot edit control-marked" in error for error in report.errors))

    def test_documentation_curator_rejects_skill_contract(self) -> None:
        report = self.validate_authority_fixture(
            role_id="documentation-curator",
            path_text=".codex/skills/continue-research/SKILL.md",
            text="# Skill\n",
        )
        self.assertTrue(any("documentation-curator cannot edit control markdown" in error for error in report.errors))

    def test_project_control_maintainer_accepts_skill_contract(self) -> None:
        report = self.validate_authority_fixture(
            role_id="project-control-maintainer",
            path_text=".codex/skills/continue-research/SKILL.md",
            text="# Skill\n",
        )
        self.assertEqual(report.errors, [])

    def test_project_control_maintainer_rejects_explanatory_section_without_overlay(self) -> None:
        report = self.validate_authority_fixture(
            role_id="project-control-maintainer",
            path_text="README.md",
            text="<!-- authority: explanatory -->\n# Overview\n",
        )
        self.assertTrue(any("project-control-maintainer cannot edit explanatory section" in error for error in report.errors))

    def test_mixed_markdown_rejects_unmarked_change(self) -> None:
        report = self.validate_authority_fixture(
            role_id="validator-engineer",
            path_text="README.md",
            text="# Unmarked\n",
        )
        self.assertTrue(any("outside an authority marker" in error for error in report.errors))

    def test_continue_research_reports_director_context_packet(self) -> None:
        program_state = self.strict_yaml.loads(
            (REPO_ROOT / "research_control" / "program_state.yaml").read_text(
                encoding="utf-8"
            )
        )
        status = self.continue_research.continuation_status()
        self.assertEqual(status["status"], "ready")
        self.assertIn(status["boundary"], {"director_decision_required", "existing_agent_job_ready", "human_gate_required", "blocked", "no_action"})
        self.assertEqual(status["active_task_id"], program_state["active_task_id"])
        self.assertEqual(status["latest_handoff_id"], program_state["latest_handoff_id"])
        self.assertTrue(status["checkpoint_required_after_execution"])
        self.assertEqual(status["execution_boundary"], "one bounded AgentJob per invocation")

    def test_checkpoint_global_sync_allowlist_is_narrow(self) -> None:
        self.assertTrue(
            self.checkpoint.allowed_by_any(
                "registries/WIKI_ARTIFACT_REGISTRY.csv",
                self.checkpoint.GLOBAL_SYNC_ALLOWLIST,
            )
        )
        self.assertFalse(
            self.checkpoint.allowed_by_any(
                "wiki/tex/generated-note.md",
                self.checkpoint.GLOBAL_SYNC_ALLOWLIST,
            )
        )

    def test_commit_message_uses_execution_role_ref(self) -> None:
        lines = self.checkpoint.commit_message(
            {
                "task_id": "RT-TEST",
                "decision_id": "DDR-TEST",
                "job_id": "AJ-TEST",
                "notes": "fallback summary",
            },
            "overlay-RT-TEST-refuter@0.1.0-clock-audit",
            {"handoff_id": "handoff-9999", "summary": "Completed one bounded audit."},
        )
        self.assertEqual(
            lines[0],
            "Research control: RT-TEST overlay-RT-TEST-refuter@0.1.0-clock-audit completion",
        )
        self.assertIn("Push: not performed", lines)

    def validate_execution_role_fixture(
        self,
        *,
        kind: str,
        added_constraints: list[str] | None = None,
        removed_permissions: list[str] | None = None,
        expanded_permissions: list[str] | None = None,
        requires_human_gate: str = "false",
        base_role_id: str = "refuter",
        base_role_version: str = "0.1.0",
        provisional_role_name: str = "",
        justification: str = "",
        non_reusable_until_registered: str = "false",
        expires_after: str = "AJ-TEST",
    ):
        added = added_constraints if added_constraints is not None else [""]
        removed = removed_permissions if removed_permissions is not None else [""]
        expanded = expanded_permissions if expanded_permissions is not None else [""]
        execution_ref = f"{kind}-fixture"
        record_path = f"research_control/tasks/RT-TEST/roles/{execution_ref}.yaml"
        row = {
            "execution_role_ref": execution_ref,
            "role_execution_kind": kind,
            "task_id": "RT-TEST",
            "agent_job_id": "AJ-TEST",
            "record_path": record_path,
            "base_role_id": base_role_id,
            "base_role_version": base_role_version,
            "provisional_role_name": provisional_role_name,
            "authority_delta_summary": "Synthetic role fixture.",
            "added_constraints": ";".join(added),
            "removed_permissions": ";".join(removed),
            "expanded_permissions": ";".join(expanded),
            "allowed_write_paths": "research_control/tasks/RT-TEST/**",
            "requires_human_gate": requires_human_gate,
            "expires_after": expires_after,
            "justification": justification,
            "non_reusable_until_registered": non_reusable_until_registered,
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            path = root / record_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "\n".join(
                    [
                        f'execution_role_ref: "{execution_ref}"',
                        f'role_execution_kind: "{kind}"',
                        'task_id: "RT-TEST"',
                        'agent_job_id: "AJ-TEST"',
                        f'base_role_id: "{base_role_id}"',
                        f'base_role_version: "{base_role_version}"',
                        f'provisional_role_name: "{provisional_role_name}"',
                        'authority_delta_summary: "Synthetic role fixture."',
                        "added_constraints:",
                        *[f'  - "{item}"' for item in added],
                        "removed_permissions:",
                        *[f'  - "{item}"' for item in removed],
                        "expanded_permissions:",
                        *[f'  - "{item}"' for item in expanded],
                        "allowed_write_paths:",
                        '  - "research_control/tasks/RT-TEST/**"',
                        f"requires_human_gate: {requires_human_gate}",
                        f'expires_after: "{expires_after}"',
                        f'justification: "{justification}"',
                        f"non_reusable_until_registered: {non_reusable_until_registered}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            report = self.validator.ValidationReport()
            with mock.patch.object(self.validator, "REPO_ROOT", root):
                self.validator.validate_execution_roles(
                    report,
                    [row],
                    {self.validator.role_key("refuter", "0.1.0"): {"version": "0.1.0"}},
                    {"AJ-TEST": {"task_id": "RT-TEST", "job_path": ""}},
                    {"RT-TEST": {"task_id": "RT-TEST"}},
                )
        return report

    def test_execution_role_accepts_exact_registered_role(self) -> None:
        report = self.validate_execution_role_fixture(kind="registered_role")
        self.assertEqual(report.errors, [])

    def test_execution_role_accepts_task_overlay_with_added_constraints(self) -> None:
        report = self.validate_execution_role_fixture(
            kind="task_overlay",
            added_constraints=["Audit only the bounded task artifact."],
        )
        self.assertEqual(report.errors, [])

    def test_execution_role_accepts_task_overlay_with_bounded_nonprotected_expansion(self) -> None:
        report = self.validate_execution_role_fixture(
            kind="task_overlay",
            expanded_permissions=["May add a task-local diagnostic table."],
        )
        self.assertEqual(report.errors, [])

    def test_execution_role_rejects_task_overlay_without_delta(self) -> None:
        report = self.validate_execution_role_fixture(kind="task_overlay")
        self.assertTrue(any("task_overlay must declare an authority delta" in error for error in report.errors))

    def test_execution_role_rejects_protected_expansion_without_human_gate(self) -> None:
        report = self.validate_execution_role_fixture(
            kind="task_overlay",
            expanded_permissions=["May issue a Gate Chair verdict."],
        )
        self.assertTrue(any("protected expanded_permissions require a human gate" in error for error in report.errors))

    def test_execution_role_accepts_brand_new_provisional_role(self) -> None:
        report = self.validate_execution_role_fixture(
            kind="one_job_provisional_role",
            base_role_id="",
            base_role_version="",
            provisional_role_name="Novel Audit Pilot",
            justification="No registered role fits this synthetic one-job audit.",
            non_reusable_until_registered="true",
        )
        self.assertEqual(report.errors, [])

    def test_execution_role_accepts_template_derived_provisional_role(self) -> None:
        report = self.validate_execution_role_fixture(
            kind="one_job_provisional_role",
            base_role_id="refuter",
            base_role_version="0.1.0",
            provisional_role_name="Refuter Ledger Pilot",
            justification="The task derives from Refuter but needs a distinct one-job identity.",
            non_reusable_until_registered="true",
        )
        self.assertEqual(report.errors, [])

    def test_execution_role_rejects_reusable_provisional_role(self) -> None:
        report = self.validate_execution_role_fixture(
            kind="one_job_provisional_role",
            base_role_id="",
            base_role_version="",
            provisional_role_name="Reusable Pilot",
            justification="Synthetic reusable provisional role.",
            non_reusable_until_registered="false",
        )
        self.assertTrue(any("provisional role must be non-reusable" in error for error in report.errors))

    def test_execution_role_rejects_provisional_expiry_mismatch(self) -> None:
        report = self.validate_execution_role_fixture(
            kind="one_job_provisional_role",
            base_role_id="",
            base_role_version="",
            provisional_role_name="Expiry Pilot",
            justification="Synthetic expiry mismatch.",
            non_reusable_until_registered="true",
            expires_after="AJ-OTHER",
        )
        self.assertTrue(any("provisional role must expire after its AgentJob" in error for error in report.errors))


if __name__ == "__main__":
    unittest.main()
