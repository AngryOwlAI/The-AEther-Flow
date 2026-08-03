#!/usr/bin/env python3
"""Validate the exact P15-T07 four-package no-external-action decision."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = ROOT / "research_control/tasks/RT-20260802-010/artifacts"
REPORT_PATH = ARTIFACTS / "p15_t07_no_external_action_validation_v1.json"
RECEIPT_PATH = ARTIFACTS / "p15_t07_no_external_action_compact_receipt_v1.json"
FIXED_TIME = "2026-08-02T21:10:21Z"

PACKAGES = {
    "P15-T01-EXACT-GR-INTERPRETIVE": {
        "plan_task_id": "P15-T01",
        "primary_path": "research_control/tasks/RT-20260722-021/artifacts/exact_gr_interpretive_manuscript_v1.md",
        "primary_sha256": "17d215509eb3f0ee4544c2f25eed56462d346106f41bc520fc27441c09c0add9",
        "archive_path": "research_control/tasks/RT-20260802-009/artifacts/p15_t01_exact_gr_interpretive_source_bundle_v1.tar",
        "archive_sha256": "cdb3e01b113287380e587004e91ad0f7445b63d538bcdbfdce63155207d757d8",
        "disposition": "future_reviewer_contact_candidate",
    },
    "P15-T02-AI-METHODOLOGY": {
        "plan_task_id": "P15-T02",
        "primary_path": "research_control/tasks/RT-20260802-008/artifacts/p15_t02_methodology_manuscript.md",
        "primary_sha256": "05151b543111f1107a07f1b02afabc78d97ef07820d1eed824da38fdd8e441a3",
        "archive_path": "research_control/tasks/RT-20260802-009/artifacts/p15_t02_ai_methodology_source_bundle_v1.tar",
        "archive_sha256": "056d81f87c1595b1f3b4bb40a1dc8b5e6ac895eff989ef6de0a2ae4f94718bbe",
        "disposition": "revision_before_any_release",
    },
    "P15-T03-SELECTOR-THEOREM": {
        "plan_task_id": "P15-T03",
        "primary_path": "research_control/tasks/RT-20260723-003/artifacts/selector_minimum_extension_theorem_manuscript_v1.tex",
        "primary_sha256": "348fba00dc68f7791ffec4fb3edb8d70bc7db18cfd405f052572a639c51b62fa",
        "archive_path": "research_control/tasks/RT-20260802-009/artifacts/p15_t03_selector_theorem_source_bundle_v1.tar",
        "archive_sha256": "cea3d636d4a8e1dc3734a8fc1a8a3aee8861b6f88527c501498573411da352fc",
        "disposition": "future_reviewer_contact_candidate",
    },
    "P15-T04-SOURCE-DYNAMICS": {
        "plan_task_id": "P15-T04",
        "primary_path": "research_control/tasks/RT-20260727-006/artifacts/source_dynamics_reconstruction_technical_report_v1.tex",
        "primary_sha256": "5724a07c2181f87d517b80d7878f437b47d8802045596cd16d3e62929dfe5cff",
        "archive_path": "research_control/tasks/RT-20260802-009/artifacts/p15_t04_source_dynamics_source_bundle_v1.tar",
        "archive_sha256": "cedb2ca1f6a6a93fb3626a750759ec9463e607f2a1d8dab2dbfd972ee023f866",
        "disposition": "revision_before_any_release",
    },
}
ACTIONS = ("submission", "public_release", "reviewer_contact", "outreach")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_yaml(relative: str) -> dict[str, Any]:
    value = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping: {relative}")
    return value


def canonical_json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    approval = load_yaml("research_control/approvals/approval-20260802-001.yaml")
    human = load_yaml(
        "research_control/tasks/RT-20260802-010/artifacts/"
        "human_authorization_p15_t07_no_external_action_v1.yaml"
    )
    decisions = load_yaml(
        "research_control/tasks/RT-20260802-010/artifacts/"
        "p15_t07_submission_claim_venue_decisions_v1.yaml"
    )
    action_log = load_yaml(
        "research_control/tasks/RT-20260802-010/artifacts/"
        "p15_t07_external_action_log_v1.yaml"
    )
    advisory = load_yaml(
        "research_control/tasks/RT-20260802-010/artifacts/"
        "p15_t07_internal_ai_advisory_review_v1.yaml"
    )
    child_math = load_yaml(
        "research_control/tasks/RT-20260802-010/artifacts/"
        "child_phys_math_p15_t07_external_action_decision.yaml"
    )
    child_phil = load_yaml(
        "research_control/tasks/RT-20260802-010/artifacts/"
        "child_phys_phil_p15_t07_external_action_decision.yaml"
    )
    conflict = load_yaml(
        "research_control/tasks/RT-20260802-010/artifacts/"
        "parent_conflict_review_p15_t07_external_action_decision.yaml"
    )
    manifest = load_yaml(
        "research_control/tasks/RT-20260802-010/artifacts/"
        "p15_t07_reproducibility_manifest_v1.yaml"
    )

    check(
        "approval_exact_identity",
        approval.get("approval_id") == "approval-20260802-001"
        and approval.get("human_authorization_id")
        == "HUMAN-AUTH-P15-T07-NO-EXTERNAL-ACTION-2026-08-02-001",
        "Approval and human-authorization identifiers match the one-time record.",
    )
    check(
        "approval_exact_message",
        approval.get("source_message_text")
        == "I explicitly approve the exact four-package P15-T07 no-external-action decision matrix in your prior message."
        and approval.get("source_message_sha256")
        == "7bb7607b66e7c8e58c2f1566800095e3a29828a79934f0be14b1cc54ba8a6179",
        "Exact user message and SHA-256 are preserved.",
    )
    check(
        "approval_consumed_once",
        approval.get("one_time_use") is True
        and approval.get("status") == "consumed"
        and approval.get("consumed_by") == "AJ-RT-20260802-010-001",
        "Approval is one-time and consumed only by this job.",
    )
    check(
        "approval_decision_code",
        approval.get("decision_code")
        == "AUTHORIZED_EXACT_P15_T07_NO_EXTERNAL_ACTION_MATRIX",
        "Approval authorizes recording the exact all-denied matrix only.",
    )
    check(
        "human_matrix_cardinality",
        human.get("package_count") == 4
        and human.get("action_type_count") == 4
        and human.get("authorization_cell_count") == 16
        and human.get("authorized_cell_count") == 0
        and human.get("denied_cell_count") == 16,
        "Human authorization records four packages four actions and sixteen denials.",
    )
    check(
        "human_nondelegated_limits",
        human.get("authorship_assignment_status") == "unassigned"
        and human.get("embargoed_distribution_authorized") is False
        and human.get("reviewer_identity_publication_authorized") is False
        and human.get("reviewer_report_publication_authorized") is False,
        "Authorship embargo identity and report permissions remain closed.",
    )

    approval_packages = {p.get("package_id"): p for p in approval.get("package_matrix", [])}
    human_packages = {p.get("package_id"): p for p in human.get("package_matrix", [])}
    decision_packages = {p.get("package_id"): p for p in decisions.get("package_decisions", [])}
    advisory_packages = {p.get("package_id"): p for p in advisory.get("package_reviews", [])}
    check(
        "package_sets_exact",
        set(approval_packages) == set(PACKAGES)
        and set(human_packages) == set(PACKAGES)
        and set(decision_packages) == set(PACKAGES)
        and set(advisory_packages) == set(PACKAGES),
        "All decision surfaces contain exactly the four approved package identities.",
    )

    for package_id, expected in PACKAGES.items():
        primary = ROOT / expected["primary_path"]
        archive = ROOT / expected["archive_path"]
        check(
            f"{expected['plan_task_id'].lower()}_primary_exists",
            primary.is_file(),
            f"Primary artifact exists: {expected['primary_path']}",
        )
        check(
            f"{expected['plan_task_id'].lower()}_primary_hash",
            primary.is_file() and sha256(primary) == expected["primary_sha256"],
            f"Primary artifact matches {expected['primary_sha256']}.",
        )
        check(
            f"{expected['plan_task_id'].lower()}_archive_exists",
            archive.is_file(),
            f"Archive exists: {expected['archive_path']}",
        )
        check(
            f"{expected['plan_task_id'].lower()}_archive_hash",
            archive.is_file() and sha256(archive) == expected["archive_sha256"],
            f"Archive matches {expected['archive_sha256']}.",
        )
        surfaces_ok = True
        for surface in (approval_packages, human_packages, decision_packages):
            row = surface.get(package_id, {})
            surfaces_ok = surfaces_ok and (
                row.get("primary_artifact_path") == expected["primary_path"]
                and row.get("primary_artifact_sha256") == expected["primary_sha256"]
                and row.get("archive_path") == expected["archive_path"]
                and row.get("archive_sha256") == expected["archive_sha256"]
            )
        check(
            f"{expected['plan_task_id'].lower()}_identity_bound_everywhere",
            surfaces_ok,
            "Approval human authorization and decision record agree on both exact hashes.",
        )
        row = decision_packages.get(package_id, {})
        action_fields_ok = all(
            isinstance(row.get(action), dict)
            and row[action].get("authorized") is False
            for action in ACTIONS
        )
        check(
            f"{expected['plan_task_id'].lower()}_all_actions_denied",
            action_fields_ok,
            "Submission release reviewer contact and outreach are all false.",
        )
        check(
            f"{expected['plan_task_id'].lower()}_internal_disposition",
            row.get("internal_disposition") == expected["disposition"]
            and advisory_packages.get(package_id, {}).get("internal_recommendation")
            == expected["disposition"],
            f"Internal disposition is {expected['disposition']} on both surfaces.",
        )

    matrix = decisions.get("action_matrix", [])
    actual_cells = {
        (row.get("package_id"), row.get("action")): row.get("authorized")
        for row in matrix
    }
    expected_cells = {(package_id, action) for package_id in PACKAGES for action in ACTIONS}
    check(
        "matrix_exact_cartesian_domain",
        len(matrix) == 16 and set(actual_cells) == expected_cells,
        "The matrix enumerates each package-action pair exactly once.",
    )
    check(
        "matrix_all_false",
        len(actual_cells) == 16 and all(value is False for value in actual_cells.values()),
        "All sixteen explicit matrix cells are false.",
    )
    check(
        "decision_summary_counts",
        decisions.get("package_count") == 4
        and decisions.get("action_type_count") == 4
        and decisions.get("authorization_cell_count") == 16
        and decisions.get("authorized_cell_count") == 0
        and decisions.get("denied_cell_count") == 16,
        "Decision summary agrees with the explicit matrix.",
    )

    global_limits = decisions.get("global_limits", {})
    check(
        "decision_global_limits_closed",
        global_limits.get("authorship_assignment_status") == "unassigned"
        and global_limits.get("public_authorship_authorized") is False
        and global_limits.get("embargoed_distribution_authorized") is False
        and global_limits.get("reviewer_identity_publication_authorized") is False
        and global_limits.get("reviewer_report_publication_authorized") is False
        and global_limits.get("fresh_human_authority_required_for_later_version_or_action") is True,
        "All attribution distribution disclosure and future-version boundaries fail closed.",
    )
    check(
        "action_log_zero_entries",
        action_log.get("entry_count") == 0 and action_log.get("entries") == [],
        "The external-action log contains no entries.",
    )
    check(
        "action_log_all_flags_false",
        bool(action_log.get("performed_flags"))
        and all(value is False for value in action_log["performed_flags"].values()),
        "Every performed-action flag is false.",
    )
    empty_log_fields = (
        "external_systems_accessed",
        "external_people_contacted",
        "venues_selected",
        "reviewers_selected",
        "public_urls_created",
        "embargoed_distributions",
        "reviewer_identities_published",
        "reviewer_reports_published",
        "authorship_assignments",
    )
    check(
        "action_log_external_collections_empty",
        all(action_log.get(field) == [] for field in empty_log_fields),
        "All external-person system venue URL disclosure and authorship collections are empty.",
    )
    advisory_limits = advisory.get("authority_limits", {})
    check(
        "advisory_not_external_authority",
        advisory.get("review_class") == "internal_ai_advisory_same_project_context"
        and all(
            advisory_limits.get(field) is False
            for field in (
                "external_human_review",
                "independent_replication",
                "peer_review",
                "gate_chair_verdict",
                "authorship_authority",
                "external_action_authority",
                "scientific_promotion_authority",
            )
        ),
        "Internal AI review is not promoted to external human or scientific authority.",
    )
    check(
        "parent_child_outputs_complete",
        child_math.get("status") == "completed"
        and child_phil.get("status") == "completed"
        and conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflicts") == [],
        "Both child perspectives completed and the parent has no unresolved conflict.",
    )
    check(
        "child_math_exact_denial",
        child_math.get("external_action_performed_count") == 0
        and child_math.get("formalization", {}).get("cell_count") == 16
        and child_math.get("formalization", {}).get("authorized_cell_count") == 0,
        "Mathematical child records exhaustive denial and zero actions.",
    )
    check(
        "child_phil_accountability",
        child_phil.get("accountability_result", {}).get("ai_substitution_for_human_authority")
        is False
        and child_phil.get("accountability_result", {}).get("external_action_delegated_to_ai")
        is False,
        "Philosophy child preserves the non-substitution accountability boundary.",
    )
    tex = (ARTIFACTS / "p15_t07_external_action_decision_v1.tex").read_text(
        encoding="utf-8"
    )
    check(
        "tex_control_proposition_present",
        "Exact four-package no-action proposition" in tex
        and "all sixteen values" in tex
        and "% authority: science-draft" in tex,
        "Canonical task-local TeX contains the scoped control proposition and authority header.",
    )
    check(
        "tex_all_hashes_present",
        all(
            expected[hash_field] in tex
            for expected in PACKAGES.values()
            for hash_field in ("primary_sha256", "archive_sha256")
        ),
        "The TeX decision binds all eight exact SHA-256 values.",
    )
    required = manifest.get("required_task_artifacts", [])
    check(
        "manifest_required_artifacts_exist",
        len(required) == 11 and all((ROOT / path).is_file() for path in required),
        "Every task artifact required by the reproducibility manifest exists.",
    )
    invariants = manifest.get("fixed_invariants", {})
    check(
        "manifest_fixed_invariants",
        invariants.get("package_count") == 4
        and invariants.get("authorization_cell_count") == 16
        and invariants.get("authorized_cell_count") == 0
        and invariants.get("external_action_performed_count") == 0
        and invariants.get("scientific_claims_changed") is False
        and invariants.get("distance_to_gr_delta_changed") is False
        and invariants.get("physics_promotion_authorized") is False,
        "Reproducibility invariants preserve zero action and zero physics delta.",
    )

    failed = [row for row in checks if row["status"] != "PASS"]
    return {
        "schema_id": "p15_t07_no_external_action_validation_v1",
        "task_id": "RT-20260802-010",
        "job_id": "AJ-RT-20260802-010-001",
        "plan_task_id": "P15-T07",
        "generated_at": FIXED_TIME,
        "status": "PASS" if not failed else "FAIL",
        "result": (
            "PASS_EXACT_FOUR_PACKAGE_NO_EXTERNAL_ACTION_DECISION"
            if not failed
            else "FAIL_EXACT_FOUR_PACKAGE_NO_EXTERNAL_ACTION_DECISION"
        ),
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "package_count": 4,
        "action_type_count": 4,
        "authorization_cell_count": 16,
        "authorized_cell_count": 0,
        "denied_cell_count": 16,
        "external_action_performed_count": 0,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "checks": checks,
    }


def build_receipt(report_bytes: bytes, report: dict[str, Any]) -> dict[str, Any]:
    files = {
        "approval": ROOT / "research_control/approvals/approval-20260802-001.yaml",
        "human_authorization": ARTIFACTS / "human_authorization_p15_t07_no_external_action_v1.yaml",
        "decision_tex": ARTIFACTS / "p15_t07_external_action_decision_v1.tex",
        "decision_matrix": ARTIFACTS / "p15_t07_submission_claim_venue_decisions_v1.yaml",
        "external_action_log": ARTIFACTS / "p15_t07_external_action_log_v1.yaml",
        "internal_ai_advisory": ARTIFACTS / "p15_t07_internal_ai_advisory_review_v1.yaml",
        "validator": Path(__file__).resolve(),
    }
    return {
        "schema_id": "p15_t07_no_external_action_compact_receipt_v1",
        "task_id": "RT-20260802-010",
        "job_id": "AJ-RT-20260802-010-001",
        "plan_task_id": "P15-T07",
        "generated_at": FIXED_TIME,
        "status": report["status"],
        "result": report["result"],
        "check_count": report["check_count"],
        "passed_check_count": report["passed_check_count"],
        "failed_check_count": report["failed_check_count"],
        "package_count": 4,
        "authorization_cell_count": 16,
        "authorized_cell_count": 0,
        "external_action_performed_count": 0,
        "authorship_assignment_status": "unassigned",
        "external_human_review_completed": False,
        "independent_replication_completed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "validation_report_sha256": hashlib.sha256(report_bytes).hexdigest(),
        "artifact_sha256": {name: sha256(path) for name, path in files.items()},
        "authority_note": (
            "PASS validates the hash-bound all-denied control record only; it does not "
            "authorize external action or establish scientific truth."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    report_bytes = canonical_json_bytes(report)
    receipt = build_receipt(report_bytes, report)
    receipt_bytes = canonical_json_bytes(receipt)
    stored_artifacts_match = True

    if args.write_report:
        REPORT_PATH.write_bytes(report_bytes)
        RECEIPT_PATH.write_bytes(receipt_bytes)

    if args.check:
        stored_artifacts_match = (
            REPORT_PATH.is_file()
            and RECEIPT_PATH.is_file()
            and REPORT_PATH.read_bytes() == report_bytes
            and RECEIPT_PATH.read_bytes() == receipt_bytes
        )

    output = dict(report)
    output["stored_artifacts_match"] = stored_artifacts_match
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(
            f"{output['status']}: {output['passed_check_count']}/"
            f"{output['check_count']} checks; stored_artifacts_match={stored_artifacts_match}"
        )
    return 0 if report["status"] == "PASS" and stored_artifacts_match else 1


if __name__ == "__main__":
    raise SystemExit(main())

