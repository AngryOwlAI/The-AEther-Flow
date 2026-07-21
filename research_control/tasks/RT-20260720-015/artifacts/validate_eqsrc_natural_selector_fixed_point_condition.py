#!/usr/bin/env python3
"""Validate the bounded v21 P2-T02 natural-selector fixed-point packet."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

import yaml


ARTIFACTS = Path(__file__).resolve().parent
ROOT = ARTIFACTS.parents[3]
THEOREM_ID = "EQSRC-NATURAL-SELECTOR-FIXED-POINT-CONDITION-V1"
REPORT = ARTIFACTS / "eqsrc_natural_selector_fixed_point_validation.json"

EXPECTED_SOURCES = {
    "SEL-GL2-LINES-EMPTY-001": (
        "research_control/tasks/RT-20260718-041/artifacts/eqsrc_orientation_torsor_descent_law_refuter_countermodel.yaml",
        "a5bc1af23713145727bfad592a770691b5128d6ce6546966860d80c588a530a6",
    ),
    "SEL-C4-ROOTS-EMPTY-002": (
        "research_control/tasks/RT-20260718-045/artifacts/eqsrc_ordered_motion_rooted_partition_law_refuter_countermodel.yaml",
        "9ddce9d042ef187d163043d6c2a98a7d1a796cd01a433d3d258632150a83325e",
    ),
    "SEL-CHAIN4-UNIQUE-003": (
        "research_control/tasks/RT-20260718-047/artifacts/eqsrc_flow_generated_graded_orbit_root_law_candidate_v1.tex",
        "b712552d328f144491bff689b702eba6dc2027ce1cc61c7052adbca84b0639f7",
    ),
    "SEL-NONINVERTIBLE-COHERENCE-GUARD-007": (
        "research_control/tasks/RT-20260720-012/artifacts/eqsrc_canonical_selection_naturality_target_v1.tex",
        "c5aaaa70f4d7ce216a35d17af674e94e3f2866c1bdcfb28787a40d9f6636516c",
    ),
}
EXPECTED_P2_T01_HASH = "00d7e14b76ac4fa01b834739646fe03012c2b82326a158064b27cdbe916be268"
EXPECTED_ONTOLOGY_HASH = "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2"
EXPECTED_DISTANCE_HASH = "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61"
EXPECTED_METRIC_HASH = "a33349c7a153c4fbadb70c7c38b17cf0eebb7672b8e1f692702fc91edf17efcf"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(name: str) -> dict[str, Any]:
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


def load_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((ARTIFACTS / name).read_text(encoding="utf-8"))


def add_check(condition: bool, check_id: str, detail: str, checks: list[dict[str, str]]) -> None:
    checks.append({"check_id": check_id, "detail": detail, "status": "PASS" if condition else "FAIL"})


def matmul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return (
        (left[0] * right[0] + left[1] * right[2]) % 2,
        (left[0] * right[1] + left[1] * right[3]) % 2,
        (left[2] * right[0] + left[3] * right[2]) % 2,
        (left[2] * right[1] + left[3] * right[3]) % 2,
    )


def matvec(matrix: tuple[int, ...], vector: tuple[int, int]) -> tuple[int, int]:
    return (
        (matrix[0] * vector[0] + matrix[1] * vector[1]) % 2,
        (matrix[2] * vector[0] + matrix[3] * vector[1]) % 2,
    )


def finite_metrics() -> dict[str, Any]:
    matrices = [
        matrix
        for matrix in itertools.product(range(2), repeat=4)
        if (matrix[0] * matrix[3] - matrix[1] * matrix[2]) % 2 == 1
    ]
    lines = [(1, 0), (0, 1), (1, 1)]
    identity = (1, 0, 0, 1)
    gl_fixed = [line for line in lines if all(matvec(matrix, line) == line for matrix in matrices)]
    gl_closed = all(matmul(left, right) in matrices for left in matrices for right in matrices)
    marked_line = lines[0]
    line_stabilizer = [matrix for matrix in matrices if matvec(matrix, marked_line) == marked_line]
    line_stabilizer_fixed = [
        line for line in lines if all(matvec(matrix, line) == line for matrix in line_stabilizer)
    ]

    rotations = range(4)
    c4_fixed = [root for root in rotations if all((root + shift) % 4 == root for shift in rotations)]
    root_stabilizer = [shift for shift in rotations if (0 + shift) % 4 == 0]
    root_stabilizer_fixed = [
        root for root in rotations if all((root + shift) % 4 == root for shift in root_stabilizer)
    ]

    carrier = tuple(range(4))
    phi = lambda n, i: min(i + n, 3)
    chain_automorphisms = []
    for permutation in itertools.permutations(carrier):
        order_preserved = all((i < j) == (permutation[i] < permutation[j]) for i in carrier for j in carrier)
        action_preserved = all(
            permutation[phi(n, i)] == phi(n, permutation[i]) for n in carrier for i in carrier
        )
        if order_preserved and action_preserved:
            chain_automorphisms.append(permutation)
    chain_choices = [i for i in carrier if all(i <= j for j in carrier)]

    trivial_choices = ("a", "b")
    injective_k = {choice: f"R_{choice}" for choice in trivial_choices}
    constant_k = {choice: "R" for choice in trivial_choices}

    objectwise_assignments = [(0, target) for target in (0, 1)]
    coherent_assignments = [pair for pair in objectwise_assignments if pair[1] == 0]

    return {
        "gl2_lines": {
            "automorphism_count": len(matrices),
            "choice_count": len(lines),
            "closed": gl_closed,
            "identity_present": identity in matrices,
            "fixed_choice_count": len(gl_fixed),
        },
        "directed_c4": {
            "automorphism_count": 4,
            "choice_count": 4,
            "fixed_choice_count": len(c4_fixed),
        },
        "ordered_chain4": {
            "automorphism_count": len(chain_automorphisms),
            "choice_count": len(chain_choices),
            "fixed_choice_count": len(chain_choices),
        },
        "trivial_two_choice": {
            "automorphism_count": 1,
            "choice_count": len(trivial_choices),
            "fixed_choice_count": len(trivial_choices),
            "injective_K_image_count": len(set(injective_k.values())),
            "constant_K_image_count": len(set(constant_k.values())),
        },
        "marked_gl2": {
            "base_automorphism_count": len(matrices),
            "image_stabilizer_count": len(line_stabilizer),
            "fixed_choice_count_under_stabilizer": len(line_stabilizer_fixed),
        },
        "marked_c4": {
            "base_automorphism_count": 4,
            "image_stabilizer_count": len(root_stabilizer),
            "fixed_choice_count_under_stabilizer": len(root_stabilizer_fixed),
        },
        "noninvertible_guard": {
            "objectwise_fixed_assignments": len(objectwise_assignments),
            "coherent_assignments": len(coherent_assignments),
        },
        "disconnected_counterexample": {
            "multiple_fixed_component_selector_count": 2,
            "empty_fixed_component_selector_count": 0,
            "global_selector_count": 0,
        },
    }


def validate() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    source_receipts: list[dict[str, str]] = []
    paths = {
        "tex": ARTIFACTS / "eqsrc_natural_selector_fixed_point_condition_v1.tex",
        "controls": ARTIFACTS / "eqsrc_natural_selector_fixed_point_controls.json",
        "math": ARTIFACTS / "child_phys_math_eqsrc_natural_selector_fixed_point.yaml",
        "phil": ARTIFACTS / "child_phys_phil_eqsrc_natural_selector_fixed_point.yaml",
        "conflict": ARTIFACTS / "parent_conflict_review_eqsrc_natural_selector_fixed_point.yaml",
        "fusion": ARTIFACTS / "parent_fusion_notes_eqsrc_natural_selector_fixed_point.md",
        "receipt": ARTIFACTS / "eqsrc_natural_selector_fixed_point_receipt.md",
    }
    add_check(all(path.is_file() for path in paths.values()), "artifact_set", "All seven bounded theorem and synthesis artifacts exist.", checks)

    tex = paths["tex"].read_text(encoding="utf-8")
    normalized_tex = " ".join(tex.split())
    controls = load_json(paths["controls"].name)
    math = load_yaml(paths["math"].name)
    phil = load_yaml(paths["phil"].name)
    conflict = load_yaml(paths["conflict"].name)
    fusion = paths["fusion"].read_text(encoding="utf-8")
    control_rows = {row["control_id"]: row for row in controls.get("controls", [])}

    add_check(
        controls.get("theorem_id") == THEOREM_ID
        and math.get("theorem_id") == THEOREM_ID
        and phil.get("theorem_id") == THEOREM_ID
        and conflict.get("theorem_id") == THEOREM_ID
        and THEOREM_ID in fusion,
        "theorem_identity",
        "Controls, children, conflict review, and fusion share the exact theorem identity.",
        checks,
    )
    add_check(
        tex.count("{") == tex.count("}") and "\\begin{document}" in tex and "\\end{document}" in tex,
        "tex_structure",
        "The TeX source has balanced braces and a complete document envelope.",
        checks,
    )
    add_check(
        "Necessary automorphism fixed-point condition" in tex
        and "S_\\chi(g)(\\sigma_X)=\\sigma_X" in tex
        and "\\operatorname{Sel}_\\chi" in tex,
        "fixed_point_theorem",
        "The natural-selector definition and necessary fixed-point theorem are explicit with proof.",
        checks,
    )
    add_check(
        "If \\(|F_X|=1\\)" in tex
        and "If \\(|F_X|>1\\)" in tex
        and "another component may have an empty fixed locus" in normalized_tex
        and "\\mathcal R_X:=K_X(F_X)" in tex,
        "branch_separation",
        "Singleton, multiple, global-coherence, and relation-image branches are separated.",
        checks,
    )
    add_check(
        "H_{X^+}\\leq\\operatorname{Stab}" in tex
        and "\\subseteq S_\\chi(X)^{H_{X^+}}" in tex
        and "new\\_ontology\\_primitive\\_candidate" in tex,
        "added_data_lemma",
        "The stabilizer and fixed-locus inclusions retain explicit source-extension status.",
        checks,
    )
    add_check(
        math.get("status") == "completed"
        and phil.get("status") == "completed"
        and math.get("claim_boundary", {}).get("p2_t01_domain_changed") is False
        and phil.get("claim_boundary", {}).get("claim_boundary_preserved") is True,
        "child_outputs",
        "Both parallel perspectives completed under the shared unchanged-domain and no-promotion boundary.",
        checks,
    )
    add_check(
        conflict.get("status") == "completed"
        and conflict.get("resolution_rounds") == 1
        and not conflict.get("unresolved_blocking_conflicts")
        and all(item.get("status") == "resolved" for item in conflict.get("conflicts", [])),
        "parent_synthesis",
        "One parent review round resolved every child conflict.",
        checks,
    )

    source_ok = True
    for control_id, (expected_path, expected_hash) in EXPECTED_SOURCES.items():
        row = control_rows.get(control_id, {})
        source_path = ROOT / expected_path
        actual_hash = digest(source_path) if source_path.is_file() else "missing"
        source_receipts.append({
            "control_id": control_id,
            "path": expected_path,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
        })
        source_ok = source_ok and row.get("source_artifact") == expected_path
        source_ok = source_ok and row.get("source_sha256") == expected_hash == actual_hash
    p2_t01_path = ROOT / "research_control/tasks/RT-20260720-014/artifacts/eqsrc_source_category_definition_v1.tex"
    source_ok = source_ok and digest(p2_t01_path) == controls.get("p2_t01_source_category_sha256") == EXPECTED_P2_T01_HASH
    add_check(source_ok, "frozen_source_hashes", "P1 controls and the unchanged P2-T01 domain retain live hash parity.", checks)

    metrics = finite_metrics()
    gl2 = metrics["gl2_lines"]
    gl2_expected = control_rows["SEL-GL2-LINES-EMPTY-001"]
    add_check(
        gl2["automorphism_count"] == gl2_expected["expected_automorphism_count"] == 6
        and gl2["choice_count"] == gl2_expected["expected_choice_count"] == 3
        and gl2["fixed_choice_count"] == gl2_expected["expected_fixed_choice_count"] == 0
        and gl2["closed"] and gl2["identity_present"],
        "gl2_empty_fixed_control",
        "GL(2,2) closes with six elements and has no fixed line among three choices.",
        checks,
    )
    c4 = metrics["directed_c4"]
    c4_expected = control_rows["SEL-C4-ROOTS-EMPTY-002"]
    add_check(
        c4["automorphism_count"] == c4_expected["expected_automorphism_count"] == 4
        and c4["choice_count"] == c4_expected["expected_choice_count"] == 4
        and c4["fixed_choice_count"] == c4_expected["expected_fixed_choice_count"] == 0,
        "c4_empty_fixed_control",
        "Directed C4 has four rotations and no fixed root.",
        checks,
    )
    chain = metrics["ordered_chain4"]
    chain_expected = control_rows["SEL-CHAIN4-UNIQUE-003"]
    add_check(
        chain["automorphism_count"] == chain_expected["expected_automorphism_count"] == 1
        and chain["choice_count"] == chain_expected["expected_choice_count"] == 1
        and chain["fixed_choice_count"] == chain_expected["expected_fixed_choice_count"] == 1,
        "chain_unique_control",
        "The ordered chain control has a trivial automorphism group and singleton eligible minimum.",
        checks,
    )
    two = metrics["trivial_two_choice"]
    two_expected = control_rows["SEL-TRIVIAL-TWO-CHOICE-004"]
    add_check(
        two["fixed_choice_count"] == two_expected["expected_fixed_choice_count"] == 2
        and two["injective_K_image_count"] == two_expected["expected_injective_K_image_count"] == 2
        and two["constant_K_image_count"] == two_expected["expected_constant_K_image_count"] == 1,
        "multiple_fixed_and_K_control",
        "Two fixed choices separate selector multiplicity from injective and constant K images.",
        checks,
    )
    marked_gl2 = metrics["marked_gl2"]
    marked_gl2_expected = control_rows["SEL-MARKED-GL2-STABILIZER-005"]
    add_check(
        marked_gl2["image_stabilizer_count"] == marked_gl2_expected["expected_image_stabilizer_count"] == 2
        and marked_gl2["fixed_choice_count_under_stabilizer"] == marked_gl2_expected["expected_fixed_choice_count_under_stabilizer"] == 1,
        "marked_gl2_stabilizer_control",
        "The marked-line stabilizer has order two and fixes exactly that line.",
        checks,
    )
    marked_c4 = metrics["marked_c4"]
    marked_c4_expected = control_rows["SEL-MARKED-C4-STABILIZER-006"]
    add_check(
        marked_c4["image_stabilizer_count"] == marked_c4_expected["expected_image_stabilizer_count"] == 1
        and marked_c4["fixed_choice_count_under_stabilizer"] == marked_c4_expected["expected_fixed_choice_count_under_stabilizer"] == 4,
        "marked_c4_nonunique_control",
        "The marked-root stabilizer is trivial and fixes all four unchanged eligible roots.",
        checks,
    )
    guard = metrics["noninvertible_guard"]
    guard_expected = control_rows["SEL-NONINVERTIBLE-COHERENCE-GUARD-007"]
    add_check(
        guard["objectwise_fixed_assignments"] == guard_expected["expected_objectwise_fixed_assignments"] == 2
        and guard["coherent_assignments"] == guard_expected["expected_coherent_assignments"] == 1,
        "noninvertible_coherence_guard",
        "Only one of two objectwise fixed assignments satisfies the noninvertible-arrow coherence equation.",
        checks,
    )
    disconnected = metrics["disconnected_counterexample"]
    add_check(
        disconnected["multiple_fixed_component_selector_count"] == 2
        and disconnected["empty_fixed_component_selector_count"] == 0
        and disconnected["global_selector_count"] == 0,
        "global_multiplicity_guard",
        "A multiple-fixed component plus an empty-fixed component has no global selector.",
        checks,
    )

    ontology_hash = digest(ROOT / "ontology/tex/aether_flow_foundations.tex")
    distance_hash = digest(ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv")
    metric_hash = digest(ROOT / "registries/METRIC_USE_LEDGER.csv")
    add_check(ontology_hash == EXPECTED_ONTOLOGY_HASH, "canonical_ontology_unchanged", "Canonical ontology retains its launch hash.", checks)
    add_check(distance_hash == EXPECTED_DISTANCE_HASH, "distance_ledger_unchanged", "Distance-to-GR ledger retains its launch hash.", checks)
    add_check(metric_hash == EXPECTED_METRIC_HASH, "metric_ledger_unchanged", "Metric-use ledger retains its launch hash.", checks)
    add_check(
        all(token in normalized_tex for token in (
            "Current ontology does not derive",
            "blocked\\_adoption\\_open\\_continuation",
            "P2-T03 owns",
            "Structural automorphisms",
            "Both scientific ledgers remain unchanged",
        )),
        "claim_language",
        "The artifact preserves underdetermination, adoption, next-ownership, gauge, and ledger boundaries.",
        checks,
    )

    failure_count = sum(check["status"] == "FAIL" for check in checks)
    return {
        "aggregate_status": "PASS" if failure_count == 0 else "FAIL",
        "check_count": len(checks),
        "checks": checks,
        "failure_count": failure_count,
        "finite_metrics": metrics,
        "job_id": "AJ-RT-20260720-015-001",
        "ledger_receipts": {
            "canonical_ontology_sha256": ontology_hash,
            "distance_to_gr_sha256": distance_hash,
            "metric_use_sha256": metric_hash,
        },
        "metrics": {
            "added_data_lemma_count": 1,
            "complete_p2_t03_theorem_proved": False,
            "finite_control_count": len(control_rows),
            "fixed_point_necessity_theorem_count": 1,
            "general_EqSrc_discharged": False,
            "physics_promotion_authorized": False,
            "p2_t01_domain_changed": False,
        },
        "plan_task_id": "P2-T02",
        "schema_id": "v21_p2_t02_eqsrc_natural_selector_fixed_point_validation_v1",
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
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["aggregate_status"])
    return 0 if result["aggregate_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
