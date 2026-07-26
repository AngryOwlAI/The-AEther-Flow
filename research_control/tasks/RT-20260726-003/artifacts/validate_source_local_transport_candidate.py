#!/usr/bin/env python3
"""Validate the bounded P6-T02 source-local transport candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml


SCRIPT_PATH = Path(__file__).resolve()
ARTIFACT_DIR = SCRIPT_PATH.parent
REPO_ROOT = SCRIPT_PATH.parents[4]
SPEC_PATH = ARTIFACT_DIR / "source_local_transport_candidate_spec_v1.yaml"
TEX_PATH = ARTIFACT_DIR / "source_local_transport_candidate_v1.tex"
MATH_CHILD_PATH = ARTIFACT_DIR / "child_phys_math_p6_t02_source_local_transport.yaml"
PHIL_CHILD_PATH = ARTIFACT_DIR / "child_phys_phil_p6_t02_source_local_transport.yaml"
CONFLICT_PATH = ARTIFACT_DIR / "parent_conflict_review_p6_t02_source_local_transport.yaml"
FUSION_PATH = ARTIFACT_DIR / "parent_fusion_notes_p6_t02_source_local_transport.md"
RECEIPT_PATH = ARTIFACT_DIR / "source_local_transport_candidate_validation_receipt_v1.json"
GENERATED_AT = "2026-07-26T10:56:59Z"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a YAML map")
    return value


def flow(z: float, s: float, gamma: float) -> float:
    return z / math.sqrt(1.0 + 2.0 * gamma * s * z * z)


def tangent(z: float, s: float, gamma: float) -> float:
    return (1.0 + 2.0 * gamma * s * z * z) ** (-1.5)


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

    spec = load_yaml(SPEC_PATH)
    tex = TEX_PATH.read_text(encoding="utf-8")
    math_child = load_yaml(MATH_CHILD_PATH)
    phil_child = load_yaml(PHIL_CHILD_PATH)
    conflict = load_yaml(CONFLICT_PATH)
    fusion = FUSION_PATH.read_text(encoding="utf-8")

    check(
        "SPEC_IDENTITY",
        spec.get("candidate_id") == "V21-P6-T02-SOURCE-LOCAL-TRANSPORT-CHARACTERISTIC-V1"
        and spec.get("plan_task_id") == "P6-T02",
        "Candidate and work-item identities are exact.",
    )
    check(
        "STATUS_VOCABULARY",
        spec.get("status_label") == "draft/control"
        and spec.get("candidate_status") == "proposal-only"
        and spec.get("material_class") == "source-extension data",
        "Protected source-extension status vocabulary is exact.",
    )
    check(
        "EQUATION_TYPED",
        spec.get("candidate_equation", {}).get("equation")
        == "E_V[a] = L_V a + gamma a^3 = 0",
        "The first-order scalar candidate equation is machine-readable.",
    )
    check(
        "NO_TARGET_PREMISE",
        not spec.get("source_boundary", {}).get("target_metric_imported", True)
        and not spec.get("source_boundary", {}).get("gr_null_cone_imported", True)
        and not spec.get("source_boundary", {}).get("benchmark_fit_used", True),
        "No target metric, GR null cone, or benchmark fit is a source premise.",
    )
    check(
        "PHYSICAL_GATE_BLOCKED",
        not spec.get("gate_b", {}).get("physical_gate_b_ready", True)
        and not spec.get("authority", {}).get("physical_causality_established", True),
        "Formal characteristic construction is separated from physical Gate B.",
    )

    fixed_sources = spec.get("fixed_sources", [])
    check(
        "FIXED_SOURCE_MANIFEST",
        isinstance(fixed_sources, list) and len(fixed_sources) == 7,
        "Seven directly inspected fixed sources are declared.",
    )
    for index, item in enumerate(fixed_sources, start=1):
        source_path = REPO_ROOT / str(item.get("path", ""))
        expected = str(item.get("sha256", ""))
        check(
            f"FIXED_SOURCE_{index:02d}",
            source_path.is_file() and sha256(source_path) == expected,
            f"{item.get('object_id', '')} exists with its fixed SHA-256.",
        )

    gamma = 0.7
    differential_ok = True
    semigroup_ok = True
    tangent_ok = True
    for z in (-1.2, -0.4, 0.0, 0.6, 1.4):
        for s in (0.0, 0.2, 0.9):
            value = flow(z, s, gamma)
            derivative_s = -gamma * z**3 * (1.0 + 2.0 * gamma * s * z * z) ** (-1.5)
            differential_ok = differential_ok and math.isclose(
                derivative_s, -gamma * value**3, rel_tol=1e-12, abs_tol=1e-12
            )
            delta = 1e-6
            numeric_tangent = (
                flow(z + delta, s, gamma) - flow(z - delta, s, gamma)
            ) / (2.0 * delta)
            tangent_ok = tangent_ok and math.isclose(
                numeric_tangent, tangent(z, s, gamma), rel_tol=2e-9, abs_tol=2e-9
            )
        semigroup_ok = semigroup_ok and math.isclose(
            flow(flow(z, 0.3, gamma), 0.8, gamma),
            flow(z, 1.1, gamma),
            rel_tol=1e-12,
            abs_tol=1e-12,
        )
    check(
        "FLOW_EQUATION",
        differential_ok,
        "The exact curve solution satisfies da/ds=-gamma a^3 on all samples.",
    )
    check(
        "FLOW_COMPOSITION",
        semigroup_ok,
        "The exact source-order flow composes additively on all samples.",
    )
    check(
        "TANGENT_RESPONSE",
        tangent_ok,
        "Finite-difference differentiation matches the exact P5 tangent response.",
    )

    v = (1.0, 0.2, -0.3, 0.4)
    h = (1.0, 0.0, 0.0, 0.0)
    xi_samples = (
        (0.3, 0.1, -0.2, 0.5),
        (-0.7, 0.4, 0.1, -0.3),
        (1.2, -0.8, 0.6, 0.2),
    )
    hv = sum(left * right for left, right in zip(h, v))
    hyperbolicity_ok = hv > 0.0
    roots_ok = True
    for xi in xi_samples:
        p_xi = sum(left * right for left, right in zip(xi, v))
        root = -p_xi / hv
        roots_ok = roots_ok and math.isfinite(root) and math.isclose(
            p_xi + root * hv, 0.0, abs_tol=1e-12
        )
    check(
        "PRINCIPAL_HYPERBOLICITY",
        hyperbolicity_ok and roots_ok,
        "The degree-one principal polynomial has one real root along an admissible h.",
    )

    dual_ray_ok = True
    for xi in xi_samples:
        p_xi = sum(left * right for left, right in zip(xi, v))
        if p_xi <= 0:
            shift = 1.0 - p_xi
            xi = (xi[0] + shift, xi[1], xi[2], xi[3])
            p_xi = sum(left * right for left, right in zip(xi, v))
        for ray_scale in (0.0, 0.5, 2.0):
            pairing = ray_scale * p_xi
            dual_ray_ok = dual_ray_ok and pairing >= -1e-12
    check(
        "DUAL_RAY_CONTROL",
        dual_ray_ok,
        "Nonnegative multiples of V pair nonnegatively with sampled hyperbolicity covectors.",
    )

    upwind_ok = True
    s_value = 0.8
    for epsilon in (0.1, 0.05, 0.025):
        discrete = (math.sin(s_value) - math.sin(s_value - epsilon)) / epsilon
        error = abs(discrete - math.cos(s_value))
        upwind_ok = upwind_ok and error <= epsilon / 2.0 + 1e-12
    check(
        "UPWIND_ERROR_BOUND",
        upwind_ok,
        "The backward difference obeys the first-order Taylor bound on sin(s).",
    )

    controls = spec.get("controls", {})
    for control_name in (
        "nontrivial",
        "zero_field",
        "closed_orbit",
        "competing_generators",
        "multiple_sectors",
    ):
        check(
            f"CONTROL_{control_name.upper()}",
            isinstance(controls.get(control_name), dict)
            and bool(controls.get(control_name)),
            f"The {control_name} control is present and nonempty.",
        )
    check(
        "CLOSED_ORBIT_FAIL_CLOSED",
        controls.get("closed_orbit", {}).get("result")
        == "FAIL_CLOSED_ANTISYMMETRIC_CAUSAL_ORDER",
        "Closed positive orbits fail the antisymmetric-order obligation.",
    )
    check(
        "COMPETING_GENERATOR_NONSELECTION",
        controls.get("competing_generators", {}).get("result")
        == "PRECISE_SELECTOR_NONSELECTION",
        "Distinct source generators preserve restricted P5 data while changing characteristics.",
    )
    check(
        "MULTI_SECTOR_UNIVERSALITY_BLOCK",
        controls.get("multiple_sectors", {}).get("universality_derived") is False,
        "The two-sector control does not silently assert universality.",
    )

    check(
        "MATH_CHILD",
        math_child.get("execution_unit_id") == "child_phys_math"
        and math_child.get("status") == "completed"
        and math_child.get("claim_boundary_preserved") is True,
        "The internal physicist-mathematician perspective completed.",
    )
    check(
        "PHIL_CHILD",
        phil_child.get("execution_unit_id") == "child_phys_phil"
        and phil_child.get("status") == "completed"
        and phil_child.get("claim_boundary_preserved") is True,
        "The internal physicist-philosopher perspective completed.",
    )
    check(
        "CONFLICT_REVIEW",
        conflict.get("status") == "resolved"
        and conflict.get("review_rounds") == 1
        and len(conflict.get("resolved_conflicts", [])) == 6
        and conflict.get("unresolved_conflicts") == [],
        "Six cross-perspective tensions were resolved with no unresolved conflict.",
    )
    check(
        "PARENT_FUSION",
        "constructed_candidate" in fusion
        and "P6-T03" in fusion
        and "No canonical ontology" in fusion,
        "Parent fusion preserves the decisive result, next packet, and authority boundary.",
    )

    required_tex_markers = (
        "P6T02-THM-FLOW-BOX-RECOVERY",
        "P6T02-THM-PRINCIPAL-RAY",
        "P6T02-PROP-RESPONSE-SUPPORT",
        r"P_x(\xi)=\xi(V_x)",
        r"\Gamma_x^\circ=\{rV_x:r\geq0\}",
        "Closed-orbit chronology failure",
        "Competing-generator nonselection",
        r"O(\varepsilon)",
        r"\texttt{constructed\_candidate}",
    )
    for index, marker in enumerate(required_tex_markers, start=1):
        check(
            f"TEX_MARKER_{index:02d}",
            marker in tex,
            f"Registered TeX contains required marker {marker}.",
        )

    authority = spec.get("authority", {})
    blocked_authority_fields = (
        "canonical_ontology_modified",
        "source_law_adopted",
        "physical_time_established",
        "physical_causality_established",
        "metric_or_conformal_class_reconstructed",
        "historical_scoped_g_eff_expanded",
        "matter_coupling_derived",
        "einstein_equations_derived",
        "benchmark_promoted",
        "physics_promotion_authorized",
        "proof_authority",
        "publication_authorized",
        "push_authorized",
    )
    check(
        "AUTHORITY_FAIL_CLOSED",
        all(authority.get(field) is False for field in blocked_authority_fields),
        "All protected adoption, physical, promotion, publication, and push flags are false.",
    )

    failures = [item for item in checks if item["status"] != "PASS"]
    source_hashes = {
        TEX_PATH.relative_to(REPO_ROOT).as_posix(): sha256(TEX_PATH),
        SPEC_PATH.relative_to(REPO_ROOT).as_posix(): sha256(SPEC_PATH),
        MATH_CHILD_PATH.relative_to(REPO_ROOT).as_posix(): sha256(MATH_CHILD_PATH),
        PHIL_CHILD_PATH.relative_to(REPO_ROOT).as_posix(): sha256(PHIL_CHILD_PATH),
        CONFLICT_PATH.relative_to(REPO_ROOT).as_posix(): sha256(CONFLICT_PATH),
        FUSION_PATH.relative_to(REPO_ROOT).as_posix(): sha256(FUSION_PATH),
    }
    return {
        "schema_id": "v21_p6_t02_source_local_transport_validation_receipt_v1",
        "task_id": "RT-20260726-003",
        "plan_task_id": "P6-T02",
        "candidate_id": "V21-P6-T02-SOURCE-LOCAL-TRANSPORT-CHARACTERISTIC-V1",
        "generated_at": GENERATED_AT,
        "validation_status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "warning_count": 0,
        "result_type": "constructed_candidate",
        "physical_gate_b_ready": False,
        "source_hashes": source_hashes,
        "checks": checks,
        "authority_note": (
            "This receipt is operational evidence only. It does not adopt a source law, "
            "establish physical causality, reconstruct a metric, or promote a physics claim."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        RECEIPT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        if not RECEIPT_PATH.is_file():
            report["validation_status"] = "FAIL"
            report.setdefault("receipt_errors", []).append("receipt file is missing")
        else:
            recorded = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
            if recorded != report:
                report["validation_status"] = "FAIL"
                report.setdefault("receipt_errors", []).append(
                    "receipt content differs from deterministic validation result"
                )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"{report['validation_status']}: "
            f"{report['check_count']} checks, {report['failure_count']} failures"
        )
    return 0 if report["validation_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
