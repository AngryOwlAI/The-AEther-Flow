#!/usr/bin/env python3
"""Validate and render the v18 support-formalization traceability registry."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path
from typing import Any, Mapping

SCRIPT_DIR = Path(__file__).resolve().parent
RESEARCH_CONTROL_SCRIPT_DIR = SCRIPT_DIR.parent
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

from strict_yaml import StrictYamlError, loads as load_yaml_text  # noqa: E402
from support_formalization.traceability_io import TraceabilityInputs  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY_PATH = (
    "research_control/design/support_formalization_traceability_registry_v18.yaml"
)
DEFAULT_PNF_REGISTRY_PATH = "registries/PROOF_NORMAL_FORM_REGISTRY.csv"
COMMON_FORBIDDEN_OVERREADS = {
    "support tool as proof authority",
    "validator PASS as theorem",
    "executable spec as proof authority",
    "canonical ontology edit",
    "source-law adoption",
    "target metric import",
    "MetricData(E) adoption",
    "g_eff adoption or scope expansion",
    "matter-coupling derivation or adoption",
    "stress-energy semantics",
    "stress-energy tensor",
    "matter action",
    "Einstein equations",
    "benchmark promotion",
    "Gate Chair verdict",
    "completed derivation",
}


class V18TraceabilityError(RuntimeError):
    """Raised when v18 support-formalization traceability is invalid."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise V18TraceabilityError(message)


def sha256_file(inputs: TraceabilityInputs, rel_path: str) -> str:
    try:
        return inputs.sha256_file(rel_path)
    except FileNotFoundError:
        raise V18TraceabilityError(f"missing path: {rel_path}")


def load_strict_yaml(inputs: TraceabilityInputs, rel_path: str) -> dict[str, Any]:
    try:
        text = inputs.read_text(rel_path)
    except FileNotFoundError:
        raise V18TraceabilityError(f"missing YAML source: {rel_path}")
    try:
        loaded = load_yaml_text(text)
    except StrictYamlError as exc:
        raise V18TraceabilityError(f"invalid YAML source {rel_path}: {exc}") from exc
    require(isinstance(loaded, dict), f"YAML source is not a map: {rel_path}")
    return loaded


def load_json(inputs: TraceabilityInputs, rel_path: str) -> dict[str, Any]:
    try:
        text = inputs.read_text(rel_path)
    except FileNotFoundError:
        raise V18TraceabilityError(f"missing JSON report: {rel_path}")
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError as exc:
        raise V18TraceabilityError(f"invalid JSON report {rel_path}: {exc}") from exc
    require(isinstance(loaded, dict), f"JSON report is not a map: {rel_path}")
    return loaded


def require_list(value: Any, context: str) -> list[Any]:
    require(isinstance(value, list), f"{context} must be a list")
    return value


def require_list_of_maps(value: Any, context: str) -> list[dict[str, Any]]:
    items = require_list(value, context)
    for item in items:
        require(isinstance(item, dict), f"{context} item must be a map")
    return items


def require_list_of_strings(value: Any, context: str) -> list[str]:
    items = require_list(value, context)
    for item in items:
        require(isinstance(item, str), f"{context} item must be a string")
    return items


def validate_hashed_paths(
    inputs: TraceabilityInputs,
    items: list[dict[str, Any]],
    context: str,
) -> None:
    require(items, f"{context} must not be empty")
    for item in items:
        rel_path = str(item.get("path", ""))
        source_hash = str(item.get("source_hash", ""))
        require(rel_path, f"{context} item missing path")
        require(source_hash, f"{context} item missing source_hash")
        actual_hash = sha256_file(inputs, rel_path)
        require(
            actual_hash == source_hash,
            f"{context} hash mismatch for {rel_path}: {actual_hash} != {source_hash}",
        )


