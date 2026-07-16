from __future__ import annotations

import importlib.util
import csv
import hashlib
import json
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
        cls.continue_research_memory_preflight = load_module(
            "continue_research_memory_preflight",
            "continue_research_memory_preflight.py",
        )
        cls.checkpoint = load_module("checkpoint_research_transaction", "checkpoint_research_transaction.py")
        cls.metrics = load_module(
            "report_physics_progress_metrics",
            "report_physics_progress_metrics.py",
        )
        cls.ai_methodology_dashboard = load_module(
            "render_ai_methodology_metrics_dashboard",
            "render_ai_methodology_metrics_dashboard.py",
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
        self.assertIn("operational_validation_metrics", metrics)
        self.assertIn("scientific_progress_metrics", metrics)
        self.assertFalse(report["authority_boundary"]["physics_claim_promotion_authorized"])

    def test_physics_progress_metrics_separate_operational_and_scientific_scoreboards(self) -> None:
        report = self.metrics.build_report(REPO_ROOT)
        metrics = report["metrics"]
        operational = metrics["operational_validation_metrics"]
        scientific = metrics["scientific_progress_metrics"]

        self.assertIn("completion_validation_status_counts", operational)
        self.assertNotIn("completion_validation_status_counts", scientific)
        self.assertEqual(self.metrics.scientific_metric_key_violations(scientific), [])
        self.assertEqual(metrics["metric_separation_guard"]["status"], "pass")

    def test_support_only_checker_metrics_are_operational_only(self) -> None:
        report = self.metrics.build_report(REPO_ROOT)
        metrics = report["metrics"]
        operational = metrics["operational_validation_metrics"]
        scientific = metrics["scientific_progress_metrics"]

        self.assertIn("support_only_checker_reports_found", operational)
        self.assertGreaterEqual(operational["support_only_checker_reports_found"], 1)
        self.assertNotIn("support_only_checker_reports_found", scientific)
        self.assertNotIn("support_only_checker_status_counts", scientific)
        self.assertEqual(metrics["metric_separation_guard"]["status"], "pass")

    def test_payload_density_and_route_orbit_metrics_are_operational_only(self) -> None:
        report = self.metrics.build_report(REPO_ROOT)
        metrics = report["metrics"]
        scientific = metrics["scientific_progress_metrics"]
        payload_density = metrics["payload_density_metrics"]
        route_orbit = metrics["route_orbit_risk_metrics"]

        for key in (
            "tasks_since_last_distance_to_gr_delta",
            "tasks_since_last_burden_discharged",
            "new_payload_items_per_physics_task",
            "new_payload_items_per_cycle",
            "selector_cycles_without_new_payload",
        ):
            self.assertIn(key, payload_density)
            self.assertNotIn(key, scientific)

        for key in (
            "same_burden_repetition_count",
            "freeze_reviews_triggered_by_repetition",
            "bridge_attempts_since_last_gate",
            "obstructions_created",
            "obstructions_reused",
            "candidate_construct_audit_stress_selector_cycles",
            "gate_ready_cycles_without_gate_verdict",
            "support_only_tooling_reports",
            "physics_promotion_authorized_true_count",
            "physics_promotion_authorized_false_count",
        ):
            self.assertIn(key, route_orbit)
            self.assertNotIn(key, scientific)

        self.assertEqual(metrics["metric_separation_guard"]["status"], "pass")

    def test_physics_progress_integration_metrics_count_required_packet_types(self) -> None:
        report = self.metrics.build_report(REPO_ROOT)
        metrics = report["metrics"]
        scientific = metrics["scientific_progress_metrics"]
        integration = metrics["physics_progress_integration_metrics"]
        separate_counts = integration["separate_packet_counts"]

        self.assertEqual(integration["status"], "pass")
        self.assertTrue(integration["not_physics_proof"])
        self.assertFalse(integration["physics_claim_promotion_authorized"])
        self.assertTrue(report["authority_boundary"]["metrics_report_not_physics_proof"])
        self.assertIn("effect_counts", integration["distance_delta"])

        for key in (
            "candidate_packet_count",
            "obstruction_packet_count",
            "freeze_packet_count",
            "theorem_packet_count",
            "process_only_packet_count",
        ):
            self.assertIn(key, separate_counts)
            self.assertIsInstance(separate_counts[key], int)

        self.assertGreaterEqual(separate_counts["process_only_packet_count"], 1)
        self.assertIn("payload_density_summary", integration)
        self.assertNotIn("physics_progress_integration_metrics", scientific)
        self.assertEqual(metrics["metric_separation_guard"]["status"], "pass")

    def test_ai_methodology_metrics_are_support_only_and_separate(self) -> None:
        report = self.metrics.build_report(REPO_ROOT)
        metrics = report["metrics"]
        scientific = metrics["scientific_progress_metrics"]
        methodology = metrics["ai_research_agent_methodology_metrics"]

        self.assertEqual(
            set(methodology["metrics"]),
            set(self.metrics.AI_METHODOLOGY_REQUIRED_METRICS),
        )
        self.assertEqual(methodology["metric_count"], 9)
        self.assertEqual(methodology["separation_guard"]["status"], "pass")
        self.assertTrue(methodology["separation_guard"]["kept_out_of_scientific_progress_metrics"])
        self.assertTrue(methodology["separation_guard"]["not_physics_proof"])
        self.assertFalse(
            methodology["authority_boundary"]["physics_claim_authority_created"],
        )
        self.assertFalse(
            methodology["authority_boundary"]["physics_promotion_authorized"],
        )
        self.assertTrue(report["authority_boundary"]["ai_methodology_metrics_are_support_only"])
        self.assertNotIn("ai_research_agent_methodology_metrics", scientific)

        for metric in methodology["metrics"].values():
            self.assertIn(metric["status"], {"measured", "partial", "not_measured"})
            self.assertFalse(metric["authority_boundary"]["physics_claim_authority_created"])
            self.assertFalse(metric["authority_boundary"]["physics_promotion_authorized"])
            self.assertFalse(metric["authority_boundary"]["gate_chair_verdict_created"])
            self.assertFalse(metric["authority_boundary"]["benchmark_promotion_authorized"])

    def test_payload_density_warnings_are_advisory(self) -> None:
        report = self.metrics.build_report(REPO_ROOT)
        warnings = report["metrics"]["diagnostic_warnings"]

        self.assertIsInstance(warnings, list)
        for warning in warnings:
            self.assertEqual(warning["severity"], "warning")
            self.assertFalse(warning["hard_gate"])
            self.assertFalse(warning["physics_claim_authority"])
            self.assertIn("warning_id", warning)
            self.assertIn("recommended_guard_action", warning)

    def test_physics_progress_metrics_markdown_renders_diagnostic_sections(self) -> None:
        report = self.metrics.build_report(REPO_ROOT)
        rendered = self.metrics.render_markdown(report)

        self.assertIn("## Payload-Density Metrics", rendered)
        self.assertIn("## Route-Orbit Risk Metrics", rendered)
        self.assertIn("## Physics-Progress Integration Metrics", rendered)
        self.assertIn("## AI Research-Agent Methodology Metrics", rendered)
        self.assertIn("## AI Methodology Acceptance Warnings", rendered)
        self.assertIn("`overclaim_catch_rate`", rendered)
        self.assertIn("Claim-boundary control", rendered)
        self.assertIn("## Diagnostic Warnings", rendered)

    def test_ai_methodology_dashboard_is_support_only_and_not_truth_ranking(self) -> None:
        dashboard = self.ai_methodology_dashboard.build_dashboard(REPO_ROOT)
        rendered = self.ai_methodology_dashboard.render_markdown(dashboard)

        self.assertEqual(dashboard["schema_id"], "ai_methodology_metrics_dashboard_v1")
        self.assertEqual(dashboard["dashboard_type"], "support_only_ai_system_diagnostic")
        self.assertEqual(dashboard["dashboard_labels"]["primary_label"], "AI-system diagnostic")
        self.assertTrue(dashboard["dashboard_labels"]["support_only"])
        self.assertTrue(dashboard["dashboard_labels"]["no_physics_truth_ranking"])
        self.assertEqual(dashboard["dashboard_labels"]["truth_ranking"], "none")
        self.assertEqual(dashboard["plan_task_id"], "P8-T04")
        self.assertIn("P12-T04", dashboard["plan_task_ids"])
        self.assertIn("P8-T04", dashboard["plan_task_ids"])
        self.assertEqual(
            len(dashboard["metric_rows"]),
            len(self.metrics.AI_METHODOLOGY_REQUIRED_METRICS),
        )
        self.assertGreater(len(dashboard["payload_ratio_metric_rows"]), 0)
        self.assertGreater(len(dashboard["route_orbit_warning_rows"]), 0)
        self.assertEqual(
            dashboard["physics_payload_ratio_diagnostics"]["schema_id"],
            "physics_payload_ratio_route_history_metrics_v1",
        )
        self.assertTrue(
            dashboard["physics_payload_ratio_diagnostics"]["authority_boundary"][
                "does_not_rank_physics_truth"
            ],
        )
        self.assertTrue(
            dashboard["physics_payload_ratio_diagnostics"]["authority_boundary"][
                "not_physics_proof"
            ],
        )
        self.assertFalse(dashboard["claim_boundary"]["physics_claim_authority_created"])
        self.assertFalse(dashboard["claim_boundary"]["physics_promotion_authorized"])
        self.assertFalse(dashboard["claim_boundary"]["gate_chair_verdict_created"])
        self.assertFalse(dashboard["claim_boundary"]["benchmark_promotion_authorized"])
        self.assertTrue(dashboard["claim_boundary"]["dashboard_not_physics_truth_ranking"])
        self.assertTrue(dashboard["claim_boundary"]["dashboard_not_physics_truth_establishment"])

        forbidden_fields = {
            "truth_rank",
            "physics_truth_rank",
            "physics_truth_score",
            "physics_truth_ranking",
        }
        for row in dashboard["metric_rows"]:
            self.assertEqual(row["diagnostic_label"], "AI-system diagnostic")
            self.assertFalse(forbidden_fields.intersection(row))
            self.assertFalse(row["authority_boundary"]["physics_claim_authority_created"])
            self.assertFalse(row["authority_boundary"]["physics_promotion_authorized"])

        for row in dashboard["payload_ratio_metric_rows"]:
            self.assertEqual(row["diagnostic_label"], "Payload-ratio diagnostic")
            self.assertFalse(forbidden_fields.intersection(row))
            self.assertTrue(row["authority_boundary"]["does_not_rank_physics_truth"])
            self.assertTrue(row["authority_boundary"]["not_physics_proof"])

        route_warning_ids = {
            row["warning_id"] for row in dashboard["route_orbit_warning_rows"]
        }
        self.assertIn("post_gate_cycle_repeat", route_warning_ids)
        self.assertIn("gate_ready_without_gate", route_warning_ids)
        for row in dashboard["route_orbit_warning_rows"]:
            self.assertEqual(row["diagnostic_label"], "Route-orbit warning")
            self.assertFalse(row["hard_gate"])
            self.assertFalse(row["physics_claim_authority"])

        self.assertIn("AI-system diagnostic", rendered)
        self.assertIn("does not rank physics truth by workflow activity", rendered)
        self.assertIn("Payload-Ratio Diagnostics", rendered)
        self.assertIn("Route-Orbit Warnings", rendered)
        self.assertIn("do not establish physics truth", rendered)

    def test_support_only_checker_parse_errors_are_tooling_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            artifacts = repo_root / "research_control" / "tasks" / "RT-TEST" / "artifacts"
            artifacts.mkdir(parents=True)
            (artifacts / "valid_checker_report.json").write_text(
                json.dumps(
                    {
                        "checker_id": "finite_local_candidate_checker",
                        "status": "pass_support_only",
                        "boundary_statement": "This is support-only and not proof authority.",
                        "forbidden_overread_flags": [],
                        "physics_obstruction": "",
                        "tooling_error": False,
                    }
                ),
                encoding="utf-8",
            )
            (artifacts / "malformed_checker_report.json").write_text("{", encoding="utf-8")

            metrics = self.metrics.collect_support_only_checker_metrics(repo_root)

        self.assertEqual(metrics["support_only_checker_report_files_scanned"], 2)
        self.assertEqual(metrics["support_only_checker_report_parse_errors"], 1)
        self.assertEqual(metrics["support_only_checker_reports_found"], 1)
        self.assertEqual(
            metrics["support_only_checker_status_counts"],
            {"pass_support_only": 1},
        )
        self.assertEqual(metrics["support_only_checker_physics_obstruction_reports"], 0)

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

    def current_frontier_sync_fixture_report(
        self,
        *,
        snapshot_task_id: str = "RT-TEST",
        snapshot_burden_status: str = "accepted",
        milestone: str = "none",
        burden_id: str = "none",
        ledger_status: str = "accepted",
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            control = root / "research_control"
            registries = root / "registries"
            task_dir = control / "tasks" / "RT-TEST"
            handoff_dir = control / "handoffs"
            task_dir.mkdir(parents=True)
            handoff_dir.mkdir(parents=True)
            registries.mkdir(parents=True)
            next_action = "Run one bounded fixture action."
            (control / "program_state.yaml").write_text(
                "\n".join(
                    [
                        'active_task_id: "RT-TEST"',
                        'latest_handoff_id: "handoff-0001"',
                        'current_status: "fixture_status"',
                        f'next_recommended_action: "{next_action}"',
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (task_dir / "00_TASK.yaml").write_text('task_id: "RT-TEST"\n', encoding="utf-8")
            (handoff_dir / "handoff-0001.yaml").write_text(
                "\n".join(
                    [
                        'handoff_id: "handoff-0001"',
                        'task_id: "RT-TEST"',
                        'job_id: "AJ-RT-TEST-001"',
                        f'next_action: "{next_action}"',
                        "distance_to_gr:",
                        f'  milestone: "{milestone}"',
                        f'  burden_id: "{burden_id}"',
                        f'  status: "{ledger_status}"',
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (registries / "DISTANCE_TO_GR_LEDGER.csv").write_text(
                "\n".join(
                    [
                        "burden_id,milestone,required_object,current_status,blocking_burden,accept_criteria,failure_or_freeze_criteria,last_evidence_path,updated_at,notes",
                        f"{burden_id},{milestone},fixture,{ledger_status},fixture block,fixture accept,fixture fail,research_control/program_state.yaml,2026-06-28T00:00:00Z,fixture",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            target_milestone = milestone if milestone != "none" else "none; project-control fixture"
            (control / "current_frontier.md").write_text(
                "\n".join(
                    [
                        "# Current Research Frontier",
                        "",
                        "## Active Research State",
                        "",
                        "| Field | Value |",
                        "| --- | --- |",
                        f"| Active task ID | `{snapshot_task_id}` |",
                        "| Latest handoff ID | `handoff-0001` |",
                        "| Current status | `fixture_status` |",
                        f"| Target derivation milestone | {target_milestone} |",
                        "| Current burden | fixture burden |",
                        f"| Next recommended action | {next_action} |",
                        "",
                        "## Distance-To-GR Table",
                        "",
                        "| Burden ID | Milestone | Current status | Blocking burden | Last evidence |",
                        "| --- | --- | --- | --- | --- |",
                        f"| `{burden_id}` | `{milestone}` | {snapshot_burden_status} | fixture block | `research_control/program_state.yaml` |",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            report = self.validator.ValidationReport()
            with mock.patch.object(self.validator, "REPO_ROOT", root), mock.patch.object(
                self.validator, "CONTROL_DIR", control
            ), mock.patch.object(self.validator, "REGISTRY_DIR", registries):
                self.validator.validate_current_frontier_sync(
                    report,
                    {"RT-TEST": {"task_id": "RT-TEST"}},
                )
        return report

    def test_current_frontier_sync_accepts_synchronized_fixture(self) -> None:
        report = self.current_frontier_sync_fixture_report()
        self.assertEqual(report.errors, [])

    def test_current_frontier_sync_rejects_stale_active_task_snapshot(self) -> None:
        report = self.current_frontier_sync_fixture_report(snapshot_task_id="RT-OLD")
        joined = "\n".join(report.errors)
        self.assertIn("field=active_task_id", joined)
        self.assertIn("authoritative_value='RT-TEST'", joined)
        self.assertIn("snapshot_value='RT-OLD'", joined)
        self.assertIn("authoritative_source=research_control/program_state.yaml", joined)
        self.assertIn("suggested_repair_route=", joined)

    def test_current_frontier_sync_rejects_stale_active_burden_status(self) -> None:
        report = self.current_frontier_sync_fixture_report(
            milestone="matter_coupling",
            burden_id="matter_coupling",
            ledger_status="accepted",
            snapshot_burden_status="stale",
        )
        joined = "\n".join(report.errors)
        self.assertIn("field=distance_to_gr.current_status[matter_coupling]", joined)
        self.assertIn("authoritative_value='accepted'", joined)
        self.assertIn("snapshot_value='stale'", joined)
        self.assertIn("authoritative_source=registries/DISTANCE_TO_GR_LEDGER.csv", joined)

    def test_continue_research_memory_preflight_refreshes_local_cache_warning(self) -> None:
        warning_payload = {
            "core_validation_status": "PASS",
            "freshness_status": "WARN",
            "local_retrieval_status": "WARN",
            "vault_exists": True,
            "memory_index_exists": True,
            "source_object_count": 3,
            "vault_row_count": 3,
            "semantic_row_count": 3,
            "relationship_row_count": 7,
            "freshness_categories": {
                "blocking": [],
                "non_blocking": [],
                "local_cache_only": ["Memory SQLite index is older than inputs"],
            },
            "freshness_warnings": ["Memory SQLite index is older than inputs"],
        }
        fresh_payload = {
            **warning_payload,
            "freshness_status": "PASS",
            "local_retrieval_status": "PASS",
            "freshness_categories": {
                "blocking": [],
                "non_blocking": [],
                "local_cache_only": [],
            },
            "freshness_warnings": [],
        }

        with mock.patch.object(
            self.continue_research_memory_preflight,
            "memory_status",
            side_effect=[warning_payload, fresh_payload],
        ) as status_mock, mock.patch.object(
            self.continue_research_memory_preflight,
            "sync_local_retrieval",
            return_value={"command": "sync"},
        ) as sync_mock:
            payload = self.continue_research_memory_preflight.run_preflight(Path("/tmp/repo"))

        self.assertTrue(payload["refresh_needed"])
        self.assertTrue(payload["refresh_performed"])
        self.assertEqual(payload["status_summary"]["local_retrieval_status"], "PASS")
        self.assertEqual(status_mock.call_count, 2)
        sync_mock.assert_called_once()

    def test_continue_research_memory_preflight_skips_refresh_when_fresh(self) -> None:
        fresh_payload = {
            "core_validation_status": "PASS",
            "freshness_status": "PASS",
            "local_retrieval_status": "PASS",
            "vault_exists": True,
            "memory_index_exists": True,
            "source_object_count": 3,
            "vault_row_count": 3,
            "semantic_row_count": 3,
            "relationship_row_count": 7,
            "freshness_categories": {
                "blocking": [],
                "non_blocking": [],
                "local_cache_only": [],
            },
            "freshness_warnings": [],
        }

        with mock.patch.object(
            self.continue_research_memory_preflight,
            "memory_status",
            return_value=fresh_payload,
        ) as status_mock, mock.patch.object(
            self.continue_research_memory_preflight,
            "sync_local_retrieval",
        ) as sync_mock:
            payload = self.continue_research_memory_preflight.run_preflight(Path("/tmp/repo"))

        self.assertFalse(payload["refresh_needed"])
        self.assertFalse(payload["refresh_performed"])
        self.assertEqual(payload["status_summary"]["local_retrieval_status"], "PASS")
        status_mock.assert_called_once()
        sync_mock.assert_not_called()

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

    def test_write_path_diff_runs_claim_language_gate_for_public_changes(self) -> None:
        report = self.validator.ValidationReport()
        jobs = {
            "AJ-TEST": {
                "job_id": "AJ-TEST",
                "role_id": "validator-engineer",
                "status": "completed",
                "created_at": "2026-07-01T00:00:00Z",
                "allowed_write_paths": "README.md",
                "output_paths": "",
            }
        }
        linter_report = {
            "config_errors": [],
            "findings": [
                {
                    "path": "README.md",
                    "line": 1,
                    "class_id": "einstein_equation_overclaim",
                    "matched_text": "GR derived",
                    "severity": "hard_fail_current_public",
                    "corrective_language": "Use scoped non-promotional wording.",
                }
            ],
        }
        with mock.patch.object(
            self.validator,
            "changed_paths",
            return_value=["README.md"],
        ), mock.patch.object(
            self.validator,
            "validate_markdown_authority_boundaries",
        ), mock.patch.object(
            self.validator.claim_language_linter,
            "claim_language_gate_paths",
            return_value=["README.md"],
        ), mock.patch.object(
            self.validator.claim_language_linter,
            "validate_paths",
            return_value=linter_report,
        ):
            self.validator.validate_diff(report, jobs, "HEAD", False)

        self.assertTrue(any("claim-language hard failure" in error for error in report.errors))

    def test_write_path_diff_accepts_bridge_referenced_sidecar_pair(self) -> None:
        report = self.validator.ValidationReport()
        source_path = (
            "research_control/tasks/RT-TEST/jobs/completions/"
            "AJC-AJ-RT-TEST-001.yaml"
        )
        sidecar_yaml = (
            "research_control/project_improvement_handoffs/"
            "improve-project-handoff_20260622_777.yaml"
        )
        sidecar_markdown = sidecar_yaml.replace(".yaml", ".md")
        jobs = {
            "AJ-TEST": {
                "job_id": "AJ-TEST",
                "status": "completed",
                "created_at": "2026-06-22T00:00:00Z",
                "allowed_write_paths": source_path,
                "output_paths": "",
                "job_path": "",
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / source_path
            source.parent.mkdir(parents=True)
            source.write_text(
                "\n".join(
                    [
                        'completion_id: "AJC-AJ-RT-TEST-001"',
                        'completed_at: "2026-06-22T06:00:00Z"',
                        "project_improvement_signals:",
                        '  - signal_id: "PIS-RT-TEST-001"',
                        '    signal_type: "validator_gap"',
                        '    severity: "high"',
                        '    evidence: "Synthetic test signal."',
                        f'    evidence_path: "{source_path}"',
                        '    recommended_skill: "improve-project-system"',
                        '    recommended_role: "validator-engineer"',
                        "project_improvement_bridge:",
                        "  required: true",
                        f'  improvement_handoff_path: "{sidecar_yaml}"',
                        "  signal_ids:",
                        '    - "PIS-RT-TEST-001"',
                        '  bridge_status: "generated"',
                        '  notes: "Synthetic bridge reference."',
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            sidecar = root / sidecar_yaml
            sidecar.parent.mkdir(parents=True)
            sidecar.write_text(
                "\n".join(
                    [
                        'improvement_handoff_id: "improve-project-handoff_20260622_777"',
                        'status: "open"',
                        "source:",
                        f'  completion_path: "{source_path}"',
                        '  regular_handoff_yaml_path: ""',
                        "normal_research_continuation:",
                        "  sidecar_does_not_replace_regular_handoff: true",
                        "project_boundary:",
                        '  recommended_skill: "improve-project-system"',
                        "  project_system_only: true",
                        "  physics_claim_promotion_authorized: false",
                        "  canonical_science_source_edits_authorized: false",
                        "  generated_derivative_hand_edits_authorized: false",
                        "signal_summary:",
                        "  signal_ids:",
                        '    - "PIS-RT-TEST-001"',
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (root / sidecar_markdown).write_text(
                "# improve-project-handoff_20260622_777\n",
                encoding="utf-8",
            )

            with mock.patch.object(self.validator, "REPO_ROOT", root), mock.patch.object(
                self.validator,
                "changed_paths",
                return_value=[source_path, sidecar_yaml, sidecar_markdown],
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
        object_id: str = "MD-IMMUTABLE-CONTROL-SOURCE",
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
                    "object_id": object_id,
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
                    "command": f".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup {object_id} --json",
                    "query_type": "lookup",
                    "query_text": object_id,
                    "returned_object_ids": [object_id],
                }
            ],
            "canonical_inspections": [],
            "authority_note": "Obsidian, semantic extracts, wiki notes, and .local are retrieval layers only and not authority.",
        }
        if include_inspection:
            receipt["canonical_inspections"].append(
                {
                    "object_id": object_id,
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

    def test_memory_preflight_allows_historical_skill_contract_hash(self) -> None:
        root, receipt = self.memory_preflight_fixture(
            stale_hash=True,
            object_id="MD-SKILL-CONTINUE-RESEARCH",
        )
        with mock.patch.object(self.validator, "REPO_ROOT", root), mock.patch.object(
            self.validator, "REGISTRY_DIR", root / "registries"
        ):
            report = self.validate_memory_preflight_fixture(receipt)
        self.assertFalse(any("source_hash" in error for error in report.errors))

    def test_memory_preflight_allows_historical_current_frontier_hash(self) -> None:
        root = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        control = root / "research_control"
        registries = root / "registries"
        control.mkdir(parents=True)
        registries.mkdir(parents=True)
        (control / "program_state.yaml").write_text(
            'active_task_id: "RT-ACTIVE"\n',
            encoding="utf-8",
        )
        frontier = control / "current_frontier.md"
        frontier.write_text("current frontier\n", encoding="utf-8")
        current_hash = sha256_text("current frontier\n")
        with (registries / "MARKDOWN_SOURCE_REGISTRY.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["object_id", "path", "source_hash"])
            writer.writeheader()
            writer.writerow(
                {
                    "object_id": "MD-RESEARCH-CONTROL-CURRENT-FRONTIER",
                    "path": "research_control/current_frontier.md",
                    "source_hash": current_hash,
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
                    "command": ".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup MD-RESEARCH-CONTROL-CURRENT-FRONTIER --json",
                    "query_type": "lookup",
                    "query_text": "MD-RESEARCH-CONTROL-CURRENT-FRONTIER",
                    "returned_object_ids": ["MD-RESEARCH-CONTROL-CURRENT-FRONTIER"],
                }
            ],
            "canonical_inspections": [
                {
                    "object_id": "MD-RESEARCH-CONTROL-CURRENT-FRONTIER",
                    "source_registry": "MARKDOWN_SOURCE_REGISTRY.csv",
                    "registry_path": "registries/MARKDOWN_SOURCE_REGISTRY.csv",
                    "canonical_path": "research_control/current_frontier.md",
                    "source_hash": "historical-frontier-hash",
                }
            ],
            "authority_note": "Obsidian, semantic extracts, wiki notes, and .local are retrieval layers only and not authority.",
        }
        report = self.validator.ValidationReport()
        with (
            mock.patch.object(self.validator, "REPO_ROOT", root),
            mock.patch.object(self.validator, "REGISTRY_DIR", registries),
            mock.patch.object(self.validator, "CONTROL_DIR", control),
        ):
            self.validator.validate_memory_preflight(
                report,
                {
                    "job_id": "AJ-HISTORICAL",
                    "task_id": "RT-HISTORICAL",
                    "created_at": "2026-06-18T15:33:00Z",
                },
                {"memory_preflight": receipt},
                "research_control/tasks/RT-HISTORICAL/jobs/AJ-HISTORICAL.yaml",
            )
        self.assertEqual(report.errors, [])

    def test_memory_preflight_allows_historical_public_documentation_hash(self) -> None:
        root = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        control = root / "research_control"
        registries = root / "registries"
        control.mkdir(parents=True)
        registries.mkdir(parents=True)
        (control / "program_state.yaml").write_text(
            'active_task_id: "RT-ACTIVE"\n',
            encoding="utf-8",
        )
        readme = root / "README.md"
        readme.write_text("current public summary\n", encoding="utf-8")
        current_hash = sha256_text("current public summary\n")
        with (registries / "MARKDOWN_SOURCE_REGISTRY.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["object_id", "path", "source_hash"])
            writer.writeheader()
            writer.writerow(
                {
                    "object_id": "MD-README",
                    "path": "README.md",
                    "source_hash": current_hash,
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
                    "command": ".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup MD-README --json",
                    "query_type": "lookup",
                    "query_text": "MD-README",
                    "returned_object_ids": ["MD-README"],
                }
            ],
            "canonical_inspections": [
                {
                    "object_id": "MD-README",
                    "source_registry": "MARKDOWN_SOURCE_REGISTRY.csv",
                    "registry_path": "registries/MARKDOWN_SOURCE_REGISTRY.csv",
                    "canonical_path": "README.md",
                    "source_hash": "historical-readme-hash",
                }
            ],
            "authority_note": "Obsidian, semantic extracts, wiki notes, and .local are retrieval layers only and not authority.",
        }
        report = self.validator.ValidationReport()
        with (
            mock.patch.object(self.validator, "REPO_ROOT", root),
            mock.patch.object(self.validator, "REGISTRY_DIR", registries),
            mock.patch.object(self.validator, "CONTROL_DIR", control),
        ):
            self.validator.validate_memory_preflight(
                report,
                {
                    "job_id": "AJ-HISTORICAL",
                    "task_id": "RT-HISTORICAL",
                    "created_at": "2026-06-18T15:33:00Z",
                },
                {"memory_preflight": receipt},
                "research_control/tasks/RT-HISTORICAL/jobs/AJ-HISTORICAL.yaml",
            )
        self.assertEqual(report.errors, [])

    def test_memory_preflight_allows_historical_validation_inventory_hash(self) -> None:
        root = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        control = root / "research_control"
        design = control / "design"
        registries = root / "registries"
        design.mkdir(parents=True)
        registries.mkdir(parents=True)
        (control / "program_state.yaml").write_text(
            'active_task_id: "RT-ACTIVE"\n',
            encoding="utf-8",
        )
        inventory = design / "validation_command_inventory_v16.md"
        inventory.write_text("current validation inventory\n", encoding="utf-8")
        current_hash = sha256_text("current validation inventory\n")
        with (registries / "MARKDOWN_SOURCE_REGISTRY.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["object_id", "path", "source_hash"])
            writer.writeheader()
            writer.writerow(
                {
                    "object_id": "MD-RESEARCH-CONTROL-DESIGN-VALIDATION-COMMAND-INVENTORY-V16",
                    "path": "research_control/design/validation_command_inventory_v16.md",
                    "source_hash": current_hash,
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
                    "command": ".venv/bin/python .codex/skills/project-memory-system/scripts/query_memory.py lookup MD-RESEARCH-CONTROL-DESIGN-VALIDATION-COMMAND-INVENTORY-V16 --json",
                    "query_type": "lookup",
                    "query_text": "MD-RESEARCH-CONTROL-DESIGN-VALIDATION-COMMAND-INVENTORY-V16",
                    "returned_object_ids": [
                        "MD-RESEARCH-CONTROL-DESIGN-VALIDATION-COMMAND-INVENTORY-V16"
                    ],
                }
            ],
            "canonical_inspections": [
                {
                    "object_id": "MD-RESEARCH-CONTROL-DESIGN-VALIDATION-COMMAND-INVENTORY-V16",
                    "source_registry": "MARKDOWN_SOURCE_REGISTRY.csv",
                    "registry_path": "registries/MARKDOWN_SOURCE_REGISTRY.csv",
                    "canonical_path": "research_control/design/validation_command_inventory_v16.md",
                    "source_hash": "historical-inventory-hash",
                }
            ],
            "authority_note": "Obsidian, semantic extracts, wiki notes, and .local are retrieval layers only and not authority.",
        }
        report = self.validator.ValidationReport()
        with (
            mock.patch.object(self.validator, "REPO_ROOT", root),
            mock.patch.object(self.validator, "REGISTRY_DIR", registries),
            mock.patch.object(self.validator, "CONTROL_DIR", control),
        ):
            self.validator.validate_memory_preflight(
                report,
                {
                    "job_id": "AJ-HISTORICAL",
                    "task_id": "RT-HISTORICAL",
                    "created_at": "2026-06-18T15:33:00Z",
                },
                {"memory_preflight": receipt},
                "research_control/tasks/RT-HISTORICAL/jobs/AJ-HISTORICAL.yaml",
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
        self.assertIn("dependency_graph_summary", status)
        graph_summary = status["dependency_graph_summary"]
        self.assertEqual(graph_summary["active_task"], program_state["active_task_id"])
        self.assertEqual(graph_summary["latest_handoff"], program_state["latest_handoff_id"])
        for field_name in (
            "active_burden",
            "immediate_upstream_objects",
            "accepted_scoped_objects",
            "draft_control_objects",
            "human_gated_objects",
            "blocked_downstream_objects",
            "frozen_negative_routes",
            "next_recommended_route",
            "graph_path_or_hash",
        ):
            self.assertIn(field_name, graph_summary)

    def test_continue_research_dependency_graph_summary_is_support_only(self) -> None:
        status = self.continue_research.continuation_status()
        graph_summary = status["dependency_graph_summary"]

        self.assertEqual(graph_summary["status"], "available")
        self.assertTrue(graph_summary["source_inspection_required"])
        self.assertIn("navigational support only", graph_summary["authority_note"])
        self.assertIn("cannot promote claims", graph_summary["authority_note"])
        self.assertEqual(graph_summary["graph_path"], "output/research_dependency_graph.json")
        self.assertRegex(graph_summary["graph_hash"], r"^[0-9a-f]{64}$")
        self.assertIn("output/research_dependency_graph.json#", graph_summary["graph_path_or_hash"])
        self.assertEqual(graph_summary["freshness_status"], "not_checked_by_continue_research")
        self.assertIn("render_dependency_graph.py --check", graph_summary["freshness_check_command"])
        for list_field in (
            "immediate_upstream_objects",
            "accepted_scoped_objects",
            "draft_control_objects",
            "human_gated_objects",
            "blocked_downstream_objects",
            "frozen_negative_routes",
        ):
            self.assertLessEqual(len(graph_summary[list_field]), self.continue_research.GRAPH_SUMMARY_LIMIT)

    def test_continue_research_route_orbit_diagnostics_are_advisory(self) -> None:
        fake_report = {
            "metrics": {
                "payload_density_metrics": {
                    "selector_cycles_without_new_payload": 3,
                },
                "route_orbit_risk_metrics": {
                    "same_burden_repetition_count": 5,
                    "gate_ready_cycles_without_gate_verdict": 9,
                },
                "diagnostic_warnings": [
                    {
                        "warning_id": "selector_cycles_without_new_payload",
                        "metric_key": "selector_cycles_without_new_payload",
                        "recommended_guard_action": "Require construction, obstruction, gate, or freeze before another selector cycle.",
                        "hard_gate": False,
                        "physics_claim_authority": False,
                    },
                    {
                        "warning_id": "gate_ready_without_gate",
                        "metric_key": "gate_ready_cycles_without_gate_verdict",
                        "recommended_guard_action": "Route the next eligible packet to Gate Chair review only with exact authority.",
                        "hard_gate": False,
                        "physics_claim_authority": False,
                    },
                ],
            }
        }

        with mock.patch.object(
            self.continue_research,
            "build_physics_progress_report",
            return_value=fake_report,
        ):
            diagnostics = self.continue_research.route_orbit_diagnostic_context(
                Path("/tmp/repo")
            )

        self.assertEqual(diagnostics["status"], "pass")
        self.assertTrue(diagnostics["warnings_are_advisory_only"])
        self.assertFalse(diagnostics["warning_hard_gates_created"])
        self.assertFalse(diagnostics["physics_claim_authority_created"])
        self.assertTrue(diagnostics["payload_density_warning"]["triggered"])
        self.assertTrue(diagnostics["route_orbit_warning"]["triggered"])
        self.assertTrue(diagnostics["same_burden_repetition_warning"]["triggered"])
        self.assertTrue(diagnostics["gate_ready_without_gate_warning"]["triggered"])
        self.assertFalse(diagnostics["route_orbit_warning"]["hard_gate"])
        self.assertFalse(diagnostics["route_orbit_warning"]["physics_claim_authority"])
        self.assertIn("selector_cycles_without_new_payload", diagnostics["recommended_guard_action"])

    def test_continue_research_context_warnings_do_not_block_gate_chair_route(self) -> None:
        fake_report = {
            "metrics": {
                "payload_density_metrics": {},
                "route_orbit_risk_metrics": {
                    "gate_ready_cycles_without_gate_verdict": 1,
                },
                "diagnostic_warnings": [
                    {
                        "warning_id": "gate_ready_without_gate",
                        "metric_key": "gate_ready_cycles_without_gate_verdict",
                        "recommended_guard_action": "Keep Gate Chair review available when exact authorization exists.",
                        "hard_gate": False,
                        "physics_claim_authority": False,
                    }
                ],
            }
        }

        with mock.patch.object(
            self.continue_research,
            "build_physics_progress_report",
            return_value=fake_report,
        ):
            status = self.continue_research.continuation_status()

        self.assertIn("payload_density_warning", status)
        self.assertIn("route_orbit_warning", status)
        self.assertIn("same_burden_repetition_warning", status)
        self.assertIn("gate_ready_without_gate_warning", status)
        self.assertIn("recommended_guard_action", status)
        self.assertIn("route_orbit_diagnostics", status)
        self.assertTrue(status["gate_ready_without_gate_warning"]["triggered"])
        self.assertFalse(status["route_orbit_warning"]["hard_gate"])
        self.assertFalse(status["route_orbit_warning"]["physics_claim_authority"])
        self.assertFalse(status["route_orbit_diagnostics"]["warning_hard_gates_created"])
        self.assertNotIn("route_orbit_warning", status["stop_conditions"])
        self.assertTrue(
            any(role["role_id"] == "gate-chair" for role in status["available_roles"])
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

    def test_checkpoint_post_sync_claim_obligation_uses_integrated_diff_gate(self) -> None:
        commands = self.checkpoint.post_sync_validation_commands()
        self.assertNotIn(
            [
                ".venv/bin/python",
                "scripts/project_control/validate_claim_language.py",
                "--json",
                "--changed",
            ],
            commands,
        )
        self.assertEqual(
            (SCRIPT_DIR / "checkpoint_research_transaction.py")
            .read_text(encoding="utf-8")
            .count("scripts/project_control/validate_claim_language.py"),
            1,
        )

        working_diff = [
            ".venv/bin/python",
            "scripts/research_control/validate_research_control.py",
            "--check-diff",
        ]
        staged_diff = [*working_diff, "--staged-only", "--json"]
        working_output = (
            "Research-control validation passed.\n"
            "Warning: README.md:1: claim-language warning reviewed_warning text (warn_review)\n"
        )
        staged_output = json.dumps(
            {
                "findings": [
                    {
                        "gate_id": "claim_language_changed",
                        "finding_id": "claim_language_changed:public_overclaim",
                        "severity": "hard_fail_current_public",
                    }
                ]
            }
        )
        counts = self.checkpoint.checkpoint_command_counts(
            [
                self.checkpoint.CommandResult(working_diff, 0, working_output, ""),
                self.checkpoint.CommandResult(staged_diff, 1, staged_output, ""),
            ]
        )
        self.assertEqual(counts["claim_language_standalone_working"], 0)
        self.assertEqual(counts["claim_language_standalone_staged"], 0)
        self.assertEqual(counts["research_control_diff_working"], 1)
        self.assertEqual(counts["research_control_diff_staged"], 1)
        self.assertEqual(
            [summary["finding_count"] for summary in counts["claim_language_integrated_summaries"]],
            [1, 1],
        )
        self.assertEqual(
            counts["claim_language_integrated_summaries"][1]["finding_ids"],
            ["claim_language_changed:public_overclaim"],
        )
        self.assertIn(
            [
                ".venv/bin/python",
                "scripts/research_control/validate_research_control.py",
                "--check-diff",
            ],
            commands,
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

    def test_checkpoint_git_status_preserves_both_rename_endpoints(self) -> None:
        command = ["git", "status", "--porcelain"]
        result = self.checkpoint.CommandResult(
            command,
            0,
            "R  outside/old.txt -> allowed/new.txt\n",
            "",
        )
        with mock.patch.object(self.checkpoint, "run_command", return_value=result):
            statuses = self.checkpoint.git_status_paths()

        self.assertEqual(
            statuses,
            {
                "outside/old.txt": "R ",
                "allowed/new.txt": "R ",
            },
        )

    def test_checkpoint_stages_scope_before_sync_and_validates_final_index(self) -> None:
        commands: list[list[str]] = []

        def fake_run(command: list[str]):
            commands.append(command)
            if command == ["git", "write-tree"]:
                return self.checkpoint.CommandResult(command, 0, "original-tree\n", "")
            if command == ["git", "ls-files", "-z"]:
                return self.checkpoint.CommandResult(
                    command,
                    0,
                    "tracked.txt\0research_control/tasks/RT-TEST/00_TASK.yaml\0",
                    "",
                )
            return self.checkpoint.CommandResult(command, 0, "", "")

        path = "research_control/tasks/RT-TEST/00_TASK.yaml"
        preflight = {path: "??"}
        staged = {path: "A "}
        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={"job_id": "AJ-TEST", "task_id": "RT-TEST"},
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint,
                "execution_role_ref_for_job",
                return_value="validator-engineer@0.2.0--RT-TEST",
            ),
            mock.patch.object(
                self.checkpoint,
                "git_status_paths",
                side_effect=[preflight, staged, staged, staged],
            ),
            mock.patch.object(
                self.checkpoint,
                "allowed_patterns_for_changed_paths",
                return_value=["research_control/tasks/RT-TEST/**"],
            ),
            mock.patch.object(
                self.checkpoint,
                "changed_registered_tex_requiring_pdf",
                return_value=[],
            ),
            mock.patch.object(
                self.checkpoint,
                "post_sync_validation_commands",
                return_value=[["final-index-validation"]],
            ),
            mock.patch.object(
                self.checkpoint,
                "memory_sync",
                side_effect=lambda **_kwargs: fake_run(["memory_sync()"]),
            ),
            mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run),
        ):
            result = self.checkpoint.checkpoint("AJ-TEST", no_commit=True)

        sync = ["memory_sync()"]
        add_indices = [
            index for index, command in enumerate(commands) if command[:2] == ["git", "add"]
        ]
        self.assertEqual(result["status"], "ready_to_commit")
        self.assertEqual(result["sync_passes"], 1)
        self.assertGreaterEqual(len(add_indices), 2)
        self.assertLess(add_indices[0], commands.index(sync))
        self.assertLess(commands.index(sync), add_indices[-1])
        self.assertLess(add_indices[-1], commands.index(["final-index-validation"]))
        self.assertLess(
            commands.index(["final-index-validation"]),
            commands.index(self.checkpoint.final_memory_validation_command()),
        )
        self.assertEqual(
            result["checkpoint_receipt"]["final_validator"]["git_index_tree"],
            "original-tree",
        )

    def test_checkpoint_repeats_sync_until_index_paths_stabilize(self) -> None:
        commands: list[list[str]] = []
        index_outputs = iter(
            [
                "tracked.txt\0source.txt\0",
                "tracked.txt\0source.txt\0generated/new.md\0",
                "tracked.txt\0source.txt\0generated/new.md\0",
                "tracked.txt\0source.txt\0generated/new.md\0",
            ]
        )

        def fake_run(command: list[str]):
            commands.append(command)
            if command == ["git", "write-tree"]:
                return self.checkpoint.CommandResult(command, 0, "original-tree\n", "")
            if command == ["git", "ls-files", "-z"]:
                return self.checkpoint.CommandResult(command, 0, next(index_outputs), "")
            return self.checkpoint.CommandResult(command, 0, "", "")

        source = "source.txt"
        generated = "generated/new.md"
        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={"job_id": "AJ-TEST", "task_id": "RT-TEST"},
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint,
                "execution_role_ref_for_job",
                return_value="validator-engineer@0.2.0--RT-TEST",
            ),
            mock.patch.object(
                self.checkpoint,
                "git_status_paths",
                side_effect=[
                    {source: "??"},
                    {source: "A ", generated: "??"},
                    {source: "A ", generated: "A "},
                    {source: "A ", generated: "A "},
                    {source: "A ", generated: "A "},
                ],
            ),
            mock.patch.object(
                self.checkpoint,
                "allowed_patterns_for_changed_paths",
                return_value=["source.txt", "generated/**"],
            ),
            mock.patch.object(
                self.checkpoint,
                "changed_registered_tex_requiring_pdf",
                return_value=[],
            ),
            mock.patch.object(
                self.checkpoint,
                "post_sync_validation_commands",
                return_value=[],
            ),
            mock.patch.object(
                self.checkpoint,
                "memory_sync",
                side_effect=lambda **_kwargs: fake_run(["memory_sync()"]),
            ),
            mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run),
        ):
            result = self.checkpoint.checkpoint("AJ-TEST", no_commit=True)

        self.assertEqual(result["status"], "ready_to_commit")
        self.assertEqual(result["sync_passes"], 2)
        self.assertEqual(commands.count(["memory_sync()"]), 2)
        self.assertEqual(result["command_counts"]["memory_core"], 1)
        self.assertEqual(result["command_counts"]["compatibility_bootstrap"], 0)

    def test_checkpoint_restores_original_index_on_sync_failure(self) -> None:
        commands: list[list[str]] = []

        def fake_run(command: list[str]):
            commands.append(command)
            if command == ["git", "write-tree"]:
                return self.checkpoint.CommandResult(command, 0, "original-tree\n", "")
            if command == ["git", "ls-files", "-z"]:
                return self.checkpoint.CommandResult(command, 0, "tracked.txt\0new.txt\0", "")
            return self.checkpoint.CommandResult(command, 0, "", "")

        changes = {"new.txt": "??"}
        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={"job_id": "AJ-TEST", "task_id": "RT-TEST"},
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint,
                "execution_role_ref_for_job",
                return_value="validator-engineer@0.2.0--RT-TEST",
            ),
            mock.patch.object(
                self.checkpoint,
                "git_status_paths",
                side_effect=[changes, changes],
            ),
            mock.patch.object(
                self.checkpoint,
                "allowed_patterns_for_changed_paths",
                return_value=["new.txt"],
            ),
            mock.patch.object(
                self.checkpoint,
                "memory_sync",
                return_value=self.checkpoint.CommandResult(
                    ["memory_sync()"], 1, "", "sync failed"
                ),
            ),
            mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run),
        ):
            result = self.checkpoint.checkpoint("AJ-TEST", no_commit=True)

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["reason"], "memory synchronization failed")
        self.assertIn(["git", "read-tree", "original-tree"], commands)
        self.assertNotIn(["git", "commit"], commands)

    def test_checkpoint_restores_entry_index_on_helper_exception(self) -> None:
        commands: list[list[str]] = []
        snapshots = iter(["entry-tree\n", "inner-tree\n"])

        def fake_run(command: list[str]):
            commands.append(command)
            if command == ["git", "write-tree"]:
                return self.checkpoint.CommandResult(command, 0, next(snapshots), "")
            if command == ["git", "ls-files", "-z"]:
                return self.checkpoint.CommandResult(command, 1, "", "index read failed")
            return self.checkpoint.CommandResult(command, 0, "", "")

        changes = {"new.txt": "??"}
        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={"job_id": "AJ-TEST", "task_id": "RT-TEST"},
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint,
                "execution_role_ref_for_job",
                return_value="validator-engineer@0.2.0--RT-TEST",
            ),
            mock.patch.object(
                self.checkpoint,
                "git_status_paths",
                return_value=changes,
            ),
            mock.patch.object(
                self.checkpoint,
                "allowed_patterns_for_changed_paths",
                return_value=["new.txt"],
            ),
            mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run),
        ):
            with self.assertRaisesRegex(RuntimeError, "index read failed"):
                self.checkpoint.checkpoint("AJ-TEST", no_commit=True)

        self.assertIn(["git", "read-tree", "entry-tree"], commands)

    def test_checkpoint_retries_entry_snapshot_when_no_action_restore_fails(self) -> None:
        commands: list[list[str]] = []
        snapshots = iter(["entry-tree\n", "inner-tree\n"])
        restore_results = iter([1, 0])

        def fake_run(command: list[str]):
            commands.append(command)
            if command == ["git", "write-tree"]:
                return self.checkpoint.CommandResult(command, 0, next(snapshots), "")
            if command == ["git", "ls-files", "-z"]:
                return self.checkpoint.CommandResult(command, 0, "tracked.txt\0new.txt\0", "")
            if command[:2] == ["git", "read-tree"]:
                returncode = next(restore_results)
                return self.checkpoint.CommandResult(
                    command,
                    returncode,
                    "",
                    "inner restore failed" if returncode else "",
                )
            return self.checkpoint.CommandResult(command, 0, "", "")

        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={"job_id": "AJ-TEST", "task_id": "RT-TEST"},
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint,
                "execution_role_ref_for_job",
                return_value="validator-engineer@0.2.0--RT-TEST",
            ),
            mock.patch.object(
                self.checkpoint,
                "git_status_paths",
                side_effect=[{"new.txt": "??"}, {}, {}],
            ),
            mock.patch.object(
                self.checkpoint,
                "allowed_patterns_for_changed_paths",
                return_value=["new.txt"],
            ),
            mock.patch.object(
                self.checkpoint,
                "changed_registered_tex_requiring_pdf",
                return_value=[],
            ),
            mock.patch.object(
                self.checkpoint,
                "post_sync_validation_commands",
                return_value=[],
            ),
            mock.patch.object(
                self.checkpoint,
                "memory_sync",
                side_effect=lambda **_kwargs: fake_run(["memory_sync()"]),
            ),
            mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run),
        ):
            with self.assertRaisesRegex(RuntimeError, "inner restore failed"):
                self.checkpoint.checkpoint("AJ-TEST", no_commit=True)

        self.assertEqual(
            [command for command in commands if command[:2] == ["git", "read-tree"]],
            [
                ["git", "read-tree", "inner-tree"],
                ["git", "read-tree", "entry-tree"],
            ],
        )

    def test_checkpoint_blocks_unstaged_residue_after_final_validation(self) -> None:
        commands: list[list[str]] = []

        def fake_run(command: list[str]):
            commands.append(command)
            if command == ["git", "write-tree"]:
                return self.checkpoint.CommandResult(command, 0, "original-tree\n", "")
            if command == ["git", "ls-files", "-z"]:
                return self.checkpoint.CommandResult(command, 0, "tracked.txt\0changed.txt\0", "")
            return self.checkpoint.CommandResult(command, 0, "", "")

        path = "changed.txt"
        with (
            mock.patch.object(
                self.checkpoint,
                "select_job",
                return_value={"job_id": "AJ-TEST", "task_id": "RT-TEST"},
            ),
            mock.patch.object(self.checkpoint, "load_job_contract", return_value={}),
            mock.patch.object(
                self.checkpoint,
                "execution_role_ref_for_job",
                return_value="validator-engineer@0.2.0--RT-TEST",
            ),
            mock.patch.object(
                self.checkpoint,
                "git_status_paths",
                side_effect=[
                    {path: " M"},
                    {path: "M "},
                    {path: "M "},
                    {path: "MM"},
                ],
            ),
            mock.patch.object(
                self.checkpoint,
                "allowed_patterns_for_changed_paths",
                return_value=[path],
            ),
            mock.patch.object(
                self.checkpoint,
                "changed_registered_tex_requiring_pdf",
                return_value=[],
            ),
            mock.patch.object(
                self.checkpoint,
                "post_sync_validation_commands",
                return_value=[],
            ),
            mock.patch.object(
                self.checkpoint,
                "memory_sync",
                side_effect=lambda **_kwargs: fake_run(["memory_sync()"]),
            ),
            mock.patch.object(self.checkpoint, "run_command", side_effect=fake_run),
        ):
            result = self.checkpoint.checkpoint("AJ-TEST", no_commit=True)

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(
            result["reason"],
            "unstaged transaction changes remain after final validation",
        )
        self.assertEqual(result["validation_errors"], [path])
        self.assertIn(["git", "read-tree", "original-tree"], commands)

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

    def validation_schema_split_completion(self) -> dict:
        return {
            "completed_at": "2026-07-01T23:20:00Z",
            "validation_status": "PASS",
            "validation_layers": {
                "pre_execution": {
                    "status": "PASS",
                    "evidence": ["memory preflight and targeted query passed"],
                },
                "completion_internal": {
                    "status": "PASS",
                    "evidence": ["completion record is internally consistent"],
                },
                "post_write": {
                    "status": "PASS",
                    "evidence": ["post-write validators passed"],
                },
                "post_checkpoint": {
                    "status": "PENDING",
                    "evidence": ["checkpoint will run after final generated-state synchronization"],
                },
                "renderer": {
                    "status": "PASS",
                    "evidence": ["renderer displays split layer names"],
                },
                "memory_bootstrap": {
                    "status": "PASS",
                    "evidence": ["memory bootstrap completed"],
                },
                "claim_language_linter": {
                    "status": "PASS",
                    "evidence": ["claim-language linter passed"],
                },
            },
            "authorization_layers": {
                "protected_scoped_gate_review_authorized": True,
                "protected_scoped_gate_review_scope": "validation schema split only",
                "protected_scoped_gate_review_authority_source_path": "research_control/tasks/RT-TEST/DDR.md",
                "downstream_physics_promotion_authorized": False,
                "benchmark_promotion_authorized": False,
                "completed_derivation_authorized": False,
            },
            "physics_progress_status": {
                "status": "project_control_only",
                "physics_promotion_authorized": False,
            },
        }

    def validation_schema_split_job_row(self) -> dict[str, str]:
        return {
            "job_id": "AJ-TEST",
            "created_at": "2026-07-01T23:20:00Z",
            "started_at": "2026-07-01T23:20:00Z",
            "completed_at": "2026-07-01T23:20:00Z",
        }

    def test_validation_schema_split_accepts_layered_completion(self) -> None:
        report = self.validator.ValidationReport()
        completion = self.validation_schema_split_completion()
        row = self.validation_schema_split_job_row()

        self.validator.validate_validation_layers(report, row, completion, "fixture.yaml")
        self.validator.validate_authorization_layers(report, row, completion, "fixture.yaml")

        self.assertEqual(report.errors, [])

    def test_validation_schema_split_rejects_unexplained_pending_layer(self) -> None:
        report = self.validator.ValidationReport()
        completion = self.validation_schema_split_completion()
        completion["validation_layers"]["post_checkpoint"]["evidence"] = []
        row = self.validation_schema_split_job_row()

        self.validator.validate_validation_layers(report, row, completion, "fixture.yaml")

        self.assertTrue(
            any("post_checkpoint.evidence must explain the layer status" in error for error in report.errors)
        )

    def test_validation_schema_split_rejects_ambiguous_legacy_promotion(self) -> None:
        report = self.validator.ValidationReport()
        completion = self.validation_schema_split_completion()
        completion["physics_progress_status"]["physics_promotion_authorized"] = True
        row = self.validation_schema_split_job_row()

        self.validator.validate_authorization_layers(report, row, completion, "fixture.yaml")

        self.assertTrue(
            any(
                "physics_progress_status.physics_promotion_authorized must match" in error
                for error in report.errors
            )
        )

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

    def distance_delta_yaml(
        self,
        *,
        effect: str = "no_distance_delta",
        downstream_unlocked: str = "none",
    ) -> str:
        return "\n".join(
            [
                "distance_to_gr_delta:",
                f'  effect: "{effect}"',
                "  changed: false",
                '  burden_id: "m_src"',
                '  milestone: "source_manifold_m_src"',
                '  old_status: "not discharged"',
                '  new_status: "not discharged"',
                "  ledger_row_updated: false",
                '  ledger_path: "registries/DISTANCE_TO_GR_LEDGER.csv"',
                "  downstream_unlocked:",
                f'    - "{downstream_unlocked}"',
                "  downstream_still_blocked:",
                '    - "g_eff"',
                '    - "matter_coupling"',
                '    - "einstein_equations"',
                '    - "benchmark_promotion"',
                '  explanation: "Synthetic P9-T01 fixture records the actual Distance-to-GR effect."',
            ]
        )

    def validate_p9_distance_delta_fixture(self, completion_extra: str):
        completion = self.strict_yaml.loads(
            "\n".join(
                [
                    'completed_at: "2026-07-03T11:24:00Z"',
                    'status: "completed"',
                    *completion_extra.splitlines(),
                    "",
                ]
            )
        )
        report = self.validator.ValidationReport()
        row = {
            "job_id": "AJ-TEST",
            "task_id": "RT-TEST",
            "decision_id": "DDR-TEST",
            "role_id": "smuggling-auditor",
            "role_version": "0.2.0",
            "job_path": "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
            "completion_path": "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml",
            "status": "completed",
            "created_at": "2026-07-03T11:24:00Z",
            "started_at": "2026-07-03T11:24:00Z",
            "completed_at": "2026-07-03T11:24:00Z",
        }
        path = REPO_ROOT / "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml"
        self.validator.validate_loop_control_completion(report, row, {}, completion, path)
        return report

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

    def distance_to_gr_ledger_fixture_report(self, mutator):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            registries = root / "registries"
            registries.mkdir(parents=True)
            source_path = REPO_ROOT / "registries" / "DISTANCE_TO_GR_LEDGER.csv"
            with source_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            mutator(rows)
            target_path = registries / "DISTANCE_TO_GR_LEDGER.csv"
            with target_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=self.validator.DISTANCE_TO_GR_LEDGER_COLUMNS,
                )
                writer.writeheader()
                writer.writerows(rows)

            report = self.validator.ValidationReport()
            with mock.patch.object(self.validator, "REGISTRY_DIR", registries):
                self.validator.validate_distance_to_gr_ledger(report)
        return report

    def test_distance_to_gr_ledger_requires_layered_overread_guards(self) -> None:
        def remove_stress_energy_guard(rows):
            for row in rows:
                if row["burden_id"] == "matter_coupling":
                    tokens = row["overread_guard"].split(";")
                    tokens.remove("no_stress_energy_tensor")
                    row["overread_guard"] = ";".join(tokens)
                    break

        report = self.distance_to_gr_ledger_fixture_report(remove_stress_energy_guard)
        joined = "\n".join(report.errors)
        self.assertIn("matter_coupling missing overread_guard tokens", joined)
        self.assertIn("no_stress_energy_tensor", joined)

    def test_distance_to_gr_ledger_rejects_matter_coupling_physical_overread(self) -> None:
        def overread_matter_coupling(rows):
            for row in rows:
                if row["burden_id"] == "matter_coupling":
                    row["physical_status"] = "benchmark_compatible_interpretive_boundary_only"
                    break

        report = self.distance_to_gr_ledger_fixture_report(overread_matter_coupling)
        joined = "\n".join(report.errors)
        self.assertIn("matter_coupling physical_status must be", joined)
        self.assertIn("explicit not/no/blocked wording", joined)

    def test_distance_to_gr_ledger_rejects_geff_unscoped_or_benchmark_overread(self) -> None:
        def overread_geff(rows):
            for row in rows:
                if row["burden_id"] == "g_eff":
                    row["physical_status"] = "benchmark_compatible_interpretive_boundary_only"
                    row["overread_guard"] = row["overread_guard"].replace(
                        "no_unscoped_geff_adoption;", ""
                    )
                    break

        report = self.distance_to_gr_ledger_fixture_report(overread_geff)
        joined = "\n".join(report.errors)
        self.assertIn("g_eff physical_status must be", joined)
        self.assertIn("no_unscoped_geff_adoption", joined)

    def test_distance_to_gr_ledger_rejects_accepted_without_scoped_layers(self) -> None:
        def remove_scoped_promotion(rows):
            for row in rows:
                if row["burden_id"] == "g_eff":
                    row["promotion_status"] = "none"
                    break

        report = self.distance_to_gr_ledger_fixture_report(remove_scoped_promotion)
        joined = "\n".join(report.errors)
        self.assertIn("g_eff promotion_status must be scoped_source_object_only", joined)
        self.assertIn("accepted current_status must use scoped promotion_status", joined)

    def test_distance_to_gr_ledger_rejects_frozen_toy_global_freeze_overread(self) -> None:
        def remove_future_extension_guard(rows):
            for row in rows:
                if row["burden_id"] == "finite_toy_metric_response":
                    tokens = row["overread_guard"].split(";")
                    tokens.remove("no_future_source_extension_impossibility")
                    row["overread_guard"] = ";".join(tokens)
                    break

        report = self.distance_to_gr_ledger_fixture_report(remove_future_extension_guard)
        joined = "\n".join(report.errors)
        self.assertIn("finite_toy_metric_response missing overread_guard tokens", joined)
        self.assertIn("no_future_source_extension_impossibility", joined)

    def test_distance_to_gr_ledger_rejects_generated_snapshot_as_layer_authority(self) -> None:
        def cite_current_frontier(rows):
            for row in rows:
                if row["burden_id"] == "g_eff":
                    row["last_evidence_path"] = "research_control/current_frontier.md"
                    break

        report = self.distance_to_gr_ledger_fixture_report(cite_current_frontier)
        joined = "\n".join(report.errors)
        self.assertIn("generated snapshot or noncanonical retrieval path", joined)
        self.assertIn("g_eff", joined)

    def frontier_inventory_fixture_report(
        self,
        inventory_text: str,
        *,
        create_source_path: str | None = "AGENTS.md",
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            control = root / "research_control"
            registries = root / "registries"
            inventory_path = control / "design" / "frontier_theorem_inventory.md"
            inventory_path.parent.mkdir(parents=True)
            registries.mkdir(parents=True)
            inventory_path.write_text(inventory_text, encoding="utf-8")
            if create_source_path:
                source_path = root / create_source_path
                source_path.parent.mkdir(parents=True, exist_ok=True)
                source_path.write_text("fixture source\n", encoding="utf-8")
            registry_path = registries / "MARKDOWN_SOURCE_REGISTRY.csv"
            with registry_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "object_id",
                        "path",
                        "format",
                        "role",
                        "authority_status",
                        "audience",
                        "source_hash",
                        "related_source",
                        "generated_from",
                        "generated_outputs",
                        "owner_skill",
                        "validation_status",
                        "last_validated_at",
                        "notes",
                        "github_facing",
                        "agent_documentation",
                        "contains_mermaid",
                        "contains_math",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "object_id": self.validator.FRONTIER_INVENTORY_OBJECT_ID,
                        "path": self.validator.FRONTIER_INVENTORY_PATH,
                        "format": "markdown",
                        "role": "control_inventory",
                        "authority_status": "project_control",
                        "audience": "agents",
                        "source_hash": hashlib.sha256(
                            inventory_text.encode("utf-8")
                        ).hexdigest(),
                        "related_source": "",
                        "generated_from": "",
                        "generated_outputs": "",
                        "owner_skill": "project-memory-system",
                        "validation_status": "PASS",
                        "last_validated_at": "2026-06-29T00:00:00Z",
                        "notes": "fixture",
                        "github_facing": "false",
                        "agent_documentation": "true",
                        "contains_mermaid": "false",
                        "contains_math": "false",
                    }
                )

            report = self.validator.ValidationReport()
            with (
                mock.patch.object(self.validator, "REPO_ROOT", root),
                mock.patch.object(self.validator, "CONTROL_DIR", control),
                mock.patch.object(self.validator, "REGISTRY_DIR", registries),
            ):
                self.validator.validate_frontier_theorem_inventory(report)
        return report

    def frontier_inventory_fixture_text(
        self,
        *,
        source_path: str = "AGENTS.md",
        physical_non_conclusions: str = "  - No benchmark promotion.\n  - No completed derivation.",
    ) -> str:
        return "\n".join(
            [
                "<!-- authority: control -->",
                "",
                "# Frontier Theorem Inventory",
                "",
                "## Inventory Items",
                "",
                "### Item 1: fixture_item",
                "",
                "- `frontier_item_id`: `fixture_item`",
                "- `frontier_item_class`: `definition;missing_theorem`",
                "- `object_or_claim_name`: Fixture source-control item.",
                "- `status_layer_summary`:",
                '  - `control_status`: `draft_control_object_exists`',
                '  - `mathematical_status`: `definition_only_or_draft_object`',
                '  - `physical_status`: `no_physical_interpretation_authorized`',
                '  - `promotion_status`: `draft_control_only`',
                '  - `overread_guard`: `no_benchmark_promotion;no_completed_derivation`',
                f"- `source_artifact_path`: `{source_path}`",
                "- `source_authority_type`: `registered_markdown_control`",
                "- `assumptions`:",
                "  - Fixture assumption.",
                "- `definitions_used`: fixture primitive.",
                "- `statement_or_decision`: Fixture records a missing theorem only.",
                "- `mathematical_conclusion`: none_supplied.",
                "- `physical_non_conclusions`:",
                physical_non_conclusions,
                "- `allowed_reuse`:",
                "  - Fixture reuse.",
                "- `blocked_reuse`:",
                "  - Do not promote fixture.",
                "- `dependency_items`: `none`",
                "- `missing_theorem_or_primitive`: Fixture theorem.",
                "- `candidate_next_task`: none.",
                "- `overread_guard`: `no_benchmark_promotion;no_completed_derivation`",
                "- `external_review_notes`: Fixture note.",
                "",
            ]
        )

    def test_frontier_inventory_validator_accepts_live_inventory(self) -> None:
        report = self.validator.ValidationReport()
        self.validator.validate_frontier_theorem_inventory(report)
        self.assertEqual(report.errors, [])

    def test_frontier_inventory_validator_rejects_missing_non_conclusions(self) -> None:
        report = self.frontier_inventory_fixture_report(
            self.frontier_inventory_fixture_text(physical_non_conclusions="")
        )
        joined = "\n".join(report.errors)
        self.assertIn("physical_non_conclusions", joined)

    def test_frontier_inventory_validator_rejects_bad_source_paths(self) -> None:
        report = self.frontier_inventory_fixture_report(
            self.frontier_inventory_fixture_text(
                source_path="research_control/missing_source.md"
            ),
            create_source_path=None,
        )
        self.assertIn("source_artifact_path does not exist", "\n".join(report.errors))

        generated_report = self.frontier_inventory_fixture_report(
            self.frontier_inventory_fixture_text(source_path="wiki/generated.md"),
            create_source_path=None,
        )
        self.assertIn(
            "generated derivative source path requires paired canonical source path",
            "\n".join(generated_report.errors),
        )

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

    def test_p9_future_physics_completion_requires_distance_delta_effect(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
            ]
        )
        report = self.validate_p9_distance_delta_fixture(completion_extra)
        self.assertTrue(
            any("missing distance_to_gr_delta.effect" in error for error in report.errors)
        )

    def test_p9_future_physics_completion_rejects_unknown_distance_delta_effect(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
                self.distance_delta_yaml(effect="vague_progress"),
            ]
        )
        report = self.validate_p9_distance_delta_fixture(completion_extra)
        self.assertTrue(
            any("distance_to_gr_delta.effect is not allowed: vague_progress" in error for error in report.errors)
        )

    def test_p9_future_physics_completion_accepts_allowed_distance_delta_effect(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
                self.distance_delta_yaml(effect="scoped_source_extension_object"),
            ]
        )
        report = self.validate_p9_distance_delta_fixture(completion_extra)
        self.assertEqual(report.errors, [])

    def test_p9_distance_delta_effect_does_not_authorize_downstream_unlock(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
                self.distance_delta_yaml(
                    effect="milestone_discharge",
                    downstream_unlocked="einstein_equations",
                ),
            ]
        )
        report = self.validate_p9_distance_delta_fixture(completion_extra)
        self.assertTrue(
            any("distance_to_gr_delta.effect does not authorize downstream_unlocked" in error for error in report.errors)
        )

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
        self.assertTrue(
            any("mathematical decisiveness: missing mathematical_payload_manifest" in error for error in report.errors)
        )
        self.assertTrue(
            any("mathematical decisiveness: missing forbidden_conclusion_summary" in error for error in report.errors)
        )

    def test_mathematical_decisiveness_rejects_incomplete_payload_manifest_item(self) -> None:
        replacements = {
            "payload_id": ('  - payload_id: "PAYLOAD-001"', '  - payload_id: ""'),
            "payload_type": ('    payload_type: "packet_selection"', '    payload_type: ""'),
            "object_name": (
                '    object_name: "source-cover selector fixture"',
                '    object_name: ""',
            ),
            "claim_status": ('    claim_status: "draft/control"', '    claim_status: ""'),
            "source_path": (
                '    source_path: "research_control/tasks/RT-TEST/artifacts/fixture.yaml"',
                '    source_path: ""',
            ),
            "burden_effect": ('    burden_effect: "selects_next"', '    burden_effect: ""'),
            "summary": (
                '    summary: "Names a packet without adoption."',
                '    summary: ""',
            ),
        }

        for field_name, (original, replacement) in replacements.items():
            with self.subTest(field_name=field_name):
                completion_extra = "\n".join(
                    [
                        self.roadmap_distance_matrix_yaml(),
                        self.minimal_payload_yaml(),
                        self.decisiveness_completion_yaml().replace(original, replacement),
                    ]
                )
                report = self.validate_completion_fixture(
                    role_id="smuggling-auditor",
                    job_extra=self.decisiveness_opt_in_job_yaml(),
                    completion_extra=completion_extra,
                    timestamp="2026-06-18T15:32:59Z",
                )
                self.assertTrue(
                    any(
                        f"mathematical_payload_manifest[1].{field_name} is empty" in error
                        for error in report.errors
                    )
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

    def test_mathematical_decisiveness_candidate_constructor_requires_result(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
                self.decisiveness_completion_yaml(),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="candidate-constructor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertTrue(
            any("Candidate Constructor completion requires candidate_constructor_result" in error for error in report.errors)
        )

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

    def test_mathematical_decisiveness_repeated_burden_requires_freeze_and_route_cycle(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml(),
                self.decisiveness_completion_yaml(),
                "loop_risk_decision:",
                '  category: "repeated_unmet_burdens_no_new_payload"',
                '  next_route: "theoretical_decision_role_selection"',
                '  rationale: "The same burden recurred without new mathematical payload."',
                "  repeated_burdens:",
                '    - "M_src"',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="smuggling-auditor",
            job_extra=self.decisiveness_opt_in_job_yaml(),
            completion_extra=completion_extra,
            timestamp="2026-06-18T15:32:59Z",
        )
        self.assertTrue(
            any("requires route_cycle_control" in error for error in report.errors)
        )
        self.assertTrue(
            any("requires freeze_criteria_status" in error for error in report.errors)
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

    def source_extension_selector_yaml(self) -> str:
        return "\n".join(
            [
                "theoretical_decision_output:",
                '  selected_next_packet_type: "source_extension_candidate"',
                '  decision_basis: "Synthetic source-extension route selection."',
                '  theoretical_method: "Classify the source-extension output before any downstream use."',
                '  preserves_claim_blocks: "No source-law adoption matter coupling benchmark promotion or completed derivation is authorized."',
                "  requires_human_gate: false",
                '  human_gate_reason: ""',
                '  source_extension_category: "source_extension_candidate"',
                '  source_extension_import_classification: "conservative definitional extension candidate, not adopted ontology"',
            ]
        )

    def test_source_extension_completion_requires_classification_receipt(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("source_extension_classification"),
                self.source_extension_selector_yaml(),
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-07-03T06:45:01Z",
        )
        self.assertTrue(
            any("missing source_extension_classification receipt" in error for error in report.errors)
        )

    def test_source_extension_classification_receipt_requires_required_fields(self) -> None:
        completion_extra = "\n".join(
            [
                self.roadmap_distance_matrix_yaml(),
                self.minimal_payload_yaml("source_extension_classification"),
                self.source_extension_selector_yaml(),
                "source_extension_classification:",
                '  checklist_id: "source_extension_classification_checklist_v1"',
                "  records:",
                '    - item_id: "SyntheticSourceExtension"',
            ]
        )
        report = self.validate_completion_fixture(
            role_id="theoretical-continuation-selector",
            completion_extra=completion_extra,
            timestamp="2026-07-03T06:45:01Z",
        )
        joined = "\n".join(report.errors)
        self.assertIn(".classification is not allowed", joined)
        self.assertIn("requires claim_boundary", joined)
        self.assertIn("requires blocked_overreads", joined)
        self.assertIn(".relation_to_current_ontology is not allowed", joined)
        self.assertIn(".protected_authority_required is required", joined)
        self.assertIn(".downstream_promotion_authorized is required", joined)

    def test_source_extension_classification_receipt_accepts_valid_record(self) -> None:
        report = self.validator.ValidationReport()
        job_row = {
            "role_id": "theoretical-continuation-selector",
            "created_at": "2026-07-03T06:45:01Z",
            "started_at": "2026-07-03T06:45:01Z",
            "completed_at": "2026-07-03T06:45:01Z",
        }
        job_contract = {
            "route_label": "source_extension_candidate",
        }
        completion = {
            "completed_at": "2026-07-03T06:45:01Z",
            "source_extension_classification": {
                "checklist_id": "source_extension_classification_checklist_v1",
                "records": [
                    {
                        "item_id": "SyntheticSourceExtension",
                        "item_source_path": "research_control/tasks/RT-TEST/artifacts/synthetic.md",
                        "classification": "conservative_definitional_extension",
                        "claim_boundary_id": "CB-TEST-SOURCE-EXTENSION",
                        "blocked_overreads": [
                            "source-law adoption",
                            "matter-coupling derivation",
                        ],
                        "relation_to_current_ontology": "conservative",
                        "protected_authority_required": False,
                        "downstream_promotion_authorized": False,
                        "physics_promotion_authorized": False,
                    }
                ],
            },
        }
        self.validator.validate_source_extension_classification_receipt(
            report,
            job_row,
            job_contract,
            completion,
            "fixture.yaml",
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
