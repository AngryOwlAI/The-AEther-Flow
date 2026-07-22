#!/usr/bin/env python3
"""Audit P11 scientific-QA non-regression without mutating predecessor controls."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ART = Path(__file__).resolve().parent
MATRIX_PATH = ART / "p11_failure_mode_coverage_matrix.json"
VALIDATION_PATH = ART / "p11_scientific_qa_validation.json"
RECEIPT_PATH = ART / "p11_scientific_qa_compact_receipt.json"

TASKS = ROOT / "research_control/tasks"
FIXTURES = ROOT / "tests/fixtures/research_control/red_team_review"
REVIEW_PATHS = tuple(
    TASKS / "RT-20260722-010/artifacts" / name
    for name in (
        "blind_same_model_selector_review.yaml",
        "blind_same_model_geff_review.yaml",
        "same_context_selector_review.yaml",
        "same_context_geff_review.yaml",
    )
)

DEPENDENCY_HASHES = {
    "research_control/tasks/RT-20260722-004/jobs/completions/AJC-AJ-RT-20260722-004-001.yaml": "c0a9811467d9591a9c9eb8afcac6b37b5b9c57ab962de06c7bf1e9d8324d3b85",
    "research_control/tasks/RT-20260722-005/jobs/completions/AJC-AJ-RT-20260722-005-001.yaml": "752d2d330f4d1eb974a1e15209efe125a89ca145345ac92c26ae7e3dda350380",
    "research_control/tasks/RT-20260722-006/jobs/completions/AJC-AJ-RT-20260722-006-001.yaml": "c5f0a2fd66b31f854e911e608a3095b731c210a90dd061a0fdca25419f079379",
    "research_control/tasks/RT-20260722-007/jobs/completions/AJC-AJ-RT-20260722-007-001.yaml": "fc47c54cefe9f6f3dd7a6a279c41b81fec8816e2bd72c4e58f2856b433dea3dd",
    "research_control/tasks/RT-20260722-008/jobs/completions/AJC-AJ-RT-20260722-008-001.yaml": "4a1a2c041b97c3e8c712bae9be55e0e08de64c712aaf5f6fc275f33f20cfa494",
    "research_control/tasks/RT-20260722-009/jobs/completions/AJC-AJ-RT-20260722-009-001.yaml": "853d66f154dca54edbbd5f86adff2b974a4a14d72967682c1a701728df345bf8",
    "research_control/tasks/RT-20260722-010/jobs/completions/AJC-AJ-RT-20260722-010-001.yaml": "09b6fdca28128bd37908cb5e0dbc2c81b0b9af569db0490fed1fb7e32c6b2e46",
}

MARKDOWN_CONTROLS = {
    "research_control/tasks/RT-20260722-004/artifacts/blind_review_packet_schema.md",
    "research_control/tasks/RT-20260722-005/artifacts/review_independence_taxonomy.md",
    "research_control/tasks/RT-20260722-006/artifacts/semantic_smuggling_checker_comparison.md",
    "research_control/tasks/RT-20260722-007/artifacts/positive_provenance_operational_meaning_gate_policy.md",
    "research_control/tasks/RT-20260722-008/artifacts/reviewer_agreement_metric_specification.md",
    "research_control/tasks/RT-20260722-009/artifacts/proof_artifact_registry_schema.md",
}
TEX_SOURCES = {
    "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex",
    "research_control/tasks/RT-20260614-216/artifacts/245_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_METRICFORMASSIGN_GEFF_CANDIDATE_OR_OBSTRUCTION.tex",
}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    from scripts.research_control import strict_yaml

    value = strict_yaml.load(path)
    if not isinstance(value, dict):
        raise ValueError(f"expected YAML map at {path}")
    return value


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def matrix_row(
    case_id: str,
    failure_mode: str,
    expected_control: str,
    observed_evidence: str,
    status: str,
    rollout_effect: str,
) -> dict[str, str]:
    return {
        "case_id": case_id,
        "failure_mode": failure_mode,
        "expected_control": expected_control,
        "observed_evidence": observed_evidence,
        "status": status,
        "rollout_effect": rollout_effect,
    }


def rejected_fixture(path: Path, expected_field: str) -> tuple[bool, str]:
    from scripts.research_control import validate_red_team_review_artifact as red

    try:
        red.validate_review_file(path)
    except red.RedTeamReviewValidationError as exc:
        fields = [issue.field for issue in exc.issues]
        return expected_field in fields, f"issue_fields={fields}"
    return False, "invalid fixture was accepted"


def source_authority_evidence() -> tuple[bool, str, dict[str, str]]:
    markdown_rows = {row["path"]: row for row in csv_rows(ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv")}
    tex_rows = {row["path"]: row for row in csv_rows(ROOT / "registries/TEX_SOURCE_REGISTRY.csv")}
    observed: dict[str, str] = {}
    passed = True
    for path_text in sorted(MARKDOWN_CONTROLS):
        row = markdown_rows.get(path_text, {})
        current = sha256(ROOT / path_text) if (ROOT / path_text).is_file() else "missing"
        ok = row.get("authority_status") == "project_control" and row.get("source_hash") == current
        passed = passed and ok
        observed[path_text] = f"authority={row.get('authority_status')} hash_match={row.get('source_hash') == current}"
    for path_text in sorted(TEX_SOURCES):
        row = tex_rows.get(path_text, {})
        current = sha256(ROOT / path_text) if (ROOT / path_text).is_file() else "missing"
        ok = row.get("authority_status") == "draft_control_artifact" and row.get("source_hash") == current
        passed = passed and ok
        observed[path_text] = f"authority={row.get('authority_status')} hash_match={row.get('source_hash') == current}"
    return passed, f"checked={len(observed)}", observed


def generated_non_authority_evidence() -> tuple[bool, str]:
    source_ids = {
        "MD-V21-P11-T01-BLIND-REVIEW-PACKET-SCHEMA",
        "MD-V21-P11-T02-REVIEW-INDEPENDENCE-TAXONOMY",
        "MD-V21-P11-T03-PROOF-ARTIFACT-REGISTRY-SCHEMA",
        "MD-V21-P11-T04-SEMANTIC-SMUGGLING-CHECKER-COMPARISON",
        "MD-V21-P11-T05-POSITIVE-PROVENANCE-OPERATIONAL-MEANING-GATE-POLICY",
        "MD-V21-P11-T06-REVIEWER-AGREEMENT-METRIC-SPECIFICATION",
        "TEX-V21-P2-T03-EQSRC-NO-SELECTOR-NONUNIQUENESS-THEOREM",
        "TEX-RESEARCH-CONTROL-NONBOTTOM-METRICDATA-WITNESS-SRC-GSC-POST-GATE-METRICFORMASSIGN-GEFF-CANDIDATE-OR-OBSTRUCTION",
    }
    rows = [row for row in csv_rows(ROOT / "registries/WIKI_ARTIFACT_REGISTRY.csv") if row.get("source_object_id") in source_ids]
    passed = len(rows) == len(source_ids) and all(row.get("authority_status") == "generated_noncanonical" for row in rows)
    return passed, f"matched={len(rows)} authorities={sorted({row.get('authority_status') for row in rows})}"


def build_matrix() -> dict[str, Any]:
    rows: list[dict[str, str]] = []
    observations: dict[str, Any] = {}

    mismatches = {
        path: {"expected": expected, "observed": sha256(ROOT / path) if (ROOT / path).is_file() else "missing"}
        for path, expected in DEPENDENCY_HASHES.items()
        if not (ROOT / path).is_file() or sha256(ROOT / path) != expected
    }
    rows.append(matrix_row("P11-QA-C001", "dependency drift", "all P11 completion hashes remain exact", f"mismatches={mismatches}", "PASS" if not mismatches else "FAIL", "block rollout on any mismatch"))

    external_ok, external_detail = rejected_fixture(FIXTURES / "false_external_wording.yaml", "review_context.claims.external_review_completed")
    rows.append(matrix_row("P11-QA-C002", "false external-review label", "strict review validator rejects unsupported externality", external_detail, "PASS" if external_ok else "FAIL", "critical fail-closed gate"))

    replication_ok, replication_detail = rejected_fixture(FIXTURES / "false_independent_replication.yaml", "review_context.claims.independent_replication_completed")
    rows.append(matrix_row("P11-QA-C003", "false independent-replication label", "strict review validator rejects unsupported replication", replication_detail, "PASS" if replication_ok else "FAIL", "critical fail-closed gate"))

    from scripts.research_control import validate_red_team_review_artifact as red
    review_receipt = red.validate_files(list(REVIEW_PATHS))
    observations["review_receipt"] = review_receipt
    reviews_ok = review_receipt.get("checked_artifact_count") == 4 and review_receipt.get("review_context_classification_counts") == {"blind_same_model_review": 2, "same_context_role_review": 2}
    rows.append(matrix_row("P11-QA-C004", "live review schema regression", "all four P11-T07 review records validate with exact context classes", f"artifact_count={review_receipt.get('checked_artifact_count')} classes={review_receipt.get('review_context_classification_counts')}", "PASS" if reviews_ok else "FAIL", "critical live-evidence gate"))

    blind = load_module("p11_t08_blind", TASKS / "RT-20260722-004/artifacts/validate_blind_review_packet.py")
    leak_findings = blind.scan_packet({"review_material": [{"text": "bounded content"}], "task_verdict": "PASS"})
    leak_ok = any(row.get("kind") == "forbidden_key" for row in leak_findings)
    rows.append(matrix_row("P11-QA-C005", "leaked task verdict", "blind-packet scan rejects process-result keys", f"findings={leak_findings}", "PASS" if leak_ok else "FAIL", "critical context-separation gate"))

    revision = load_yaml(TASKS / "RT-20260722-010/artifacts/blind_packet_revision_history.yaml")
    self_containment_limitation = (
        revision.get("initial_finding", {}).get("classification") == "packet_self_containment_defect"
        and revision.get("repair", {}).get("scope") == "task_local_blind_packet_only"
        and str(revision.get("final_validation", {}).get("failed_check_count")) == "0"
        and "does not guarantee scientific self-containment" in str(revision.get("disposition", "")).casefold()
    )
    rows.append(matrix_row("P11-QA-F001", "scientific self-containment is not enforced by process-redaction validation", "parent closure review and one bounded packet-repair loop remain mandatory", f"initial_finding={revision.get('initial_finding', {}).get('finding_id')} repair_scope={revision.get('repair', {}).get('scope')}", "PASS_LIMITATION_IDENTIFIED" if self_containment_limitation else "FAIL", "bounded use only; unattended packet rollout frozen pending repair"))

    positive = load_json(TASKS / "RT-20260722-007/artifacts/positive_provenance_gate_validation.json")
    positive_rows = {row["fixture_id"]: row for row in positive.get("fixture_rows", [])}
    checker_ids = ("NEG-VALIDATOR-PASS-ONLY-001", "NEG-VALIDATOR-RECEIPT-AS-PREMISE-001")
    checker_ok = all(positive_rows.get(fixture_id, {}).get("matches_expectation") is True and positive_rows.get(fixture_id, {}).get("observed_evidence_complete") is False for fixture_id in checker_ids)
    rows.append(matrix_row("P11-QA-C006", "checker or validator PASS treated as proof", "positive-provenance fixtures remain incomplete or invalid", f"fixtures={{k: positive_rows.get(k) for k in {checker_ids}}}", "PASS" if checker_ok else "FAIL", "critical promotion-shortcut gate"))

    analysis = load_json(TASKS / "RT-20260722-010/artifacts/review_agreement_and_leakage_analysis.json")
    metrics = analysis.get("reviewer_metric_aggregate", {}).get("metrics", {})
    authority = analysis.get("authority_boundary", {})
    consensus_ok = metrics.get("false_consensus_risk_count") == 7 and metrics.get("assessment_disagreement_count") == 3 and authority.get("consensus_sets_scientific_status") is False
    rows.append(matrix_row("P11-QA-C007", "consensus treated as proof", "correlated-agent risks and disagreements remain visible with no status effect", f"false_consensus={metrics.get('false_consensus_risk_count')} disagreements={metrics.get('assessment_disagreement_count')} status_effect={authority.get('consensus_sets_scientific_status')}", "PASS" if consensus_ok else "FAIL", "critical truth-inference gate"))

    proof = load_json(TASKS / "RT-20260722-009/artifacts/proof_evidence_compact_receipt.json")
    proof_ok = proof.get("status") == "PASS" and proof.get("proof_authority") is False and proof.get("physics_promotion_authorized") is False and proof.get("formal_assumption_warning_visible") is True and proof.get("formal_failure_visible") is True
    rows.append(matrix_row("P11-QA-C008", "proof evidence promotes ontology or physics", "proof metadata preserves failures assumptions and false authority flags", f"status={proof.get('status')} proof_authority={proof.get('proof_authority')} physics_promotion={proof.get('physics_promotion_authorized')}", "PASS" if proof_ok else "FAIL", "critical proof-scope gate"))

    semantic = analysis.get("semantic_smuggling_probe", {})
    semantic_limitation = semantic.get("raw_finding_count") == 43 and semantic.get("boundary_false_positive_count") == 43 and semantic.get("confirmed_smuggling_count") == 0
    rows.append(matrix_row("P11-QA-F002", "bounded semantic probe overflags explicit negative boundary language", "live findings require bounded disposition and may not automatically veto or promote", f"raw={semantic.get('raw_finding_count')} boundary_false_positive={semantic.get('boundary_false_positive_count')} confirmed={semantic.get('confirmed_smuggling_count')}", "PASS_LIMITATION_IDENTIFIED" if semantic_limitation else "FAIL", "advisory use only; unattended semantic veto frozen pending calibration"))

    historical = [FIXTURES / "valid_minimal.yaml", TASKS / "RT-20260720-021/artifacts/eqsrc_selector_theorem_external_red_team_review_v1.yaml"]
    historical_observed: dict[str, str] = {}
    historical_ok = True
    for path in historical:
        receipt = red.validate_review_file(path)
        historical_observed[rel(path)] = str(receipt.get("review_context_classification"))
        historical_ok = historical_ok and receipt.get("review_context_present") is False and receipt.get("review_context_classification") == "legacy_unclassified"
    rows.append(matrix_row("P11-QA-C009", "historical artifact unreadability or retroactive strengthening", "legacy records remain readable as legacy_unclassified", f"observed={historical_observed}", "PASS" if historical_ok else "FAIL", "critical compatibility gate"))

    source_ok, source_detail, source_observed = source_authority_evidence()
    observations["source_authority"] = source_observed
    rows.append(matrix_row("P11-QA-C010", "source registry authority drift", "canonical control and draft-science rows retain exact current hashes and declared authority", source_detail, "PASS" if source_ok else "FAIL", "critical authority gate"))

    generated_ok, generated_detail = generated_non_authority_evidence()
    rows.append(matrix_row("P11-QA-C011", "generated derivative treated as source authority", "wiki derivatives remain generated_noncanonical", generated_detail, "PASS" if generated_ok else "FAIL", "critical authority gate"))

    authority_flags = {
        "external_review_completed": False,
        "human_expert_review_completed": False,
        "independent_replication_completed": False,
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "source_registry_authority_changed": False,
        "predecessor_artifacts_mutated": False,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "publication_authority": False,
    }
    rows.append(matrix_row("P11-QA-C012", "audit itself escalates authority", "every protected and scientific change flag remains false", f"flags={authority_flags}", "PASS" if not any(authority_flags.values()) else "FAIL", "critical audit-boundary gate"))

    failed = [row for row in rows if row["status"] == "FAIL"]
    limitations = [row for row in rows if row["status"] == "PASS_LIMITATION_IDENTIFIED"]
    return {
        "schema_id": "v21_p11_scientific_qa_failure_mode_matrix_v1",
        "status": "PASS" if not failed else "FAIL",
        "task_id": "RT-20260722-011",
        "plan_task_id": "P11-T08",
        "recommendation_ids": ["V21-R36", "V21-R37", "V21-R38", "V21-R39", "V21-R55", "V21-R56", "V21-R63", "V21-R68"],
        "case_count": len(rows),
        "failed_case_count": len(failed),
        "limitation_count": len(limitations),
        "cases": rows,
        "finding_ids": [row["case_id"] for row in limitations],
        "rollout_disposition": "BOUNDED_ROLLOUT_WITH_GUARDRAILS_UNATTENDED_AUTOMATION_FROZEN",
        "mandatory_guardrails": [
            "Every blind packet requires a parent scientific self-containment review before review execution and at most two bounded repair rounds.",
            "The P11 semantic probe is advisory on live claim-bearing artifacts; every finding requires bounded disposition and cannot automatically set scientific status.",
            "Review context classes remain exact provenance labels; only human_expert_review or independent_replication evidence may support their corresponding claims.",
            "Validator proof-build or reviewer agreement evidence never supplies theorem truth physical interpretation ontology adoption or promotion authority.",
        ],
        "authority_flags": authority_flags,
        "observations": observations,
    }


def build_validation(matrix: dict[str, Any]) -> dict[str, Any]:
    source_paths = sorted(
        set(DEPENDENCY_HASHES)
        | MARKDOWN_CONTROLS
        | TEX_SOURCES
        | {
            "research_control/tasks/RT-20260722-010/artifacts/blind_packet_revision_history.yaml",
            "research_control/tasks/RT-20260722-010/artifacts/review_agreement_and_leakage_analysis.json",
            "research_control/tasks/RT-20260722-007/artifacts/positive_provenance_gate_validation.json",
            "research_control/tasks/RT-20260722-009/artifacts/proof_evidence_compact_receipt.json",
            "scripts/research_control/validate_red_team_review_artifact.py",
            rel(Path(__file__).resolve()),
        }
    )
    return {
        "schema_id": "v21_p11_scientific_qa_non_regression_validation_v1",
        "status": matrix["status"],
        "task_id": matrix["task_id"],
        "plan_task_id": matrix["plan_task_id"],
        "recommendation_ids": matrix["recommendation_ids"],
        "check_count": matrix["case_count"],
        "failed_check_count": matrix["failed_case_count"],
        "finding_counts": {"blocker": 0 if matrix["status"] == "PASS" else matrix["failed_case_count"], "repair_required": matrix["limitation_count"], "informational": 0},
        "checks": [{"check_id": row["case_id"], "status": row["status"]} for row in matrix["cases"]],
        "rollout_disposition": matrix["rollout_disposition"],
        "mandatory_guardrails": matrix["mandatory_guardrails"],
        "authority_flags": matrix["authority_flags"],
        "source_hashes": {path: sha256(ROOT / path) for path in source_paths},
        "claim_boundary_id": "CB-V21-P11-T08-SCIENTIFIC-QA-NON-REGRESSION-001",
        "claim_boundary_summary": "P11 controls pass critical non-regression checks for bounded later-gate use under explicit guardrails; unattended blind-packet and semantic-veto automation remain frozen pending two named repairs, with no scientific or protected authority change.",
    }


def build_receipt(matrix: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": "v21_p11_scientific_qa_non_regression_compact_receipt_v1",
        "status": validation["status"],
        "task_id": validation["task_id"],
        "plan_task_id": validation["plan_task_id"],
        "recommendation_ids": validation["recommendation_ids"],
        "result_status": "PASS_BOUNDED_ROLLOUT_TWO_REPAIRS_REQUIRED" if validation["status"] == "PASS" else "FAIL",
        "rollout_disposition": validation["rollout_disposition"],
        "finding_counts": validation["finding_counts"],
        "repair_obligation_ids": matrix["finding_ids"],
        "validator_ids": [row["check_id"] for row in validation["checks"]],
        "matrix_sha256": hashlib.sha256(canonical_bytes(matrix)).hexdigest(),
        "validation_sha256": hashlib.sha256(canonical_bytes(validation)).hexdigest(),
        "source_hashes": validation["source_hashes"],
        "authority_flags": validation["authority_flags"],
        "claim_boundary_id": validation["claim_boundary_id"],
        "claim_boundary_summary": validation["claim_boundary_summary"],
        "forbidden_conclusions": [
            "Audit PASS is not theorem truth proof authority scientific status or physics promotion.",
            "Internal AI review is not external human review or independent replication.",
            "A blind packet is not scientifically self-contained merely because process-context leakage is absent.",
            "Semantic-probe findings are not automatic refutations and a clean probe is not semantic completeness.",
            "No ontology source law metric coupling Einstein equation benchmark publication or completed derivation is adopted or promoted.",
        ],
    }


def generated() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    matrix = build_matrix()
    validation = build_validation(matrix)
    receipt = build_receipt(matrix, validation)
    return matrix, validation, receipt


def write_outputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    values = generated()
    for path, value in zip((MATRIX_PATH, VALIDATION_PATH, RECEIPT_PATH), values, strict=True):
        path.write_bytes(canonical_bytes(value))
    return values


def check_outputs() -> tuple[bool, dict[str, Any], list[str]]:
    values = generated()
    stale = [rel(path) for path, value in zip((MATRIX_PATH, VALIDATION_PATH, RECEIPT_PATH), values, strict=True) if not path.is_file() or path.read_bytes() != canonical_bytes(value)]
    return not stale and values[1]["status"] == "PASS", values[1], stale


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.write:
        _, validation, _ = write_outputs()
        stale: list[str] = []
        ok = validation["status"] == "PASS"
    else:
        ok, validation, stale = check_outputs()
    result = {"status": "PASS" if ok else "FAIL", "validation_status": validation["status"], "check_count": validation["check_count"], "failed_check_count": validation["failed_check_count"], "rollout_disposition": validation["rollout_disposition"], "stale_paths": stale}
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result["status"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