def load_pnf_rows(
    inputs: TraceabilityInputs, pnf_registry_path: str
) -> dict[str, dict[str, str]]:
    if inputs.proof_normal_form_rows is not None:
        rows = {
            row_id: {key: value or "" for key, value in row.items()}
            for row_id, row in inputs.proof_normal_form_rows.items()
        }
    else:
        try:
            text = inputs.read_text(pnf_registry_path)
        except FileNotFoundError:
            raise V18TraceabilityError(
                f"missing proof-normal-form registry: {pnf_registry_path}"
            )
        rows = {
            row["proof_normal_form_row_id"]: {
                key: value or "" for key, value in row.items()
            }
            for row in csv.DictReader(io.StringIO(text))
        }
    require(rows, "proof-normal-form registry has no rows")
    return rows


def validate_report(inputs: TraceabilityInputs, entry: dict[str, Any]) -> None:
    context = str(entry.get("entry_id", "entry"))
    report_path = str(entry.get("report_path", ""))
    report = load_json(inputs, report_path)
    require(report.get("support_only") is True, f"{context} report support_only is not true")
    require(report.get("proof_authority") is False, f"{context} report proof_authority is not false")
    if "physics_promotion_authorized" in report:
        require(
            report.get("physics_promotion_authorized") is False,
            f"{context} report physics_promotion_authorized is not false",
        )


def validate_entry(
    inputs: TraceabilityInputs,
    entry: dict[str, Any],
    pnf_rows: dict[str, dict[str, str]],
) -> dict[str, Any]:
    entry_id = str(entry.get("entry_id", ""))
    require(entry_id, "entry missing entry_id")
    require(entry.get("support_only") is True, f"{entry_id} support_only is not true")
    require(entry.get("proof_authority") is False, f"{entry_id} proof_authority is not false")
    require(
        entry.get("validators_and_executable_specs_support_only") is True,
        f"{entry_id} validators_and_executable_specs_support_only is not true",
    )
    require(str(entry.get("status", "")) == "pass_support_only", f"{entry_id} bad status")

    authority_boundary = entry.get("authority_boundary")
    require(isinstance(authority_boundary, dict), f"{entry_id} authority_boundary must be a map")
    require(authority_boundary.get("support_only") is True, f"{entry_id} boundary support_only is not true")
    require(
        authority_boundary.get("proof_authority") is False,
        f"{entry_id} boundary proof_authority is not false",
    )
    require(
        authority_boundary.get("physics_promotion_authorized") is False,
        f"{entry_id} boundary physics_promotion_authorized is not false",
    )

    forbidden_overreads = set(require_list_of_strings(entry.get("forbidden_overreads"), entry_id))
    missing = sorted(COMMON_FORBIDDEN_OVERREADS - forbidden_overreads)
    require(not missing, f"{entry_id} missing forbidden overreads: {missing}")

    source_artifacts = require_list_of_maps(entry.get("source_artifacts"), f"{entry_id} source_artifacts")
    tool_artifacts = require_list_of_maps(entry.get("tool_artifacts"), f"{entry_id} tool_artifacts")
    test_evidence = require_list_of_maps(entry.get("test_evidence"), f"{entry_id} test_evidence")
    validate_hashed_paths(inputs, source_artifacts, f"{entry_id} source_artifacts")
    validate_hashed_paths(inputs, tool_artifacts, f"{entry_id} tool_artifacts")
    require(test_evidence, f"{entry_id} test_evidence must not be empty")
    require(str(entry.get("report_path", "")), f"{entry_id} missing report_path")
    require(
        sha256_file(inputs, str(entry["report_path"]))
        == str(entry.get("report_hash", "")),
        f"{entry_id} report_hash mismatch",
    )
    validate_report(inputs, entry)

    pnf_row_id = str(entry.get("proof_normal_form_row_id", ""))
    require(pnf_row_id in pnf_rows, f"{entry_id} missing proof-normal-form row: {pnf_row_id}")
    pnf_row = pnf_rows[pnf_row_id]
    require(pnf_row["authority_status"] == "support_only", f"{entry_id} PNF row is not support_only")
    require(pnf_row["machine_checkable_fragment"] == "true", f"{entry_id} PNF row is not machine-checkable")

    return {
        "entry_id": entry_id,
        "tool_id": entry.get("tool_id"),
        "plan_task_id": entry.get("plan_task_id"),
        "proof_normal_form_row_id": pnf_row_id,
        "source_artifact_count": len(source_artifacts),
        "tool_artifact_count": len(tool_artifacts),
        "test_evidence_count": len(test_evidence),
        "status": "PASS",
    }


