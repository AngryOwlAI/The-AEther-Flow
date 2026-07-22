#!/usr/bin/env python3
"""Validate the bounded v21 P11-T04 semantic-smuggling fixture suite."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Sequence


ARTIFACT_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[4]
MUTATOR_PATH = ARTIFACT_DIR / "semantic_smuggling_mutator.py"
CATALOG_PATH = ARTIFACT_DIR / "semantic_smuggling_fixture_catalog.json"
COMPARISON_PATH = ARTIFACT_DIR / "semantic_smuggling_checker_comparison.json"
COMPARISON_MD_PATH = ARTIFACT_DIR / "semantic_smuggling_checker_comparison.md"
VALIDATION_PATH = ARTIFACT_DIR / "semantic_smuggling_validation.json"
RECEIPT_PATH = ARTIFACT_DIR / "semantic_smuggling_compact_receipt.json"
TEST_PATH = REPO_ROOT / "tests" / "test_semantic_smuggling_adversarial_suite.py"
LINTER_PATH = REPO_ROOT / "scripts" / "project_control" / "validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control" / "design" / "claim_language_linter_taxonomy.yaml"
GUARD_MAP_PATH = REPO_ROOT / "research_control" / "design" / "no_target_import_guard_map.md"
DEPENDENCY_COMPLETIONS = {
    REPO_ROOT
    / "research_control/tasks/RT-20260722-004/jobs/completions/AJC-AJ-RT-20260722-004-001.yaml":
        "c0a9811467d9591a9c9eb8afcac6b37b5b9c57ab962de06c7bf1e9d8324d3b85",
    REPO_ROOT
    / "research_control/tasks/RT-20260722-005/jobs/completions/AJC-AJ-RT-20260722-005-001.yaml":
        "752d2d330f4d1eb974a1e15209efe125a89ca145345ac92c26ae7e3dda350380",
}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_mutator() -> Any:
    spec = importlib.util.spec_from_file_location("p11_t04_semantic_smuggling_mutator_validator", MUTATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import mutator from {MUTATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_suite() -> dict[str, Any]:
    checks: list[dict[str, str]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({
            "check_id": check_id,
            "detail": detail,
            "status": "PASS" if passed else "FAIL",
        })

    required_paths = (
        MUTATOR_PATH,
        CATALOG_PATH,
        COMPARISON_PATH,
        COMPARISON_MD_PATH,
        TEST_PATH,
        LINTER_PATH,
        TAXONOMY_PATH,
        GUARD_MAP_PATH,
        *DEPENDENCY_COMPLETIONS,
    )
    for path in required_paths:
        check(f"exists:{path.name}", path.is_file(), f"{repo_relative(path)} exists")

    mutator = load_mutator()
    generated = mutator.generated_outputs()
    drift_paths = [
        repo_relative(path)
        for path, expected in generated.items()
        if not path.is_file() or path.read_bytes() != expected
    ]
    check("corpus_deterministic_rebuild", not drift_paths, f"drift_paths={drift_paths}")

    catalog = load_json(CATALOG_PATH)
    comparison = load_json(COMPARISON_PATH)
    attack_rows = [row for row in comparison.get("rows", []) if row.get("label") == "attack"]
    benign_rows = [row for row in comparison.get("rows", []) if row.get("label") == "benign"]
    direct_rows = [
        row
        for row in comparison.get("rows", [])
        if next(
            (
                fixture.get("direct_import_control")
                for fixture in catalog.get("fixtures", [])
                if fixture.get("fixture_id") == row.get("fixture_id")
            ),
            False,
        )
    ]
    observed_attack_classes = {row.get("attack_class") for row in attack_rows}
    check(
        "attack_class_coverage",
        observed_attack_classes == set(mutator.ATTACK_CLASSES),
        f"observed={sorted(observed_attack_classes)}",
    )
    check(
        "direct_import_controls_fail",
        bool(direct_rows) and all(row.get("lexical_detected") is True for row in direct_rows),
        f"direct_controls={len(direct_rows)} lexical_misses={sum(not row.get('lexical_detected') for row in direct_rows)}",
    )
    check(
        "semantic_attack_recall",
        bool(attack_rows)
        and all(row.get("semantic_detected") is True for row in attack_rows)
        and comparison.get("probe", {}).get("metrics", {}).get("false_negative") == 0,
        f"attacks={len(attack_rows)} false_negatives={comparison.get('probe', {}).get('metrics', {}).get('false_negative')}",
    )
    check(
        "benign_control_specificity",
        len(benign_rows) >= 6
        and all(row.get("semantic_detected") is False for row in benign_rows)
        and comparison.get("probe", {}).get("metrics", {}).get("false_positive") == 0,
        f"benign={len(benign_rows)} false_positives={comparison.get('probe', {}).get('metrics', {}).get('false_positive')}",
    )
    row_map = {row.get("fixture_id"): row for row in comparison.get("rows", [])}
    check(
        "misleading_certificate_detection",
        "misleading_no_target_certificate"
        in row_map.get("ATT-MISLEADING-CERTIFICATE-001", {}).get("semantic_rule_ids", []),
        "misleading no-target certificate is rejected by the bounded probe",
    )
    prompt_rule_ids = {
        rule_id
        for fixture_id in (
            "ATT-PROMPT-WORLDLINE-READOUT-001",
            "ATT-PROMPT-REFERENCE-SUITE-001",
        )
        for rule_id in row_map.get(fixture_id, {}).get("semantic_rule_ids", [])
    }
    check(
        "prompt_level_attack_detection",
        {
            "prompt_level_proper_time_import",
            "prompt_level_benchmark_import",
        }.issubset(prompt_rule_ids),
        f"prompt_rule_ids={sorted(prompt_rule_ids)}",
    )
    lexical_metrics = comparison.get("lexical_linter", {}).get("metrics", {})
    semantic_metrics = comparison.get("probe", {}).get("metrics", {})
    check(
        "checker_confusion_matrix",
        lexical_metrics.get("false_negative", 0) >= 1
        and semantic_metrics.get("false_negative") == 0
        and semantic_metrics.get("false_positive") == 0,
        f"lexical={lexical_metrics} semantic={semantic_metrics}",
    )
    limitations = " ".join(comparison.get("limitations", [])).casefold()
    check(
        "explicit_limitations",
        "does not establish semantic completeness" in limitations
        and "blind" in limitations
        and "human" in limitations
        and "scientific truth" in limitations,
        "semantic completeness, scientific truth, blind review, and human review remain outside the result",
    )
    check(
        "boundary_flags_false",
        comparison.get("production_linter_changed") is False
        and all(value is False for value in comparison.get("boundary", {}).values())
        and all(
            all(value is False for value in fixture.get("boundary", {}).values())
            for fixture in catalog.get("fixtures", [])
        ),
        "production policy, proof, review, science, adoption, and promotion authority remain false",
    )
    dependency_observations: dict[str, str] = {}
    for path, expected_hash in DEPENDENCY_COMPLETIONS.items():
        observed_hash = sha256_file(path)
        dependency_observations[repo_relative(path)] = observed_hash
        check(
            f"dependency_hash:{path.parent.parent.parent.name}",
            observed_hash == expected_hash,
            f"expected={expected_hash} observed={observed_hash}",
        )

    failed = [item for item in checks if item["status"] == "FAIL"]
    hashed_paths = sorted({*required_paths, Path(__file__)})
    return {
        "artifact_hashes": {repo_relative(path): sha256_file(path) for path in hashed_paths},
        "attack_class_count": len(observed_attack_classes),
        "attack_fixture_count": len(attack_rows),
        "benign_fixture_count": len(benign_rows),
        "boundary": dict(mutator.BOUNDARY),
        "check_count": len(checks),
        "checks": checks,
        "corpus_sha256": comparison.get("corpus_sha256"),
        "dependency_completion_hashes": dict(sorted(dependency_observations.items())),
        "failed_check_count": len(failed),
        "fixture_count": comparison.get("fixture_count"),
        "lexical_metrics": lexical_metrics,
        "limitations": comparison.get("limitations", []),
        "plan_task_id": "P11-T04",
        "production_linter_changed": False,
        "probe_id": comparison.get("probe", {}).get("probe_id"),
        "recommendation_ids": ["V21-R55", "V21-R56", "V21-R59", "V21-R63"],
        "schema_id": "v21_semantic_smuggling_validation_v1",
        "semantic_metrics": semantic_metrics,
        "status": "PASS" if not failed else "FAIL",
    }


def build_receipt(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_hashes": report["artifact_hashes"],
        "attack_class_count": report["attack_class_count"],
        "attack_fixture_count": report["attack_fixture_count"],
        "benign_fixture_count": report["benign_fixture_count"],
        "boundary": report["boundary"],
        "check_count": report["check_count"],
        "claim_boundary_summary": (
            "Finite corpus-bounded adversarial validator evidence only; no semantic-completeness, "
            "scientific-proof, review, source-law, ontology, benchmark, publication, or completed-derivation authority."
        ),
        "corpus_sha256": report["corpus_sha256"],
        "failed_check_count": report["failed_check_count"],
        "fixture_count": report["fixture_count"],
        "lexical_false_negative_count": report["lexical_metrics"].get("false_negative"),
        "lexical_false_positive_count": report["lexical_metrics"].get("false_positive"),
        "plan_task_id": report["plan_task_id"],
        "production_linter_changed": False,
        "recommendation_ids": report["recommendation_ids"],
        "schema_id": "v21_semantic_smuggling_compact_receipt_v1",
        "semantic_false_negative_count": report["semantic_metrics"].get("false_negative"),
        "semantic_false_positive_count": report["semantic_metrics"].get("false_positive"),
        "status": report["status"],
        "validator_ids": [item["check_id"] for item in report["checks"]],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = validate_suite()
        receipt = build_receipt(report)
        if args.write:
            VALIDATION_PATH.write_bytes(canonical_bytes(report))
            RECEIPT_PATH.write_bytes(canonical_bytes(receipt))
        else:
            if not VALIDATION_PATH.is_file() or load_json(VALIDATION_PATH) != report:
                raise ValueError("validation report drift")
            if not RECEIPT_PATH.is_file() or load_json(RECEIPT_PATH) != receipt:
                raise ValueError("compact receipt drift")
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        result = {"error": str(exc), "status": "FAIL"}
        print(json.dumps(result, sort_keys=True) if args.json else f"FAIL: {exc}")
        return 1

    result = {
        "attack_fixture_count": report["attack_fixture_count"],
        "benign_fixture_count": report["benign_fixture_count"],
        "check_count": report["check_count"],
        "failed_check_count": report["failed_check_count"],
        "fixture_count": report["fixture_count"],
        "lexical_false_negative_count": report["lexical_metrics"].get("false_negative"),
        "semantic_false_negative_count": report["semantic_metrics"].get("false_negative"),
        "semantic_false_positive_count": report["semantic_metrics"].get("false_positive"),
        "status": report["status"],
    }
    print(json.dumps(result, sort_keys=True) if args.json else result["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
