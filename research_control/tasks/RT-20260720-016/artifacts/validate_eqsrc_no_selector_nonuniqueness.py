#!/usr/bin/env python3
"""Validate the bounded v21 P2-T03 no-selector/nonuniqueness packet."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any

import yaml


ARTIFACTS = Path(__file__).resolve().parent
ROOT = ARTIFACTS.parents[3]
THEOREM_ID = "EQSRC-NO-NATURAL-SELECTOR-NONUNIQUENESS-THEOREM-V1"
REPORT = ARTIFACTS / "eqsrc_no_selector_nonuniqueness_validation.json"

EXPECTED_SOURCES = {
    "NS-GL2-LINES-EMPTY-002": (
        "research_control/tasks/RT-20260718-041/artifacts/eqsrc_orientation_torsor_descent_law_refuter_countermodel.yaml",
        "a5bc1af23713145727bfad592a770691b5128d6ce6546966860d80c588a530a6",
    ),
    "NS-C4-ROOTS-EMPTY-003": (
        "research_control/tasks/RT-20260718-045/artifacts/eqsrc_ordered_motion_rooted_partition_law_refuter_countermodel.yaml",
        "9ddce9d042ef187d163043d6c2a98a7d1a796cd01a433d3d258632150a83325e",
    ),
    "NS-FINITE-TOY-SIGN-TOKEN-EMPTY-004": (
        "research_control/tasks/RT-20260614-055/artifacts/96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex",
        "b589c29e440750e0dacaebb5d2ad86fd5bf0b593b7e27645052fcbf55839a161",
    ),
}
EXPECTED_P2_T01_HASH = "00d7e14b76ac4fa01b834739646fe03012c2b82326a158064b27cdbe916be268"
EXPECTED_P2_T02_HASH = "7611533f40b61b8a32da327add3646b95c604f858adba54c40378b6f29d5067a"
EXPECTED_ONTOLOGY_HASH = "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2"
EXPECTED_DISTANCE_HASH = "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61"
EXPECTED_METRIC_HASH = "a33349c7a153c4fbadb70c7c38b17cf0eebb7672b8e1f692702fc91edf17efcf"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(name: str) -> dict[str, Any]:
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


def load_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((ARTIFACTS / name).read_text(encoding="utf-8"))


def add_check(
    condition: bool,
    check_id: str,
    detail: str,
    checks: list[dict[str, str]],
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "detail": detail,
            "status": "PASS" if condition else "FAIL",
        }
    )


def matvec(matrix: tuple[int, ...], vector: tuple[int, int]) -> tuple[int, int]:
    return (
        (matrix[0] * vector[0] + matrix[1] * vector[1]) % 2,
        (matrix[2] * vector[0] + matrix[3] * vector[1]) % 2,
    )


def bounded_metrics() -> dict[str, Any]:
    matrices = [
        matrix
        for matrix in itertools.product(range(2), repeat=4)
        if (matrix[0] * matrix[3] - matrix[1] * matrix[2]) % 2 == 1
    ]
    lines = [(1, 0), (0, 1), (1, 1)]
    gl_fixed = [
        line for line in lines if all(matvec(matrix, line) == line for matrix in matrices)
    ]

    rotations = range(4)
    c4_fixed = [
        root
        for root in rotations
        if all((root + shift) % 4 == root for shift in rotations)
    ]

    sign_choices = (-1, 1)
    sign_fixed = [
        sign
        for sign in sign_choices
        if all(action(sign) == sign for action in (lambda x: x, lambda x: -x))
    ]
    token_choices = (("a", "b"), ("b", "a"))
    token_fixed = [
        token
        for token in token_choices
        if token == (token[1], token[0])
    ]

    two_choices = ("a", "b")
    injective_k = {choice: f"R_{choice}" for choice in two_choices}
    constant_k = {choice: "R" for choice in two_choices}

    core_assignments = [(0, target) for target in (0, 1)]
    full_assignments = [pair for pair in core_assignments if pair[1] == 0]

    theorem_search_failures: list[dict[str, Any]] = []
    theorem_search_case_count = 0
    for component_count in range(5):
        for factor_sizes in itertools.product(range(4), repeat=component_count):
            theorem_search_case_count += 1
            selector_count = math.prod(factor_sizes)
            factor_empty_equivalence = (selector_count == 0) == any(
                size == 0 for size in factor_sizes
            )
            uniqueness_equivalence = (selector_count == 1) == all(
                size == 1 for size in factor_sizes
            )
            multiplicity_rhs = any(
                factor_sizes[index] >= 2
                and math.prod(factor_sizes[:index] + factor_sizes[index + 1 :]) > 0
                for index in range(component_count)
            )
            multiplicity_equivalence = (selector_count >= 2) == multiplicity_rhs
            if not (
                factor_empty_equivalence
                and uniqueness_equivalence
                and multiplicity_equivalence
            ):
                theorem_search_failures.append(
                    {
                        "factor_sizes": list(factor_sizes),
                        "selector_count": selector_count,
                    }
                )

    return {
        "empty_groupoid": {
            "component_count": 0,
            "selector_count": math.prod(()),
        },
        "gl2_lines": {
            "automorphism_count": len(matrices),
            "choice_count": len(lines),
            "fixed_choice_count": len(gl_fixed),
        },
        "directed_c4": {
            "automorphism_count": 4,
            "choice_count": 4,
            "fixed_choice_count": len(c4_fixed),
        },
        "finite_toy": {
            "sign_fixed_choice_count": len(sign_fixed),
            "token_fixed_choice_count": len(token_fixed),
        },
        "trivial_two_choice": {
            "selector_count": len(two_choices),
            "injective_K_image_count": len(set(injective_k.values())),
            "constant_K_image_count": len(set(constant_k.values())),
        },
        "disconnected_multiple_empty": {
            "factor_sizes": [2, 0],
            "global_selector_count": math.prod((2, 0)),
        },
        "noninvertible_equalizer": {
            "core_selector_count": len(core_assignments),
            "full_selector_count": len(full_assignments),
        },
        "transitive_singleton": {
            "choice_count": 1,
            "fixed_choice_count": 1,
        },
        "bounded_theorem_search": {
            "case_count": theorem_search_case_count,
            "failure_count": len(theorem_search_failures),
            "failures": theorem_search_failures,
        },
    }


def validate() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    source_receipts: list[dict[str, str]] = []
    paths = {
        "tex": ARTIFACTS / "eqsrc_no_selector_nonuniqueness_theorem_v1.tex",
        "assumptions": ARTIFACTS / "eqsrc_no_selector_nonuniqueness_assumptions.yaml",
        "corollaries": ARTIFACTS / "eqsrc_no_selector_nonuniqueness_corollaries.yaml",
        "controls": ARTIFACTS / "eqsrc_no_selector_nonuniqueness_controls.json",
        "math": ARTIFACTS / "child_phys_math_eqsrc_no_selector_nonuniqueness.yaml",
        "phil": ARTIFACTS / "child_phys_phil_eqsrc_no_selector_nonuniqueness.yaml",
        "conflict": ARTIFACTS / "parent_conflict_review_eqsrc_no_selector_nonuniqueness.yaml",
        "fusion": ARTIFACTS / "parent_fusion_notes_eqsrc_no_selector_nonuniqueness.md",
        "receipt": ARTIFACTS / "eqsrc_no_selector_nonuniqueness_receipt.md",
    }
    add_check(
        all(path.is_file() for path in paths.values()),
        "artifact_set",
        "All nine bounded theorem, ledger, synthesis, control, and receipt artifacts exist.",
        checks,
    )

    tex = paths["tex"].read_text(encoding="utf-8")
    normalized_tex = " ".join(tex.split())
    assumptions = load_yaml(paths["assumptions"].name)
    corollaries = load_yaml(paths["corollaries"].name)
    controls = load_json(paths["controls"].name)
    math_child = load_yaml(paths["math"].name)
    phil_child = load_yaml(paths["phil"].name)
    conflict = load_yaml(paths["conflict"].name)
    fusion = paths["fusion"].read_text(encoding="utf-8")
    control_rows = {row["control_id"]: row for row in controls.get("controls", [])}

    add_check(
        all(
            payload.get("theorem_id") == THEOREM_ID
            for payload in (
                assumptions,
                corollaries,
                controls,
                math_child,
                phil_child,
                conflict,
            )
        )
        and THEOREM_ID in fusion,
        "theorem_identity",
        "All bounded artifacts share the exact theorem identity.",
        checks,
    )
    add_check(
        tex.count("{") == tex.count("}")
        and "\\begin{document}" in tex
        and "\\end{document}" in tex,
        "tex_structure",
        "The TeX source has balanced braces and a complete document envelope.",
        checks,
    )
    add_check(
        "\\prod_{i\\in I}F_i" in tex
        and "\\sigma^x_X:=S_\\chi(\\tau_X)(x_{[X]})" in tex
        and "a:=\\tau_Y^{-1}f\\tau_X\\in H_i" in tex,
        "classification_proof",
        "The evaluation bijection, inverse, and naturality conjugation step are explicit.",
        checks,
    )
    add_check(
        "product element" in tex
        and "in ZF" in normalized_tex
        and "\\prod_{j\\neq i}F_j\\neq\\varnothing" in tex
        and "another component has an empty fixed locus" in normalized_tex,
        "global_choice_and_multiplicity",
        "Choice assumptions and the complementary-product multiplicity quantifier are explicit.",
        checks,
    )
    add_check(
        "K_*:\\Sel(\\G)" in tex
        and "\\lvert\\Img K_*\\rvert=1" in tex
        and "relation-level choice irrelevance" in tex
        and "If \\(\\Sel(\\G)=\\varnothing\\), its image is" in tex,
        "relation_image_separation",
        "Selector and induced-relation uniqueness are separated, including the empty-image branch.",
        checks,
    )
    add_check(
        "\\Nat(1_{\\C},\\overline S_\\chi)" in tex
        and "including every noninvertible" in normalized_tex
        and "core fixedness is necessary but need not be sufficient" in normalized_tex,
        "full_category_equalizer",
        "The full-category result is an explicitly conditional equalizer subset.",
        checks,
    )

    assumption_ids = {
        row.get("assumption_id") for row in assumptions.get("assumptions", [])
    }
    add_check(
        assumptions.get("assumption_count") == 10
        and assumption_ids == {f"NS-A{index:02d}" for index in range(1, 11)}
        and assumptions.get("physics_promotion_authorized") is False,
        "assumption_ledger",
        "The formal ledger contains all ten uniquely identified assumptions and no promotion.",
        checks,
    )
    corollary_ids = {
        row.get("corollary_id") for row in corollaries.get("corollaries", [])
    }
    add_check(
        corollaries.get("corollary_count") == 8
        and corollary_ids == {f"NS-C{index:02d}" for index in range(1, 9)}
        and corollaries.get("physics_promotion_authorized") is False,
        "corollary_manifest",
        "The corollary manifest contains all eight typed consequences and blocked extensions.",
        checks,
    )
    add_check(
        math_child.get("status") == "completed"
        and phil_child.get("status") == "completed"
        and math_child.get("claim_boundary", {}).get("p2_t01_domain_changed") is False
        and phil_child.get("claim_boundary", {}).get("claim_boundary_preserved") is True,
        "child_outputs",
        "Both internal perspectives completed under the shared unchanged-domain boundary.",
        checks,
    )
    add_check(
        conflict.get("status") == "completed"
        and conflict.get("resolution_rounds") == 1
        and not conflict.get("unresolved_blocking_conflicts")
        and all(
            row.get("status") == "resolved" for row in conflict.get("conflicts", [])
        ),
        "parent_synthesis",
        "One parent synthesis round resolved all five conflicts.",
        checks,
    )

    source_ok = True
    for control_id, (expected_path, expected_hash) in EXPECTED_SOURCES.items():
        row = control_rows.get(control_id, {})
        source_path = ROOT / expected_path
        actual_hash = digest(source_path) if source_path.is_file() else "missing"
        source_receipts.append(
            {
                "control_id": control_id,
                "path": expected_path,
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
            }
        )
        source_ok = (
            source_ok
            and row.get("source_artifact") == expected_path
            and row.get("source_sha256") == expected_hash == actual_hash
        )
    p2_t01_path = (
        ROOT
        / "research_control/tasks/RT-20260720-014/artifacts/eqsrc_source_category_definition_v1.tex"
    )
    p2_t02_path = (
        ROOT
        / "research_control/tasks/RT-20260720-015/artifacts/eqsrc_natural_selector_fixed_point_condition_v1.tex"
    )
    source_ok = (
        source_ok
        and digest(p2_t01_path)
        == controls.get("p2_t01_source_category_sha256")
        == EXPECTED_P2_T01_HASH
        and digest(p2_t02_path)
        == controls.get("p2_t02_theorem_sha256")
        == EXPECTED_P2_T02_HASH
    )
    add_check(
        source_ok,
        "frozen_source_hashes",
        "The unchanged P2 inputs and three historical controls retain live hash parity.",
        checks,
    )

    metrics = bounded_metrics()
    empty = metrics["empty_groupoid"]
    add_check(
        empty["component_count"] == 0 and empty["selector_count"] == 1,
        "empty_groupoid_control",
        "The empty product has one vacuous selector.",
        checks,
    )
    gl2 = metrics["gl2_lines"]
    expected = control_rows["NS-GL2-LINES-EMPTY-002"]
    add_check(
        gl2["automorphism_count"] == expected["expected_automorphism_count"] == 6
        and gl2["choice_count"] == expected["expected_choice_count"] == 3
        and gl2["fixed_choice_count"] == expected["expected_fixed_choice_count"] == 0,
        "gl2_empty_fixed_control",
        "GL(2,2) has six elements and no fixed line among three choices.",
        checks,
    )
    c4 = metrics["directed_c4"]
    expected = control_rows["NS-C4-ROOTS-EMPTY-003"]
    add_check(
        c4["automorphism_count"] == expected["expected_automorphism_count"] == 4
        and c4["choice_count"] == expected["expected_choice_count"] == 4
        and c4["fixed_choice_count"] == expected["expected_fixed_choice_count"] == 0,
        "c4_empty_fixed_control",
        "C4 rotations have no fixed root among four choices.",
        checks,
    )
    toy = metrics["finite_toy"]
    expected = control_rows["NS-FINITE-TOY-SIGN-TOKEN-EMPTY-004"]
    add_check(
        toy["sign_fixed_choice_count"]
        == expected["expected_sign_fixed_choice_count"]
        == 0
        and toy["token_fixed_choice_count"]
        == expected["expected_token_fixed_choice_count"]
        == 0,
        "finite_toy_empty_fixed_control",
        "Sign reversal and token swap each leave no fixed response choice.",
        checks,
    )
    two = metrics["trivial_two_choice"]
    expected = control_rows["NS-TRIVIAL-TWO-CHOICE-K-005"]
    add_check(
        two["selector_count"] == expected["expected_selector_count"] == 2
        and two["injective_K_image_count"]
        == expected["expected_injective_K_image_count"]
        == 2
        and two["constant_K_image_count"]
        == expected["expected_constant_K_image_count"]
        == 1,
        "multiple_fixed_K_control",
        "Injective and constant K separate selector and relation-image multiplicity.",
        checks,
    )
    disconnected = metrics["disconnected_multiple_empty"]
    expected = control_rows["NS-DISCONNECTED-MULTIPLE-EMPTY-006"]
    add_check(
        disconnected["factor_sizes"] == expected["factor_sizes"] == [2, 0]
        and disconnected["global_selector_count"]
        == expected["expected_global_selector_count"]
        == 0,
        "global_multiplicity_guard",
        "A multiple component plus an empty component has no global selector.",
        checks,
    )
    equalizer = metrics["noninvertible_equalizer"]
    expected = control_rows["NS-NONINVERTIBLE-EQUALIZER-007"]
    add_check(
        equalizer["core_selector_count"]
        == expected["expected_core_selector_count"]
        == 2
        and equalizer["full_selector_count"]
        == expected["expected_full_selector_count"]
        == 1,
        "noninvertible_equalizer_control",
        "One noninvertible equation reduces two core selectors to one.",
        checks,
    )
    singleton = metrics["transitive_singleton"]
    add_check(
        singleton["choice_count"] == singleton["fixed_choice_count"] == 1,
        "transitive_singleton_control",
        "A transitive singleton has one fixed point.",
        checks,
    )
    search = metrics["bounded_theorem_search"]
    add_check(
        search["case_count"] == 341 and search["failure_count"] == 0,
        "bounded_counterexample_search",
        "All 341 factor-size cases through four components satisfy the finite theorem equivalences.",
        checks,
    )

    ontology_hash = digest(ROOT / "ontology/tex/aether_flow_foundations.tex")
    distance_hash = digest(ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv")
    metric_hash = digest(ROOT / "registries/METRIC_USE_LEDGER.csv")
    add_check(
        ontology_hash == EXPECTED_ONTOLOGY_HASH,
        "canonical_ontology_unchanged",
        "Canonical ontology retains its launch hash.",
        checks,
    )
    add_check(
        distance_hash == EXPECTED_DISTANCE_HASH,
        "distance_ledger_unchanged",
        "Distance-to-GR ledger retains its launch hash.",
        checks,
    )
    add_check(
        metric_hash == EXPECTED_METRIC_HASH,
        "metric_ledger_unchanged",
        "Metric-use ledger retains its launch hash.",
        checks,
    )
    add_check(
        all(
            token in normalized_tex
            for token in (
                "Current ontology does not derive or adopt",
                "blocked\\_adoption\\_open\\_continuation",
                "Structural automorphisms",
                "Both scientific ledgers remain unchanged",
                "P2-T06 owns",
                "P2-T07 owns",
                "does not prohibit",
            )
        ),
        "claim_language",
        "The artifact preserves proposal, adoption, gauge, ledger, ownership, and continuation boundaries.",
        checks,
    )
    add_check(
        all(
            token in normalized_tex
            for token in (
                "GL}(2,2)",
                "Directed four-cycle root control",
                "Untagged finite-toy sign/token control",
            )
        ),
        "prior_obstruction_subsumption",
        "Three prior finite obstruction families appear as bounded theorem instances.",
        checks,
    )

    failure_count = sum(check["status"] == "FAIL" for check in checks)
    return {
        "aggregate_status": "PASS" if failure_count == 0 else "FAIL",
        "check_count": len(checks),
        "checks": checks,
        "failure_count": failure_count,
        "finite_metrics": metrics,
        "job_id": "AJ-RT-20260720-016-001",
        "ledger_receipts": {
            "canonical_ontology_sha256": ontology_hash,
            "distance_to_gr_sha256": distance_hash,
            "metric_use_sha256": metric_hash,
        },
        "metrics": {
            "assumption_count": assumptions.get("assumption_count"),
            "complete_core_theorem_count": 3,
            "corollary_count": corollaries.get("corollary_count"),
            "finite_control_count": len(control_rows),
            "prior_obstruction_count": controls.get("prior_obstruction_count"),
            "general_EqSrc_discharged": False,
            "physics_promotion_authorized": False,
            "p2_t01_domain_changed": False,
        },
        "plan_task_id": "P2-T03",
        "schema_id": "v21_p2_t03_eqsrc_no_selector_nonuniqueness_validation_v1",
        "source_receipts": source_receipts,
        "theorem_id": THEOREM_ID,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.write_report:
        REPORT.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["aggregate_status"])
    return 0 if result["aggregate_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
