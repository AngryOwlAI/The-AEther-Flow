#!/usr/bin/env python3
"""Validate the bounded P2-T08 blinded selector-theorem review packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
REPORT_PATH = ARTIFACT_DIR / "eqsrc_selector_theorem_review_validation.json"

PATHS = {
    "theorem": ROOT / "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex",
    "finite_atlas": ROOT / "research_control/tasks/RT-20260720-017/artifacts/eqsrc_finite_countermodel_atlas_v1.tex",
    "lean_source": ROOT / "research_control/tasks/RT-20260720-018/artifacts/proof/SelectorKernel.lean",
    "audit": ROOT / "research_control/tasks/RT-20260720-019/artifacts/eqsrc_selector_theorem_smuggling_audit_v1.tex",
    "stress": ROOT / "research_control/tasks/RT-20260720-020/artifacts/eqsrc_selector_theorem_refuter_stress_v1.tex",
    "blind_packet": ARTIFACT_DIR / "eqsrc_selector_theorem_blind_review_packet_v1.md",
    "child_phys_math": ARTIFACT_DIR / "child_phys_math_eqsrc_selector_theorem_review.yaml",
    "child_phys_phil": ARTIFACT_DIR / "child_phys_phil_eqsrc_selector_theorem_review.yaml",
    "fresh_context_different_model": ARTIFACT_DIR / "fresh_context_different_model_eqsrc_selector_theorem_review.yaml",
    "disagreement_matrix": ARTIFACT_DIR / "eqsrc_selector_theorem_review_disagreement_matrix.yaml",
    "fused_review": ARTIFACT_DIR / "eqsrc_selector_theorem_external_red_team_review_v1.yaml",
    "human_review_acquisition": ARTIFACT_DIR / "eqsrc_selector_theorem_independent_human_review_acquisition.yaml",
    "compact_receipt": ARTIFACT_DIR / "eqsrc_selector_theorem_review_compact_receipt.json",
}

EXPECTED_HASHES = {
    "theorem": "d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae",
    "finite_atlas": "4a7c84ecf769b19e92b2b2dffd7224ddd4e1e02e4cc93cff797d01fa0e1bc62b",
    "lean_source": "6f23c92d72779e4fc5b13f56b34a8709ece2dfec27f7ce767170ed54d3d9f356",
    "audit": "d093d7b0afbe322cf537644de54f17156ea2427fcc0988f4fc8fb305e93a0f76",
    "stress": "d519bcc9534af3b2ca3e3d44604bd56bf72c425e0d06322c33cc7e66abfd2b49",
    "blind_packet": "07cd421844f3317985f54660311b34bd92bdd6eed621a3d3b5aca28f73706a2e",
    "child_phys_math": "d38748ebf3bfee7c1a3d16aac11d07bbd321f6b4e9deb24a7c7b4877636549ff",
    "child_phys_phil": "bc10ed35f6fe34bf4e3b3520694c64ae36d1fb5d5bd8c3e21641c292fcad78f4",
    "fresh_context_different_model": "24cc23ccc7671f28bfa9d7dc9ecd493d1a8d2d989354a9a942e886c7dd0596b8",
    "disagreement_matrix": "66a6bed029cd46b31a1a0210f9ffa2730385ddc00c181a5d1a718ddf5773fbba",
    "fused_review": "25e8e0ec587c72c3d2d7f2269ba2646986828393054f98ce4e82dc9da5b52645",
    "human_review_acquisition": "c887206755ccabca92096c6118e6a71e3e95594d28909f7239b49cde0fbf2d80",
}

EXPECTED_VERDICT = "no_blocking_defect_found_as_written"
BLIND_FORBIDDEN_TOKENS = (
    "P2-T0",
    "handoff-",
    "result_classification",
    "theorem_survives",
    "validation_status:",
    "route_label:",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a YAML mapping")
    return value


def add_check(checks: list[dict[str, object]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})


def provenance_text(document: dict[str, object]) -> str:
    return json.dumps(document.get("reviewer_provenance", {}), sort_keys=True).lower()


def validate() -> dict[str, object]:
    checks: list[dict[str, object]] = []

    for name, expected in EXPECTED_HASHES.items():
        path = PATHS[name]
        actual = sha256(path) if path.is_file() else "missing"
        add_check(checks, f"hash_{name}", actual == expected, f"expected={expected} actual={actual}")

    blind_text = PATHS["blind_packet"].read_text(encoding="utf-8")
    leaked = [token for token in BLIND_FORBIDDEN_TOKENS if token in blind_text]
    add_check(checks, "blind_packet_context_stripping", not leaked, f"forbidden tokens={leaked}")
    add_check(checks, "blind_packet_nonclaim_boundary", "## Explicit nonclaims" in blind_text, "nonclaims present")
    add_check(checks, "blind_packet_response_contract", "## Response contract" in blind_text, "review requirements present")

    child_names = ("child_phys_math", "child_phys_phil", "fresh_context_different_model")
    child_docs = {name: load_yaml(PATHS[name]) for name in child_names}
    for name, document in child_docs.items():
        add_check(checks, f"{name}_verdict", document.get("verdict") == EXPECTED_VERDICT, str(document.get("verdict")))
        add_check(checks, f"{name}_promotion_false", document.get("physics_promotion_authorized") is False, "must be false")
        text = provenance_text(document)
        nonhuman = "human_status" in text and any(
            phrase in text for phrase in ("not human", "non-human", "no human")
        )
        not_external = any(
            phrase in text
            for phrase in (
                "not external replication",
                "not an external replication",
                "neither external human review nor independent replication",
            )
        )
        add_check(checks, f"{name}_nonhuman", nonhuman, text[:500])
        add_check(checks, f"{name}_not_external_replication", not_external, text[:500])
        add_check(checks, f"{name}_blind_file_scope", "eqsrc_selector_theorem_blind_review_packet_v1.md" in text, "blind packet is the declared file input")

    matrix = load_yaml(PATHS["disagreement_matrix"])
    add_check(checks, "matrix_three_arms", len(matrix.get("review_arms", [])) == 3, "three review arms")
    add_check(checks, "matrix_no_unresolved", matrix.get("unresolved_conflicts") == [], "no unresolved conflicts")
    add_check(checks, "matrix_external_false", matrix.get("actual_external_human_review_completed") is False, "must be false")
    add_check(checks, "matrix_preserves_differences", len(matrix.get("preserved_differences", [])) >= 4, "at least four preserved differences")

    fused = load_yaml(PATHS["fused_review"])
    required_fused = {
        "reviewed_object_id", "reviewed_source_paths", "claim_under_review",
        "assumptions_read", "definitions_read", "proof_steps_checked",
        "circularity_findings", "hidden_import_findings",
        "notation_overload_findings", "unproven_equivalence_findings",
        "minimal_countermodel_attempt", "external_mathematical_pressure_points",
        "verdict", "recommended_next_route", "physics_promotion_authorized",
    }
    add_check(checks, "fused_required_fields", required_fused.issubset(fused), f"missing={sorted(required_fused - set(fused))}")
    add_check(checks, "fused_verdict", fused.get("verdict") == EXPECTED_VERDICT, str(fused.get("verdict")))
    add_check(checks, "fused_promotion_false", fused.get("physics_promotion_authorized") is False, "must be false")
    review_provenance = fused.get("reviewer_provenance", {})
    add_check(checks, "fused_external_false", isinstance(review_provenance, dict) and review_provenance.get("actual_external_human_review_completed") is False, "external review absent")
    findings = fused.get("finding_dispositions", {})
    add_check(checks, "fused_no_blocking_defects", isinstance(findings, dict) and findings.get("blocking_defect_count") == 0, "zero blocking defects")
    authority = fused.get("authority_boundary", {})
    add_check(checks, "fused_protected_authority_false", isinstance(authority, dict) and all(value is False for value in authority.values()), "all protected authority fields false")

    acquisition = load_yaml(PATHS["human_review_acquisition"])
    add_check(checks, "acquisition_external_false", acquisition.get("genuine_external_human_review_completed") is False, "no manufactured external completion")
    add_check(checks, "acquisition_no_outreach", acquisition.get("external_outreach_performed") is False, "no outreach performed")
    action = acquisition.get("precise_human_action", {})
    add_check(checks, "acquisition_precise_action", isinstance(action, dict) and bool(action.get("action")) and len(action.get("acceptance_evidence", [])) >= 6, "action plus receipt criteria")
    add_check(checks, "acquisition_promotion_false", acquisition.get("physics_promotion_authorized") is False, "must be false")

    compact = json.loads(PATHS["compact_receipt"].read_text(encoding="utf-8"))
    add_check(checks, "compact_result_parity", compact.get("result_status") == EXPECTED_VERDICT, str(compact.get("result_status")))
    add_check(checks, "compact_review_count", compact.get("review_arm_count") == 3, "three arms")
    add_check(checks, "compact_external_false", compact.get("actual_external_human_review_completed") is False, "must be false")
    compact_hashes = compact.get("source_hashes", {})
    add_check(checks, "compact_hash_parity", isinstance(compact_hashes, dict) and all(compact_hashes.get(name) == expected for name, expected in EXPECTED_HASHES.items()), "all fixed hashes copied exactly")
    add_check(checks, "compact_promotion_false", compact.get("physics_promotion_authorized") is False, "must be false")

    failures = [check for check in checks if check["status"] != "PASS"]
    return {
        "schema_id": "eqsrc-selector-theorem-review-validation.v1",
        "status": "PASS" if not failures else "FAIL",
        "task_id": "RT-20260720-021",
        "plan_task_id": "P2-T08",
        "result_status": EXPECTED_VERDICT,
        "check_count": len(checks),
        "failed_check_count": len(failures),
        "blind_review_count": len(child_docs),
        "actual_external_human_review_completed": False,
        "precise_human_action_recorded": True,
        "recommended_next_route": "P3-T01",
        "physics_promotion_authorized": False,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        passed = report["check_count"] - report["failed_check_count"]
        print(f"{report['status']}: {passed}/{report['check_count']} checks")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
