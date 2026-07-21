#!/usr/bin/env python3
"""Validate the bounded v21 P1-T03 EqSrc family-freeze decision packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

import yaml


ARTIFACT_DIR = Path(__file__).resolve().parent
REPO_ROOT = ARTIFACT_DIR.parents[3]
DECISION_PATH = ARTIFACT_DIR / "eqsrc_canonical_choice_family_freeze_decision.yaml"
MANIFEST_PATH = ARTIFACT_DIR / "eqsrc_canonical_choice_family_freeze_manifest.yaml"
CHILD_MATH_PATH = ARTIFACT_DIR / "child_phys_math_eqsrc_canonical_choice_family_freeze.yaml"
CHILD_PHIL_PATH = ARTIFACT_DIR / "child_phys_phil_eqsrc_canonical_choice_family_freeze.yaml"
CONFLICT_PATH = ARTIFACT_DIR / "parent_conflict_review_eqsrc_canonical_choice_family_freeze.yaml"
FUSION_PATH = ARTIFACT_DIR / "parent_fusion_notes_eqsrc_canonical_choice_family_freeze.md"
REPORT_PATH = ARTIFACT_DIR / "eqsrc_canonical_choice_family_freeze_validation.json"

EXPECTED_FAMILIES = {
    "EQSRC-CANONICAL-CHOICE-INTRINSIC-DISCRIMINATOR": {
        "EQSRC-IDISC-V1", "EQSRC-IDISC-V2", "EQSRC-IDISC-V3"
    },
    "EQSRC-CANONICAL-CHOICE-CYCLE-BOUNDARY-LINE": {"EQSRC-CYCLE-BOUNDARY-V1"},
    "EQSRC-CANONICAL-CHOICE-ORIENTATION-TORSOR": {"EQSRC-ORIENTATION-TORSOR-V1"},
    "EQSRC-CANONICAL-CHOICE-ROOTED-PARTITION": {"EQSRC-ROOTED-PARTITION-V1"},
    "EQSRC-CANONICAL-CHOICE-GRADED-ORBIT-ROOT": {"EQSRC-GRADED-ORBIT-ROOT-V1"},
}
EXPECTED_ROUTE_CLASSES = {
    "general_theorem",
    "current_ontology_derivation",
    "physical_irrelevance_theorem",
    "material_ledger_delta",
}
EXPECTED_REOPENING_CLASSES = EXPECTED_ROUTE_CLASSES | {"human_gate"}
THEOREM_TARGET = "EQSRC-CANONICAL-SELECTION-NATURALITY-TARGET-V1"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected mapping: {path}")
    return payload


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def validate() -> dict[str, Any]:
    decision = load_yaml(DECISION_PATH)
    manifest = load_yaml(MANIFEST_PATH)
    child_math = load_yaml(CHILD_MATH_PATH)
    child_phil = load_yaml(CHILD_PHIL_PATH)
    conflict = load_yaml(CONFLICT_PATH)
    fusion = FUSION_PATH.read_text(encoding="utf-8")

    errors: list[str] = []
    checks: list[dict[str, Any]] = []

    def record(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail}
        )
        if not passed:
            errors.append(f"{check_id}: {detail}")

    families = manifest.get("families", [])
    family_map = {
        str(item.get("family_id", "")): set(item.get("member_candidate_ids", []))
        for item in families
    }
    candidate_ids = set().union(*family_map.values()) if family_map else set()
    record(
        "family_and_candidate_identity",
        family_map == EXPECTED_FAMILIES and len(candidate_ids) == 7,
        f"families={len(family_map)} candidates={len(candidate_ids)}",
    )

    freeze_labels = [str(item.get("scoped_freeze_label", "")) for item in families]
    freeze_ids = [str(item.get("member_freeze_id", "")) for item in families]
    labels_ok = (
        len(freeze_labels) == len(set(freeze_labels)) == 5
        and all(label.startswith("EQSRC-FAMILY-FREEZE-") for label in freeze_labels)
        and len(freeze_ids) == len(set(freeze_ids)) == 5
        and all(identifier.startswith("FRZ-RT-20260720-011-") for identifier in freeze_ids)
        and manifest.get("freeze_record_id")
        == "FRZ-RT-20260720-011-EQSRC-CANONICAL-CHOICE-SUPERFAMILY"
    )
    record("freeze_labels_unique_and_scoped", labels_ok, f"labels={len(set(freeze_labels))}")

    dispositions_ok = all(
        item.get("qualification_result") == "fail"
        and item.get("final_disposition") == "family_locally_frozen"
        and item.get("materially_distinct_selector_resolution") is False
        for item in families
    )
    record("all_exact_families_frozen", dispositions_ok, "expected five failed family routes")

    qualification = manifest.get("qualification_test", {})
    route_classes = set(qualification.get("qualifying_route_classes", []))
    next_route = manifest.get("next_allowed_route", {})
    qualification_ok = (
        route_classes == EXPECTED_ROUTE_CLASSES
        and next_route.get("plan_task_id") == "P1-T04"
        and next_route.get("route_id") == THEOREM_TARGET
        and next_route.get("route_class") == "general_theorem"
        and next_route.get("materially_distinct") is True
        and next_route.get("constructs_theorem_now") is False
    )
    record("qualification_and_distinct_route", qualification_ok, str(next_route.get("route_id")))

    barred_routes = manifest.get("barred_routes", [])
    barred_ok = (
        len(barred_routes) >= 5
        and len({item.get("route_id") for item in barred_routes}) == len(barred_routes)
        and all(item.get("match_rule") and item.get("disposition") for item in barred_routes)
    )
    record("barred_routes_machine_readable", barred_ok, f"routes={len(barred_routes)}")

    reopening = manifest.get("reopening_criteria", [])
    reopening_classes = {item.get("qualification_class") for item in reopening}
    reopening_ok = (
        reopening_classes == EXPECTED_REOPENING_CLASSES
        and len({item.get("criterion_id") for item in reopening}) == len(reopening)
        and all(item.get("evidence_required") and item.get("opens") for item in reopening)
    )
    record("reopening_criteria_explicit", reopening_ok, f"criteria={len(reopening)}")

    theoretical = decision.get("theoretical_decision_output", {})
    target = decision.get("general_selector_theorem_target", {})
    target_ok = (
        theoretical.get("selected_next_packet_type") == "ontology_law_research_packet"
        and theoretical.get("route_label") == "ontology-law-research-packet"
        and theoretical.get("selected_next_plan_task") == "P1-T04"
        and theoretical.get("next_execution_role_family") == "ontology-formalizer@0.2.0"
        and theoretical.get("selected_theorem_target_id") == THEOREM_TARGET
        and theoretical.get("adoption_status") == "blocked_adoption_open_continuation"
        and theoretical.get("requires_human_gate") is False
        and target.get("theorem_target_id") == THEOREM_TARGET
        and target.get("proof_status") == "not_formalized"
        and target.get("theorem_proved") is False
        and target.get("authorized_now") is False
    )
    record("single_theoretical_route_decision", target_ok, str(theoretical.get("selected_next_plan_task")))

    branches = set(target.get("theorem_branches_to_state", []))
    target_interface_ok = (
        any("no fixed point" in branch for branch in branches)
        and any("multiple fixed points" in branch for branch in branches)
        and any("choice irrelevance" in branch for branch in branches)
        and any("relation-unique" in branch for branch in branches)
        and len(target.get("formal_objects_to_define", [])) >= 7
    )
    record("theorem_target_interface", target_interface_ok, f"branches={len(branches)}")

    source_hash_errors = 0
    for item in decision.get("source_evidence", []):
        path = REPO_ROOT / str(item.get("path", ""))
        if not path.is_file() or file_sha256(path) != item.get("sha256"):
            source_hash_errors += 1
    record("source_evidence_hashes", source_hash_errors == 0, f"mismatches={source_hash_errors}")

    ledger = decision.get("ledger_evidence", {})
    ledger_errors = 0
    for path_key, hash_key in (
        ("distance_to_gr_path", "distance_to_gr_sha256"),
        ("metric_use_path", "metric_use_sha256"),
    ):
        path = REPO_ROOT / str(ledger.get(path_key, ""))
        if not path.is_file() or file_sha256(path) != ledger.get(hash_key):
            ledger_errors += 1
    record(
        "scientific_ledgers_unchanged",
        ledger_errors == 0 and ledger.get("changed") is False and ledger.get("effect") == "no_distance_delta",
        f"mismatches={ledger_errors}",
    )

    authority = decision.get("authority_boundary", {})
    manifest_authority = manifest.get("authority_boundary", {})
    authority_ok = (
        authority.get("family_freeze_authorized") is True
        and authority.get("theorem_construction_authorized") is False
        and authority.get("canonical_ontology_edit_authorized") is False
        and authority.get("source_law_adoption_authorized") is False
        and authority.get("source_law_rejection_authorized") is False
        and authority.get("general_eqsrc_discharged") is False
        and authority.get("distance_to_gr_delta_changed") is False
        and authority.get("physics_promotion_authorized") is False
        and authority.get("proof_authority") is False
        and manifest_authority.get("global_theory_rejection") is False
        and manifest_authority.get("future_source_extension_impossibility") is False
    )
    record("claim_and_authority_boundary", authority_ok, "local freeze only; promotion false")

    child_ok = (
        child_math.get("status") == "completed"
        and len(child_math.get("family_findings", [])) == 5
        and child_math.get("p1_t04_evaluation", {}).get("qualifies") is True
        and child_phil.get("status") == "completed"
        and child_phil.get("verdict", {}).get("continuation_decision") == "route_to_p1_t04"
        and conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflicts") == []
    )
    record("parent_child_synthesis", child_ok, "two children completed; conflicts resolved")

    fusion_tokens = [
        "locally freeze all five stable",
        THEOREM_TARGET,
        "no-fixed-point obstruction",
        "not candidate rejection",
        "No canonical ontology",
    ]
    missing_fusion_tokens = [token for token in fusion_tokens if token not in fusion]
    record("fusion_boundary", not missing_fusion_tokens, f"missing={missing_fusion_tokens}")

    status = "PASS" if not errors else "FAIL"
    return {
        "schema_id": "v21_p1_t03_eqsrc_canonical_choice_family_freeze_validation_v1",
        "task_id": "RT-20260720-011",
        "job_id": "AJ-RT-20260720-011-001",
        "status": status,
        "operational_evidence_only": True,
        "physics_proof_authority": False,
        "physics_promotion_authorized": False,
        "counts": {
            "families_frozen": len(families),
            "candidates_frozen": len(candidate_ids),
            "barred_routes": len(barred_routes),
            "reopening_criteria": len(reopening),
            "qualifying_next_routes": 1,
            "errors": len(errors),
        },
        "artifact_hashes": {
            "decision": file_sha256(DECISION_PATH),
            "freeze_manifest": file_sha256(MANIFEST_PATH),
            "child_phys_math": file_sha256(CHILD_MATH_PATH),
            "child_phys_phil": file_sha256(CHILD_PHIL_PATH),
            "conflict_review": file_sha256(CONFLICT_PATH),
            "fusion_notes": file_sha256(FUSION_PATH),
        },
        "checks": checks,
        "errors": errors,
        "claim_boundary_summary": "PASS validates a scoped family freeze and one P1-T04 theorem-target route only. It is not proof, ontology adoption or rejection, general EqSrc discharge, ledger progress, downstream GR, or promotion authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        atomic_write_json(REPORT_PATH, report)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']}: {report['counts']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
