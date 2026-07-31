#!/usr/bin/env python3
"""Validate the bounded P9-T08 benchmark-suite audit.

This validator checks immutable input identities, suite-level fail-closed
status, parent/child synthesis, and selected independent-method arithmetic.
Passing it is control evidence only. It does not establish independent
replication, a benchmark pass, Gate E authority, or physics promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

TASK_DIR = REPO_ROOT / "research_control/tasks/RT-20260731-001"
ARTIFACT_DIR = TASK_DIR / "artifacts"
REPORT_PATH = ARTIFACT_DIR / "p9_t08_benchmark_audit_validation_v1.json"

EXPECTED_HASHES = {
    "research_control/tasks/RT-20260729-012/artifacts/source_derived_benchmark_protocol_v1.tex":
        "88ef097bf712ad115e9af62cc18a8b3eabb12f8545350f714ad065f702471007",
    "research_control/tasks/RT-20260729-012/artifacts/source_derived_benchmark_case_schema_v1.yaml":
        "5045de8fbaeb6c80b89ec88b71143a8aeaca1c892efadc4b7293cb438ee808d8",
    "research_control/tasks/RT-20260729-012/artifacts/target_import_firewall_v1.yaml":
        "ccb9297f817a9b4eeb886834a510e1f21d518a2668bc3fde9695b909d6884acf",
    "research_control/tasks/RT-20260729-012/artifacts/gate_e_readiness_checklist_v1.yaml":
        "a9cefe08cc6bc8b0653fdfc72144d24e54fb14e565f8a499be49093bc615bb76",
    "research_control/tasks/RT-20260730-008/artifacts/p9_t02_vacuum_minkowski_case_v1.yaml":
        "2fadb19c5849f1da5843c0e0599dbdc31790eab46587ce6718abbf4d3a0be79c",
    "research_control/tasks/RT-20260730-008/artifacts/p9_t02_provenance_dag_v1.yaml":
        "163d9154e81a7249cdd145841e28c0313fd4ee7b4dccb9621f29bb6b61633e7e",
    "research_control/tasks/RT-20260730-008/artifacts/p9_t02_source_output_seal_v1.json":
        "71b7dfb67b40d748867a5c49abf7b50c684f9e4a7f5962d8787a960a3dc541dd",
    "research_control/tasks/RT-20260730-008/artifacts/p9_t02_target_exposure_ledger_v1.yaml":
        "2bcb4a9c82508af58e680ea488e862e74a379ac82bc66253db4d120c71b3ac3b",
    "research_control/tasks/RT-20260730-008/artifacts/p9_t02_benchmark_case_receipt_v1.json":
        "49172f707fbaa243462788a2c22a63e19fcdd3ac0656142281fc1f013c8d884b",
    "research_control/tasks/RT-20260730-010/artifacts/p9_t03_weak_field_clock_case_v1.yaml":
        "45b79d5e3e371b3a2bcdde3f26296dad8c6ff65306d17cdf672bf76383eeb864",
    "research_control/tasks/RT-20260730-010/artifacts/p9_t03_provenance_dag_v1.yaml":
        "59fea0af53cf4b1c7277b239937ce6f868df8ada20e4c1cd9e651282e5bcbfb4",
    "research_control/tasks/RT-20260730-010/artifacts/p9_t03_source_output_seal_v1.json":
        "a1b12e2a8277c94c6a626092a6dd9c5c7ab79399e420551dcd9e8ddae22194c0",
    "research_control/tasks/RT-20260730-010/artifacts/p9_t03_target_exposure_ledger_v1.yaml":
        "6b6661d96a01f87b7ef66deaefd1154b26420c8a242405ee661d00f92d9d6586",
    "research_control/tasks/RT-20260730-010/artifacts/p9_t03_weak_field_clock_receipt_v1.json":
        "2142b17e344c5877fc056aa8d757d88b27b1b5fd58f450ff79eff29a45e142da",
    "research_control/tasks/RT-20260730-011/artifacts/p9_t04_causal_freefall_case_v1.yaml":
        "f3ee6d0d7c19f68daf9f6ed9a2e10cec964633694688cc62074edc9089f66255",
    "research_control/tasks/RT-20260730-011/artifacts/p9_t04_provenance_dag_v1.yaml":
        "bfa67fbe669ff42f13e9a18f6f95b6492d621bee861e569e02f20dec864e3fb4",
    "research_control/tasks/RT-20260730-011/artifacts/p9_t04_source_output_seal_v1.json":
        "852e029864b6ac3ee3d7f4803c7787049d9d23d2a9c5efc2bfdedbc324a3eb60",
    "research_control/tasks/RT-20260730-011/artifacts/p9_t04_target_exposure_ledger_v1.yaml":
        "421612292120ef16792972dacb3467c447627322d780c9e7a96ffb8368053fb6",
    "research_control/tasks/RT-20260730-011/artifacts/p9_t04_causal_freefall_receipt_v1.json":
        "fe12f4fed9561cd2e282b3a26bdac357e6862af4a915f10961caa77a31ed86ec",
    "research_control/tasks/RT-20260730-012/artifacts/p9_t05_cosmology_case_v1.yaml":
        "bfe3f84f49b083c566486a9b2281ee1bfd3798f81832203ec9a10264afd1ba4f",
    "research_control/tasks/RT-20260730-012/artifacts/p9_t05_provenance_dag_v1.yaml":
        "03b14a1ed39206e79a4e4891580359b29e5b75e43acf6ce19256c9555dcf370a",
    "research_control/tasks/RT-20260730-012/artifacts/p9_t05_source_output_seal_v1.json":
        "a76522a8e3598498bb5e946653ce235f8589bd860af1ab0c5bc4446072c3be86",
    "research_control/tasks/RT-20260730-012/artifacts/p9_t05_target_exposure_ledger_v1.yaml":
        "cf9674a4f51743d8f2325099f358fabdd1e69969ac791f89df708ba05e105d5d",
    "research_control/tasks/RT-20260730-012/artifacts/p9_t05_cosmology_receipt_v1.json":
        "d7dbf50217b47a5e1dd2bbb7195cac769b9ecd2e616fe6789b5c1e877dd5698b",
    "research_control/tasks/RT-20260730-013/artifacts/p9_t06_radiative_case_v1.yaml":
        "5fd283fa7d2fd0e76ad317270eb33cae33e9f0f5e42378dba846963f706de5dc",
    "research_control/tasks/RT-20260730-013/artifacts/p9_t06_provenance_dag_v1.yaml":
        "f4b9b45bccbd6d768fa7de9b07cdc03638c3f742a54128a61273c65e9a83b929",
    "research_control/tasks/RT-20260730-013/artifacts/p9_t06_source_output_seal_v1.json":
        "75652be75e31376fad01ab5ed45f7685108609e57ad7a185b287443c5d2f00a6",
    "research_control/tasks/RT-20260730-013/artifacts/p9_t06_target_exposure_ledger_v1.yaml":
        "f24d62e6289ee6021555b8e7199fd9c13d6b0d6a93cf5015ad385a093d25352d",
    "research_control/tasks/RT-20260730-013/artifacts/p9_t06_radiative_receipt_v1.json":
        "23cb0118404723f3151e70d2c96c17841a448118b31b1978dd0071ccd4343a6f",
    "research_control/tasks/RT-20260730-015/artifacts/p9_t07_nonlinear_compact_case_v1.yaml":
        "d9f2af284c192a053623c3b8fed3755309e19957236d6da6fedad8787a61cb7d",
    "research_control/tasks/RT-20260730-015/artifacts/p9_t07_provenance_dag_v1.yaml":
        "d503a8419b135edcddf77f86d7bca23bc3110aec48dabce4451116fcba25638c",
    "research_control/tasks/RT-20260730-015/artifacts/p9_t07_source_output_seal_v1.json":
        "762bba485a575df727bd2e69bd50d92e0d74fea32b191b0ffdfef955b541179c",
    "research_control/tasks/RT-20260730-015/artifacts/p9_t07_target_exposure_ledger_v1.yaml":
        "1e2d6e12ed515a8184c15746daf721bb8951bfb86c8816d05d46f1205f704d8c",
    "research_control/tasks/RT-20260730-015/artifacts/p9_t07_nonlinear_compact_receipt_v1.json":
        "18c29dcbd6d3b8e8d9af880841b8a59e5afabd8e691b86e82aa96627bfb860e8",
}

CASE_PATHS = {
    "P9-T02": "research_control/tasks/RT-20260730-008/artifacts/p9_t02_vacuum_minkowski_case_v1.yaml",
    "P9-T03": "research_control/tasks/RT-20260730-010/artifacts/p9_t03_weak_field_clock_case_v1.yaml",
    "P9-T04": "research_control/tasks/RT-20260730-011/artifacts/p9_t04_causal_freefall_case_v1.yaml",
    "P9-T05": "research_control/tasks/RT-20260730-012/artifacts/p9_t05_cosmology_case_v1.yaml",
    "P9-T06": "research_control/tasks/RT-20260730-013/artifacts/p9_t06_radiative_case_v1.yaml",
    "P9-T07": "research_control/tasks/RT-20260730-015/artifacts/p9_t07_nonlinear_compact_case_v1.yaml",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML map")
    return value


def values_for_key(value: Any, target: str) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key) == target:
                found.append(child)
            found.extend(values_for_key(child, target))
    elif isinstance(value, list):
        for child in value:
            found.extend(values_for_key(child, target))
    return found


def matrix_vector(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def run_checks() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"check": name, "passed": bool(condition), "detail": detail})

    for rel_path, expected in EXPECTED_HASHES.items():
        path = REPO_ROOT / rel_path
        actual = sha256(path) if path.is_file() else ""
        check(f"hash:{rel_path}", actual == expected, f"expected={expected} actual={actual}")

    cases: dict[str, dict[str, Any]] = {}
    for task_id, rel_path in CASE_PATHS.items():
        case = load_yaml(REPO_ROOT / rel_path)
        cases[task_id] = case
        outcomes = [str(item) for item in values_for_key(case, "outcome")]
        firewalls = [str(item) for item in values_for_key(case, "source_stage_firewall_status")]
        independence = [
            str(item) for item in values_for_key(case, "independent_reproduction_status")
        ]
        mutation_counts = values_for_key(
            case, "source_mutation_after_target_comparison_count"
        )
        mutation_authorizations = values_for_key(
            case, "mutation_after_seal_authorized"
        )
        rerun_counts = values_for_key(case, "target_informed_rerun_count")
        check(f"{task_id}:outcome", "INCONCLUSIVE" in outcomes, str(outcomes))
        check(f"{task_id}:firewall", "PASS" in firewalls, str(firewalls))
        check(
            f"{task_id}:independence",
            "NOT_ACQUIRED" in independence,
            str(independence),
        )
        check(
            f"{task_id}:mutation",
            (
                bool(mutation_counts)
                and all(int(item) == 0 for item in mutation_counts)
            )
            or (
                not mutation_counts
                and bool(mutation_authorizations)
                and all(item is False for item in mutation_authorizations)
            ),
            f"counts={mutation_counts} authorized={mutation_authorizations}",
        )
        check(
            f"{task_id}:rerun",
            bool(rerun_counts) and all(int(item) == 0 for item in rerun_counts),
            str(rerun_counts),
        )

    review = load_yaml(ARTIFACT_DIR / "p9_t08_benchmark_suite_red_team_review_v1.yaml")
    smuggling = load_yaml(ARTIFACT_DIR / "p9_t08_benchmark_smuggling_audit_v1.yaml")
    consistency = load_yaml(
        ARTIFACT_DIR / "p9_t08_cross_case_assumption_consistency_v1.yaml"
    )
    replication = load_yaml(
        ARTIFACT_DIR / "p9_t08_independent_replication_status_v1.yaml"
    )
    gate = load_yaml(ARTIFACT_DIR / "p9_t08_gate_e_readiness_matrix_v1.yaml")
    compact = json.loads(
        (ARTIFACT_DIR / "p9_t08_benchmark_audit_compact_receipt_v1.json").read_text()
    )
    math_child = load_yaml(
        ARTIFACT_DIR / "child_phys_math_p9_t08_benchmark_audit.yaml"
    )
    phil_child = load_yaml(
        ARTIFACT_DIR / "child_phys_phil_p9_t08_benchmark_audit.yaml"
    )
    conflict = load_yaml(
        ARTIFACT_DIR / "parent_conflict_review_p9_t08_benchmark_audit.yaml"
    )

    check(
        "review:verdict",
        review.get("verdict") == "external_expert_review_required",
        str(review.get("verdict")),
    )
    check(
        "review:context",
        review.get("review_context", {}).get("classification")
        == "same_context_role_review",
        str(review.get("review_context", {}).get("classification")),
    )
    check(
        "review:no_promotion",
        review.get("physics_promotion_authorized") is False,
        str(review.get("physics_promotion_authorized")),
    )
    check(
        "smuggling:result",
        smuggling.get("result")
        == "NO_DECLARED_TARGET_IMPORT_DETECTED_READINESS_STILL_BLOCKED",
        str(smuggling.get("result")),
    )
    check(
        "smuggling:six_cases",
        len(smuggling.get("case_audits", [])) == 6,
        str(len(smuggling.get("case_audits", []))),
    )
    check(
        "consistency:result",
        consistency.get("result")
        == "CONSISTENT_PROTOCOL_BOUNDARY_HETEROGENEOUS_SOURCE_CONTROLS_NO_UNIVERSAL_CALIBRATION",
        str(consistency.get("result")),
    )
    check(
        "replication:not_acquired",
        replication.get("qualifying_independent_replication_completed") is False,
        str(replication.get("qualifying_independent_replication_completed")),
    )
    check(
        "replication:same_context_not_independent",
        replication.get("same_context_method_checks_count_as_independent_replication")
        is False,
        str(
            replication.get(
                "same_context_method_checks_count_as_independent_replication"
            )
        ),
    )
    check(
        "gate:not_ready",
        gate.get("overall_readiness")
        == "NOT_READY_NO_BENCHMARK_PASS_NO_QUALIFYING_INDEPENDENT_REPLICATION",
        str(gate.get("overall_readiness")),
    )
    check("gate:criteria_count", len(gate.get("criteria", [])) == 10, "expected 10")
    check("compact:cases", compact.get("executed_case_count") == 6, str(compact))
    check("compact:inconclusive", compact.get("inconclusive_case_count") == 6, str(compact))
    check("compact:passes", compact.get("benchmark_pass_count") == 0, str(compact))
    check(
        "children:complete",
        math_child.get("status") == "completed"
        and phil_child.get("status") == "completed"
        and math_child.get("subagent_count") == 0
        and phil_child.get("subagent_count") == 0,
        "two internal perspectives; no delegated subagents",
    )
    check(
        "conflict:resolved",
        conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflicts") == [],
        str(conflict.get("unresolved_conflicts")),
    )
    check(
        "fusion:exists",
        (ARTIFACT_DIR / "parent_fusion_notes_p9_t08_benchmark_audit.md").is_file(),
        "parent fusion note",
    )

    record_a = [Fraction(0), Fraction(0), Fraction(0)]
    record_b = [Fraction(1, 8), Fraction(1, 16), Fraction(1, 4)]
    check("math:P9-T03", record_a != record_b and sum(record_b) == Fraction(7, 16), "coefficient records distinct")

    e_common = [Fraction(0)] * 5
    e_split = [Fraction(1), Fraction(1, 2), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)]
    check(
        "math:P9-T04",
        e_common != e_split and sum(abs(item) for item in e_split) == Fraction(9, 4),
        "E_split L1 sum=9/4",
    )

    lam = 1.25
    amplitude = 1.0 / math.sqrt(1.0 + 2.0 * lam)
    analytic_derivative = -(1.0 + 2.0 * lam) ** (-1.5)
    check(
        "math:P9-T05",
        math.isclose(analytic_derivative, -(amplitude**3), rel_tol=0, abs_tol=1e-15),
        "dA/dlambda=-A^3 at A0=gamma=1",
    )

    c4 = [
        [Fraction(2), Fraction(-1), Fraction(0), Fraction(-1)],
        [Fraction(-1), Fraction(2), Fraction(-1), Fraction(0)],
        [Fraction(0), Fraction(-1), Fraction(2), Fraction(-1)],
        [Fraction(-1), Fraction(0), Fraction(-1), Fraction(2)],
    ]
    c4_vectors = [
        ([Fraction(1), Fraction(0), Fraction(-1), Fraction(0)], Fraction(2)),
        ([Fraction(0), Fraction(1), Fraction(0), Fraction(-1)], Fraction(2)),
        ([Fraction(1), Fraction(-1), Fraction(1), Fraction(-1)], Fraction(4)),
    ]
    check(
        "math:P9-T06",
        all(
            matrix_vector(c4, vector) == [eigenvalue * item for item in vector]
            for vector, eigenvalue in c4_vectors
        ),
        "C4 quotient eigenvalues 2,2,4",
    )

    h = [Fraction(2, 3), Fraction(-1, 3), Fraction(-1, 3)]
    rho = [Fraction(4, 3), Fraction(-2, 3), Fraction(-2, 3)]
    nonlinear_gradient: list[Fraction] = []
    for i in range(3):
        total = Fraction(0)
        for j in range(3):
            if i == j:
                continue
            difference = h[i] - h[j]
            total += Fraction(1, 3) * (difference + difference**3)
        nonlinear_gradient.append(total)
    hessian = [
        [Fraction(8, 3), Fraction(-4, 3), Fraction(-4, 3)],
        [Fraction(-4, 3), Fraction(5, 3), Fraction(-1, 3)],
        [Fraction(-4, 3), Fraction(-1, 3), Fraction(5, 3)],
    ]
    v2 = [Fraction(0), Fraction(1), Fraction(-1)]
    v4 = [Fraction(2), Fraction(-1), Fraction(-1)]
    check(
        "math:P9-T07",
        nonlinear_gradient == rho
        and matrix_vector(hessian, v2) == [Fraction(2) * item for item in v2]
        and matrix_vector(hessian, v4) == [Fraction(4) * item for item in v4],
        "nonlinear residual zero and quotient Hessian eigenvalues 2,4",
    )

    failures = [item for item in checks if not item["passed"]]
    return {
        "schema_id": "p9_t08_benchmark_audit_validation_v1",
        "task_id": "RT-20260731-001",
        "plan_task_id": "P9-T08",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failures),
        "failures": failures,
        "checks": checks,
        "selected_method_recomputation_status": (
            "PASS_SAME_CONTEXT_NOT_INDEPENDENT_REPLICATION"
            if not failures
            else "FAIL"
        ),
        "qualifying_independent_replication_completed": False,
        "benchmark_pass_count": 0,
        "gate_e_verdict_issued": False,
        "physics_promotion_authorized": False,
        "authority_boundary": (
            "validation_and_same_context_recomputation_only_no_proof_gate_or_promotion_authority"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = run_checks()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.check:
        if not REPORT_PATH.is_file():
            report["status"] = "FAIL"
            report["failures"].append(
                {"check": "validation_report_exists", "passed": False, "detail": str(REPORT_PATH)}
            )
        else:
            saved = json.loads(REPORT_PATH.read_text())
            if saved.get("status") != report.get("status"):
                report["status"] = "FAIL"
                report["failures"].append(
                    {
                        "check": "validation_report_status_parity",
                        "passed": False,
                        "detail": f"saved={saved.get('status')} live={report.get('status')}",
                    }
                )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"{report['status']}: {report['check_count']} checks, "
            f"{report['failed_check_count']} failures"
        )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
