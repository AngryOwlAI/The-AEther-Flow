from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260721-007/artifacts/validate_v21_event_store_architecture.py"
)
SPEC = importlib.util.spec_from_file_location("validate_v21_event_store_architecture", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class EventStoreArchitectureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = MODULE.load_contract()

    @staticmethod
    def failed_names(checks: list[dict[str, str]]) -> set[str]:
        return {item["name"] for item in checks if item["status"] != "PASS"}

    def test_live_contract_sources_and_documents_pass(self) -> None:
        report, receipt = MODULE.build_outputs(self.contract)
        self.assertEqual("PASS", report["status"])
        self.assertEqual([], report["failed_checks"])
        self.assertEqual("PASS", receipt["validation_status"])

    def test_architecture_selection_is_exclusive(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["architecture_options"][0]["selected"] = True
        failed = self.failed_names(MODULE.validate_contract_data(mutated))
        self.assertIn("exactly_one_architecture_selected", failed)

    def test_activation_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["activation_state"]["pilot_executed"] = True
        failed = self.failed_names(MODULE.validate_contract_data(mutated))
        self.assertIn("pilot_and_cutover_not_executed", failed)

    def test_all_required_event_domains_are_enforced(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["event_domains"] = mutated["event_domains"][:-1]
        failed = self.failed_names(MODULE.validate_contract_data(mutated))
        self.assertIn("required_event_domains_present", failed)

    def test_generated_views_cannot_claim_authority(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["generated_views"][0]["authority"] = True
        failed = self.failed_names(MODULE.validate_contract_data(mutated))
        self.assertIn("generated_views_non_authoritative_and_deterministic", failed)

    def test_identity_requires_stable_operation_id(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["event_identity"]["identity_basis_fields"].remove("operation_id")
        failed = self.failed_names(MODULE.validate_contract_data(mutated))
        self.assertIn("deterministic_content_identity", failed)

    def test_transaction_requires_compare_and_swap(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["transaction_contract"]["expected_head_compare_and_swap"] = False
        failed = self.failed_names(MODULE.validate_contract_data(mutated))
        self.assertIn("single_writer_checkpoint_transaction", failed)

    def test_migration_cannot_implicitly_authorize_cutover(self) -> None:
        mutated = copy.deepcopy(self.contract)
        for phase in mutated["migration_contract"]["phases"]:
            if phase["id"] == "reader_cutover":
                phase["status"] = "active"
                phase["writes_authorized"] = True
        failed = self.failed_names(MODULE.validate_contract_data(mutated))
        self.assertIn("migration_is_shadow_then_explicit_cutover", failed)

    def test_authority_flags_are_enforced(self) -> None:
        mutated = copy.deepcopy(self.contract)
        mutated["authority_contract"]["generated_sqlite_is_authority"] = True
        failed = self.failed_names(MODULE.validate_contract_data(mutated))
        self.assertIn("authority_hierarchy_preserved", failed)

    def test_outputs_are_deterministic(self) -> None:
        first = MODULE.build_outputs(self.contract)
        second = MODULE.build_outputs(self.contract)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
