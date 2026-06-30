#!/usr/bin/env python3
"""Validate the support-only formalization traceability registry."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
RESEARCH_CONTROL_SCRIPT_DIR = SCRIPT_DIR.parent
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY_PATH = (
    "research_control/design/support_formalization_traceability_registry_v1.yaml"
)
REQUIRED_BOUNDARY_PHRASES = (
    "proof_authority=false",
    "not canonical ontology",
    "not source-law adoption",
    "not MetricData(E) adoption",
    "not g_eff",
    "not matter coupling",
    "not stress-energy",
    "not Einstein equations",
    "not benchmark promotion",
    "not completed derivation",
)
REQUIRED_BLOCKED_OVERREADS = (
    "canonical ontology edit",
    "source-law adoption",
    "MetricData(E) adoption",
    "g_eff adoption or scope expansion",
    "coupling-law adoption",
    "matter-coupling derivation or adoption",
    "stress-energy semantics",
    "stress-energy tensor",
    "detector semantics",
    "matter action",
    "Einstein equations",
    "benchmark promotion",
    "completed derivation",
    "future source-extension impossibility",
    "global theory rejection",
)
FORBIDDEN_AUTHORITY_PATH_PREFIXES = (".local/", "wiki/", "output/", "html/")


class TraceabilityRegistryError(RuntimeError):
    """Raised when the traceability registry is missing required evidence."""


def repo_path(repo_root: Path, rel_path: str) -> Path:
    return repo_root / rel_path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TraceabilityRegistryError(message)


def sha256_file(repo_root: Path, rel_path: str) -> str:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        raise TraceabilityRegistryError(f"missing path: {rel_path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_boundary_text(text: str, context: str) -> None:
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        require(phrase in text, f"{context} missing boundary phrase: {phrase}")


def ensure_non_generated_authority_path(rel_path: str, context: str) -> None:
    for prefix in FORBIDDEN_AUTHORITY_PATH_PREFIXES:
        require(
            not rel_path.startswith(prefix),
            f"{context} uses generated or local path as authority: {rel_path}",
        )


def load_json(repo_root: Path, rel_path: str) -> dict[str, Any]:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        raise TraceabilityRegistryError(f"missing JSON report: {rel_path}")
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TraceabilityRegistryError(f"invalid JSON report {rel_path}: {exc}") from exc
    require(isinstance(loaded, dict), f"JSON report is not a map: {rel_path}")
    return loaded


def load_strict_yaml(repo_root: Path, rel_path: str) -> dict[str, Any]:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        raise TraceabilityRegistryError(f"missing YAML source: {rel_path}")
    try:
        loaded = load_yaml(path)
    except StrictYamlError as exc:
        raise TraceabilityRegistryError(f"invalid YAML source {rel_path}: {exc}") from exc
    require(isinstance(loaded, dict), f"YAML source is not a map: {rel_path}")
    return loaded


def list_of_strings(value: Any, context: str) -> list[str]:
    require(isinstance(value, list), f"{context} must be a list")
    output: list[str] = []
    for item in value:
        require(isinstance(item, str), f"{context} item must be a string")
        output.append(item)
    return output


def list_of_maps(value: Any, context: str) -> list[dict[str, Any]]:
    require(isinstance(value, list), f"{context} must be a list")
    output: list[dict[str, Any]] = []
    for item in value:
        require(isinstance(item, dict), f"{context} item must be a map")
        output.append(item)
    return output


def artifact_key(artifact: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(artifact.get("object_id", "")),
        str(artifact.get("path", "")),
        str(artifact.get("source_hash", "")),
    )


def validate_artifact_hashes(
    repo_root: Path, artifacts: list[dict[str, Any]], context: str, authority: bool
) -> None:
    require(artifacts, f"{context} has no artifacts")
    for artifact in artifacts:
        object_id = str(artifact.get("object_id", ""))
        rel_path = str(artifact.get("path", ""))
        source_hash = str(artifact.get("source_hash", ""))
        registry_name = str(artifact.get("registry_name", ""))
        require(object_id, f"{context} artifact missing object_id")
        require(rel_path, f"{context} artifact {object_id} missing path")
        require(source_hash, f"{context} artifact {object_id} missing source_hash")
        require(registry_name, f"{context} artifact {object_id} missing registry_name")
        if authority:
            ensure_non_generated_authority_path(rel_path, context)
        actual_hash = sha256_file(repo_root, rel_path)
        require(
            actual_hash == source_hash,
            f"{context} artifact hash mismatch for {rel_path}: {actual_hash} != {source_hash}",
        )


def validate_report(entry: dict[str, Any], report: dict[str, Any]) -> None:
    context = str(entry.get("entry_id", "entry"))
    require(report.get("checker_id") == entry.get("checker_id"), f"{context} checker_id drift")
    require(
        report.get("checker_version") == entry.get("checker_version"),
        f"{context} checker_version drift",
    )
    require(report.get("status") == entry.get("status"), f"{context} status drift")
    require(report.get("support_only") is True, f"{context} report support_only is not true")
    require(
        report.get("proof_authority") is False,
        f"{context} report proof_authority is not false",
    )
    ensure_boundary_text(str(report.get("boundary_statement", "")), f"{context} report")
    flags = report.get("forbidden_authority_flags")
    require(isinstance(flags, dict) and flags, f"{context} missing forbidden authority flags")
    enabled_flags = [key for key, value in flags.items() if value is not False]
    require(not enabled_flags, f"{context} forbidden authority flags enabled: {enabled_flags}")

    reported_propositions = {
        str(item.get("proposition_id", ""))
        for item in list_of_maps(report.get("proposition_results"), f"{context} report propositions")
    }
    required_propositions = set(list_of_strings(entry.get("proposition_ids"), context))
    require(
        required_propositions <= reported_propositions,
        f"{context} report missing propositions: {sorted(required_propositions - reported_propositions)}",
    )

    reported_formal_objects = set(list_of_strings(report.get("formal_objects"), context))
    mapped_formal_objects = {
        str(item.get("formal_object", ""))
        for item in list_of_maps(entry.get("formal_object_mappings"), context)
    }
    require(
        reported_formal_objects <= mapped_formal_objects,
        f"{context} missing formal object mappings: {sorted(reported_formal_objects - mapped_formal_objects)}",
    )


def validate_report_source_links(entry: dict[str, Any], report: dict[str, Any]) -> None:
    context = str(entry.get("entry_id", "entry"))
    manifest_artifacts = [
        *list_of_maps(entry.get("canonical_source_artifacts"), context),
        *list_of_maps(entry.get("support_dependency_artifacts"), context),
    ]
    manifest_keys = {artifact_key(artifact) for artifact in manifest_artifacts}
    if "source_artifacts" in report:
        report_keys = {
            artifact_key(artifact)
            for artifact in list_of_maps(report.get("source_artifacts"), f"{context} report source_artifacts")
        }
        require(
            manifest_keys <= report_keys,
            f"{context} report missing source artifacts from manifest",
        )
    else:
        key = (
            str(report.get("source_artifact_object_id", "")),
            str(report.get("source_artifact_path", "")),
            str(report.get("source_artifact_hash", "")),
        )
        require(key in manifest_keys, f"{context} report source artifact not in manifest")


def validate_traceability(entry: dict[str, Any], traceability: dict[str, Any]) -> None:
    context = str(entry.get("entry_id", "entry"))
    require(traceability.get("task_id") == entry.get("task_id"), f"{context} task_id drift")
    require(
        traceability.get("proof_authority") is False,
        f"{context} traceability proof_authority is not false",
    )
    require(
        traceability.get("support_only") is True,
        f"{context} traceability support_only is not true",
    )
    trace_mapping = {
        str(item.get("formal_object", ""))
        for item in list_of_maps(traceability.get("formal_object_mapping"), context)
    }
    manifest_mapping = {
        str(item.get("formal_object", ""))
        for item in list_of_maps(entry.get("formal_object_mappings"), context)
    }
    require(
        manifest_mapping == trace_mapping,
        f"{context} traceability formal object mapping drift",
    )
    blocked = set(list_of_strings(traceability.get("blocked_overreads"), context))
    required = set(REQUIRED_BLOCKED_OVERREADS)
    require(required <= blocked, f"{context} traceability missing blocked overreads")


def validate_entry(repo_root: Path, entry: dict[str, Any]) -> dict[str, Any]:
    entry_id = str(entry.get("entry_id", ""))
    require(entry_id, "entry missing entry_id")
    require(entry.get("support_only") is True, f"{entry_id} support_only is not true")
    require(entry.get("proof_authority") is False, f"{entry_id} proof_authority is not false")
    require(str(entry.get("status", "")) == "pass_support_only", f"{entry_id} bad status")

    for formalization_file in list_of_strings(
        entry.get("formalization_files"), f"{entry_id} formalization_files"
    ):
        sha256_file(repo_root, formalization_file)

    report_path = str(entry.get("report_path", ""))
    traceability_path = str(entry.get("traceability_path", ""))
    require(report_path, f"{entry_id} missing report_path")
    require(traceability_path, f"{entry_id} missing traceability_path")
    require(
        sha256_file(repo_root, report_path) == str(entry.get("report_hash", "")),
        f"{entry_id} report_hash mismatch",
    )
    require(
        sha256_file(repo_root, traceability_path) == str(entry.get("traceability_hash", "")),
        f"{entry_id} traceability_hash mismatch",
    )

    canonical_artifacts = list_of_maps(
        entry.get("canonical_source_artifacts"), f"{entry_id} canonical_source_artifacts"
    )
    support_artifacts = list_of_maps(
        entry.get("support_dependency_artifacts"), f"{entry_id} support_dependency_artifacts"
    )
    validate_artifact_hashes(repo_root, canonical_artifacts, entry_id, authority=True)
    if support_artifacts:
        validate_artifact_hashes(repo_root, support_artifacts, entry_id, authority=False)

    report = load_json(repo_root, report_path)
    validate_report(entry, report)
    validate_report_source_links(entry, report)
    traceability = load_strict_yaml(repo_root, traceability_path)
    validate_traceability(entry, traceability)

    return {
        "canonical_source_artifact_count": len(canonical_artifacts),
        "checker_id": entry.get("checker_id"),
        "entry_id": entry_id,
        "formal_object_count": len(list_of_maps(entry.get("formal_object_mappings"), entry_id)),
        "status": "PASS",
        "support_dependency_artifact_count": len(support_artifacts),
    }


def validate_registry(
    registry_path: str = DEFAULT_REGISTRY_PATH, repo_root: Path = REPO_ROOT
) -> dict[str, Any]:
    registry = load_strict_yaml(repo_root, registry_path)
    require(
        registry.get("registry_id") == "support_formalization_traceability_registry_v1",
        "unexpected registry_id",
    )
    require(registry.get("support_only") is True, "registry support_only is not true")
    require(registry.get("proof_authority") is False, "registry proof_authority is not false")
    ensure_boundary_text(str(registry.get("authority_boundary", "")), "registry")

    entries = list_of_maps(registry.get("entries"), "entries")
    require(entries, "registry has no entries")
    entry_ids = [str(entry.get("entry_id", "")) for entry in entries]
    require(len(set(entry_ids)) == len(entry_ids), "duplicate registry entry_id")
    entry_results = [validate_entry(repo_root, entry) for entry in entries]
    return {
        "authority_boundary_status": "proof_authority_false_preserved",
        "checked_entry_count": len(entry_results),
        "entries": entry_results,
        "proof_authority": False,
        "registry_path": registry_path,
        "status": "PASS",
        "support_only": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate support-only formalization proof-to-source traceability."
    )
    parser.add_argument(
        "--registry",
        default=DEFAULT_REGISTRY_PATH,
        help="repo-relative registry manifest path",
    )
    parser.add_argument("--json", action="store_true", help="print JSON receipt")
    parser.add_argument("--json-output", type=Path, help="write JSON receipt")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        receipt = validate_registry(args.registry)
    except TraceabilityRegistryError as exc:
        print(f"support_formalization_traceability_registry: FAIL: {exc}", file=sys.stderr)
        return 1
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print("support_formalization_traceability_registry: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
