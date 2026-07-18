from __future__ import annotations

from copy import deepcopy
import io
import json
from pathlib import Path
from unittest import mock
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"

from scripts.project_control.classify_project_changes import classify_paths
from scripts.validation import cli
from scripts.validation.plan import (
    PlannerError,
    build_plan,
    load_manifest,
    render_explanation,
)


class ValidationPlannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(MANIFEST_PATH)

    def plan_for(
        self,
        paths: list[str],
        *,
        profile: str = "affected",
        scopes: tuple[str, ...] = (),
        obligations: tuple[str, ...] = (),
    ):
        return build_plan(
            self.manifest,
            classify_paths(paths),
            profile=profile,
            scopes=scopes,
            role_obligations=obligations,
        )

    def test_explicit_path_order_does_not_change_canonical_plan(self) -> None:
        left = self.plan_for(["scripts/validation/plan.py", "README.md"])
        right = self.plan_for(["README.md", "scripts/validation/plan.py"])
        self.assertEqual(left.canonical_json(), right.canonical_json())

    def test_planner_executes_no_subprocesses(self) -> None:
        classification = classify_paths(["scripts/validation/plan.py"])
        with mock.patch("subprocess.run", side_effect=AssertionError("command executed")):
            plan = build_plan(self.manifest, classification, profile="affected")
        self.assertFalse(plan.to_dict()["planner_executes_commands"])

    def test_unknown_governed_path_falls_back_to_full(self) -> None:
        plan = self.plan_for(["future_governed_surface/example.rule"], profile="fast")
        self.assertEqual(plan.effective_profile, "full")
        self.assertEqual(plan.unknown_paths, ("future_governed_surface/example.rule",))
        self.assertIn("profile_full_research_control", plan.selected_gate_ids)
        self.assertIn("unknown_path_full_fallback", {entry["status"] for entry in plan.entries})

    def test_generated_only_edit_is_blocked_and_uses_full_fallback(self) -> None:
        plan = self.plan_for(["wiki/markdown/unregistered.md"], profile="affected")
        self.assertEqual(plan.status, "BLOCKED_CONFIGURATION")
        self.assertEqual(plan.effective_profile, "full")
        self.assertEqual(plan.blocked_paths, ("wiki/markdown/unregistered.md",))
        self.assertIn("blocked_path", {entry["status"] for entry in plan.entries})

    def test_mixed_documentation_and_validator_change_is_deduplicated(self) -> None:
        plan = self.plan_for(["README.md", "scripts/validation/plan.py"])
        self.assertEqual(len(plan.selected_gate_ids), len(set(plan.selected_gate_ids)))
        self.assertIn("documentation_impact", plan.selected_gate_ids)
        self.assertIn("research_control_diff", plan.selected_gate_ids)

    def test_registered_pdf_required_tex_selects_targeted_build(self) -> None:
        plan = self.plan_for(["legacy_ontology/tex/aether_flow_consistency.tex"])
        self.assertIn("targeted_pdf_build", plan.selected_gate_ids)

    def test_registered_mermaid_selects_mermaid_gate(self) -> None:
        plan = self.plan_for(["README.md"])
        self.assertIn("mermaid_sources", plan.selected_gate_ids)

    def test_dependency_graph_input_selects_graph_freshness(self) -> None:
        plan = self.plan_for(["registries/RESEARCH_TASK_REGISTRY.csv"])
        self.assertIn("dependency_graph_freshness", plan.selected_gate_ids)

    def test_dependency_graph_implementation_paths_select_graph_freshness(self) -> None:
        paths = [
            "scripts/research_control/render_dependency_graph.py",
            "scripts/research_control/dependency_graph_model.py",
        ]
        for path in paths:
            with self.subTest(path=path):
                plan = self.plan_for([path])
                self.assertEqual(plan.effective_profile, "affected")
                self.assertEqual(plan.unknown_paths, ())
                self.assertIn("dependency_graph_freshness", plan.selected_gate_ids)

        joint_plan = self.plan_for(paths)
        self.assertEqual(joint_plan.effective_profile, "affected")
        self.assertEqual(joint_plan.unknown_paths, ())
        self.assertIn("dependency_graph_freshness", joint_plan.selected_gate_ids)

    def test_task_input_selects_task_index_freshness(self) -> None:
        plan = self.plan_for(["research_control/tasks/RT-TEST/00_TASK.yaml"])
        self.assertIn("task_index_freshness", plan.selected_gate_ids)

    def test_traceability_input_selects_repository_test_shard(self) -> None:
        plan = self.plan_for(["registries/FORMALIZATION_TRACEABILITY_REGISTRY.csv"])
        self.assertIn("test_shard_repository", plan.selected_gate_ids)

    def test_scientific_checker_selects_repository_test_shard(self) -> None:
        plan = self.plan_for(
            ["scripts/research_control/support_formalization/example_checker.py"]
        )
        self.assertIn("test_shard_repository", plan.selected_gate_ids)

    def test_local_retrieval_requires_explicit_scope(self) -> None:
        without_scope = self.plan_for([".local/example.db"], profile="doctor")
        with_scope = self.plan_for(
            [".local/example.db"], profile="doctor", scopes=("local_retrieval",)
        )
        self.assertNotIn("local_retrieval_sync", without_scope.selected_gate_ids)
        self.assertIn("local_retrieval_sync", with_scope.selected_gate_ids)
        self.assertLess(
            with_scope.ordered_gate_ids.index("local_retrieval_sync"),
            with_scope.ordered_gate_ids.index("local_retrieval_lint"),
        )

    def test_role_obligation_selects_gate_and_prerequisites(self) -> None:
        plan = self.plan_for(
            [], profile="fast", obligations=("project_improvement_signals",)
        )
        self.assertIn("project_improvement_signals", plan.selected_gate_ids)
        self.assertIn("classify_changes", plan.selected_gate_ids)
        self.assertLess(
            plan.ordered_gate_ids.index("classify_changes"),
            plan.ordered_gate_ids.index("project_improvement_signals"),
        )

    def test_independent_mutator_precedes_read_only_gate(self) -> None:
        plan = self.plan_for(["scripts/validation/plan.py"], profile="affected")
        self.assertLess(
            plan.ordered_gate_ids.index("memory_sync"),
            plan.ordered_gate_ids.index("memory_core"),
        )

    def test_every_selected_gate_has_a_reason(self) -> None:
        plan = self.plan_for(["scripts/validation/plan.py"])
        entries = {entry["gate_id"]: entry for entry in plan.entries if entry["gate_id"]}
        for gate_id in plan.selected_gate_ids:
            self.assertTrue(entries[gate_id]["reasons"])

    def test_unselected_gates_are_explicitly_skipped(self) -> None:
        plan = self.plan_for([], profile="fast")
        entries = {entry["gate_id"]: entry for entry in plan.entries if entry["gate_id"]}
        self.assertEqual(entries["memory_status_diagnostic"]["status"], "skipped_not_applicable")
        self.assertIn("memory_status_diagnostic", plan.skipped_gate_ids)

    def test_current_shadow_manifest_activates_no_supersedence(self) -> None:
        plan = self.plan_for(["research_control/tasks/RT-TEST/00_TASK.yaml"])
        self.assertEqual(plan.superseded_gate_ids, ())
        self.assertEqual(plan.execution_authority, "legacy")

    def test_planner_authoritative_manifest_authorizes_executor_only(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["migration_epoch"] = "planner_authoritative"
        manifest["execution_authority"] = "manifest_planner"
        classification = classify_paths(["scripts/validation/plan.py"])
        with mock.patch("subprocess.run", side_effect=AssertionError("command executed")):
            plan = build_plan(manifest, classification, profile="affected")
        self.assertEqual(plan.execution_authority, "manifest_planner")
        self.assertTrue(plan.to_dict()["planner_executes_commands"])
        self.assertFalse(plan.to_dict()["authority"]["legacy_result_authoritative"])

    def test_invalid_manifest_planner_epoch_pair_fails_closed(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["execution_authority"] = "manifest_planner"
        with self.assertRaisesRegex(PlannerError, "requires planner_authoritative"):
            build_plan(manifest, classify_paths([]), profile="fast")

        manifest = deepcopy(self.manifest)
        manifest["migration_epoch"] = "legacy_retired"
        with self.assertRaisesRegex(PlannerError, "requires manifest_planner"):
            build_plan(manifest, classify_paths([]), profile="fast")

    def test_cycle_fails_closed(self) -> None:
        manifest = deepcopy(self.manifest)
        first = manifest["gates"][0]
        second = manifest["gates"][1]
        first["prerequisites"] = [second["gate_id"]]
        second["prerequisites"] = [first["gate_id"]]
        with self.assertRaisesRegex(PlannerError, "cycle"):
            build_plan(manifest, classify_paths([]), profile="affected")

    def test_unknown_prerequisite_fails_closed(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["gates"][0]["prerequisites"] = ["missing_gate"]
        with self.assertRaisesRegex(PlannerError, "unknown prerequisites"):
            build_plan(manifest, classify_paths([]), profile="affected")

    def test_unknown_manifest_field_fails_closed(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["unregistered_default"] = True
        with self.assertRaisesRegex(PlannerError, "fields differ"):
            build_plan(manifest, classify_paths([]), profile="affected")

    def test_invalid_authority_fails_closed(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["authority"]["physics_claim_authority"] = True
        with self.assertRaisesRegex(PlannerError, "non-promotion boundary"):
            build_plan(manifest, classify_paths([]), profile="affected")

    def test_active_supersedence_fails_without_evidence_contract(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["gates"][0]["supersedes"] = [
            {
                "gate_id": manifest["gates"][1]["gate_id"],
                "predicate_id": "future_identity_predicate",
                "status": "active",
            }
        ]
        with self.assertRaisesRegex(PlannerError, "evidence contract"):
            build_plan(manifest, classify_paths([]), profile="affected")

    def test_duplicate_manifest_key_fails_closed(self) -> None:
        with mock.patch.object(Path, "read_text", return_value='{"schema_id":1,"schema_id":2}'):
            with self.assertRaisesRegex(PlannerError, "duplicate manifest key"):
                load_manifest(Path("unused"))

    def test_explanation_traces_reasons_and_obligations(self) -> None:
        plan = self.plan_for(
            ["research_control/tasks/RT-TEST/00_TASK.yaml"],
            obligations=("documentation_impact",),
        )
        explanation = render_explanation(plan)
        self.assertIn("selected documentation_impact", explanation)
        self.assertIn("role_obligation:documentation_impact", explanation)
        self.assertIn("obligations=documentation_impact", explanation)

    def test_cli_json_is_machine_readable_and_deterministic(self) -> None:
        arguments = [
            "plan",
            "--profile",
            "affected",
            "--paths",
            "scripts/validation/plan.py",
            "--json",
        ]
        outputs: list[str] = []
        for _ in range(2):
            stream = io.StringIO()
            with mock.patch("sys.stdout", stream):
                self.assertEqual(cli.main(arguments), 0)
            outputs.append(stream.getvalue())
        self.assertEqual(outputs[0], outputs[1])
        payload = json.loads(outputs[0])
        self.assertEqual(payload["schema_id"], "validation_plan_v1")
        self.assertFalse(payload["planner_executes_commands"])

    def test_cli_explain_is_concise_text(self) -> None:
        stream = io.StringIO()
        with mock.patch("sys.stdout", stream):
            code = cli.main(
                [
                    "plan",
                    "--profile",
                    "fast",
                    "--paths",
                    "scripts/validation/plan.py",
                    "--explain",
                ]
            )
        self.assertEqual(code, 0)
        self.assertTrue(stream.getvalue().startswith("validation plan requested=fast"))


if __name__ == "__main__":
    unittest.main()
