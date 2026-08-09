from __future__ import annotations

import copy
import unittest
from pathlib import Path

from scripts.research_control.v22_track_governance import (
    FIXTURE_PATH,
    RESOURCE_DIMENSIONS,
    TRACK_IDS,
    build_validation_report,
    load_governance,
    validate_assignment_manifest,
    validate_budget,
    validate_cross_track_link,
    validate_fixture_suite,
    validate_protected_action,
    validate_publication_summary,
    validate_repository_decision,
    validate_resource_events,
    validate_scorecard_record,
    validate_scorecard_schemas,
)


ROOT = Path(__file__).resolve().parents[1]


class V22TrackGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.governance = load_governance(ROOT)

    def test_combined_contract_and_fixture_report_passes(self) -> None:
        report = build_validation_report(ROOT)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["governance"]["assignment_count"], 40)
        self.assertEqual(report["governance"]["scorecard_schema_count"], 4)
        self.assertEqual(report["fixtures"]["fixture_case_count"], 15)
        self.assertEqual(report["fixtures"]["fixture_failure_count"], 0)
        self.assertFalse(report["authority_limits"]["scientific_status_changed"])

    def test_all_40_backlog_packages_have_one_primary_assignment(self) -> None:
        errors = validate_assignment_manifest(
            self.governance["backlog"], self.governance["assignment"]
        )
        self.assertEqual(errors, [])
        counts = self.governance["assignment"]["expected_primary_track_counts"]
        self.assertEqual(
            counts,
            {"track_a": 1, "track_b": 22, "track_c": 3, "shared_control": 14},
        )

    def test_duplicate_or_multiple_assignment_fails_closed(self) -> None:
        manifest = copy.deepcopy(self.governance["assignment"])
        manifest["assignments"][0]["primary_track"] = ["track_a", "shared_control"]
        errors = validate_assignment_manifest(self.governance["backlog"], manifest)
        self.assertIn("assignment_multiple_primary_tracks:P0-T01", errors)
        self.assertIn("assignment_declared_counts_mismatch", errors)

    def test_scorecard_identifiers_and_lanes_are_disjoint(self) -> None:
        schemas = self.governance["scorecards"]
        self.assertEqual(validate_scorecard_schemas(schemas, self.governance["authority"]), [])
        for field in ("schema_id", "metric_namespace", "dashboard_id", "publication_lane_id"):
            values = [schemas[track_id][field] for track_id in TRACK_IDS]
            self.assertEqual(len(values), len(set(values)))

    def test_track_a_c_and_shared_cannot_change_distance_to_gr(self) -> None:
        for track_id in ("track_a", "track_c", "shared_control"):
            schema = self.governance["scorecards"][track_id]
            record = {
                "track_id": track_id,
                "metric_namespace": schema["metric_namespace"],
                "dashboard_id": schema["dashboard_id"],
                "publication_lane_id": schema["publication_lane_id"],
                "distance_to_gr_effect": "reduced",
                "gate_evidence_classes": [],
                "claim_classes": [],
                "resource_accounting": {key: "not_measured" for key in RESOURCE_DIMENSIONS},
                "gate_verdict_issued": False,
                "publication_authorized": False,
            }
            errors = validate_scorecard_record(
                record, self.governance["scorecards"], self.governance["authority"]
            )
            self.assertIn(f"{track_id}_distance_to_gr_effect_forbidden", errors)

    def test_track_b_rejects_interpretive_and_process_gate_evidence(self) -> None:
        schema = self.governance["scorecards"]["track_b"]
        for evidence in (
            "track_a_interpretive_coherence",
            "target_side_exact_gr_agreement",
            "track_c_methodology_success",
            "workflow_pass",
            "validator_pass",
            "checkpoint_pass",
            "control_traceability",
        ):
            record = {
                "track_id": "track_b",
                "metric_namespace": schema["metric_namespace"],
                "dashboard_id": schema["dashboard_id"],
                "publication_lane_id": schema["publication_lane_id"],
                "distance_to_gr_effect": "none",
                "gate_evidence_classes": [evidence],
                "claim_classes": [],
                "resource_accounting": {key: "not_measured" for key in RESOURCE_DIMENSIONS},
                "gate_verdict_issued": False,
                "publication_authorized": False,
            }
            errors = validate_scorecard_record(
                record, self.governance["scorecards"], self.governance["authority"]
            )
            self.assertIn(f"track_b_forbidden_gate_evidence:{evidence}", errors)

    def test_cross_track_reference_cannot_promote_evidence_or_authority(self) -> None:
        link = {
            "link_id": "test-link",
            "source_track": "track_a",
            "target_track": "track_b",
            "relation_type": "context_reference",
            "source_path": "research_control/design/v22_three_track_charter_v1.md",
            "source_sha256": "0" * 64,
            "consumer_path": "research_control/design/v22_track_authority_matrix_v1.yaml",
            "authority_effect": "none",
            "evidence_credit": "gate_credit",
            "distance_to_gr_effect": "none",
            "gate_effect": "none",
            "resource_reattribution": "none",
        }
        errors = validate_cross_track_link(link, self.governance["cross_track"])
        self.assertEqual(errors, ["cross_track_promotion_forbidden:evidence_credit"])

    def test_budget_has_four_dimensions_without_double_counting(self) -> None:
        errors = validate_budget(
            self.governance["budget"],
            self.governance["assignment"],
            self.governance["scorecards"],
        )
        self.assertEqual(errors, [])
        self.assertEqual(
            set(self.governance["budget"]["resource_dimensions"]),
            set(RESOURCE_DIMENSIONS),
        )
        self.assertEqual(
            sum(center["planned_task_count"] for center in self.governance["budget"]["cost_centers"].values()),
            40,
        )
        events = [{
            "resource_event_id": "event-1",
            "primary_cost_centers": ["track_a", "track_b"],
            "dimension": "compute",
        }]
        self.assertIn(
            "resource_event_primary_cost_center_not_exactly_one:event-1",
            validate_resource_events(events),
        )

    def test_publication_lanes_cannot_be_blended(self) -> None:
        summary = {
            "preserves_separate_lanes": False,
            "claim_merge": True,
            "blended_publication_lane_id": "combined_success",
            "entries": [],
        }
        errors = validate_publication_summary(summary, self.governance["scorecards"])
        self.assertIn("publication_summary_blended_lane_forbidden", errors)
        self.assertIn("publication_summary_claim_merge_forbidden", errors)

    def test_repository_split_remains_measured_and_human_gated(self) -> None:
        self.assertEqual(validate_repository_decision(self.governance["repository"]), [])
        decision = self.governance["repository"]
        self.assertEqual(decision["current_decision"], "retain_monorepo")
        self.assertFalse(decision["automatic_split_authorized"])
        self.assertFalse(decision["current_evidence"]["split_trigger_satisfied"])

    def test_shared_control_cannot_issue_a_gate_verdict(self) -> None:
        errors = validate_protected_action({
            "requested": True,
            "action": "gate_verdict",
            "primary_track": "shared_control",
            "exact_human_authority_present": False,
        })
        self.assertIn("protected_action_track_forbidden:gate_verdict", errors)
        self.assertIn("protected_action_human_authority_missing:gate_verdict", errors)

    def test_fixture_suite_has_explicit_negative_cases(self) -> None:
        self.assertTrue((ROOT / FIXTURE_PATH).is_file())
        report = validate_fixture_suite(ROOT)
        self.assertEqual(report["status"], "PASS")
        negatives = [result for result in report["results"] if not result["expected_valid"]]
        self.assertEqual(len(negatives), 10)
        self.assertTrue(all(result["errors"] for result in negatives))
        self.assertTrue(all(result["expectation_met"] for result in negatives))


if __name__ == "__main__":
    unittest.main()
