#!/usr/bin/env python3
"""Support-only mutation tester for no-target-import guard behavior.

This tester creates deterministic text fixtures from a source-safe control
snippet, applies the v18 P7-T04 forbidden-premise mutations, and verifies that
the existing claim-language linter fails closed. It is support-only validator
tooling. It is not proof authority, not source-law adoption, not target metric
import, not MetricData(E) adoption, not g_eff adoption or scope expansion, not
matter coupling, not Einstein equations, not benchmark promotion, and not a
completed derivation.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"
GUARD_MAP_PATH = REPO_ROOT / "research_control/design/no_target_import_guard_map.md"

TESTER_ID = "no_target_import_mutation_tester"
TESTER_VERSION = "0.1.0"
SUPPORT_ONLY = True
PROOF_AUTHORITY = False
PHYSICS_PROMOTION_AUTHORIZED = False

BOUNDARY_STATEMENT = (
    "This no-target import mutation tester is support-only validator tooling. "
    "It has proof_authority=false and does not prove a source law, adopt a "
    "source law, import a target metric, adopt MetricData(E), adopt or expand "
    "g_eff, derive matter coupling, derive Einstein equations, promote a "
    "benchmark, issue a Gate Chair verdict, or complete the derivation."
)

BASE_SAFE_TEXT = (
    "The source-side audit record checks only source predicates and records "
    "fail-closed no-target import hygiene. No proof authority, source-law "
    "adoption, metric construction, matter coupling derivation, Einstein "
    "equations, benchmark promotion, or completed derivation follows."
)


@dataclass(frozen=True)
class MutationSpec:
    """One deterministic forbidden-premise mutation."""

    mutation_id: str
    inserted_text: str
    expected_linter_class_ids: tuple[str, ...]
    forbidden_source_classes: tuple[str, ...]
    fail_closed_response: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "expected_linter_class_ids": list(self.expected_linter_class_ids),
            "fail_closed_response": self.fail_closed_response,
            "forbidden_source_classes": list(self.forbidden_source_classes),
            "inserted_text": self.inserted_text,
            "mutation_id": self.mutation_id,
        }


MUTATIONS: tuple[MutationSpec, ...] = (
    MutationSpec(
        mutation_id="insert_target_metric_premise",
        inserted_text="Target-metric certificate supplies source certificate validity.",
        expected_linter_class_ids=(
            "source_certificate_overread",
            "target_metric_used_as_source_certificate",
        ),
        forbidden_source_classes=("target_metric",),
        fail_closed_response=(
            "Reject target-side metric evidence as source-certificate input."
        ),
    ),
    MutationSpec(
        mutation_id="insert_proper_time_normalization",
        inserted_text="Source certificate supplies detector protocol.",
        expected_linter_class_ids=(
            "semantic_layer_collapse_overclaim",
            "proper_time_used_as_source_readout",
        ),
        forbidden_source_classes=("proper_time", "empirical_detector_semantics"),
        fail_closed_response=(
            "Reject detector-clock or protocol readout as source-side semantics."
        ),
    ),
    MutationSpec(
        mutation_id="insert_empirical_detector_protocol",
        inserted_text=(
            "Detector-semantics certificate supplies source certificate validity."
        ),
        expected_linter_class_ids=(
            "source_certificate_overread",
            "detector_calibration_treated_as_source_label",
        ),
        forbidden_source_classes=("empirical_detector_semantics",),
        fail_closed_response=(
            "Reject detector semantics as a source-label substitute."
        ),
    ),
    MutationSpec(
        mutation_id="insert_stress_energy_semantics",
        inserted_text="Matter-sector evidence implies stress-energy tensor.",
        expected_linter_class_ids=(
            "premature_efe_prerequisite_overclaim",
            "stress_energy_tensor_used_to_prove_matter_semantics",
        ),
        forbidden_source_classes=("stress_energy_semantics",),
        fail_closed_response=(
            "Reject target-side stress-energy notation as source matter semantics."
        ),
    ),
    MutationSpec(
        mutation_id="insert_matter_action_premise",
        inserted_text="Matter-sector evidence as coupling law.",
        expected_linter_class_ids=(
            "semantic_layer_collapse_overclaim",
            "matter_action_used_to_prove_coupling_law",
        ),
        forbidden_source_classes=("matter_action",),
        fail_closed_response=(
            "Reject target action language as source coupling-law derivation."
        ),
    ),
    MutationSpec(
        mutation_id="insert_benchmark_behavior_premise",
        inserted_text=(
            "Benchmark-behavior certificate supplies source certificate validity."
        ),
        expected_linter_class_ids=(
            "source_certificate_overread",
            "benchmark_fit_used_as_source_evidence",
        ),
        forbidden_source_classes=("benchmark_success",),
        fail_closed_response="Reject benchmark behavior as source-side evidence.",
    ),
    MutationSpec(
        mutation_id="insert_validator_as_proof_premise",
        inserted_text="Validator PASS proves EFE.",
        expected_linter_class_ids=(
            "premature_efe_prerequisite_overclaim",
            "validator_pass_used_as_proof",
        ),
        forbidden_source_classes=("validator_authority",),
        fail_closed_response="Reject validator output as proof authority.",
    ),
)

MUTATION_IDS = tuple(spec.mutation_id for spec in MUTATIONS)


def _load_linter_module() -> Any:
    spec = importlib.util.spec_from_file_location("validate_claim_language", LINTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import linter from {LINTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _scan_text(text: str) -> dict[str, Any]:
    linter = _load_linter_module()
    taxonomy = linter.load_taxonomy(TAXONOMY_PATH)
    scanned_path = "research_control/current_frontier.md"
    findings = linter.scan_text_map(
        {scanned_path: text},
        taxonomy=taxonomy,
        reviewed_contexts=[],
        active_handoffs=set(),
    )
    return linter.report_dict(findings, scanned_paths=[scanned_path])


def select_mutations(selection: str) -> tuple[MutationSpec, ...]:
    if selection == "all":
        return MUTATIONS
    for spec in MUTATIONS:
        if spec.mutation_id == selection:
            return (spec,)
    raise ValueError(f"unknown mutation: {selection}")


def mutated_text(spec: MutationSpec) -> str:
    return f"{BASE_SAFE_TEXT} {spec.inserted_text}"


def run_mutation(spec: MutationSpec) -> dict[str, Any]:
    report = _scan_text(mutated_text(spec))
    observed_class_ids = sorted({finding["class_id"] for finding in report["findings"]})
    missing_expected = [
        class_id
        for class_id in spec.expected_linter_class_ids
        if class_id not in observed_class_ids
    ]
    passed = report["status"] == "FAIL" and not missing_expected
    return {
        "expected_linter_class_ids": list(spec.expected_linter_class_ids),
        "fail_closed": passed,
        "fail_closed_response": spec.fail_closed_response,
        "forbidden_source_classes": list(spec.forbidden_source_classes),
        "inserted_text": spec.inserted_text,
        "missing_expected_linter_class_ids": missing_expected,
        "mutation_id": spec.mutation_id,
        "mutated_text": mutated_text(spec),
        "observed_linter_class_ids": observed_class_ids,
        "observed_status": report["status"],
        "support_only": SUPPORT_ONLY,
        "proof_authority": PROOF_AUTHORITY,
        "physics_promotion_authorized": PHYSICS_PROMOTION_AUTHORIZED,
    }


def generate_report(selection: str = "all") -> dict[str, Any]:
    selected = select_mutations(selection)
    base_report = _scan_text(BASE_SAFE_TEXT)
    results = [run_mutation(spec) for spec in selected]
    failed_checks = [
        result["mutation_id"]
        for result in results
        if not result["fail_closed"]
    ]
    if base_report["status"] != "PASS":
        failed_checks.append("base_safe_text")
    return {
        "base_safe_text": BASE_SAFE_TEXT,
        "base_safe_text_status": base_report["status"],
        "boundary_statement": BOUNDARY_STATEMENT,
        "configured_mutations": list(MUTATION_IDS),
        "failed_check_count": len(failed_checks),
        "failed_checks": failed_checks,
        "guard_map_path": str(GUARD_MAP_PATH.relative_to(REPO_ROOT)),
        "mutation_count": len(results),
        "mutation_results": results,
        "physics_promotion_authorized": PHYSICS_PROMOTION_AUTHORIZED,
        "proof_authority": PROOF_AUTHORITY,
        "schema_id": "no_target_import_mutation_tester_report_v1",
        "source_law_adopted": False,
        "status": "PASS" if not failed_checks else "FAIL",
        "support_only": SUPPORT_ONLY,
        "tester_id": TESTER_ID,
        "tester_version": TESTER_VERSION,
        "validator_behavior_changed": False,
    }


def write_fixture_dir(report: dict[str, Any], fixture_dir: Path) -> None:
    fixture_dir.mkdir(parents=True, exist_ok=True)
    for result in report["mutation_results"]:
        path = fixture_dir / f"{result['mutation_id']}.json"
        payload = {
            "boundary_statement": BOUNDARY_STATEMENT,
            "fixture_id": result["mutation_id"],
            "mutated_text": result["mutated_text"],
            "support_only": SUPPORT_ONLY,
            "proof_authority": PROOF_AUTHORITY,
            "physics_promotion_authorized": PHYSICS_PROMOTION_AUTHORIZED,
            "expected_linter_class_ids": result["expected_linter_class_ids"],
        }
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# No-Target Import Mutation Tester Report",
        "",
        BOUNDARY_STATEMENT,
        "",
        f"- Status: `{report['status']}`",
        f"- Mutation count: `{report['mutation_count']}`",
        f"- Failed check count: `{report['failed_check_count']}`",
        "",
        "## Mutations",
        "",
    ]
    for result in report["mutation_results"]:
        lines.extend(
            [
                f"### `{result['mutation_id']}`",
                "",
                f"- Observed status: `{result['observed_status']}`",
                "- Observed classes: "
                + ", ".join(f"`{item}`" for item in result["observed_linter_class_ids"]),
                f"- Fail closed: `{str(result['fail_closed']).lower()}`",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _json_dump(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run support-only no-target import mutation tests."
    )
    parser.add_argument(
        "--mutation",
        default="all",
        choices=("all",) + MUTATION_IDS,
        help="Mutation to run; default runs all configured mutations.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    parser.add_argument("--json-output", type=Path, help="Write JSON report.")
    parser.add_argument("--markdown", type=Path, help="Write Markdown report.")
    parser.add_argument("--fixture-dir", type=Path, help="Write one fixture per mutation.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = generate_report(args.mutation)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(_json_dump(report), encoding="utf-8")
    if args.fixture_dir:
        write_fixture_dir(report, args.fixture_dir)
    if args.markdown:
        write_markdown(report, args.markdown)
    if args.json or not any((args.json_output, args.fixture_dir, args.markdown)):
        print(_json_dump(report), end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