def validate_registry(
    registry_path: str = DEFAULT_REGISTRY_PATH,
    *,
    pnf_registry_path: str = DEFAULT_PNF_REGISTRY_PATH,
    repo_root: Path = REPO_ROOT,
    dependencies: TraceabilityInputs | None = None,
) -> dict[str, Any]:
    inputs = dependencies or TraceabilityInputs(repo_root=repo_root)
    registry: Mapping[str, Any]
    if inputs.registry is None:
        registry = load_strict_yaml(inputs, registry_path)
    else:
        registry = inputs.registry
    require(
        registry.get("registry_id") == "support_formalization_traceability_registry_v18",
        "unexpected registry_id",
    )
    require(registry.get("support_only") is True, "registry support_only is not true")
    require(registry.get("proof_authority") is False, "registry proof_authority is not false")
    require(
        registry.get("validators_and_executable_specs_support_only") is True,
        "registry validators_and_executable_specs_support_only is not true",
    )
    entries = require_list_of_maps(registry.get("entries"), "entries")
    pnf_rows = load_pnf_rows(inputs, pnf_registry_path)
    entry_results = [validate_entry(inputs, entry, pnf_rows) for entry in entries]
    plan_task_ids = [str(entry.get("plan_task_id", "")) for entry in entries]
    require(
        plan_task_ids == ["P7-T02", "P7-T03", "P7-T04", "P7-T05", "P7-T06"],
        f"unexpected plan_task_id order: {plan_task_ids}",
    )
    return {
        "status": "PASS",
        "registry_path": registry_path,
        "proof_normal_form_registry_path": pnf_registry_path,
        "entry_count": len(entry_results),
        "entries": entry_results,
        "support_only": True,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "authority_boundary_status": "support_only_no_proof_authority_preserved",
    }


def markdown_for_registry(receipt: dict[str, Any], registry: dict[str, Any]) -> str:
    lines = [
        "<!-- generated: true; authority: derivative -->",
        "",
        "# V18 Support Formalization Traceability",
        "",
        "This generated index is reader support only. It is not proof authority, not a source artifact, not a Gate Chair verdict, and not physics-promotion authority.",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Registry | `{receipt['registry_path']}` |",
        f"| Entry count | {receipt['entry_count']} |",
        f"| Proof authority | {str(receipt['proof_authority']).lower()} |",
        f"| Physics promotion authorized | {str(receipt['physics_promotion_authorized']).lower()} |",
        "",
        "## Tools",
        "",
        "| Plan task | Tool | Source artifacts | Test evidence | PNF row | Boundary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in registry["entries"]:
        sources = "<br>".join(f"`{item['path']}`" for item in entry["source_artifacts"])
        tests = "<br>".join(f"`{item['command']}`" for item in entry["test_evidence"])
        boundary = str(entry["authority_boundary"]["statement"])
        lines.append(
            "| `{plan}` | `{tool}` | {sources} | {tests} | `{pnf}` | {boundary} |".format(
                plan=entry["plan_task_id"],
                tool=entry["tool_id"],
                sources=sources,
                tests=tests,
                pnf=entry["proof_normal_form_row_id"],
                boundary=boundary,
            )
        )
    lines.extend(
        [
            "",
            "## Forbidden Overreads",
            "",
        ]
    )
    for item in sorted(COMMON_FORBIDDEN_OVERREADS):
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the v18 support-formalization traceability registry."
    )
    parser.add_argument("--registry", default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--pnf-registry", default=DEFAULT_PNF_REGISTRY_PATH)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = TraceabilityInputs(repo_root=REPO_ROOT)
    try:
        receipt = validate_registry(
            args.registry,
            pnf_registry_path=args.pnf_registry,
            dependencies=inputs,
        )
        registry = load_strict_yaml(inputs, args.registry)
    except V18TraceabilityError as exc:
        print(f"support_formalization_traceability_registry_v18: FAIL: {exc}", file=sys.stderr)
        return 1
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(markdown_for_registry(receipt, registry), encoding="utf-8")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print("support_formalization_traceability_registry_v18: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
