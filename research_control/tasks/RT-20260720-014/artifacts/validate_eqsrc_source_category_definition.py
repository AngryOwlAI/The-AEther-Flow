#!/usr/bin/env python3
"""Validate the bounded v21 P2-T01 EqSrc source-category packet."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = Path(__file__).resolve().parent
CATEGORY_ID = "EQSRC-SOURCE-CATEGORY-DEFINITION-V1"
EXPECTED_DISTANCE_HASH = "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61"
EXPECTED_METRIC_HASH = "a33349c7a153c4fbadb70c7c38b17cf0eebb7672b8e1f692702fc91edf17efcf"
EXPECTED_ONTOLOGY_HASH = "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2"
EXPECTED_SOURCES = {
    "FIN-ORIENTATION-F2-001": (
        "research_control/tasks/RT-20260718-041/artifacts/eqsrc_orientation_torsor_descent_law_refuter_countermodel.yaml",
        "a5bc1af23713145727bfad592a770691b5128d6ce6546966860d80c588a530a6",
    ),
    "FIN-DIRECTED-C4-002": (
        "research_control/tasks/RT-20260718-045/artifacts/eqsrc_ordered_motion_rooted_partition_law_refuter_countermodel.yaml",
        "9ddce9d042ef187d163043d6c2a98a7d1a796cd01a433d3d258632150a83325e",
    ),
    "FIN-ORDERED-CHAIN4-003": (
        "research_control/tasks/RT-20260718-047/artifacts/eqsrc_flow_generated_graded_orbit_root_law_candidate_v1.tex",
        "b712552d328f144491bff689b702eba6dc2027ce1cc61c7052adbca84b0639f7",
    ),
    "FIN-NONINVERTIBLE-004": (
        "research_control/tasks/RT-20260720-012/artifacts/eqsrc_canonical_selection_naturality_target_v1.tex",
        "c5aaaa70f4d7ce216a35d17af674e94e3f2866c1bdcfb28787a40d9f6636516c",
    ),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    value = yaml.safe_load((ARTIFACTS / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{name} must contain one YAML mapping")
    return value


def load_json(name: str) -> dict[str, Any]:
    value = json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{name} must contain one JSON object")
    return value


def check(condition: bool, check_id: str, detail: str, checks: list[dict[str, str]]) -> None:
    checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})


def matmul(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, c, d = left
    e, f, g, h = right
    return (
        (a * e + b * g) % 2,
        (a * f + b * h) % 2,
        (c * e + d * g) % 2,
        (c * f + d * h) % 2,
    )


def matvec(matrix: tuple[int, int, int, int], vector: tuple[int, int]) -> tuple[int, int]:
    a, b, c, d = matrix
    x, y = vector
    return ((a * x + b * y) % 2, (c * x + d * y) % 2)


def compute_finite_metrics() -> dict[str, Any]:
    matrices = [
        matrix
        for matrix in itertools.product(range(2), repeat=4)
        if (matrix[0] * matrix[3] - matrix[1] * matrix[2]) % 2 == 1
    ]
    matrix_set = set(matrices)
    identity_matrix = (1, 0, 0, 1)
    gl_compositions = [matmul(left, right) for left in matrices for right in matrices]
    gl_inverse_count = sum(
        any(
            matmul(matrix, candidate) == identity_matrix
            and matmul(candidate, matrix) == identity_matrix
            for candidate in matrices
        )
        for matrix in matrices
    )
    lines = [(1, 0), (0, 1), (1, 1)]
    gl_action_composition = all(
        matvec(matmul(left, right), line) == matvec(left, matvec(right, line))
        for left in matrices
        for right in matrices
        for line in lines
    )
    gl_transitive = all({matvec(matrix, line) for matrix in matrices} == set(lines) for line in lines)
    gl_common_fixed = [line for line in lines if all(matvec(matrix, line) == line for matrix in matrices)]

    rotations = list(range(4))
    c4_compositions = [(left + right) % 4 for left in rotations for right in rotations]
    c4_inverse_count = sum(any((rotation + candidate) % 4 == 0 for candidate in rotations) for rotation in rotations)
    c4_action_composition = all(
        ((vertex + right) % 4 + left) % 4 == (vertex + (left + right)) % 4
        for left in rotations
        for right in rotations
        for vertex in rotations
    )
    c4_transitive = all({(vertex + rotation) % 4 for rotation in rotations} == set(rotations) for vertex in rotations)
    c4_common_fixed = [vertex for vertex in rotations if all((vertex + rotation) % 4 == vertex for rotation in rotations)]

    carrier = tuple(range(4))
    phi = lambda n, i: min(i + n, 3)
    chain_action_checks = sum(1 for m in carrier for n in carrier for i in carrier if phi(m, phi(n, i)) == phi(m + n, i))
    chain_automorphisms = []
    for permutation in itertools.permutations(carrier):
        order_preserved = all((i < j) == (permutation[i] < permutation[j]) for i in carrier for j in carrier)
        action_preserved = all(permutation[phi(n, i)] == phi(n, permutation[i]) for n in carrier for i in carrier)
        if order_preserved and action_preserved:
            chain_automorphisms.append(permutation)
    chain_minima = [i for i in carrier if all(i <= j for j in carrier)]
    parity_relation = {(i, j) for i in carrier for j in carrier if i % 2 == j % 2}

    inclusion_source = {0}
    inclusion_target = {0, 1}
    source_equality = {(0, 0)}
    inclusion_direct_image = {(0, 0) for _ in source_equality}
    inclusion_reflexive = all((value, value) in inclusion_direct_image for value in inclusion_target)

    collapse_source = {0, 1}
    collapse_target_equality = {("star", "star")}
    collapse = {0: "star", 1: "star"}
    collapse_pullback = {
        (left, right)
        for left in collapse_source
        for right in collapse_source
        if (collapse[left], collapse[right]) in collapse_target_equality
    }
    collapse_source_equality = {(value, value) for value in collapse_source}

    return {
        "orientation": {
            "automorphism_count": len(matrices),
            "composition_check_count": len(gl_compositions),
            "closed": set(gl_compositions) <= matrix_set,
            "identity_present": identity_matrix in matrix_set,
            "inverse_check_count": gl_inverse_count,
            "action_composition": gl_action_composition,
            "transitive": gl_transitive,
            "common_fixed_candidate_count": len(gl_common_fixed),
        },
        "directed_c4": {
            "automorphism_count": len(rotations),
            "composition_check_count": len(c4_compositions),
            "closed": set(c4_compositions) <= set(rotations),
            "identity_present": 0 in rotations,
            "inverse_check_count": c4_inverse_count,
            "action_composition": c4_action_composition,
            "transitive": c4_transitive,
            "common_fixed_candidate_count": len(c4_common_fixed),
        },
        "ordered_chain4": {
            "action_pair_check_count": chain_action_checks,
            "automorphism_count": len(chain_automorphisms),
            "unique_minimum": chain_minima[0] if len(chain_minima) == 1 else None,
            "parity_relation_pair_count": len(parity_relation),
        },
        "noninvertible": {
            "inclusion_direct_image_reflexive": inclusion_reflexive,
            "collapse_pullback_pair_count": len(collapse_pullback),
            "source_equality_pair_count": len(collapse_source_equality),
            "collapse_pullback_equals_source_equality": collapse_pullback == collapse_source_equality,
        },
    }


def validate() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    source_receipts: list[dict[str, str]] = []

    tex_path = ARTIFACTS / "eqsrc_source_category_definition_v1.tex"
    schema_path = ARTIFACTS / "eqsrc_source_morphism_variation_schema.yaml"
    examples_path = ARTIFACTS / "eqsrc_source_category_finite_examples.json"
    math_path = ARTIFACTS / "child_phys_math_eqsrc_source_category.yaml"
    phil_path = ARTIFACTS / "child_phys_phil_eqsrc_source_category.yaml"
    conflict_path = ARTIFACTS / "parent_conflict_review_eqsrc_source_category.yaml"
    fusion_path = ARTIFACTS / "parent_fusion_notes_eqsrc_source_category.md"
    receipt_path = ARTIFACTS / "eqsrc_source_category_definition_receipt.md"
    required_paths = [tex_path, schema_path, examples_path, math_path, phil_path, conflict_path, fusion_path, receipt_path]
    check(all(path.is_file() for path in required_paths), "artifact_set", "All eight bounded source-category artifacts exist.", checks)

    tex = tex_path.read_text(encoding="utf-8")
    schema = load_yaml(schema_path.name)
    examples = load_json(examples_path.name)
    math = load_yaml(math_path.name)
    phil = load_yaml(phil_path.name)
    conflict = load_yaml(conflict_path.name)
    fusion = fusion_path.read_text(encoding="utf-8")

    check(
        schema.get("source_category_id") == CATEGORY_ID
        and examples.get("source_category_id") == CATEGORY_ID
        and math.get("source_category_id") == CATEGORY_ID
        and phil.get("source_category_id") == CATEGORY_ID,
        "category_identity",
        "Schema, finite examples, and both child records share the exact category identity.",
        checks,
    )
    check(
        "Category closure" in tex
        and "Core relation-transport and action functoriality" in tex
        and "does not prove the P1-T04 natural" in tex
        and "P2-T02" in tex,
        "theorem_scope",
        "The category and core-functor theorem have proofs while the selector theorem remains P2-T02 work.",
        checks,
    )
    check(
        tex.count("{") == tex.count("}")
        and "\\begin{document}" in tex
        and "\\end{document}" in tex,
        "tex_structure",
        "The TeX source has balanced braces and a complete document envelope.",
        checks,
    )
    check(
        schema.get("morphisms", {}).get("candidate_blind") is True
        and schema.get("morphisms", {}).get("identity_closed") is True
        and schema.get("morphisms", {}).get("composition_closed") is True
        and schema.get("isomorphism_certificate", {}).get("certificate_type") == "explicit_inverse_provenance_token",
        "morphism_contract",
        "Morphisms are candidate-blind and closed, and isomorphisms require explicit inverse provenance.",
        checks,
    )
    check(
        schema.get("relation_transport", {}).get("core_covariant") is True
        and schema.get("relation_transport", {}).get("arbitrary_noninvertible_covariant") is False
        and set(schema.get("relation_transport", {}).get("permitted_noninvertible_modes", []))
        == {"preservation", "exact_reflection", "proved_quotient_or_span_specific_transport", "undefined"},
        "relation_variance",
        "Covariant transport is confined to the core and all noninvertible branches are explicit.",
        checks,
    )
    check(
        schema.get("candidate_family", {}).get("object_meaning") == "eligible choices, not a selected choice"
        and schema.get("candidate_family", {}).get("natural_selector_constructed") is False
        and schema.get("candidate_family", {}).get("selector_theorem_status") == "reserved_for_P2-T02",
        "selector_boundary",
        "The candidate family is not a selected section and the selector theorem remains reserved for P2-T02.",
        checks,
    )
    check(
        schema.get("core_groupoid", {}).get("structural_automorphism_implies_physical_gauge") is False
        and schema.get("variations", {}).get("structural_morphism_by_default") is False
        and schema.get("source_extensions", {}).get("reduct_implies_conservative") is False,
        "ontology_model_boundary",
        "Structural automorphisms, variations, physical gauge, and extension conservativity remain distinct.",
        checks,
    )
    check(
        schema.get("adoption_status") == "blocked_adoption_open_continuation"
        and schema.get("claim_status") == "proposal-only"
        and schema.get("claim_boundary", {}).get("physics_promotion_authorized") is False
        and schema.get("claim_boundary", {}).get("next_plan_task") == "P2-T02",
        "status_vocabulary",
        "Controlled status, blocked adoption, no promotion, and the single next work item are explicit.",
        checks,
    )
    check(
        math.get("status") == "completed"
        and phil.get("status") == "completed"
        and math.get("claim_boundary", {}).get("selector_theorem_proved") is False
        and phil.get("claim_boundary", {}).get("claim_boundary_preserved") is True,
        "child_outputs",
        "Both required perspectives completed under the shared no-selector and no-promotion boundary.",
        checks,
    )
    check(
        conflict.get("status") == "completed"
        and conflict.get("resolution_rounds") == 1
        and not conflict.get("unresolved_blocking_conflicts")
        and all(item.get("status") == "resolved" for item in conflict.get("conflicts", []))
        and CATEGORY_ID in fusion,
        "parent_synthesis",
        "One parent review round resolved all conflicts and preserved the exact fused identity.",
        checks,
    )

    example_rows = {item["example_id"]: item for item in examples.get("examples", [])}
    source_ok = set(example_rows) == set(EXPECTED_SOURCES)
    for example_id, (expected_path, expected_hash) in EXPECTED_SOURCES.items():
        row = example_rows.get(example_id, {})
        source_path = ROOT / expected_path
        actual_hash = digest(source_path) if source_path.is_file() else "missing"
        source_receipts.append(
            {
                "example_id": example_id,
                "path": expected_path,
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
            }
        )
        source_ok = source_ok and row.get("source_artifact") == expected_path
        source_ok = source_ok and row.get("source_sha256") == expected_hash == actual_hash
    check(source_ok, "historical_source_hashes", "All three historical finite families and the P1 target retain live hash parity.", checks)

    metrics = compute_finite_metrics()
    orientation = metrics["orientation"]
    orientation_expected = example_rows["FIN-ORIENTATION-F2-001"]
    check(
        orientation["automorphism_count"] == orientation_expected["expected_automorphism_count"] == 6
        and orientation["composition_check_count"] == orientation_expected["expected_composition_checks"] == 36
        and orientation["inverse_check_count"] == orientation_expected["expected_inverse_checks"] == 6
        and orientation["common_fixed_candidate_count"] == orientation_expected["expected_common_fixed_candidate_count"] == 0
        and orientation["closed"]
        and orientation["identity_present"]
        and orientation["action_composition"]
        and orientation["transitive"],
        "finite_orientation_action",
        "GL(2,2) passes 36 compositions, six inverse checks, action composition, transitivity, and the no-fixed-line count.",
        checks,
    )

    directed_c4 = metrics["directed_c4"]
    c4_expected = example_rows["FIN-DIRECTED-C4-002"]
    check(
        directed_c4["automorphism_count"] == c4_expected["expected_automorphism_count"] == 4
        and directed_c4["composition_check_count"] == c4_expected["expected_composition_checks"] == 16
        and directed_c4["inverse_check_count"] == c4_expected["expected_inverse_checks"] == 4
        and directed_c4["common_fixed_candidate_count"] == c4_expected["expected_common_fixed_candidate_count"] == 0
        and directed_c4["closed"]
        and directed_c4["identity_present"]
        and directed_c4["action_composition"]
        and directed_c4["transitive"],
        "finite_directed_c4_action",
        "Directed C4 passes 16 compositions, four inverse checks, action composition, transitivity, and the no-fixed-root count.",
        checks,
    )

    chain = metrics["ordered_chain4"]
    chain_expected = example_rows["FIN-ORDERED-CHAIN4-003"]
    check(
        chain["action_pair_check_count"] == chain_expected["expected_action_pair_checks"] == 64
        and chain["automorphism_count"] == chain_expected["expected_automorphism_count"] == 1
        and chain["unique_minimum"] == chain_expected["expected_unique_minimum"] == 0
        and chain["parity_relation_pair_count"] == chain_expected["expected_parity_relation_pair_count"] == 8,
        "finite_ordered_chain_action",
        "The four-chain passes all 64 action checks, has one structural automorphism, one loaded minimum, and eight parity-relation pairs.",
        checks,
    )

    noninvertible = metrics["noninvertible"]
    noninvertible_expected = example_rows["FIN-NONINVERTIBLE-004"]
    check(
        noninvertible["inclusion_direct_image_reflexive"] is noninvertible_expected["expected_inclusion_direct_image_reflexive"] is False
        and noninvertible["collapse_pullback_pair_count"] == noninvertible_expected["expected_collapse_pullback_pair_count"] == 4
        and noninvertible["source_equality_pair_count"] == noninvertible_expected["expected_source_equality_pair_count"] == 2
        and noninvertible["collapse_pullback_equals_source_equality"] is False,
        "finite_noninvertible_variance_guard",
        "Inclusion direct image fails codomain reflexivity and collapse pullback strictly enlarges source equality.",
        checks,
    )

    distance_hash = digest(ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv")
    metric_hash = digest(ROOT / "registries/METRIC_USE_LEDGER.csv")
    ontology_hash = digest(ROOT / "ontology/tex/aether_flow_foundations.tex")
    check(distance_hash == EXPECTED_DISTANCE_HASH, "distance_ledger_unchanged", "Distance-to-GR ledger retains its launch hash.", checks)
    check(metric_hash == EXPECTED_METRIC_HASH, "metric_ledger_unchanged", "Metric-use ledger retains its launch hash.", checks)
    check(ontology_hash == EXPECTED_ONTOLOGY_HASH, "canonical_ontology_unchanged", "Canonical ontology retains its launch hash.", checks)
    check(
        all(
            token in tex
            for token in (
                "Current ontology does not derive",
                "blocked\\_adoption\\_open\\_continuation",
                "No selector is",
                "General \\(\\mathsf{EqSrc}\\)",
                "Both scientific",
                "P2-T02",
            )
        ),
        "claim_language",
        "The artifact preserves exact underdetermination, adoption, selector, EqSrc, ledger, and next-route boundaries.",
        checks,
    )

    failure_count = sum(item["status"] == "FAIL" for item in checks)
    return {
        "aggregate_status": "PASS" if failure_count == 0 else "FAIL",
        "check_count": len(checks),
        "checks": checks,
        "failure_count": failure_count,
        "finite_metrics": metrics,
        "job_id": "AJ-RT-20260720-014-001",
        "ledger_receipts": {
            "canonical_ontology_sha256": ontology_hash,
            "distance_to_gr_sha256": distance_hash,
            "metric_use_sha256": metric_hash,
        },
        "metrics": {
            "category_definition_count": 1,
            "finite_example_count": len(example_rows),
            "general_EqSrc_discharged": False,
            "inverse_provenance_schema_count": 1,
            "physics_promotion_authorized": False,
            "proved_core_functoriality_theorem_count": 1,
            "selector_constructed": False,
            "selector_theorem_proved": False,
        },
        "plan_task_id": "P2-T01",
        "schema_id": "v21_p2_t01_eqsrc_source_category_definition_validation_v1",
        "source_category_id": CATEGORY_ID,
        "source_receipts": source_receipts,
        "task_id": "RT-20260720-014",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        report_path = ARTIFACTS / "eqsrc_source_category_definition_validation.json"
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['aggregate_status']}: {report['check_count']} checks, {report['failure_count']} failures")
    return 0 if report["aggregate_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
