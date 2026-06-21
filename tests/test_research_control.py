from __future__ import annotations

import importlib.util
import csv
import hashlib
import shutil
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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class ResearchControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.strict_yaml = load_module("strict_yaml", "strict_yaml.py")
        cls.validator = load_module("validate_research_control", "validate_research_control.py")
        cls.resolver = load_module("resolve_latest_handoff", "resolve_latest_handoff.py")
        cls.continue_research = load_module("continue_research", "continue_research.py")
        cls.checkpoint = load_module("checkpoint_research_transaction", "checkpoint_research_transaction.py")
        cls.metrics = load_module(
            "report_physics_progress_metrics",
            "report_physics_progress_metrics.py",
        )

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

    def test_strict_yaml_accepts_only_inline_empty_lists(self) -> None:
        parsed = self.strict_yaml.loads("unresolved_conflicts: []\n")
        self.assertEqual(parsed["unresolved_conflicts"], [])
        dumped = self.strict_yaml.dumps({"unresolved_conflicts": []})
        self.assertIn("unresolved_conflicts: []", dumped)
        with self.assertRaises(self.strict_yaml.StrictYamlError):
            self.strict_yaml.loads("unresolved_conflicts: [alpha]\n")

    def test_static_research_control_validation_passes(self) -> None:
        report = self.validator.validate_all()
        self.assertEqual(report.errors, [])

    def test_physics_progress_metrics_report_reads_tracked_completions(self) -> None:
        report = self.metrics.build_report(REPO_ROOT)
        metrics = report["metrics"]
        self.assertGreater(metrics["input_counts"]["completions_read"], 0)
        self.assertIn("physics_progress_metrics", metrics)
        self.assertFalse(report["authority_boundary"]["physics_claim_promotion_authorized"])

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

    def memory_preflight_fixture(
        self,
        *,
        include_inspection: bool = True,
        stale_hash: bool = False,
    ):
        root = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        source = root / ".codex/skills/continue-research/SKILL.md"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("# Continue Research\n", encoding="utf-8")
        source_hash = sha256_text("# Continue Research\n")
        registry = root / "registries/MARKDOWN_SOURCE_REGISTRY.csv"
        registry.parent.mkdir(parents=True, exist_ok=True)
        with registry.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["object_id", "path", "source_hash"])
            writer.writeheader()
            writer.writerow(
                {
                    "object_id": "MD-SKILL-CONTINUE-RESEARCH",
                    "path": ".codex/skills/continue-research/SKILL.md",
                    "source_hash": source_hash,
                }
            )
        receipt = {
            "status_command": ".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py status --json",
            "status_summary": {
                "vault_exists": True,
                "memory_index_exists": True,
                "source_object_count": 1,
            },
            "queries": [
                {
                    "command": ".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup MD-SKILL-CONTINUE-RESEARCH --json",
                    "query_type": "lookup",
                    "query_text": "MD-SKILL-CONTINUE-RESEARCH",
                    "returned_object_ids": ["MD-SKILL-CONTINUE-RESEARCH"],
                }
            ],
            "canonical_inspections": [],
            "authority_note": "Obsidian, semantic extracts, wiki notes, and .local are retrieval layers only and not authority.",
        }
        if include_inspection:
            receipt["canonical_inspections"].append(
                {
                    "object_id": "MD-SKILL-CONTINUE-RESEARCH",
                    "source_registry": "MARKDOWN_SOURCE_REGISTRY.csv",
                    "registry_path": "registries/MARKDOWN_SOURCE_REGISTRY.csv",
                    "canonical_path": ".codex/skills/continue-research/SKILL.md",
                    "source_hash": "stale" if stale_hash else source_hash,
                }
            )
        return root, receipt

    def validate_memory_preflight_fixture(self, receipt):
        report = self.validator.ValidationReport()
        job_row = {
            "job_id": "AJ-TEST",
            "created_at": "2026-06-18T15:33:00Z",
            "started_at": "",
            "completed_at": "",
        }
        self.validator.validate_memory_preflight(
            report,
            job_row,
            {"memory_preflight": receipt},
            "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
        )
        return report

    def test_memory_preflight_receipt_accepts_canonical_inspection(self) -> None:
        root, receipt = self.memory_preflight_fixture()
        with mock.patch.object(self.validator, "REPO_ROOT", root), mock.patch.object(
            self.validator, "REGISTRY_DIR", root / "registries"
        ):
            report = self.validate_memory_preflight_fixture(receipt)
        self.assertEqual(report.errors, [])

    def test_memory_preflight_required_after_activation(self) -> None:
        report = self.validator.ValidationReport()
        self.validator.validate_memory_preflight(
            report,
            {"job_id": "AJ-TEST", "created_at": "2026-06-18T15:33:00Z"},
            {},
            "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
        )
        self.assertTrue(any("missing memory_preflight" in error for error in report.errors))

    def test_memory_preflight_requires_canonical_inspection_for_hits(self) -> None:
        root, receipt = self.memory_preflight_fixture(include_inspection=False)
        with mock.patch.object(self.validator, "REPO_ROOT", root), mock.patch.object(
            self.validator, "REGISTRY_DIR", root / "registries"
        ):
            report = self.validate_memory_preflight_fixture(receipt)
        self.assertTrue(any("lack canonical inspection" in error for error in report.errors))

    def test_memory_preflight_explains_generated_retrieval_ids(self) -> None:
        root, receipt = self.memory_preflight_fixture(include_inspection=False)
        receipt["queries"][0]["returned_object_ids"] = ["WIKI-MD-SKILL-CONTINUE-RESEARCH"]
        with mock.patch.object(self.validator, "REPO_ROOT", root), mock.patch.object(
            self.validator, "REGISTRY_DIR", root / "registries"
        ):
            report = self.validate_memory_preflight_fixture(receipt)
        self.assertTrue(any("generated retrieval IDs" in error for error in report.errors))

    def test_memory_preflight_rejects_stale_source_hash(self) -> None:
        root, receipt = self.memory_preflight_fixture(stale_hash=True)
        with mock.patch.object(self.validator, "REPO_ROOT", root), mock.patch.object(
            self.validator, "REGISTRY_DIR", root / "registries"
        ):
            report = self.validate_memory_preflight_fixture(receipt)
        self.assertTrue(any("source_hash does not match registry row" in error for error in report.errors))

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
        self.assertEqual(status["bridge_or_fail_policy"]["policy_id"], "bridge_or_fail_loop_control_v1")
        self.assertEqual(
            status["theoretical_continuation_policy"]["decision_role_id"],
            "theoretical-continuation-selector",
        )
        self.assertEqual(
            status["parent_child_decomposition_policy"]["mode"],
            "parent_child_parallel_synthesis",
        )
        self.assertEqual(
            status["gr_derivation_roadmap_policy"]["policy_id"],
            "gr_derivation_roadmap_v1",
        )

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

    def test_checkpoint_stageable_paths_include_tracked_local_derivative(self) -> None:
        self.assertEqual(
            self.checkpoint.stageable_paths(
                [
                    ".local/content_semantics/markdown/md-readme.txt",
                    ".local/content_semantics/markdown/scratch.txt",
                    "research_control/README.md",
                ],
                tracked_local={".local/content_semantics/markdown/md-readme.txt"},
            ),
            [
                ".local/content_semantics/markdown/md-readme.txt",
                "research_control/README.md",
            ],
        )

    def test_checkpoint_add_stageable_paths_force_adds_local_derivative(self) -> None:
        commands: list[list[str]] = []

        def fake_run(command: list[str]):
            commands.append(command)
            return self.checkpoint.CommandResult(command, 0, "", "")

        with mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run):
            results = self.checkpoint.add_stageable_paths(
                [
                    ".local/content_semantics/markdown/md-readme.txt",
                    "FOLDER_MAP.md",
                    "research_control/README.md",
                ]
            )

        self.assertEqual([result.returncode for result in results], [0, 0])
        self.assertEqual(
            commands,
            [
                ["git", "add", "--", "FOLDER_MAP.md", "research_control/README.md"],
                [
                    "git",
                    "add",
                    "-f",
                    "--",
                    ".local/content_semantics/markdown/md-readme.txt",
                ],
            ],
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

    def parent_child_decomposition_fixture(
        self,
        *,
        allowed_write_paths: list[str] | None = None,
        expected_outputs: list[str] | None = None,
        registry_output_paths: str | None = None,
        child_phys_math_perspective: str = "physicist_mathematician",
        extra_child_fields: str = "",
    ):
        fused = "research_control/tasks/RT-TEST/artifacts/fused_result.tex"
        job_contract = self.strict_yaml.loads(
            "\n".join(
                [
                    "allowed_write_paths:",
                    *[
                        f'  - "{item}"'
                        for item in (
                            allowed_write_paths
                            if allowed_write_paths is not None
                            else ["research_control/tasks/RT-TEST/**"]
                        )
                    ],
                    "expected_outputs:",
                    *[
                        f'  - "{item}"'
                        for item in (expected_outputs if expected_outputs is not None else [fused])
                    ],
                    "role_decomposition:",
                    '  mode: "parent_child_parallel_synthesis"',
                    '  decomposition_version: "0.1.0"',
                    "  parent:",
                    '    execution_unit_id: "parent"',
                    '    perspective: "physicist_mathematician_philosopher"',
                    "    responsibilities:",
                    '      - "derive child role definitions from the selected execution role"',
                    "  children:",
                    '    - execution_unit_id: "child_phys_math"',
                    f'      perspective: "{child_phys_math_perspective}"',
                    '      output_path: "research_control/tasks/RT-TEST/artifacts/child_phys_math_result.tex"',
                    '      status: "planned"',
                    *extra_child_fields.splitlines(),
                    '    - execution_unit_id: "child_phys_phil"',
                    '      perspective: "physicist_philosopher"',
                    '      output_path: "research_control/tasks/RT-TEST/artifacts/child_phys_phil_result.tex"',
                    '      status: "planned"',
                    "  conflict_policy:",
                    '    review_path: "research_control/tasks/RT-TEST/artifacts/parent_conflict_review.yaml"',
                    "    max_resolution_rounds: 2",
                    "    require_parallel_child_revision: true",
                    '    unresolved_conflict_status: "blocked"',
                    "  fusion_policy:",
                    '    fusion_notes_path: "research_control/tasks/RT-TEST/artifacts/parent_fusion_notes.md"',
                    f'    fused_output_path: "{fused}"',
                    "    preserve_shared_consensus: true",
                    "    preserve_unique_contributions: true",
                    "    preserve_unresolved_limitations: true",
                    "    final_output_replaces_old_single_role_artifact: true",
                    "",
                ]
            )
        )
        row = {
            "job_id": "AJ-TEST",
            "job_path": "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
            "output_paths": registry_output_paths if registry_output_paths is not None else fused,
        }
        report = self.validator.ValidationReport()
        self.validator.validate_parent_child_decomposition(report, row, job_contract)
        return report

    def test_parent_child_decomposition_accepts_valid_contract(self) -> None:
        report = self.parent_child_decomposition_fixture()
        self.assertEqual(report.errors, [])

    def test_parent_child_decomposition_rejects_wrong_child_perspective(self) -> None:
        report = self.parent_child_decomposition_fixture(
            child_phys_math_perspective="physicist_philosopher",
        )
        self.assertTrue(any("child child_phys_math perspective" in error for error in report.errors))

    def test_parent_child_decomposition_rejects_output_outside_allowlist(self) -> None:
        report = self.parent_child_decomposition_fixture(
            allowed_write_paths=["research_control/tasks/RT-OTHER/**"],
        )
        self.assertTrue(any("outside AgentJob allowlist" in error for error in report.errors))

    def test_parent_child_decomposition_requires_fused_expected_output(self) -> None:
        report = self.parent_child_decomposition_fixture(expected_outputs=[])
        self.assertTrue(any("must appear in expected_outputs" in error for error in report.errors))

    def test_parent_child_decomposition_rejects_authority_expansion(self) -> None:
        report = self.parent_child_decomposition_fixture(
            extra_child_fields='      allowed_write_paths:\n        - "ontology/**"',
        )
        self.assertTrue(any("may not declare authority fields" in error for error in report.errors))

    def parent_child_completion_fixture(
        self,
        *,
        completion_outputs: list[str] | None = None,
        conflict_status: str = "no_conflict",
        unresolved_conflict: str = "",
    ):
        fused = "research_control/tasks/RT-TEST/artifacts/fused_result.tex"
        job_contract = self.strict_yaml.loads(
            "\n".join(
                [
                    "role_decomposition:",
                    '  mode: "parent_child_parallel_synthesis"',
                    '  decomposition_version: "0.1.0"',
                    "  parent:",
                    '    execution_unit_id: "parent"',
                    '    perspective: "physicist_mathematician_philosopher"',
                    "  children:",
                    '    - execution_unit_id: "child_phys_math"',
                    '      perspective: "physicist_mathematician"',
                    '      output_path: "research_control/tasks/RT-TEST/artifacts/child_phys_math_result.tex"',
                    '    - execution_unit_id: "child_phys_phil"',
                    '      perspective: "physicist_philosopher"',
                    '      output_path: "research_control/tasks/RT-TEST/artifacts/child_phys_phil_result.tex"',
                    "  conflict_policy:",
                    '    review_path: "research_control/tasks/RT-TEST/artifacts/parent_conflict_review.yaml"',
                    "    max_resolution_rounds: 2",
                    "  fusion_policy:",
                    f'    fused_output_path: "{fused}"',
                    "",
                ]
            )
        )
        unresolved_lines = unresolved_conflict.splitlines() if unresolved_conflict else []
        completion = self.strict_yaml.loads(
            "\n".join(
                [
                    'validation_status: "PASS"',
                    "output_paths:",
                    *[
                        f'  - "{item}"'
                        for item in (completion_outputs if completion_outputs is not None else [fused])
                    ],
                    "parent_child_synthesis:",
                    '  mode: "parent_child_parallel_synthesis"',
                    '  decomposition_version: "0.1.0"',
                    "  child_outputs:",
                    '    - execution_unit_id: "child_phys_math"',
                    '      perspective: "physicist_mathematician"',
                    '      output_path: "research_control/tasks/RT-TEST/artifacts/child_phys_math_result.tex"',
                    '      status: "completed"',
                    '    - execution_unit_id: "child_phys_phil"',
                    '      perspective: "physicist_philosopher"',
                    '      output_path: "research_control/tasks/RT-TEST/artifacts/child_phys_phil_result.tex"',
                    '      status: "completed"',
                    "  conflict_review:",
                    f'    status: "{conflict_status}"',
                    '    review_path: "research_control/tasks/RT-TEST/artifacts/parent_conflict_review.yaml"',
                    "    resolution_rounds: 0",
                    "    unresolved_conflicts:",
                    *(unresolved_lines if unresolved_lines else ['      - ""']),
                    "  fusion:",
                    f'    fused_output_path: "{fused}"',
                    '    shared_consensus_summary: "Shared result."',
                    '    unique_phys_math_contributions: "Formal pressure."',
                    '    unique_phys_phil_contributions: "Conceptual pressure."',
                    '    novelty_preservation_summary: "Novelty retained."',
                    '    claim_boundary_preservation_summary: "Boundary preserved."',
                    "",
                ]
            )
        )
        report = self.validator.ValidationReport()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            path = root / "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
            with mock.patch.object(self.validator, "REPO_ROOT", root):
                self.validator.validate_parent_child_completion(
                    report,
                    {"job_id": "AJ-TEST"},
                    job_contract,
                    completion,
                    path,
                )
        return report

    def test_parent_child_completion_accepts_valid_pass(self) -> None:
        report = self.parent_child_completion_fixture()
        self.assertEqual(report.errors, [])

    def test_parent_child_completion_requires_fused_output_in_completion(self) -> None:
        report = self.parent_child_completion_fixture(completion_outputs=[])
        self.assertTrue(any("fused output path" in error for error in report.errors))

    def test_parent_child_completion_rejects_pass_with_blocking_conflict(self) -> None:
        report = self.parent_child_completion_fixture(
            conflict_status="unresolved_blocking",
            unresolved_conflict=(
                '      - type: "mathematical"\n'
                '        severity: "blocking"\n'
                '        conflict_id: "C1"'
            ),
        )
        self.assertTrue(any("unresolved blocking conflicts" in error for error in report.errors))

    def validate_completion_fixture(
        self,
        *,
        role_id: str,
        job_objective: str = "",
        job_extra: str = "",
        completion_extra: str = "",
        timestamp: str = "2026-06-16T20:00:00Z",
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            job_path_text = "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml"
            completion_path_text = "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml"
            job_path = root / job_path_text
            completion_path = root / completion_path_text
            job_path.parent.mkdir(parents=True, exist_ok=True)
            completion_path.parent.mkdir(parents=True, exist_ok=True)
            job_path.write_text(
                "\n".join(
                    [
                        'job_id: "AJ-TEST"',
                        'task_id: "RT-TEST"',
                        'decision_id: "DDR-TEST"',
                        f'role_id: "{role_id}"',
                        'role_version: "0.2.0"',
                        'status: "completed"',
                        "requires_human_gate: false",
                        f'objective: "{job_objective}"',
                        "forbidden_source_classes:",
                        '  - "canonical_ontology_write"',
                        '  - "benchmark_promotion"',
                        '  - "candidate_reconstruction"',
                        '  - "gate_chair_verdict"',
                        '  - "completed_derivation_claim"',
                        '  - "global_theory_rejection"',
                        '  - "generated_derivative_authority"',
                        'resolves_signal_routing: false',
                        *job_extra.splitlines(),
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            completion_path.write_text(
                "\n".join(
                    [
                        'completion_id: "AJC-AJ-TEST"',
                        'job_id: "AJ-TEST"',
                        'task_id: "RT-TEST"',
                        f'completed_at: "{timestamp}"',
                        'status: "completed"',
                        "command_results:",
                        '  - "validator | exit_code=0 | status=pass"',
                        *completion_extra.splitlines(),
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            report = self.validator.ValidationReport()
            row = {
                "job_id": "AJ-TEST",
                "task_id": "RT-TEST",
                "decision_id": "DDR-TEST",
                "role_id": role_id,
                "role_version": "0.2.0",
                "job_path": job_path_text,
                "completion_path": completion_path_text,
                "status": "completed",
                "created_at": timestamp,
                "started_at": timestamp,
                "completed_at": timestamp,
            }
            with mock.patch.object(self.validator, "REPO_ROOT", root):
                self.validator.validate_completion(report, row, completion_path)
        return report

    def distance_matrix_yaml(self) -> str:
        burdens = [
            "Source ontology primitives",
            "Source equivalence EqSrc",
            "Finite variation robustness",
            "Concrete negative witnesses",
            "Observer normal/readout orbit",
            "Effective Lorentzian metric",
            "Universal matter coupling",
            "Einstein equations",
            "Benchmark promotion",
            "Gate Chair review",
            "Current line hard-fail",
        ]
        lines = ["distance_to_gr_status:"]
        for burden in burdens:
            lines.extend(
                [
                    f'  - burden: "{burden}"',
                    '    status: "not discharged"',
                ]
            )
        return "\n".join(lines)

    def roadmap_distance_matrix_yaml(self) -> str:
        burdens = [
            "Source ontology primitives",
            "Source equivalence EqSrc",
            "RetainH",
            "GenH",
            "ObsLoc_lc",
            "Resp_lc",
            "M_src",
            "g_eff",
            "matter coupling",
            "Einstein equations",
            "finite-variation robustness",
            "benchmark promotion",
            "Gate Chair status",
            "current route freeze or hard-fail status",
        ]
        lines = ["distance_to_gr_status:"]
        for burden in burdens:
            lines.extend(
                [
                    f'  - burden: "{burden}"',
                    '    status: "not discharged"',
                ]
            )
        return "\n".join(lines)

    def minimal_payload_yaml(self, payload_type: str = "dependency_map_update") -> str:
        return "\n".join(
            [
                "new_mathematical_payload:",
                f'  - payload_type: "{payload_type}"',
                '    summary: "Synthetic payload evidence for future-roadmap validation."',
            ]
        )

    def decisiveness_opt_in_job_yaml(self) -> str:
        return "\n".join(
            [
                'mathematical_decisiveness_contract_active_after: "2026-06-18T15:32:59Z"',
                'mathematical_decisiveness_schema: ".agents/schemas/PHYSICS_COMPLETION_DECISIVENESS_SCHEMA.md"',
            ]
        )

    def decisiveness_completion_yaml(self) -> str:
        return "\n".join(
            [
                "physics_progress_status:",
                '  status: "selector_only_no_distance_delta"',
                '  target_derivation_milestone: "source_manifold_m_src"',
                '  milestone_burden: "M_src"',
                '  explanation: "Selector-only fixture records no physics promotion."',
                "  physics_promotion_authorized: false",
                '  promotion_authority_path: ""',
                "distance_to_gr_delta:",
                "  changed: false",
                '  burden_id: "m_src"',
                '  milestone: "source_manifold_m_src"',
                '  old_status: "not discharged"',
                '  new_status: "not discharged"',
                "  ledger_row_updated: false",
                '  ledger_path: "registries/DISTANCE_TO_GR_LEDGER.csv"',
                "  downstream_unlocked:",
                '    - "none"',
                "  downstream_still_blocked:",
                '    - "g_eff"',
                '    - "matter_coupling"',
                '    - "einstein_equations"',
                '    - "benchmark_promotion"',
                '  explanation: "No Distance-to-GR delta in this selector-only fixture."',
                "mathematical_payload_manifest:",
                '  - payload_id: "PAYLOAD-001"',
                '    payload_type: "packet_selection"',
                '    object_name: "source-cover selector fixture"',
                '    claim_status: "draft/control"',
                '    source_path: "research_control/tasks/RT-TEST/artifacts/fixture.yaml"',
                '    burden_effect: "selects_next"',
                '    summary: "Names a packet without adoption."',
                "forbidden_conclusion_summary:",
                "  physics_promotion_authorized: false",
                "  forbidden_conclusions:",
                '    - "canonical ontology edit"',
                '    - "M_src adoption"',
                '    - "g_eff claim"',
                '    - "matter coupling claim"',
                '    - "Einstein-equation claim"',
                '    - "benchmark promotion"',
                '    - "Gate Chair verdict"',
                '    - "completed derivation"',
                '    - "global theory rejection"',
                '  summary: "Validator PASS and role authority are not physics evidence."',
            ]
        )

    def decisiveness_candidate_constructor_yaml(self) -> str:
        return "\n".join(
            [
                "physics_progress_status:",
                '  status: "candidate_constructed_pending_audit"',
                '  target_derivation_milestone: "source_manifold_m_src"',
                '  milestone_burden: "M_src"',
                '  explanation: "Candidate Constructor fixture creates a source-side candidate pending audit."',
                "  physics_promotion_authorized: false",
                '  promotion_authority_path: ""',
                "distance_to_gr_delta:",
                "  changed: false",
                '  burden_id: "m_src"',
                '  milestone: "source_manifold_m_src"',
                '  old_status: "not discharged"',
                '  new_status: "candidate constructed pending audit"',
                "  ledger_row_updated: false",
                '  ledger_path: "registries/DISTANCE_TO_GR_LEDGER.csv"',
                "  downstream_unlocked:",
                '    - "none"',
                "  downstream_still_blocked:",
                '    - "g_eff"',
                '    - "matter_coupling"',
                '    - "einstein_equations"',
                '    - "benchmark_promotion"',
                '  explanation: "The candidate still requires audit and stress before any GR promotion."',
                "mathematical_payload_manifest:",
                '  - payload_id: "PAYLOAD-001"',
                '    payload_type: "construction"',
                '    object_name: "source-side selector candidate"',
                '    claim_status: "draft/control"',
                '    source_path: "research_control/tasks/RT-TEST/artifacts/candidate.yaml"',
                '    burden_effect: "narrows"',
                '    summary: "Constructs a draft/control candidate without adoption."',
                "candidate_constructor_result:",
                '  result_type: "constructed_candidate"',
                '  constructed_candidate_path: "research_control/tasks/RT-TEST/artifacts/candidate.yaml"',
                '  minimal_countermodel_path: ""',
                '  obstruction_id: ""',
                "  formal_objects:",
                '    - "selector preorder S_src"',
                "  maps:",
                '    - "source profiles to candidate selector branches"',
                "  proof_obligations:",
                '    - "hidden target import audit"',
                "  failed_components:",
                '    - ""',
                '  next_required_role: "smuggling_auditor"',
                "  no_fog_check: true",
                '  no_fog_explanation: "A draft/control selector candidate was constructed with named formal objects maps and proof obligations; downstream GR objects remain blocked."',
                "  claim_boundary_preserved: true",
                '  claim_boundary_citation: ""',
                "bridge_attempt_status:",
                '  candidate_map: "source-side selector candidate only"',
                '  missing_primitive: ""',
                '  preserves_blocks: "No g_eff matter-coupling Einstein-equation or benchmark promotion is authorized."',
                "forbidden_conclusion_summary:",
                "  physics_promotion_authorized: false",
                "  forbidden_conclusions:",
                '    - "canonical ontology edit"',
                '    - "M_src adoption"',
                '    - "g_eff claim"',
                '    - "matter coupling claim"',
                '    - "Einstein-equation claim"',
                '    - "benchmark promotion"',
                '    - "Gate Chair verdict"',
                '    - "completed derivation"',
                '    - "global theory rejection"',
                '  summary: "Candidate construction is draft/control and does not authorize GR promotion."',
            ]
        )

    def decisiveness_candidate_constructor_precise_obstruction_yaml(self) -> str:
        return "\n".join(
            [
                "candidate_constructor_result:",
                '  result_type: "precise_obstruction"',
                '  constructed_candidate_path: ""',
                '  minimal_countermodel_path: ""',
                '  obstruction_id: "OBST-TEST-001"',
                "  formal_objects:",
                '    - ""',
                "  maps:",
                '    - ""',
                "  proof_obligations:",
                '    - ""',
                "  failed_components:",
                '    - "source-side selector preorder"',
                '  next_required_role: "theoretical-continuation-selector"',
                "  no_fog_check: true",
                '  no_fog_explanation: "The source-side selector preorder fails by a named obstruction, and the route consequence is theoretical-continuation-selector."',
                "  claim_boundary_preserved: true",
                '  claim_boundary_citation: "CB-TEST"',
                "bridge_attempt_status:",
                '  candidate_map: ""',
                '  missing_primitive: "source-side selector preorder"',
                '  preserves_blocks: "No g_eff matter-coupling Einstein-equation or benchmark promotion is authorized."',
            ]
        )

    def decisiveness_obstruction_yaml(self) -> str:
        return "\n".join(
            [
                "physics_progress_status:",
                '  status: "precise_obstruction_found"',
                '  target_derivation_milestone: "source_manifold_m_src"',
                '  milestone_burden: "M_src"',
                '  explanation: "Fixture records a precise current-ontology obstruction."',
                "  physics_promotion_authorized: false",
                '  promotion_authority_path: ""',
                "distance_to_gr_delta:",
                "  changed: false",
                '  burden_id: "m_src"',
                '  milestone: "source_manifold_m_src"',
                '  old_status: "not discharged"',
                '  new_status: "precise obstruction found"',
                "  ledger_row_updated: false",
                '  ledger_path: "registries/DISTANCE_TO_GR_LEDGER.csv"',
                "  downstream_unlocked:",
                '    - "none"',
                "  downstream_still_blocked:",
                '    - "g_eff"',
                '    - "matter_coupling"',
                '    - "einstein_equations"',
                '    - "benchmark_promotion"',
                '  explanation: "The obstruction sharpens the route but does not update the ledger."',
                "mathematical_payload_manifest:",
                '  - payload_id: "PAYLOAD-001"',
                '    payload_type: "obstruction"',
                '    object_name: "current-ontology selector obstruction"',
                '    claim_status: "draft/control"',
                '    source_path: "research_control/tasks/RT-TEST/artifacts/obstruction.yaml"',
                '    burden_effect: "obstructs"',
                '    summary: "Names the failed object and route consequence."',
                "obstruction_record:",
                "  present: true",
                '  obstruction_id: "OBST-TEST-001"',
                '  scope: "current_ontology_only"',
                '  failed_object: "source-side selector preorder"',
                '  exact_failure: "The selector is not determined by the current ontology assumptions."',
                '  minimal_counterexample_path: ""',
                '  current_ontology_implication: "does_not_derive"',
                '  source_extension_implication: "repair_allowed"',
                '  consequence: "repair_candidate_allowed"',
                '  forbidden_overread: "This does not prove global theory rejection or future repair impossibility."',
                "freeze_criteria_status:",
                "  repeated_burden: true",
                "  freeze_evaluation_required: true",
                '  active_freeze_label: "M-SRC-SELECTOR-CURRENT-ONTOLOGY-OBSTRUCTION"',
                "  prior_attempts_considered:",
                '    - "RT-TEST-PRIOR"',
                "  freeze_if:",
                '    - "same failed object recurs without new payload"',
                "  do_not_freeze_if:",
                '    - "next packet constructs a source-side repair candidate"',
                '  freeze_decision: "not_frozen"',
                '  decision_reason: "The obstruction routes to a concrete repair-candidate packet."',
                '  next_allowed_route: "candidate_constructor"',
                "route_cycle_control:",
                '  cycle_family: "m_src_atlas_glue"',
                '  current_cycle_step: "obstruction_review"',
                "  prior_related_tasks:",
                '    - "RT-TEST-PRIOR"',
                '  cycle_risk: "medium"',
                '  orbit_avoidance_reason: "The next packet must construct a repair candidate or return a sharper obstruction."',
                '  next_role_consequence: "candidate_constructor"',
                "forbidden_conclusion_summary:",
                "  physics_promotion_authorized: false",
                "  forbidden_conclusions:",
                '    - "canonical ontology edit"',
                '    - "M_src adoption"',
                '    - "g_eff claim"',
                '    - "matter coupling claim"',
                '    - "Einstein-equation claim"',
                '    - "benchmark promotion"',
                '    - "Gate Chair verdict"',
                '    - "completed derivation"',
                '    - "global theory rejection"',
                '  summary: "A precise obstruction preserves downstream blocks and does not authorize GR promotion."',
            ]
        )

    def ontology_law_selector_yaml(
        self,
        *,
        decision_basis: str = "The active milestone lacks a derivation-critical source-side selector law.",
        preserves_claim_blocks: str = (
            "No canonical ontology edit benchmark promotion Gate Chair review "
            "or completed derivation is authorized."
        ),
    ) -> str:
        return "\n".join(
            [
                "theoretical_decision_output:",
                '  selected_next_packet_type: "ontology_law_research_packet"',
                f'  decision_basis: "{decision_basis}"',
                '  theoretical_method: "Route one bounded same-milestone ontology-law research packet."',
                f'  preserves_claim_blocks: "{preserves_claim_blocks}"',
                "  requires_human_gate: false",
                '  human_gate_reason: ""',
            ]
        )

    def ontology_law_receipt_yaml(
        self,
        *,
        trigger_classification: str = "derivation_critical_missing_source_law",
        target_derivation_milestone: str = "source_manifold_m_src",
        milestone_burden: str = "M_src",
        missing_source_law: str = "source-side atlas-glue selector law",
        underdetermination_statement: str = "current ontology does not derive the source-side atlas-glue selector law.",
        source_side_definition: str = "Define a source-side selector preorder from source-local discriminator profiles only.",
        status_label: str = "proposal-only",
        current_adoption: str = "blocked",
        continuation: str = "open",
        status_pair: str = "blocked_adoption_open_continuation",
        gate_required: str = "true",
        include_exact_gr_obligations: bool = True,
        include_no_target_import_scope: bool = True,
        include_human_gate_request: bool = True,
    ) -> str:
        lines = [
            "ontology_law_research_packet:",
            '  route: "ontology-law-research-packet"',
            f'  trigger_classification: "{trigger_classification}"',
            f'  target_derivation_milestone: "{target_derivation_milestone}"',
            f'  milestone_burden: "{milestone_burden}"',
            f'  missing_source_law: "{missing_source_law}"',
            f'  underdetermination_statement: "{underdetermination_statement}"',
            '  no_go_theorem_status: "not_proved"',
            "  adoption_status:",
            f'    current_adoption: "{current_adoption}"',
            f'    continuation: "{continuation}"',
            f'    status_pair: "{status_pair}"',
            '  packet_payload_mode: "candidate_law_payload"',
            "  candidate_law_payload:",
            f'    status_label: "{status_label}"',
            f'    source_side_definition: "{source_side_definition}"',
            "    formal_objects:",
            '      - "source-local discriminator profile"',
            "    domains:",
            '      - "same-milestone source objects before target atlas selection"',
            "    maps:",
            '      - "selector preorder map on source-local profiles"',
            "    proof_obligations:",
            '      - "prove source-only definition and finite-variation robustness before adoption"',
        ]
        if include_exact_gr_obligations:
            lines.extend(
                [
                    "  exact_gr_recovery_obligations:",
                    "    checklist:",
                    '      - "preserve exact-GR benchmark recovery as a downstream obligation"',
                    "    distance_to_gr_links:",
                    '      - "M_src"',
                ]
            )
        if include_no_target_import_scope:
            lines.extend(
                [
                    "  no_target_import_audit_scope:",
                    "    forbidden_source_classes:",
                    '      - "target_atlas"',
                    '      - "target_metric"',
                    '      - "benchmark_success"',
                    '      - "generated_derivative"',
                    '      - "registry_metadata_authority"',
                    '      - "role_authority"',
                    '      - "validation_authority"',
                ]
            )
        if include_human_gate_request:
            lines.extend(
                [
                    "  human_gate_request:",
                    f"    required_before_adoption: {gate_required}",
                    '    requested_decision: "Review only after candidate law audit and refutation; no adoption in this packet."',
                    '    exact_requested_ontology_edit: ""',
                ]
            )
        return "\n".join(lines)

    def freeze_status_yaml(self) -> str:
        return "\n".join(
            [
                "freeze_criteria_status:",
                '  candidate_freeze_label: "NDCL-RESP-LC-SELECTOR-UNDERDETERMINATION"',
                '  freeze_decision: "not_frozen"',
                "  criteria_evaluated:",
                '    - "constructive primitive packet"',
                '    - "concrete witness attempt"',
                '    - "smuggling audit"',
                '    - "Refuter stress test"',
                '  rationale: "Synthetic fixture records that criteria were considered without freezing."',
            ]
        )

    def test_future_physics_completion_requires_distance_matrix(self) -> None:
        report = self.validate_completion_fixture(role_id="smuggling-auditor")
        self.assertTrue(any("distance_to_gr_status" in error for error in report.errors))

    def test_distance_to_gr_ledger_is_static_validated(self) -> None:
        report = self.validator.ValidationReport()
        self.validator.validate_distance_to_gr_ledger(report)
        self.assertEqual(report.errors, [])

    def test_future_refuter_stress_rejects_generic_ontology_loop_route(self) -> None:
        completion_extra = "\n".join(
            [
                self.distance_matrix_yaml(),
                "loop_risk_decision:",
                '  category: "repeated_unmet_burdens_no_new_payload"',
                '  next_route: "candidate_constructor_bridge_attempt"',
                '  rationale: "The same source-equivalence burdens recurred without new payload."',
                "  repeated_burdens:",
                '    - "nontrivial quotient failure"',
                'next_recommendation: "Route to Ontology Formalizer for another generic repair obligation packet."',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="refuter",
            job_objective="Run a Refuter stress test.",
            completion_extra=completion_extra,
        )
        self.assertTrue(any("generic Ontology Formalizer" in error for error in report.errors))

    def test_future_refuter_rejects_generic_controlled_pause_after_policy_activation(self) -> None:
        completion_extra = "\n".join(
            [
                self.distance_matrix_yaml(),
                "loop_risk_decision:",
                '  category: "scoped_obstruction"',
                '  next_route: "controlled_pause"',
                '  rationale: "The scoped obstruction recurred without new mathematical payload."',
                '  obstruction_summary: "No source-side selector primitive is present."',
                'next_recommendation: "Enter controlled pause."',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="refuter",
            job_objective="Run a Refuter stress test.",
            completion_extra=completion_extra,
            timestamp="2026-06-17T04:29:31Z",
        )
        self.assertTrue(any("generic controlled_pause" in error for error in report.errors))

    def test_future_refuter_accepts_theoretical_decision_route_with_payload_marker(self) -> None:
        completion_extra = "\n".join(
            [
                self.distance_matrix_yaml(),
                "loop_risk_decision:",
                '  category: "scoped_obstruction"',
                '  next_route: "theoretical_decision_role_selection"',
                '  rationale: "Route to theoretical-continuation-selector for a source-side selector primitive packet."',
                '  obstruction_summary: "Resp_lc sign and scale are underdetermined."',
                'next_recommendation: "Create a theoretical-continuation-selector task for a source-side selector primitive with new mathematical payload."',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="refuter",
            job_objective="Run a Refuter stress test.",
            completion_extra=completion_extra,
            timestamp="2026-06-17T04:29:31Z",
        )
        self.assertEqual(report.errors, [])

    def test_roadmap_future_physics_completion_requires_updated_distance_matrix(self) -> None:
        completion_extra = "\n".join(
            [
                self.distance_matrix_yaml(),
                self.minimal_payload_yaml(),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("distance_to_gr_status missing burdens" in error for error in report.errors))

    def test_roadmap_future_physics_completion_requires_new_payload(self) -> None:
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            completion_extra=self.roadmap_distance_matrix_yaml(),
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("missing new_mathematical_payload" in error for error in report.errors))

    def test_mathematical_decisiveness_opt_in_missing_fields_fails(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertTrue(
            any("mathematical decisiveness: missing physics_progress_status" in error for error in report.errors)
        )
        self.assertTrue(
            any("mathematical decisiveness: missing distance_to_gr_delta" in error for error in report.errors)
        )

    def test_mathematical_decisiveness_opt_in_valid_selector_completion_passes(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
                self.decisiveness_completion_yaml(),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertEqual(report.errors, [])
        self.assertFalse(
            any("mathematical decisiveness:" in error for error in report.errors)
        )

    def test_mathematical_decisiveness_valid_candidate_constructor_passes(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
                self.decisiveness_candidate_constructor_yaml(),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="candidate-constructor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertEqual(report.errors, [])

    def test_mathematical_decisiveness_valid_candidate_constructor_precise_obstruction_passes(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("obstruction"),
                self.decisiveness_obstruction_yaml(),
                self.decisiveness_candidate_constructor_precise_obstruction_yaml(),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="candidate-constructor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertEqual(report.errors, [])

    def test_mathematical_decisiveness_valid_obstruction_with_freeze_review_passes(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("obstruction"),
                self.decisiveness_obstruction_yaml(),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertEqual(report.errors, [])

    def test_mathematical_decisiveness_rejects_vague_candidate_constructor_output(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
                self.decisiveness_candidate_constructor_yaml().replace(
                    '  no_fog_explanation: "A draft/control selector candidate was constructed with named formal objects maps and proof obligations; downstream GR objects remain blocked."',
                    '  no_fog_explanation: "more work required"',
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="candidate-constructor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertTrue(
            any("candidate_constructor_result.no_fog_explanation contains fog-only phrase" in error for error in report.errors)
        )

    def test_mathematical_decisiveness_rejects_candidate_constructor_missing_formal_objects(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
                self.decisiveness_candidate_constructor_yaml().replace(
                    '    - "selector preorder S_src"',
                    '    - ""',
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="candidate-constructor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertTrue(
            any("candidate_constructor_result.formal_objects" in error for error in report.errors)
        )

    def test_mathematical_decisiveness_rejects_obstruction_missing_consequence(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("obstruction"),
                self.decisiveness_obstruction_yaml().replace(
                    '  consequence: "repair_candidate_allowed"',
                    '  consequence: ""',
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertTrue(
            any("obstruction_record.consequence is required" in error for error in report.errors)
        )

    def test_mathematical_decisiveness_accepts_downstream_obstruction_vocabulary(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("obstruction"),
                self.decisiveness_obstruction_yaml()
                .replace('  scope: "current_ontology_only"', '  scope: "matter_coupling"')
                .replace(
                    '  consequence: "repair_candidate_allowed"',
                    '  consequence: "target_import_detected"',
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertEqual(report.errors, [])

    def test_mathematical_decisiveness_rejects_freeze_missing_next_route(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("obstruction"),
                self.decisiveness_obstruction_yaml().replace(
                    '  next_allowed_route: "candidate_constructor"',
                    '  next_allowed_route: ""',
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertTrue(
            any("freeze_criteria_status.next_allowed_route is required" in error for error in report.errors)
        )

    def test_mathematical_decisiveness_rejects_route_cycle_missing_orbit_reason(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("obstruction"),
                self.decisiveness_obstruction_yaml().replace(
                    '  orbit_avoidance_reason: "The next packet must construct a repair candidate or return a sharper obstruction."',
                    '  orbit_avoidance_reason: ""',
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertTrue(
            any("route_cycle_control.orbit_avoidance_reason is required" in error for error in report.errors)
        )

    def test_mathematical_decisiveness_rejects_promotion_without_gate(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
                self.decisiveness_completion_yaml().replace(
                    "  physics_promotion_authorized: false",
                    "  physics_promotion_authorized: true",
                    1,
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertTrue(
            any("physics_promotion_authorized requires promotion_authority_path" in error for error in report.errors)
        )

    def test_mathematical_decisiveness_non_physics_completion_unaffected(self) -> None:
        report = self.validate_completion_fixture(
            role_id="project-control-maintainer",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra='validation_status: "PASS"',
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertEqual(report.errors, [])

    def test_roadmap_refuter_scoped_obstruction_requires_freeze_status(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("obstruction"),
                "loop_risk_decision:",
                '  category: "scoped_obstruction"',
                '  next_route: "theoretical_decision_role_selection"',
                '  rationale: "Route to theoretical-continuation-selector for a source-side selector primitive packet."',
                '  obstruction_summary: "Resp_lc sign and scale are underdetermined."',
                'next_recommendation: "Create a theoretical-continuation-selector task for a source-side selector primitive with new mathematical payload."',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="refuter",
            job_objective="Run a Refuter stress test.",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("freeze_criteria_status" in error for error in report.errors))

    def test_roadmap_refuter_accepts_freeze_status(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("obstruction"),
                self.freeze_status_yaml(),
                "loop_risk_decision:",
                '  category: "scoped_obstruction"',
                '  next_route: "theoretical_decision_role_selection"',
                '  rationale: "Route to theoretical-continuation-selector for a source-side selector primitive packet."',
                '  obstruction_summary: "Resp_lc sign and scale are underdetermined."',
                'next_recommendation: "Create a theoretical-continuation-selector task for a source-side selector primitive with new mathematical payload."',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="refuter",
            job_objective="Run a Refuter stress test.",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertEqual(report.errors, [])

    def test_future_ontology_formalizer_requires_new_payload(self) -> None:
        report = self.validate_completion_fixture(
            role_id="ontology-formalizer",
            completion_extra=self.distance_matrix_yaml(),
        )
        self.assertTrue(any("new_mathematical_payload" in error for error in report.errors))

    def test_future_candidate_bridge_attempt_requires_status(self) -> None:
        report = self.validate_completion_fixture(
            role_id="candidate-constructor",
            job_objective="Construct an observer-readout bridge candidate.",
            completion_extra=self.distance_matrix_yaml(),
        )
        self.assertTrue(any("bridge_attempt_status" in error for error in report.errors))

    def test_theoretical_continuation_selector_requires_decision_output(self) -> None:
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=self.distance_matrix_yaml(),
            timestamp="2026-06-17T04:29:31Z",
        )
        self.assertTrue(any("theoretical_decision_output" in error for error in report.errors))

    def test_theoretical_continuation_selector_accepts_theoretical_packet_decision(self) -> None:
        completion_extra = "\n".join(
            [
                self.distance_matrix_yaml(),
                "theoretical_decision_output:",
                '  selected_next_packet_type: "source_side_selector_primitive"',
                '  decision_basis: "The obstruction can be tested by constructing a source-only selector primitive."',
                '  theoretical_method: "Bounded formal construction from tracked source-side assumptions."',
                '  preserves_claim_blocks: "No canonical ontology edit benchmark promotion Gate Chair review or completed derivation is authorized."',
                "  requires_human_gate: false",
                '  human_gate_reason: ""',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T04:29:31Z",
        )
        self.assertEqual(report.errors, [])

    def test_roadmap_selector_rejects_no_go_without_novelty_and_consequence(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                "theoretical_decision_output:",
                '  selected_next_packet_type: "distinct_scoped_no_go_question"',
                '  decision_basis: "Synthetic scoped no-go selection."',
                '  theoretical_method: "Bounded formal construction from tracked assumptions."',
                '  preserves_claim_blocks: "No canonical ontology edit benchmark promotion Gate Chair review or completed derivation is authorized."',
                "  requires_human_gate: false",
                '  human_gate_reason: ""',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("decision_consequence" in error for error in report.errors))
        self.assertTrue(any("new_payload_novelty" in error for error in report.errors))

    def test_roadmap_selector_accepts_source_extension_category(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("source_extension_classification"),
                "theoretical_decision_output:",
                '  selected_next_packet_type: "source_extension_candidate"',
                '  decision_basis: "Synthetic source extension category selection."',
                '  theoretical_method: "Classify whether the extension is conservative or a new primitive."',
                '  preserves_claim_blocks: "No canonical ontology edit benchmark promotion Gate Chair review or completed derivation is authorized."',
                "  requires_human_gate: false",
                '  human_gate_reason: ""',
                '  source_extension_category: "source_extension_candidate"',
                '  source_extension_import_classification: "conservative definitional extension candidate, not adopted ontology"',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertEqual(report.errors, [])

    def test_roadmap_selector_accepts_finite_toy_model_target(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("finite_toy_model_target"),
                "theoretical_decision_output:",
                '  selected_next_packet_type: "finite_toy_metric_response_model"',
                '  decision_basis: "Synthetic finite toy target selection."',
                '  theoretical_method: "Define a bounded source set and response analogue before full GR."',
                '  preserves_claim_blocks: "No canonical ontology edit benchmark promotion Gate Chair review or completed derivation is authorized."',
                "  requires_human_gate: false",
                '  human_gate_reason: ""',
                "  finite_toy_model_target:",
                '    source_set: "finite U with source-local readout syntax"',
                '    response_relation: "source-side response relation candidate"',
                '    metric_response_analogue: "toy g_eff-like distance form"',
                '    invariance_checks: "finite relabeling and perturbation checks"',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertEqual(report.errors, [])

    def test_ontology_law_selector_requires_receipt(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                self.ontology_law_selector_yaml(),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("missing ontology_law_research_packet" in error for error in report.errors))

    def test_ontology_law_receipt_accepts_valid_candidate_payload(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                self.ontology_law_selector_yaml(),
                self.ontology_law_receipt_yaml(),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertEqual(report.errors, [])

    def test_ontology_law_fixture_accepts_atlasglue_underdetermination_without_claim_promotion(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                self.ontology_law_selector_yaml(
                    decision_basis=(
                        "AtlasGlue_src^+ and M_src adoption remain blocked because current ontology "
                        "does not derive a source-side profile selector transition inverse cocycle "
                        "or finite-variation law."
                    ),
                    preserves_claim_blocks=(
                        "No AtlasGlue_src^+ adoption, M_src adoption, g_eff, matter coupling, "
                        "Einstein equations, benchmark promotion, Gate Chair status, canonical "
                        "ontology edit, or completed derivation is authorized."
                    ),
                ),
                self.ontology_law_receipt_yaml(
                    missing_source_law=(
                        "AtlasGlue_src^+ profile selector transition inverse cocycle "
                        "and finite-variation law"
                    ),
                    underdetermination_statement=(
                        "current ontology does not derive the AtlasGlue_src^+ profile selector "
                        "transition inverse cocycle and finite-variation law."
                    ),
                    source_side_definition=(
                        "Define AtlasGlue_src^+ candidate ordering from source-local discriminator "
                        "profiles and source transition data only."
                    ),
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertEqual(report.errors, [])

    def test_ontology_law_receipt_rejects_ordinary_gap_trigger(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                self.ontology_law_selector_yaml(),
                self.ontology_law_receipt_yaml(trigger_classification="ordinary_gap"),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("ordinary gaps" in error for error in report.errors))

    def test_ontology_law_fixture_rejects_documentation_or_registry_repair_route(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                self.ontology_law_selector_yaml(
                    decision_basis="A missing documentation page and registry row are incorrectly escalated.",
                ),
                self.ontology_law_receipt_yaml(
                    trigger_classification="ordinary_gap",
                    missing_source_law="missing README section and registry row",
                    underdetermination_statement=(
                        "current ontology does not derive the missing README section and registry row."
                    ),
                    source_side_definition="Repair the documentation and registry row.",
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("ordinary gaps" in error for error in report.errors))

    def test_ontology_law_receipt_rejects_target_import_definition(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                self.ontology_law_selector_yaml(),
                self.ontology_law_receipt_yaml(
                    source_side_definition="Define the selector directly from target metric and target atlas data."
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("target-GR imports" in error for error in report.errors))

    def test_ontology_law_fixture_rejects_selector_data_from_target_gr_atlas(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                self.ontology_law_selector_yaml(),
                self.ontology_law_receipt_yaml(
                    source_side_definition=(
                        "Define selector data by reading the target GR atlas chart and target metric "
                        "before source-side construction."
                    )
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("target-GR imports" in error for error in report.errors))

    def test_ontology_law_receipt_rejects_premature_impossibility_claim(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                self.ontology_law_selector_yaml(),
                self.ontology_law_receipt_yaml(
                    underdetermination_statement=(
                        "current ontology does not derive the source-side selector law; "
                        "therefore the selector is impossible"
                    )
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("impossibility" in error for error in report.errors))

    def test_ontology_law_fixture_accepts_human_gated_canonical_candidate(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                self.ontology_law_selector_yaml(),
                self.ontology_law_receipt_yaml(status_label="canonical-ontology candidate"),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertEqual(report.errors, [])

    def test_ontology_law_fixture_rejects_canonical_candidate_without_human_gate(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("packet_selection"),
                self.ontology_law_selector_yaml(),
                self.ontology_law_receipt_yaml(
                    status_label="canonical-ontology candidate",
                    gate_required="false",
                ),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-06-17T15:46:25Z",
        )
        self.assertTrue(any("human gate" in error for error in report.errors))

    def test_ontology_law_receipt_rejects_missing_required_boundary_fields(self) -> None:
        cases = [
            (
                "milestone",
                {"target_derivation_milestone": ""},
                "target_derivation_milestone is required",
            ),
            ("burden", {"milestone_burden": ""}, "milestone_burden is required"),
            ("missing-law", {"missing_source_law": ""}, "missing_source_law is required"),
            (
                "blocked-adoption",
                {"current_adoption": "adopted"},
                "adoption_status.current_adoption must be blocked",
            ),
            (
                "exact-gr",
                {"include_exact_gr_obligations": False},
                "exact_gr_recovery_obligations must be a map",
            ),
            (
                "no-target-scope",
                {"include_no_target_import_scope": False},
                "no_target_import_audit_scope must be a map",
            ),
            (
                "human-gate",
                {"include_human_gate_request": False},
                "human_gate_request must be a map",
            ),
        ]
        for name, receipt_kwargs, expected_error in cases:
            with self.subTest(name=name):
                completion_extra = "\n".join(
                    [
                        self.roadmap_distance_matrix_yaml(),
                        self.minimal_payload_yaml("packet_selection"),
                        self.ontology_law_selector_yaml(),
                        self.ontology_law_receipt_yaml(**receipt_kwargs),
                    ]
                )
                report = self.validate_completion_fixture(
                    role_id="theoretical-continuation-selector",
                    completion_extra=completion_extra,
                    timestamp="2026-06-17T15:46:25Z",
                )
                self.assertTrue(any(expected_error in error for error in report.errors))

    def test_future_physics_job_rejects_direct_ontology_write(self) -> None:
        report = self.validator.ValidationReport()
        row = {
            "job_id": "AJ-TEST",
            "role_id": "refuter",
            "job_path": "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
            "created_at": "2026-06-16T20:00:00Z",
            "started_at": "",
            "completed_at": "",
        }
        self.validator.validate_future_physics_job_authority(
            report,
            row,
            {
                "allowed_write_paths": ["ontology/tex/example.tex"],
                "forbidden_source_classes": [
                    "canonical_ontology_write",
                    "benchmark_promotion",
                    "candidate_reconstruction",
                    "gate_chair_verdict",
                    "completed_derivation_claim",
                    "global_theory_rejection",
                    "generated_derivative_authority",
                ],
            },
        )
        self.assertTrue(any("may not allow direct write path" in error for error in report.errors))

    def test_future_physics_job_requires_parent_child_decomposition_after_activation(self) -> None:
        report = self.validator.ValidationReport()
        row = {
            "job_id": "AJ-TEST",
            "role_id": "refuter",
            "job_path": "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
            "created_at": "2026-06-17T04:08:16Z",
            "started_at": "",
            "completed_at": "",
        }
        self.validator.validate_future_physics_job_authority(
            report,
            row,
            {
                "allowed_write_paths": ["research_control/tasks/RT-TEST/**"],
                "forbidden_source_classes": [
                    "canonical_ontology_write",
                    "benchmark_promotion",
                    "candidate_reconstruction",
                    "gate_chair_verdict",
                    "completed_derivation_claim",
                    "global_theory_rejection",
                    "generated_derivative_authority",
                ],
            },
        )
        self.assertTrue(any("must declare role_decomposition.mode" in error for error in report.errors))

    def test_roadmap_future_physics_job_requires_target_milestone(self) -> None:
        report = self.validator.ValidationReport()
        row = {
            "job_id": "AJ-TEST",
            "role_id": "refuter",
            "job_path": "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
            "created_at": "2026-06-17T15:46:25Z",
            "started_at": "",
            "completed_at": "",
        }
        self.validator.validate_future_physics_job_authority(
            report,
            row,
            {
                "allowed_write_paths": ["research_control/tasks/RT-TEST/**"],
                "forbidden_source_classes": [
                    "canonical_ontology_write",
                    "benchmark_promotion",
                    "candidate_reconstruction",
                    "gate_chair_verdict",
                    "completed_derivation_claim",
                    "global_theory_rejection",
                    "generated_derivative_authority",
                ],
                "role_decomposition": {},
            },
        )
        self.assertTrue(any("target_derivation_milestone" in error for error in report.errors))
        self.assertTrue(any("milestone_burden" in error for error in report.errors))

    def test_roadmap_future_physics_job_accepts_target_milestone(self) -> None:
        report = self.validator.ValidationReport()
        row = {
            "job_id": "AJ-TEST",
            "role_id": "refuter",
            "job_path": "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
            "created_at": "2026-06-17T15:46:25Z",
            "started_at": "",
            "completed_at": "",
        }
        self.validator.validate_future_physics_job_authority(
            report,
            row,
            {
                "allowed_write_paths": ["research_control/tasks/RT-TEST/**"],
                "forbidden_source_classes": [
                    "canonical_ontology_write",
                    "benchmark_promotion",
                    "candidate_reconstruction",
                    "gate_chair_verdict",
                    "completed_derivation_claim",
                    "global_theory_rejection",
                    "generated_derivative_authority",
                ],
                "role_decomposition": {},
                "target_derivation_milestone": "response_localization_resp_lc",
                "milestone_burden": "Discharge response selector sign scale and token semantics.",
            },
        )
        self.assertEqual(report.errors, [])

    def test_historical_physics_job_without_parent_child_decomposition_remains_valid(self) -> None:
        report = self.validator.ValidationReport()
        row = {
            "job_id": "AJ-TEST",
            "role_id": "refuter",
            "job_path": "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
            "created_at": "2026-06-17T04:00:00Z",
            "started_at": "",
            "completed_at": "",
        }
        self.validator.validate_future_physics_job_authority(
            report,
            row,
            {
                "allowed_write_paths": ["research_control/tasks/RT-TEST/**"],
                "forbidden_source_classes": [
                    "canonical_ontology_write",
                    "benchmark_promotion",
                    "candidate_reconstruction",
                    "gate_chair_verdict",
                    "completed_derivation_claim",
                    "global_theory_rejection",
                    "generated_derivative_authority",
                ],
            },
        )
        self.assertFalse(any("must declare role_decomposition.mode" in error for error in report.errors))


if __name__ == "__main__":
    unittest.main()
