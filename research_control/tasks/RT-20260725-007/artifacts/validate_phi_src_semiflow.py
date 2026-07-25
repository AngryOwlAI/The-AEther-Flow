#!/usr/bin/env python3
"""Validate the bounded P5-T02 Phi_src semiflow packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_ROOT = REPO_ROOT / "research_control/tasks/RT-20260725-007/artifacts"
SPEC_PATH = ARTIFACT_ROOT / "phi_src_semiflow_spec_v1.yaml"
TEX_PATH = ARTIFACT_ROOT / "phi_src_semiflow_semantics_v1.tex"
CHILD_MATH_PATH = ARTIFACT_ROOT / "child_phys_math_phi_src_semiflow.yaml"
CHILD_PHIL_PATH = ARTIFACT_ROOT / "child_phys_phil_phi_src_semiflow.yaml"
CONFLICT_PATH = ARTIFACT_ROOT / "parent_conflict_review_phi_src_semiflow.yaml"
FUSION_PATH = ARTIFACT_ROOT / "parent_fusion_notes_phi_src_semiflow.md"
REPORT_PATH = ARTIFACT_ROOT / "phi_src_semiflow_validation_receipt_v1.json"

REQUIRED_AXIOMS = {
    "S1_IDENTITY",
    "S2_FORWARD_COMPOSITION",
    "S3_ADMISSIBILITY",
    "S4_REDUNDANCY_COMPATIBILITY",
    "S5_JOINT_CONTINUITY",
}
REQUIRED_THEOREMS = {
    "P5-T02-THM-QUOTIENT-DESCENT",
    "P5-T02-THM-REPARAMETERIZATION",
}
REQUIRED_CASES = {
    "CONTINUOUS",
    "DISCRETE",
    "PERIODIC",
    "BI_INFINITE",
    "DENSE",
    "BRANCHING",
    "STOCHASTIC",
}
REQUIRED_FAIL_RESULTS = {
    "fail_closed_target_import",
    "fail_closed_action_law",
    "fail_closed_redundancy",
    "fail_closed_topology",
    "fail_closed_quotient_continuity",
    "fail_closed_unproved_structure",
    "fail_closed_physical_overread",
}


def load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(REPO_ROOT)} must contain a mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_check(checks: list[dict[str, Any]], check_id: str, ok: bool, detail: str) -> None:
    checks.append(
        {"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail}
    )


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required_paths = [
        SPEC_PATH,
        TEX_PATH,
        CHILD_MATH_PATH,
        CHILD_PHIL_PATH,
        CONFLICT_PATH,
        FUSION_PATH,
    ]
    for path in required_paths:
        add_check(
            checks,
            f"file:{path.name}",
            path.is_file() and not path.is_symlink(),
            "required regular artifact exists",
        )
    try:
        spec = load_mapping(SPEC_PATH)
        child_math = load_mapping(CHILD_MATH_PATH)
        child_phil = load_mapping(CHILD_PHIL_PATH)
        conflict = load_mapping(CONFLICT_PATH)
        tex = TEX_PATH.read_text(encoding="utf-8")
        fusion = FUSION_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return {
            "schema_id": "phi_src_semiflow_validation_receipt_v1",
            "result_status": "FAIL",
            "error": str(exc),
            "checks": checks,
            "finding_counts": {
                "pass": sum(c["status"] == "PASS" for c in checks),
                "fail": sum(c["status"] == "FAIL" for c in checks) + 1,
            },
        }

    semantics = spec.get("selected_semantics", {})
    parameter = semantics.get("parameter_object", {}) if isinstance(semantics, dict) else {}
    add_check(
        checks,
        "semantic_kind",
        semantics.get("semantic_kind") == "continuous_unital_forward_monoid_action"
        and semantics.get("conventional_name") == "topological_semiflow"
        and parameter.get("carrier") == "R_ge_0"
        and parameter.get("negative_parameters_included") is False,
        "selected kind is exactly a forward R_ge_0 topological monoid action",
    )

    axiom_ids = {
        str(item.get("axiom_id", ""))
        for item in spec.get("axioms", [])
        if isinstance(item, dict)
    }
    add_check(
        checks,
        "axiom_closure",
        axiom_ids == REQUIRED_AXIOMS,
        "identity, composition, admissibility, redundancy, and joint continuity are exact",
    )

    theorems = {
        str(item.get("theorem_id", "")): item
        for item in spec.get("theorem_payload", [])
        if isinstance(item, dict)
    }
    quotient = theorems.get("P5-T02-THM-QUOTIENT-DESCENT", {})
    reparam = theorems.get("P5-T02-THM-REPARAMETERIZATION", {})
    add_check(
        checks,
        "theorem_payload",
        set(theorems) == REQUIRED_THEOREMS
        and quotient.get("proof_status") == "proved_in_task_local_tex"
        and quotient.get("continuity_clause", {}).get("claimed_unconditionally") is False
        and reparam.get("proof_status") == "proved_in_task_local_tex"
        and "c>=0" in str(reparam.get("conclusion", "")),
        "quotient descent and reparameterization results preserve their exact hypotheses",
    )

    witnesses = {
        str(item.get("witness_id", "")): item
        for item in spec.get("witnesses", [])
        if isinstance(item, dict)
    }
    continuous = witnesses.get("CONTINUOUS-ABSORBING-TRANSLATION-V1", {})
    discrete = witnesses.get("DISCRETE-THREE-STATE-SPECIALIZATION-V1", {})
    add_check(
        checks,
        "witness_matrix",
        continuous.get("joint_continuity") is True
        and continuous.get("invertible_for_positive_parameter") is False
        and discrete.get("parameter_monoid") == "N_0"
        and discrete.get("redundancy_compatible") is True
        and discrete.get("invertible") is False,
        "continuous non-group witness and discrete quotient specialization are explicit",
    )

    case_ids = {
        str(item.get("case_id", ""))
        for item in spec.get("exceptional_case_matrix", [])
        if isinstance(item, dict) and item.get("nonconclusion")
    }
    add_check(
        checks,
        "exceptional_cases",
        case_ids == REQUIRED_CASES,
        "continuous, discrete, periodic, bi-infinite, dense, branching, and stochastic cases are classified",
    )

    fail_results = {
        str(item.get("result", ""))
        for item in spec.get("malformed_fail_closed_branches", [])
        if isinstance(item, dict) and item.get("accepted") is False
    }
    add_check(
        checks,
        "fail_closed_matrix",
        fail_results == REQUIRED_FAIL_RESULTS,
        "all seven malformed or overread branches fail closed",
    )

    boundary = spec.get("claim_boundary", {})
    false_fields = (
        "target_import_allowed",
        "canonical_ontology_modified",
        "canonical_ontology_candidate_status_claimed",
        "source_law_adopted",
        "source_law_rejected",
        "physical_time_claimed",
        "physical_clock_scale_fixed",
        "physical_gauge_claimed",
        "physical_dynamics_selected",
        "global_invertibility_assumed",
        "generator_assumed",
        "reconstruction_selected",
        "physics_promotion_authorized",
    )
    add_check(
        checks,
        "claim_boundary",
        boundary.get("source_only") is True
        and all(boundary.get(field) is False for field in false_fields),
        "source-only proposal status and all physical, adoption, and promotion nonclaims are explicit",
    )

    required_tex_markers = [
        r"\Lam=(\mathbb R_{\geq 0},+,0,\leq)",
        r"\Phi_{\lambda+\mu}(q)",
        "Redundancy-quotient descent",
        "Continuous additive reparameterization classification",
        r"\Phi_\lambda(x)=\max\{x-\lambda,0\}",
        "Current adoption is blocked while same-milestone continuation remains open.",
        "P5-T03",
    ]
    add_check(
        checks,
        "source_tex_content",
        all(marker in tex for marker in required_tex_markers),
        "TeX contains the selected law, two theorem payloads, witness, exact adoption language, and successor boundary",
    )

    add_check(
        checks,
        "parent_child_synthesis",
        child_math.get("status") == "completed"
        and child_phil.get("status") == "completed"
        and conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflicts") == []
        and "quotient" in fusion.lower()
        and "physical time" in fusion.lower(),
        "both internal perspectives completed and the parent resolved mathematical and interpretive boundaries",
    )

    source_hashes = {
        path.relative_to(REPO_ROOT).as_posix(): sha256(path) for path in required_paths
    }
    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "phi_src_semiflow_validation_receipt_v1",
        "validator_ids": [
            "p5_t02_phi_src_semiflow_validator_v1",
            "p5_t02_source_quotient_theorem_review_v1",
            "p5_t02_reparameterization_review_v1",
            "p5_t02_parent_child_synthesis_review_v1",
            "p5_t02_no_physical_overread_audit_v1",
        ],
        "result_status": "PASS" if not failed else "FAIL",
        "plan_task_id": "P5-T02",
        "object_id": spec.get("object_id", ""),
        "claim_status": "draft/control proposal-only source-extension data",
        "source_hashes": source_hashes,
        "checks": checks,
        "finding_counts": {
            "pass": len(checks) - len(failed),
            "fail": len(failed),
            "warning": 0,
        },
        "claim_boundary_summary": (
            "Phi_src is tested only as a proposal-only continuous forward monoid "
            "action. No canonical adoption, physical time, gauge, dynamics, "
            "reconstruction, downstream GR, promotion, publication, or push is authorized."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    status = report.get("result_status") == "PASS"
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.check:
        try:
            existing = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            status = False
        else:
            if existing != report:
                status = False
                report = dict(report)
                report["result_status"] = "FAIL"
                report["receipt_drift"] = True
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report.get("result_status", "FAIL"))
    return 0 if status else 1


if __name__ == "__main__":
    raise SystemExit(main())
