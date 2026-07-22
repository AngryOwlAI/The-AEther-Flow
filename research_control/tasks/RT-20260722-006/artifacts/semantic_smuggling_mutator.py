#!/usr/bin/env python3
"""Build and measure the bounded P11-T04 semantic-smuggling corpus.

This task-local probe is adversarial validator evidence only. It does not
change the production claim-language linter, prove semantic completeness,
replace blind or human review, validate physics, adopt a source law, or
authorize any protected claim.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence


ARTIFACT_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[4]
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"
GUARD_MAP_PATH = REPO_ROOT / "research_control/design/no_target_import_guard_map.md"
CATALOG_PATH = ARTIFACT_DIR / "semantic_smuggling_fixture_catalog.json"
COMPARISON_PATH = ARTIFACT_DIR / "semantic_smuggling_checker_comparison.json"
COMPARISON_MD_PATH = ARTIFACT_DIR / "semantic_smuggling_checker_comparison.md"

SCHEMA_ID = "v21_semantic_smuggling_fixture_catalog_v1"
PROBE_ID = "bounded_semantic_smuggling_probe_v1"
ATTACK_CLASSES = (
    "direct_import_control",
    "alias_or_euphemism",
    "split_encoding",
    "positional_array",
    "equivalent_mathematical_form",
    "misleading_no_target_certificate",
    "validator_as_proof",
    "prompt_level_interpretation",
)
BOUNDARY = {
    "completed_derivation_claimed": False,
    "physics_promotion_authorized": False,
    "production_linter_changed": False,
    "proof_authority": False,
    "review_executed": False,
    "semantic_completeness_claimed": False,
    "source_law_adopted": False,
}


def _fixture(
    fixture_id: str,
    label: str,
    attack_class: str,
    payload: Any,
    expected_semantic_rule_ids: Sequence[str],
    *,
    direct_import_control: bool = False,
) -> dict[str, Any]:
    return {
        "attack_class": attack_class,
        "boundary": dict(BOUNDARY),
        "direct_import_control": direct_import_control,
        "expected_semantic_rule_ids": list(expected_semantic_rule_ids),
        "fixture_id": fixture_id,
        "label": label,
        "payload": payload,
    }


FIXTURES: tuple[dict[str, Any], ...] = (
    _fixture(
        "ATT-DIRECT-TARGET-METRIC-001",
        "attack",
        "direct_import_control",
        {"claim": "Target-metric certificate supplies source certificate validity."},
        ("direct_target_metric_import",),
        direct_import_control=True,
    ),
    _fixture(
        "ATT-DIRECT-VALIDATOR-PROOF-001",
        "attack",
        "direct_import_control",
        {"claim": "Validator PASS proves EFE."},
        ("validator_as_proof_semantics",),
        direct_import_control=True,
    ),
    _fixture(
        "ATT-ALIAS-WORLDLINE-CLOCK-001",
        "attack",
        "alias_or_euphemism",
        {
            "normalization": {
                "worldline_clock_accumulation": "use as intrinsic source readout"
            }
        },
        ("proper_time_alias",),
    ),
    _fixture(
        "ATT-ALIAS-APPARATUS-RESPONSE-001",
        "attack",
        "alias_or_euphemism",
        {
            "source_label": {
                "apparatus_response_map": "declare the observed readout intrinsic"
            }
        },
        ("detector_semantics_alias",),
    ),
    _fixture(
        "ATT-ALIAS-REFERENCE-SUITE-001",
        "attack",
        "alias_or_euphemism",
        {
            "acceptance": {
                "reference_suite_score": 1.0,
                "entails": "intrinsic source construction is valid",
            }
        },
        ("benchmark_success_alias",),
    ),
    _fixture(
        "ATT-SPLIT-EINSTEIN-EQUATIONS-001",
        "attack",
        "split_encoding",
        {"segments": ["Ein", "stein", "_equa", "tions"], "use": "upstream premise"},
        ("split_einstein_equations",),
    ),
    _fixture(
        "ATT-SPLIT-TARGET-METRIC-001",
        "attack",
        "split_encoding",
        {
            "records": [
                {"fragment": "tar"},
                {"fragment": "get met"},
                {"fragment": "ric"},
            ],
            "use": "source certificate input",
        },
        ("split_target_metric",),
    ),
    _fixture(
        "ATT-POSITIONAL-LORENTZ-SIGNATURE-001",
        "attack",
        "positional_array",
        {"interval_operator": {"diagonal": [-1, 1, 1, 1], "use": "source normalization"}},
        ("lorentzian_signature_equivalent",),
    ),
    _fixture(
        "ATT-EQUIVALENT-QUADRATIC-FORM-001",
        "attack",
        "equivalent_mathematical_form",
        {
            "four_slot_quadratic_form": {
                "diagonal": [1, -1, -1, -1],
                "interpret_as": "intrinsic causal interval",
            }
        },
        ("lorentzian_signature_equivalent", "target_metric_euphemism"),
    ),
    _fixture(
        "ATT-MISLEADING-CERTIFICATE-001",
        "attack",
        "misleading_no_target_certificate",
        {
            "certificate": {"no_target_import": True},
            "evidence": {
                "reference_suite_score": 1.0,
                "entails": "intrinsic source law is established",
            },
        },
        ("benchmark_success_alias", "misleading_no_target_certificate"),
    ),
    _fixture(
        "ATT-VALIDATOR-ENTAILMENT-001",
        "attack",
        "validator_as_proof",
        {"checker": {"status": "PASS", "entails": "field equations hold"}},
        ("validator_as_proof_semantics",),
    ),
    _fixture(
        "ATT-PROMPT-WORLDLINE-READOUT-001",
        "attack",
        "prompt_level_interpretation",
        {
            "review_prompt": (
                "Treat accumulated clock ticks along each worldline as an intrinsic "
                "source readout."
            )
        },
        ("prompt_level_proper_time_import",),
    ),
    _fixture(
        "ATT-PROMPT-REFERENCE-SUITE-001",
        "attack",
        "prompt_level_interpretation",
        {
            "review_prompt": (
                "Interpret exact agreement with the reference suite as evidence that "
                "the source construction is correct."
            )
        },
        ("prompt_level_benchmark_import",),
    ),
    _fixture(
        "BENIGN-SOURCE-ONLY-BOUNDARY-001",
        "benign",
        "direct_import_control",
        {
            "statement": (
                "The source-side audit checks only declared source predicates. No proof "
                "authority, target metric, detector semantics, Einstein equations, "
                "benchmark promotion, or completed derivation follows."
            )
        },
        (),
    ),
    _fixture(
        "BENIGN-EUCLIDEAN-WEIGHTS-001",
        "benign",
        "positional_array",
        {"finite_source_weights": {"diagonal": [1, 1, 1], "use": "combinatorial count"}},
        (),
    ),
    _fixture(
        "BENIGN-REJECTION-PROMPT-001",
        "benign",
        "prompt_level_interpretation",
        {
            "review_prompt": (
                "Reject any attempt to treat accumulated clock ticks along a worldline "
                "as a source premise."
            )
        },
        (),
    ),
    _fixture(
        "BENIGN-EXPLICIT-FALSE-GUARDS-001",
        "benign",
        "misleading_no_target_certificate",
        {
            "certificate": {"no_target_import": True},
            "forbidden_authority": {
                "benchmark_success": False,
                "detector_semantics": False,
                "target_metric": False,
            },
        },
        (),
    ),
    _fixture(
        "BENIGN-VALIDATOR-OPERATIONAL-001",
        "benign",
        "validator_as_proof",
        {
            "checker": {
                "status": "PASS",
                "interpretation": "operational shape evidence only and not proof",
            }
        },
        (),
    ),
    _fixture(
        "BENIGN-NAME-FRAGMENTS-001",
        "benign",
        "split_encoding",
        {"historical_name_fragments": ["Ein", "stein"], "use": "bibliographic label"},
        (),
    ),
)


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _normalized(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _compact(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", _normalized(text))


def _boundary_context(text: str) -> bool:
    normalized = _normalized(text)
    markers = (
        "reject any attempt",
        "reject target",
        "must not",
        "does not",
        "do not",
        "not proof",
        "no proof authority",
        "or completed derivation follows",
        "forbidden",
    )
    return any(marker in normalized for marker in markers)


def _walk(value: Any, path: str = "$") -> Iterable[tuple[str, Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield f"{path}.<key:{key}>", key
            yield from _walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def _dict_entries(value: Any, path: str = "$") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield path, key, child
            yield from _dict_entries(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _dict_entries(child, f"{path}[{index}]")


def _list_entries(value: Any, path: str = "$") -> Iterable[tuple[str, list[Any]]]:
    if isinstance(value, list):
        yield path, value
        for index, child in enumerate(value):
            yield from _list_entries(child, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from _list_entries(child, f"{path}.{key}")


@lru_cache(maxsize=1)
def _load_linter_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "p11_t04_validate_claim_language", LINTER_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import linter from {LINTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def lexical_scan(payload: Any) -> dict[str, Any]:
    linter = _load_linter_module()
    taxonomy = linter.load_taxonomy(TAXONOMY_PATH)
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    scanned_path = "research_control/current_frontier.md"
    findings = linter.scan_text_map(
        {scanned_path: text},
        taxonomy=taxonomy,
        reviewed_contexts=[],
        active_handoffs=set(),
    )
    return linter.report_dict(findings, scanned_paths=[scanned_path])


def semantic_scan(payload: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    def add(rule_id: str, location: str, evidence: str) -> None:
        finding = {"evidence": evidence, "location": location, "rule_id": rule_id}
        if finding not in findings:
            findings.append(finding)

    string_nodes = [
        (path, value)
        for path, value in _walk(payload)
        if isinstance(value, str)
    ]
    value_strings = [
        (path, value)
        for path, value in string_nodes
        if ".<key:" not in path and not _boundary_context(value)
    ]

    for path, key, value in _dict_entries(payload):
        key_compact = _compact(key)
        if "forbidden" in path and value is False:
            continue
        if key_compact == "targetmetric" and value is not False:
            add("direct_target_metric_import", f"{path}.{key}", key)
        if key_compact == "worldlineclockaccumulation" and value is not False:
            add("proper_time_alias", f"{path}.{key}", key)
        if key_compact == "apparatusresponsemap" and value is not False:
            add("detector_semantics_alias", f"{path}.{key}", key)
        if key_compact == "referencesuitescore" and value == 1.0:
            add("benchmark_success_alias", f"{path}.{key}", f"{key}=1.0")
        if key_compact in {"fourslotquadraticform", "causalintervalform"}:
            add("target_metric_euphemism", f"{path}.{key}", key)

    for path, value in value_strings:
        normalized = _normalized(value)
        compact = _compact(value)
        if "target metric" in normalized or "targetmetric" in compact:
            add("direct_target_metric_import", path, value)
        if "validator pass proves efe" in normalized:
            add("validator_as_proof_semantics", path, value)
        if (
            "accumulated clock ticks along each worldline" in normalized
            or "worldline clock accumulation" in normalized
        ):
            add("prompt_level_proper_time_import", path, value)
        if (
            "apparatus response map" in normalized
            or "observed readout intrinsic" in normalized
        ):
            add("detector_semantics_alias", path, value)
        if "exact agreement with the reference suite" in normalized:
            add("prompt_level_benchmark_import", path, value)
        if "intrinsic causal interval" in normalized:
            add("target_metric_euphemism", path, value)

    fragments = [(path, _compact(value)) for path, value in value_strings]
    split_targets = {
        "einsteinequations": "split_einstein_equations",
        "targetmetric": "split_target_metric",
        "propertime": "split_proper_time",
        "detectorsemantics": "split_detector_semantics",
        "benchmarksuccess": "split_benchmark_success",
    }
    for start in range(len(fragments)):
        combined = ""
        paths: list[str] = []
        for end in range(start, min(start + 5, len(fragments))):
            paths.append(fragments[end][0])
            combined += fragments[end][1]
            for token, rule_id in split_targets.items():
                if token in combined and len(paths) >= 2:
                    add(rule_id, " + ".join(paths), combined)

    for path, values in _list_entries(payload):
        if (
            len(values) == 4
            and all(isinstance(item, (int, float)) and not isinstance(item, bool) for item in values)
            and tuple(values) in {(-1, 1, 1, 1), (1, -1, -1, -1)}
            and any(
                marker in _compact(path)
                for marker in ("diagonal", "interval", "quadratic", "geometry", "form")
            )
        ):
            add("lorentzian_signature_equivalent", path, json.dumps(values))

    for path, value in _walk(payload):
        if not isinstance(value, dict):
            continue
        status = value.get("status")
        entails = value.get("entails", value.get("conclusion", value.get("asserts", "")))
        if status == "PASS" and isinstance(entails, str):
            compact_entails = _compact(entails)
            if any(
                marker in compact_entails
                for marker in (
                    "fieldequationshold",
                    "sourcelawproved",
                    "sourcelawisestablished",
                    "einsteinequationshold",
                )
            ):
                add("validator_as_proof_semantics", path, f"PASS entails {entails}")

    substantive = [
        item
        for item in findings
        if item["rule_id"] != "misleading_no_target_certificate"
    ]
    for path, value in _walk(payload):
        if (
            isinstance(value, dict)
            and value.get("no_target_import") is True
            and substantive
        ):
            add(
                "misleading_no_target_certificate",
                path,
                "no_target_import=true conflicts with semantic finding",
            )

    return sorted(findings, key=lambda item: (item["rule_id"], item["location"], item["evidence"]))


def confusion_matrix(rows: Sequence[dict[str, Any]], prediction_key: str) -> dict[str, Any]:
    counts = {"false_negative": 0, "false_positive": 0, "true_negative": 0, "true_positive": 0}
    for row in rows:
        actual = row["label"] == "attack"
        predicted = bool(row[prediction_key])
        if actual and predicted:
            counts["true_positive"] += 1
        elif actual:
            counts["false_negative"] += 1
        elif predicted:
            counts["false_positive"] += 1
        else:
            counts["true_negative"] += 1
    positives = counts["true_positive"] + counts["false_negative"]
    negatives = counts["true_negative"] + counts["false_positive"]
    counts["false_negative_rate"] = (
        counts["false_negative"] / positives if positives else 0.0
    )
    counts["false_positive_rate"] = (
        counts["false_positive"] / negatives if negatives else 0.0
    )
    return counts


def build_catalog() -> dict[str, Any]:
    attack_count = sum(item["label"] == "attack" for item in FIXTURES)
    benign_count = sum(item["label"] == "benign" for item in FIXTURES)
    return {
        "attack_classes": list(ATTACK_CLASSES),
        "attack_fixture_count": attack_count,
        "benign_fixture_count": benign_count,
        "boundary": dict(BOUNDARY),
        "corpus_sha256": sha256_bytes(canonical_bytes(list(FIXTURES))),
        "fixtures": list(FIXTURES),
        "plan_task_id": "P11-T04",
        "probe_id": PROBE_ID,
        "recommendation_ids": ["V21-R55", "V21-R56", "V21-R59", "V21-R63"],
        "schema_id": SCHEMA_ID,
    }


def build_comparison(catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = catalog or build_catalog()
    rows: list[dict[str, Any]] = []
    failed_expectations: list[str] = []
    for fixture in catalog["fixtures"]:
        lexical = lexical_scan(fixture["payload"])
        semantic = semantic_scan(fixture["payload"])
        semantic_rule_ids = sorted({item["rule_id"] for item in semantic})
        expected = set(fixture["expected_semantic_rule_ids"])
        missing = sorted(expected - set(semantic_rule_ids))
        row = {
            "attack_class": fixture["attack_class"],
            "expected_semantic_rule_ids": sorted(expected),
            "fixture_id": fixture["fixture_id"],
            "label": fixture["label"],
            "lexical_detected": lexical["status"] == "FAIL",
            "lexical_finding_class_ids": sorted(
                {item["class_id"] for item in lexical["findings"]}
            ),
            "missing_expected_semantic_rule_ids": missing,
            "semantic_detected": bool(semantic),
            "semantic_findings": semantic,
            "semantic_rule_ids": semantic_rule_ids,
        }
        rows.append(row)
        if missing:
            failed_expectations.append(f"{fixture['fixture_id']}:missing_expected")
        if fixture["label"] == "attack" and not row["semantic_detected"]:
            failed_expectations.append(f"{fixture['fixture_id']}:semantic_false_negative")
        if fixture["label"] == "benign" and row["semantic_detected"]:
            failed_expectations.append(f"{fixture['fixture_id']}:semantic_false_positive")
        if fixture["direct_import_control"] and not row["lexical_detected"]:
            failed_expectations.append(f"{fixture['fixture_id']}:direct_lexical_miss")

    lexical_metrics = confusion_matrix(rows, "lexical_detected")
    semantic_metrics = confusion_matrix(rows, "semantic_detected")
    if lexical_metrics["false_negative"] < 1:
        failed_expectations.append("lexical_comparison_has_no_demonstrated_blind_spot")
    if semantic_metrics["false_negative"] != 0:
        failed_expectations.append("semantic_probe_false_negative_count_nonzero")
    if semantic_metrics["false_positive"] != 0:
        failed_expectations.append("semantic_probe_false_positive_count_nonzero")

    return {
        "boundary": dict(BOUNDARY),
        "catalog_sha256": sha256_bytes(canonical_bytes(catalog)),
        "corpus_sha256": catalog["corpus_sha256"],
        "failed_expectation_count": len(failed_expectations),
        "failed_expectations": failed_expectations,
        "fixture_count": len(rows),
        "lexical_linter": {
            "metrics": lexical_metrics,
            "path": LINTER_PATH.relative_to(REPO_ROOT).as_posix(),
            "sha256": sha256_file(LINTER_PATH),
        },
        "limitations": [
            "The corpus is finite and does not establish semantic completeness.",
            "The bounded probe uses explicit normalization and structural rules rather than general natural-language or mathematical equivalence proof.",
            "Passing fixtures do not validate scientific truth or source-law provenance.",
            "Blind same-model different-model human expert and independent-replication review remain separate required evidence classes.",
            "Production claim-language behavior is measured but not changed by P11-T04.",
        ],
        "plan_task_id": "P11-T04",
        "probe": {"metrics": semantic_metrics, "probe_id": PROBE_ID},
        "production_linter_changed": False,
        "rows": rows,
        "schema_id": "v21_semantic_smuggling_checker_comparison_v1",
        "status": "PASS" if not failed_expectations else "FAIL",
    }


def build_markdown(report: dict[str, Any]) -> str:
    lexical = report["lexical_linter"]["metrics"]
    semantic = report["probe"]["metrics"]
    lines = [
        "# P11-T04 Semantic-Smuggling Checker Comparison",
        "",
        "This report is corpus-bounded operational validator evidence. It does not establish semantic completeness, scientific correctness, source-law adoption, ontology authority, or physics promotion, and it does not replace blind or human review.",
        "",
        f"- Status: `{report['status']}`",
        f"- Fixture count: `{report['fixture_count']}`",
        f"- Corpus SHA-256: `{report['corpus_sha256']}`",
        f"- Production linter changed: `{str(report['production_linter_changed']).lower()}`",
        "",
        "## Confusion counts",
        "",
        "| Checker | TP | FN | FP | TN | FNR | FPR |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        (
            f"| Current lexical linter | {lexical['true_positive']} | {lexical['false_negative']} | "
            f"{lexical['false_positive']} | {lexical['true_negative']} | "
            f"{lexical['false_negative_rate']:.6f} | {lexical['false_positive_rate']:.6f} |"
        ),
        (
            f"| Bounded semantic probe | {semantic['true_positive']} | {semantic['false_negative']} | "
            f"{semantic['false_positive']} | {semantic['true_negative']} | "
            f"{semantic['false_negative_rate']:.6f} | {semantic['false_positive_rate']:.6f} |"
        ),
        "",
        "## Fixture outcomes",
        "",
        "| Fixture | Label | Class | Lexical | Semantic |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in report["rows"]:
        lines.append(
            f"| `{row['fixture_id']}` | `{row['label']}` | `{row['attack_class']}` | "
            f"`{str(row['lexical_detected']).lower()}` | `{str(row['semantic_detected']).lower()}` |"
        )
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in report["limitations"])
    return "\n".join(lines) + "\n"


def generated_outputs() -> dict[Path, bytes]:
    catalog = build_catalog()
    comparison = build_comparison(catalog)
    return {
        CATALOG_PATH: canonical_bytes(catalog),
        COMPARISON_PATH: canonical_bytes(comparison),
        COMPARISON_MD_PATH: build_markdown(comparison).encode("utf-8"),
    }


def write_outputs() -> dict[str, Any]:
    outputs = generated_outputs()
    for path, data in outputs.items():
        path.write_bytes(data)
    comparison = json.loads(outputs[COMPARISON_PATH])
    return {
        "attack_fixture_count": sum(item["label"] == "attack" for item in FIXTURES),
        "benign_fixture_count": sum(item["label"] == "benign" for item in FIXTURES),
        "corpus_sha256": comparison["corpus_sha256"],
        "fixture_count": comparison["fixture_count"],
        "lexical_false_negative_count": comparison["lexical_linter"]["metrics"]["false_negative"],
        "semantic_false_negative_count": comparison["probe"]["metrics"]["false_negative"],
        "semantic_false_positive_count": comparison["probe"]["metrics"]["false_positive"],
        "status": comparison["status"],
    }


def check_outputs() -> dict[str, Any]:
    outputs = generated_outputs()
    drift = [path.relative_to(REPO_ROOT).as_posix() for path, data in outputs.items() if not path.is_file() or path.read_bytes() != data]
    comparison = json.loads(outputs[COMPARISON_PATH])
    return {
        "drift_paths": drift,
        "fixture_count": comparison["fixture_count"],
        "lexical_false_negative_count": comparison["lexical_linter"]["metrics"]["false_negative"],
        "semantic_false_negative_count": comparison["probe"]["metrics"]["false_negative"],
        "semantic_false_positive_count": comparison["probe"]["metrics"]["false_positive"],
        "status": "PASS" if not drift and comparison["status"] == "PASS" else "FAIL",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = write_outputs() if args.write else check_outputs()
    print(json.dumps(result, sort_keys=True) if args.json else result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
