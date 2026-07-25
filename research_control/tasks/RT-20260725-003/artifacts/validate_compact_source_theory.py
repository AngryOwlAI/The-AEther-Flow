#!/usr/bin/env python3
"""Validate the bounded P5-T01 compact source-theory packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260725-003"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
SPEC_PATH = ARTIFACT_ROOT / "compact_source_theory_spec_v1.yaml"
DIAGRAM_PATH = ARTIFACT_ROOT / "compact_source_theory_type_dependency_v1.yaml"
TEX_PATH = ARTIFACT_ROOT / "compact_source_theory_object_v1.tex"
CHILD_MATH_PATH = ARTIFACT_ROOT / "child_phys_math_p5_t01_source_theory.yaml"
CHILD_PHIL_PATH = ARTIFACT_ROOT / "child_phys_phil_p5_t01_source_theory.yaml"
CONFLICT_PATH = ARTIFACT_ROOT / "parent_conflict_review_p5_t01_source_theory.yaml"
FUSION_PATH = ARTIFACT_ROOT / "parent_fusion_notes_p5_t01_source_theory.md"
REPORT_PATH = ARTIFACT_ROOT / "compact_source_theory_validation_receipt_v1.json"

EXPECTED_COMPONENTS = {
    "A": "primitive_debt",
    "pi:E->A": "proposal-only",
    "Q_adm": "proposal-only",
    "Iso_src": "derived_from_declared_source_isomorphisms",
    "Red_src": "proposal-only",
    "O_src": "derived_from_declared_redundancy",
    "Var_src": "proposal-only",
    "S_Phi": "open",
    "S_dyn": "open",
    "S_rec": "open",
    "tau": "derived",
}
REQUIRED_FAIL_RESULTS = {
    "fail_closed_target_import",
    "fail_closed_type_error",
    "fail_closed_invariance_error",
    "fail_closed_open_slot",
}
REQUIRED_FORBIDDEN_EDGES = {
    ("target_atlas", "any_source_component"),
    ("target_metric", "any_source_component"),
    ("benchmark_success", "any_source_component"),
    ("candidate_reconstruction", "any_source_component"),
}


def load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(REPO_ROOT)} must contain a mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_check(
    checks: list[dict[str, Any]],
    check_id: str,
    condition: bool,
    detail: str,
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        }
    )


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required_paths = [
        SPEC_PATH,
        DIAGRAM_PATH,
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
        diagram = load_mapping(DIAGRAM_PATH)
        child_math = load_mapping(CHILD_MATH_PATH)
        child_phil = load_mapping(CHILD_PHIL_PATH)
        conflict = load_mapping(CONFLICT_PATH)
        tex = TEX_PATH.read_text(encoding="utf-8")
        fusion = FUSION_PATH.read_text(encoding="utf-8")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return {
            "schema_id": "compact_source_theory_validation_receipt_v1",
            "validator_ids": ["p5_t01_compact_source_theory_validator_v1"],
            "result_status": "FAIL",
            "error": str(exc),
            "checks": checks,
            "finding_counts": {
                "pass": sum(item["status"] == "PASS" for item in checks),
                "fail": sum(item["status"] == "FAIL" for item in checks) + 1,
            },
        }

    components = {
        str(item.get("name", "")): str(item.get("status", ""))
        for item in spec.get("source_theory_tuple", {}).get("components", [])
        if isinstance(item, dict)
    }
    add_check(
        checks,
        "tuple_component_types",
        components == EXPECTED_COMPONENTS,
        "all eleven tuple components have the exact primitive, proposal-only, derived, or open status",
    )
    slots = {
        str(item.get("name", "")): str(item.get("status", ""))
        for item in spec.get("source_theory_tuple", {}).get("components", [])
        if isinstance(item, dict) and str(item.get("name", "")).startswith("S_")
    }
    add_check(
        checks,
        "open_slots_explicit",
        slots == {"S_Phi": "open", "S_dyn": "open", "S_rec": "open"},
        "Phi, dynamics, and reconstruction slots are tagged open",
    )

    iso = spec.get("source_isomorphism_and_gauge", {})
    add_check(
        checks,
        "source_isomorphism_and_redundancy",
        isinstance(iso, dict)
        and "groupoid" in str(iso.get("source_isomorphism", "")).lower()
        and "Red_src" in str(iso.get("gauge_equivalence", ""))
        and "physical gauge symmetry" in str(iso.get("nonclaim", "")),
        "source isomorphism, redundancy quotient, and physical-gauge nonclaim are explicit",
    )

    instantiations = spec.get("instantiations", [])
    kinds = {
        str(item.get("kind", "")): item
        for item in instantiations
        if isinstance(item, dict)
    }
    continuum = kinds.get("continuum", {})
    finite = kinds.get("finite", {})
    add_check(
        checks,
        "nontrivial_continuum_witness",
        bool(continuum.get("nontriviality_witness"))
        and continuum.get("Phi_slot") == "open"
        and continuum.get("dynamics_slot") == "open"
        and continuum.get("reconstruction_slot") == "open",
        "continuum witness has distinct states, a separating observable, and three open slots",
    )
    add_check(
        checks,
        "finite_type_witness",
        len(finite.get("states", [])) == 2
        and finite.get("Phi_slot") == "open"
        and finite.get("dynamics_slot") == "open"
        and finite.get("reconstruction_slot") == "open",
        "finite two-state reduction is explicitly proposal-only and open-slot preserving",
    )

    fail_results = {
        str(item.get("result", ""))
        for item in spec.get("malformed_fail_closed_branches", [])
        if isinstance(item, dict) and item.get("accepted") is False
    }
    add_check(
        checks,
        "malformed_fail_closed",
        fail_results == REQUIRED_FAIL_RESULTS,
        "target import, groupoid, invariance, and open-slot errors each fail closed",
    )

    forbidden_edges = {
        (str(item.get("from", "")), str(item.get("to", "")))
        for item in diagram.get("forbidden_edges", [])
        if isinstance(item, dict)
    }
    add_check(
        checks,
        "no_target_import_dependency_graph",
        forbidden_edges == REQUIRED_FORBIDDEN_EDGES,
        "dependency graph forbids target atlas, target metric, benchmark success, and candidate reconstruction imports",
    )

    required_tex_markers = [
        r"\mathfrak T_{\mathrm{src}}^{(0)}",
        r"S_{\Phi}=\Open",
        r"S_{\mathrm{dyn}}=\Open",
        r"S_{\mathrm{rec}}=\Open",
        r"\bot_{\mathrm{target}}",
        "P5-T02",
        "not adopted physical ontology",
    ]
    add_check(
        checks,
        "registered_source_object_content",
        all(marker in tex for marker in required_tex_markers),
        "TeX source contains the tuple, open-slot equations, fail-closed branch, next burden, and status boundary",
    )

    add_check(
        checks,
        "parent_child_synthesis",
        child_math.get("status") == "completed"
        and child_phil.get("status") == "completed"
        and conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflicts") == []
        and "P5-T02" in fusion,
        "both child perspectives completed, conflicts resolved, and fusion preserved the next obligation",
    )

    boundary = spec.get("claim_boundary", {})
    add_check(
        checks,
        "claim_boundary",
        isinstance(boundary, dict)
        and boundary.get("source_only") is True
        and all(
            boundary.get(field) is False
            for field in (
                "physical_ontology_adopted",
                "source_law_adopted",
                "dynamics_selected",
                "reconstruction_selected",
                "target_import_allowed",
                "physics_promotion_authorized",
            )
        ),
        "source-only draft/control status and all no-promotion booleans are explicit",
    )

    source_hashes = {
        path.relative_to(REPO_ROOT).as_posix(): sha256(path)
        for path in required_paths
    }
    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "compact_source_theory_validation_receipt_v1",
        "validator_ids": [
            "p5_t01_compact_source_theory_validator_v1",
            "p5_t01_type_and_dependency_review_v1",
            "p5_t01_no_target_import_audit_v1",
            "p5_t01_parent_child_synthesis_review_v1",
        ],
        "result_status": "PASS" if not failed else "FAIL",
        "plan_task_id": "P5-T01",
        "object_id": "V21-P5-T01-COMPACT-SOURCE-THEORY-TUPLE-V1",
        "claim_status": "draft/control",
        "source_hashes": source_hashes,
        "checks": checks,
        "finding_counts": {
            "pass": len(checks) - len(failed),
            "fail": len(failed),
            "warning": 0,
        },
        "claim_boundary_summary": (
            "One coherent source-only theory target is typed with open Phi, dynamics, "
            "and reconstruction slots. No physical ontology, source law, target object, "
            "physics promotion, benchmark promotion, or completed derivation is authorized."
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
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
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
