from __future__ import annotations

from copy import deepcopy
import io
import json
from pathlib import Path
from unittest import mock
import unittest


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "research_control/design/validation_obligation_catalog_v1.yaml"
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
ROLE_REGISTRY = ROOT / "registries/AGENT_ROLE_REGISTRY.csv"

from scripts.validation import obligations
from scripts.validation.obligations import (
    Declaration,
    EvidenceContext,
    ObligationError,
    active_role_declarations,
    annotate_satisfaction,
    audit_repository,
    compile_declarations,
    load_catalog,
    load_manifest,
    skill_declarations,
)


class ValidationObligationCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog(CATALOG_PATH)
        cls.manifest = load_manifest(MANIFEST_PATH)
        cls.context = EvidenceContext(
            tree_hash="tree-a",
            path_set_hash="paths-a",
            configuration_hash="config-a",
            generation_state="precheckpoint",
        )

    def compile(self, declarations):
        return compile_declarations(
            self.catalog, self.manifest, declarations, self.context
        )

    def test_all_thirteen_active_roles_resolve(self) -> None:
        declarations = active_role_declarations(ROLE_REGISTRY)
        roles = {declaration.source_id for declaration in declarations}
        self.assertEqual(len(roles), 13)
        requirements = self.compile(declarations)
        self.assertTrue(requirements)
        self.assertEqual(
            sum(len(requirement.required_by) for requirement in requirements),
            34,
        )

    def test_three_main_workflow_skills_resolve_declared_tokens(self) -> None:
        declarations = skill_declarations(self.catalog, ROOT)
        self.assertEqual(
            {declaration.source_id for declaration in declarations},
            {"continue-research", "improve-project-system", "user-modified-project"},
        )
        self.assertEqual(len(declarations), 27)
        requirements = self.compile(declarations)
        self.assertEqual(len(requirements), 9)

    def test_unknown_declaration_fails_closed(self) -> None:
        with self.assertRaisesRegex(ObligationError, "unmapped declaration"):
            self.compile(
                [Declaration("task_overlay", "test-task", "unknown_validator")]
            )

    def test_bootstrap_label_expands_to_sync_and_core(self) -> None:
        requirements = self.compile(
            [
                Declaration(
                    "registered_role",
                    "memory-system-maintainer@0.2.0",
                    "bootstrap_memory_system",
                )
            ]
        )
        self.assertEqual(
            {requirement.obligation_id for requirement in requirements},
            {"memory_sync", "memory_core"},
        )

    def test_repeated_declarations_deduplicate_requirement_and_keep_provenance(self) -> None:
        requirements = self.compile(
            [
                Declaration("registered_role", "role-a", "validate_documentation_impact"),
                Declaration("skill", "skill-a", "documentation_impact"),
            ]
        )
        self.assertEqual(len(requirements), 1)
        self.assertEqual(len(requirements[0].required_by), 2)

    def test_satisfying_gates_exist_and_match_direct_manifest_obligations(self) -> None:
        requirements = self.compile(
            [
                Declaration("skill", "continue-research", "memory_core"),
                Declaration("skill", "continue-research", "git_diff_check"),
            ]
        )
        manifest_ids = {gate["gate_id"] for gate in self.manifest["gates"]}
        for requirement in requirements:
            for mapping in requirement.satisfying_gates:
                self.assertIn(mapping["gate_id"], manifest_ids)

    def test_working_receipt_never_satisfies_staged_requirement(self) -> None:
        requirement = self.compile(
            [
                Declaration(
                    "task_overlay",
                    "task-a",
                    "documentation_impact",
                    scope="staged",
                )
            ]
        )
        receipt = {
            "gate_id": "documentation_impact",
            "status": "PASS",
            "tree_hash": "tree-a",
            "scope": "working",
            "path_set_hash": "paths-a",
            "configuration_hash": "config-a",
            "generation_state": "precheckpoint",
            "satisfied_predicates": [],
        }
        annotated = annotate_satisfaction(requirement, [receipt])
        self.assertEqual(annotated[0]["satisfied_obligations"], [])

    def test_research_diff_requires_same_scope_predicate_for_core(self) -> None:
        requirement = self.compile(
            [
                Declaration(
                    "task_overlay",
                    "task-a",
                    "research_control_core",
                    scope="staged",
                )
            ]
        )
        receipt = {
            "gate_id": "research_control_diff",
            "status": "PASS",
            "tree_hash": "tree-a",
            "scope": "staged",
            "path_set_hash": "paths-a",
            "configuration_hash": "config-a",
            "generation_state": "precheckpoint",
            "satisfied_predicates": [],
        }
        self.assertEqual(
            annotate_satisfaction(requirement, [receipt])[0]["satisfied_obligations"],
            [],
        )
        receipt["satisfied_predicates"] = ["rc_diff_satisfies_core_same_scope_v1"]
        self.assertEqual(
            annotate_satisfaction(requirement, [receipt])[0]["satisfied_obligations"][0][
                "obligation_id"
            ],
            "research_control_core",
        )

    def test_nonpassing_receipt_does_not_satisfy(self) -> None:
        requirement = self.compile(
            [Declaration("skill", "continue-research", "git_diff_check")]
        )
        receipt = {
            "gate_id": "git_diff_check",
            "status": "WARN",
            **requirement[0].evidence_identity,
            "satisfied_predicates": [],
        }
        self.assertEqual(
            annotate_satisfaction(requirement, [receipt])[0]["satisfied_obligations"],
            [],
        )

    def test_unknown_manifest_gate_in_catalog_fails_closed(self) -> None:
        catalog = deepcopy(self.catalog)
        catalog["obligation_specs"][0]["satisfying_gates"][0]["gate_id"] = "missing_gate"
        with self.assertRaisesRegex(ObligationError, "unknown gate"):
            compile_declarations(
                catalog,
                self.manifest,
                [Declaration("skill", "continue-research", "memory_sync")],
                self.context,
            )

    def test_skill_token_drift_fails_closed(self) -> None:
        with mock.patch.object(Path, "read_text", return_value="# no declarations\n"):
            with self.assertRaisesRegex(ObligationError, "does not declare"):
                skill_declarations(self.catalog, ROOT)

    def test_repository_audit_is_deterministic_and_nonpromotional(self) -> None:
        left = audit_repository(CATALOG_PATH, MANIFEST_PATH, ROLE_REGISTRY, ROOT)
        right = audit_repository(CATALOG_PATH, MANIFEST_PATH, ROLE_REGISTRY, ROOT)
        self.assertEqual(left, right)
        self.assertEqual(left["status"], "PASS")
        self.assertEqual(left["unmapped_declaration_count"], 0)
        self.assertEqual(left["active_role_count"], 13)
        self.assertEqual(left["skill_count"], 3)
        self.assertEqual(left["resolved_declaration_count"], 61)
        self.assertFalse(left["authority"]["scientific_claims_changed"])
        self.assertTrue(left["authority"]["legacy_execution_authoritative"])

    def test_cli_emits_canonical_machine_readable_audit(self) -> None:
        stream = io.StringIO()
        with mock.patch("sys.stdout", stream):
            self.assertEqual(obligations.main(["audit", "--json"]), 0)
        payload = json.loads(stream.getvalue())
        self.assertEqual(payload["schema_id"], "validation_obligation_resolution_audit_v1")
        self.assertEqual(payload["compiled_requirement_count"], 11)


if __name__ == "__main__":
    unittest.main()
