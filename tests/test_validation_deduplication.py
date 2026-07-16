from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import io
import json
from pathlib import Path
from unittest import mock
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
CONTRACTS_PATH = ROOT / "research_control/design/validation_supersedence_contracts_v1.yaml"
P1_FIXTURES_PATH = (
    ROOT
    / "research_control/tasks/RT-20260712-009/artifacts/gate_id_and_supersedence_fixtures.yaml"
)

from scripts.research_control.strict_yaml import load as load_yaml
from scripts.validation import deduplicate
from scripts.validation.deduplicate import (
    DeduplicationConfig,
    DeduplicationError,
    GateExecution,
    deduplicate_executions,
    evaluate_predicate,
    load_contracts,
    load_manifest,
)


class ValidationDeduplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(MANIFEST_PATH)
        cls.contracts = load_contracts(CONTRACTS_PATH)
        cls.config = DeduplicationConfig(True, True, True)

    def execution(self, execution_id: str, gate_id: str, **changes) -> GateExecution:
        evidence = {
            "implementation_family_digest": "sha256:family",
            "core_configuration_digest": "sha256:core-config",
            "environment_digest": "sha256:env",
            "tree_hash": "git-tree:tree",
            "tree_state": "index",
            "base_ref": "HEAD",
            "staged_flag": True,
            "core_scope_digest": "sha256:scope",
            "superset_executed_core": True,
            "raw_core_failures_preserved": True,
            "implementation_digest": "sha256:claim-impl",
            "path_set_digest": "sha256:paths",
            "taxonomy_digest": "sha256:taxonomy",
            "reviewed_context_policy_digest": "sha256:contexts",
            "severity_mapping_digest": "sha256:severity",
            "claim_configuration_digest": "sha256:claim-config",
            "integrated_linter_executed": True,
            "raw_claim_failures_preserved": True,
            "p1_t03_equivalence_proved": True,
        }
        values = {
            "execution_id": execution_id,
            "gate_id": gate_id,
            "implementation_digest": f"sha256:{gate_id}",
            "environment_digest": "sha256:env",
            "config_digest": "sha256:config",
            "scope": "tree_state=index;base_ref=HEAD",
            "tree_hash": "git-tree:tree",
            "generation_state": "post_generation",
            "predicate_evidence": evidence,
        }
        values.update(changes)
        return GateExecution(**values)

    def activated_policy(self, predicate_id: str, source: str, target: str):
        manifest = deepcopy(self.manifest)
        contracts = deepcopy(self.contracts)
        contracts["activation_gate"]["current_status"] = "active"
        for predicate in contracts["predicate_catalog"]:
            if predicate["predicate_id"] == predicate_id:
                predicate["status"] = "active"
        for contract in contracts["supersedence_contracts"]:
            if (
                contract["source_gate_id"] == source
                and contract["target_gate_id"] == target
                and contract["predicate_id"] == predicate_id
            ):
                contract["activation_status"] = "active"
        for gate in manifest["gates"]:
            if gate["gate_id"] == source:
                for edge in gate["supersedes"]:
                    if edge["gate_id"] == target:
                        edge["predicate_id"] = predicate_id
                        edge["status"] = "active"
        return manifest, contracts

    def test_exact_identity_duplicate_is_skipped_with_machine_reason(self) -> None:
        first = self.execution("run-1", "git_diff_check")
        second = replace(first, execution_id="run-2")
        result = deduplicate_executions(
            (first, second), self.manifest, self.contracts, self.config
        )
        self.assertEqual(result.retained_execution_ids, ("run-1",))
        self.assertEqual(result.skipped_duplicate_count, 1)
        decision = result.decisions[1]
        self.assertEqual(decision.status, "skipped_duplicate")
        self.assertEqual(decision.satisfying_execution_id, "run-1")
        self.assertEqual(decision.predicate_id, "exact_evidence_identity_v1")
        self.assertTrue(decision.predicate_evidence["identity_components"])

    def test_same_identity_duplicate_count_is_zero_after_normal_planning(self) -> None:
        first = self.execution("run-1", "git_diff_check")
        result = deduplicate_executions(
            (first, replace(first, execution_id="run-2")),
            self.manifest,
            self.contracts,
            self.config,
        )
        self.assertEqual(result.residual_repeated_identity_count, 0)

    def test_cross_tree_repetition_is_retained(self) -> None:
        first = self.execution("run-1", "git_diff_check")
        second = replace(first, execution_id="run-2", tree_hash="git-tree:other")
        result = deduplicate_executions(
            (first, second), self.manifest, self.contracts, self.config
        )
        self.assertEqual(result.retained_execution_ids, ("run-1", "run-2"))

    def test_working_and_staged_repetitions_are_retained(self) -> None:
        staged = self.execution("staged", "git_diff_check")
        working = replace(
            staged,
            execution_id="working",
            scope="tree_state=working;base_ref=HEAD",
        )
        result = deduplicate_executions(
            (staged, working), self.manifest, self.contracts, self.config
        )
        self.assertEqual(len(result.retained_execution_ids), 2)

    def test_pre_and_post_generation_repetitions_are_retained(self) -> None:
        post = self.execution("post", "git_diff_check")
        pre = replace(post, execution_id="pre", generation_state="pre_generation")
        result = deduplicate_executions(
            (pre, post), self.manifest, self.contracts, self.config
        )
        self.assertEqual(len(result.retained_execution_ids), 2)

    def test_cross_config_and_cross_implementation_repetitions_are_retained(self) -> None:
        first = self.execution("run-1", "git_diff_check")
        different_config = replace(
            first, execution_id="run-2", config_digest="sha256:other-config"
        )
        different_implementation = replace(
            first, execution_id="run-3", implementation_digest="sha256:other-impl"
        )
        result = deduplicate_executions(
            (first, different_config, different_implementation),
            self.manifest,
            self.contracts,
            self.config,
        )
        self.assertEqual(len(result.retained_execution_ids), 3)

    def test_missing_identity_is_retained_fail_closed(self) -> None:
        execution = self.execution("unresolved", "git_diff_check", tree_hash=None)
        result = deduplicate_executions(
            (execution,), self.manifest, self.contracts, self.config
        )
        self.assertEqual(result.decisions[0].status, "retained_unresolved_identity")

    def test_mutating_gate_duplicates_are_never_removed(self) -> None:
        first = self.execution("sync-1", "memory_sync")
        second = replace(first, execution_id="sync-2")
        result = deduplicate_executions(
            (first, second), self.manifest, self.contracts, self.config
        )
        self.assertEqual(len(result.retained_execution_ids), 2)
        self.assertEqual(
            {decision.status for decision in result.decisions}, {"retained_mutator"}
        )

    def test_explicit_replay_bypass_retains_duplicate_with_reason(self) -> None:
        first = self.execution("run-1", "git_diff_check")
        replay = replace(
            first,
            execution_id="replay",
            replay_bypass_reason="controlled regression replay",
        )
        result = deduplicate_executions(
            (first, replay), self.manifest, self.contracts, self.config
        )
        self.assertEqual(len(result.retained_execution_ids), 2)
        self.assertEqual(result.decisions[1].status, "retained_replay_bypass")
        self.assertIn("controlled regression replay", result.decisions[1].reasons)

    def test_feature_switch_disables_all_removal(self) -> None:
        first = self.execution("run-1", "git_diff_check")
        result = deduplicate_executions(
            (first, replace(first, execution_id="run-2")),
            self.manifest,
            self.contracts,
            DeduplicationConfig(False, True, True),
        )
        self.assertEqual(len(result.retained_execution_ids), 2)
        self.assertEqual(result.skipped_duplicate_count, 0)

    def test_deduplication_requires_prerequisite_and_obligation_resolution(self) -> None:
        execution = self.execution("run", "git_diff_check")
        with self.assertRaisesRegex(DeduplicationError, "expanded prerequisites"):
            deduplicate_executions(
                (execution,),
                self.manifest,
                self.contracts,
                DeduplicationConfig(True, False, True),
            )
        with self.assertRaisesRegex(DeduplicationError, "resolved obligations"):
            deduplicate_executions(
                (execution,),
                self.manifest,
                self.contracts,
                DeduplicationConfig(True, True, False),
            )

    def test_active_same_scope_contract_supersedes_target(self) -> None:
        predicate_id = "rc_diff_satisfies_core_same_scope_v1"
        manifest, contracts = self.activated_policy(
            predicate_id, "research_control_diff", "research_control_core"
        )
        source = self.execution("diff", "research_control_diff")
        target = self.execution("core", "research_control_core")
        result = deduplicate_executions(
            (target, source), manifest, contracts, self.config
        )
        self.assertEqual(result.retained_gate_ids, ("research_control_diff",))
        self.assertEqual(result.superseded_count, 1)
        target_decision = result.decisions[0]
        self.assertEqual(target_decision.status, "skipped_superseded")
        self.assertEqual(target_decision.satisfying_gate_id, "research_control_diff")
        self.assertEqual(target_decision.predicate_id, predicate_id)

    def test_inactive_manifest_contract_never_supersedes(self) -> None:
        source = self.execution("diff", "research_control_diff")
        target = self.execution("core", "research_control_core")
        result = deduplicate_executions(
            (target, source), self.manifest, self.contracts, self.config
        )
        self.assertEqual(result.superseded_count, 0)
        self.assertEqual(len(result.retained_execution_ids), 2)

    def test_cross_scope_cross_base_ref_and_changed_taxonomy_fail_closed(self) -> None:
        core_predicate = next(
            item
            for item in self.contracts["predicate_catalog"]
            if item["predicate_id"] == "rc_diff_satisfies_core_same_scope_v1"
        )
        source = self.execution("diff", "research_control_diff")
        target = self.execution("core", "research_control_core")
        cross_scope = replace(
            target,
            scope="tree_state=working;base_ref=HEAD",
            predicate_evidence={**target.predicate_evidence, "tree_state": "working"},
        )
        eligible, evidence = evaluate_predicate(core_predicate, source, cross_scope)
        self.assertFalse(eligible)
        self.assertIn("tree_state", evidence["required_equal_mismatches"])
        cross_base = replace(
            target,
            predicate_evidence={**target.predicate_evidence, "base_ref": "origin/main"},
        )
        self.assertFalse(evaluate_predicate(core_predicate, source, cross_base)[0])

        claim_predicate = next(
            item
            for item in self.contracts["predicate_catalog"]
            if item["predicate_id"]
            == "rc_diff_satisfies_claim_language_same_scope_v1"
        )
        claim_target = self.execution("claim", "claim_language_changed")
        changed_taxonomy = replace(
            claim_target,
            predicate_evidence={
                **claim_target.predicate_evidence,
                "taxonomy_digest": "sha256:changed-taxonomy",
            },
        )
        eligible, evidence = evaluate_predicate(
            claim_predicate, source, changed_taxonomy
        )
        self.assertFalse(eligible)
        self.assertIn("taxonomy_digest", evidence["required_equal_mismatches"])

    def test_p1_positive_and_negative_predicate_fixtures_are_preserved(self) -> None:
        fixtures = load_yaml(P1_FIXTURES_PATH)["fixtures"]
        by_id = {item["fixture_id"]: item for item in fixtures}
        self.assertTrue(by_id["same_scope_rc_core_candidate"]["expected_eligibility"])
        self.assertFalse(by_id["cross_scope_forbidden"]["expected_eligibility"])
        self.assertFalse(by_id["different_base_ref_forbidden"]["expected_eligibility"])
        self.assertFalse(
            by_id["claim_path_set_mismatch_forbidden"]["expected_eligibility"]
        )
        self.assertFalse(
            by_id["pre_generation_cannot_satisfy_post_generation"][
                "expected_eligibility"
            ]
        )

    def test_unknown_gate_and_duplicate_execution_id_fail_closed(self) -> None:
        unknown = self.execution("unknown", "missing_gate")
        with self.assertRaisesRegex(DeduplicationError, "unknown manifest gate"):
            deduplicate_executions(
                (unknown,), self.manifest, self.contracts, self.config
            )
        first = self.execution("same", "git_diff_check")
        second = self.execution("same", "research_control_core")
        with self.assertRaisesRegex(DeduplicationError, "duplicate execution_id"):
            deduplicate_executions(
                (first, second), self.manifest, self.contracts, self.config
            )

    def test_output_is_deterministic_and_does_not_execute_commands(self) -> None:
        first = self.execution("run-1", "git_diff_check")
        second = replace(first, execution_id="run-2")
        with mock.patch("subprocess.run", side_effect=AssertionError("command executed")):
            left = deduplicate_executions(
                (first, second), self.manifest, self.contracts, self.config
            ).to_dict()
            right = deduplicate_executions(
                (first, second), self.manifest, self.contracts, self.config
            ).to_dict()
        self.assertEqual(left, right)
        self.assertFalse(left["planner_executes_commands"])

    def test_audit_cli_is_machine_readable_and_nonpromotional(self) -> None:
        stream = io.StringIO()
        with mock.patch("sys.stdout", stream):
            self.assertEqual(deduplicate.main(["audit", "--json"]), 0)
        payload = json.loads(stream.getvalue())
        self.assertEqual(payload["schema_id"], "validation_deduplication_predicate_report_v1")
        self.assertEqual(payload["status"], "PASS")
        self.assertFalse(payload["authority"]["planner_integration_changed"])
        self.assertTrue(payload["authority"]["legacy_execution_authoritative"])
        self.assertFalse(payload["authority"]["scientific_claims_changed"])


if __name__ == "__main__":
    unittest.main()
