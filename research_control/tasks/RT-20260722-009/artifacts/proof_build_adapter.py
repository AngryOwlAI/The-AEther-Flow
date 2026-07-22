#!/usr/bin/env python3
"""Validate and render v21 proof-evidence registration fixtures.

This task-local adapter records reproducible formal-build evidence.  Its PASS
status is project-control evidence only: it is not theorem truth, proof
authority, ontology adoption, physical interpretation, or claim promotion.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
DEFAULT_FIXTURES = ARTIFACT_DIR / "proof_evidence_fixtures.json"
DEFAULT_REPORT = ARTIFACT_DIR / "proof_evidence_validation_report.json"
DEFAULT_COMPACT = ARTIFACT_DIR / "proof_evidence_compact_receipt.json"
SCHEMA_PATH = ARTIFACT_DIR / "proof_artifact_registry_schema.md"
POLICY_PATH = ARTIFACT_DIR / "trusted_foundation_policy.md"

RECORD_SCHEMA_ID = "v21_proof_evidence_record_v1"
FIXTURE_SCHEMA_ID = "v21_proof_evidence_fixture_suite_v1"
PASS_STATUS = "PASS_MACHINE_CHECKED_NO_AXIOM_DEPENDENCIES"
WARNING_STATUS = "PASS_WITH_FORMAL_ASSUMPTION_WARNING"
FAIL_STATUS = "FAIL"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

FORBIDDEN_PATH_PREFIXES = (
    ".local/",
    "wiki/",
    "output/",
)
REQUIRED_TOP_LEVEL = {
    "schema_id",
    "record_id",
    "subject",
    "theorem_statement",
    "proof_sources",
    "proof_objects",
    "toolchain",
    "trusted_foundation",
    "build",
    "claim_boundary",
    "authorization_layers",
    "forbidden_conclusions",
}
REQUIRED_AUTHORIZATION_FIELDS = {
    "proof_authority",
    "downstream_physics_promotion_authorized",
    "benchmark_promotion_authorized",
    "completed_derivation_authorized",
    "publication_authority",
}
REQUIRED_CLAIM_BOUNDARY_FALSE_FIELDS = {
    "proof_authority",
    "physics_promotion_authorized",
    "ontology_adoption_authorized",
    "physical_interpretation_authorized",
    "external_review_completed",
    "independent_replication_completed",
}
REQUIRED_FORBIDDEN_CONCLUSION_TOKENS = {
    "validator PASS as proof authority",
    "formalization as physical interpretation",
    "ontology adoption",
    "physics promotion",
    "completed derivation",
}


def _canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _issue(check_id: str, path: str, message: str) -> dict[str, str]:
    return {"check_id": check_id, "path": path, "message": message}


def _is_repo_relative_source(path_text: Any) -> bool:
    if not isinstance(path_text, str) or not path_text:
        return False
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts:
        return False
    return not any(path_text.startswith(prefix) for prefix in FORBIDDEN_PATH_PREFIXES)


def _check_hash_field(
    issues: list[dict[str, str]], value: Any, path: str
) -> bool:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        issues.append(_issue("sha256_shape", path, "must be lowercase SHA-256"))
        return False
    return True


def _check_live_hash(
    issues: list[dict[str, str]], path_text: Any, expected_hash: Any, field: str
) -> None:
    if not _is_repo_relative_source(path_text):
        issues.append(
            _issue("canonical_source_path", field, "must be a canonical repo-relative path")
        )
        return
    if not _check_hash_field(issues, expected_hash, f"{field}.sha256"):
        return
    path = REPO_ROOT / path_text
    if not path.is_file():
        issues.append(_issue("live_source_exists", field, "tracked source file is missing"))
        return
    actual_hash = _sha256_path(path)
    if actual_hash != expected_hash:
        issues.append(
            _issue(
                "live_source_hash",
                field,
                f"expected {expected_hash}; observed {actual_hash}",
            )
        )


def _nested_parent(record: dict[str, Any], dotted_path: str) -> tuple[Any, str | int]:
    parts = dotted_path.split(".")
    current: Any = record
    for part in parts[:-1]:
        if isinstance(current, dict) and part in current:
            current = current[part]
            continue
        if isinstance(current, list):
            try:
                index = int(part)
                current = current[index]
                continue
            except (ValueError, IndexError):
                pass
        raise KeyError(dotted_path)
    leaf: str | int = parts[-1]
    if isinstance(current, list):
        try:
            leaf = int(leaf)
        except ValueError as exc:
            raise KeyError(dotted_path) from exc
    return current, leaf


def apply_mutations(
    base_record: dict[str, Any], mutations: list[dict[str, Any]]
) -> dict[str, Any]:
    """Return a deep-copied record with deterministic fixture mutations."""

    record = copy.deepcopy(base_record)
    for mutation in mutations:
        operation = mutation.get("op")
        dotted_path = mutation.get("path")
        if operation not in {"set", "remove"} or not isinstance(dotted_path, str):
            raise ValueError("fixture mutations require op=set|remove and dotted path")
        parent, leaf = _nested_parent(record, dotted_path)
        if not isinstance(parent, (dict, list)):
            raise KeyError(dotted_path)
        if operation == "set":
            parent[leaf] = copy.deepcopy(mutation.get("value"))
        else:
            if isinstance(parent, dict) and leaf not in parent:
                raise KeyError(dotted_path)
            try:
                del parent[leaf]
            except (IndexError, TypeError) as exc:
                raise KeyError(dotted_path) from exc
    return record


def _validate_toolchain(
    record: dict[str, Any], issues: list[dict[str, str]], verify_live_files: bool
) -> None:
    toolchain = record.get("toolchain")
    if not isinstance(toolchain, dict):
        issues.append(_issue("toolchain_shape", "toolchain", "must be an object"))
        return
    required = {
        "tool",
        "version",
        "release_tag",
        "release_commit",
        "lock_path",
        "lock_sha256",
        "archive_name",
        "archive_sha256",
        "dependencies",
    }
    if set(toolchain) != required:
        issues.append(
            _issue(
                "toolchain_fields",
                "toolchain",
                f"must contain exactly {sorted(required)}",
            )
        )
        return
    if not isinstance(toolchain.get("dependencies"), list):
        issues.append(_issue("toolchain_dependencies", "toolchain.dependencies", "must be a list"))
    _check_hash_field(issues, toolchain.get("lock_sha256"), "toolchain.lock_sha256")
    _check_hash_field(issues, toolchain.get("archive_sha256"), "toolchain.archive_sha256")
    if not verify_live_files:
        return
    _check_live_hash(
        issues,
        toolchain.get("lock_path"),
        toolchain.get("lock_sha256"),
        "toolchain.lock_path",
    )
    lock_path = REPO_ROOT / str(toolchain.get("lock_path", ""))
    if not lock_path.is_file():
        return
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(_issue("toolchain_lock_parse", "toolchain.lock_path", str(exc)))
        return
    comparisons = {
        "tool": lock.get("tool"),
        "version": lock.get("version"),
        "release_tag": (lock.get("release") or {}).get("tag"),
        "release_commit": (lock.get("release") or {}).get("published_at")
        if toolchain.get("release_commit") == "not_recorded_in_lock"
        else (lock.get("release") or {}).get("release_commit", toolchain.get("release_commit")),
        "archive_name": (lock.get("archive") or {}).get("name"),
        "archive_sha256": (lock.get("archive") or {}).get("published_sha256"),
        "dependencies": lock.get("dependencies"),
    }
    # The P2 lock records the release commit in its completion rather than its
    # lock JSON.  That provenance gap is made explicit by the sentinel above.
    for field, observed in comparisons.items():
        expected = toolchain.get(field)
        if field == "release_commit" and expected == "not_recorded_in_lock":
            continue
        if observed != expected:
            issues.append(
                _issue(
                    "toolchain_lock_parity",
                    f"toolchain.{field}",
                    f"manifest {expected!r} does not match lock {observed!r}",
                )
            )


def _validate_trusted_foundation(
    record: dict[str, Any], issues: list[dict[str, str]]
) -> bool:
    trust = record.get("trusted_foundation")
    if not isinstance(trust, dict):
        issues.append(_issue("trust_shape", "trusted_foundation", "must be an object"))
        return False
    required = {
        "policy_id",
        "kernel",
        "foundation_version",
        "allowed_foundations",
        "allowed_admitted_axioms",
        "admitted_axioms",
        "theorem_axiom_report_count",
        "theorem_with_axiom_dependency_count",
        "forbidden_declaration_scan",
        "status",
    }
    if set(trust) != required:
        issues.append(
            _issue("trust_fields", "trusted_foundation", f"must contain exactly {sorted(required)}")
        )
        return False
    for field in ("allowed_foundations", "allowed_admitted_axioms", "admitted_axioms"):
        if not isinstance(trust.get(field), list):
            issues.append(_issue("trust_list", f"trusted_foundation.{field}", "must be a list"))
    scan = trust.get("forbidden_declaration_scan")
    expected_scan_keys = {"sorry", "admit", "custom_axiom", "unsafe"}
    if not isinstance(scan, dict) or set(scan) != expected_scan_keys:
        issues.append(
            _issue(
                "trust_scan_shape",
                "trusted_foundation.forbidden_declaration_scan",
                f"must contain exactly {sorted(expected_scan_keys)}",
            )
        )
    elif any(scan.values()):
        issues.append(
            _issue(
                "untrusted_formal_gap",
                "trusted_foundation.forbidden_declaration_scan",
                "sorry, admit, custom axiom, and unsafe declarations must all be absent",
            )
        )
    admitted = trust.get("admitted_axioms") if isinstance(trust.get("admitted_axioms"), list) else []
    allowed = (
        trust.get("allowed_admitted_axioms")
        if isinstance(trust.get("allowed_admitted_axioms"), list)
        else []
    )
    undeclared = sorted(set(admitted) - set(allowed))
    if undeclared:
        issues.append(
            _issue(
                "undeclared_axiom",
                "trusted_foundation.admitted_axioms",
                f"not allowed by policy: {undeclared}",
            )
        )
    report_count = trust.get("theorem_axiom_report_count")
    dependency_count = trust.get("theorem_with_axiom_dependency_count")
    if not isinstance(report_count, int) or report_count < 1:
        issues.append(
            _issue(
                "axiom_report_count",
                "trusted_foundation.theorem_axiom_report_count",
                "must be a positive integer",
            )
        )
    if not isinstance(dependency_count, int) or dependency_count < 0:
        issues.append(
            _issue(
                "axiom_dependency_count",
                "trusted_foundation.theorem_with_axiom_dependency_count",
                "must be a nonnegative integer",
            )
        )
        dependency_count = 0
    warning = bool(admitted) or bool(dependency_count)
    expected_status = "warning_admitted_axioms_present" if warning else "no_reported_axiom_dependencies"
    if trust.get("status") != expected_status:
        issues.append(
            _issue(
                "trust_status",
                "trusted_foundation.status",
                f"must be {expected_status}",
            )
        )
    return warning


def validate_record(
    record: dict[str, Any], *, verify_live_files: bool = True
) -> dict[str, Any]:
    """Validate one proof-evidence record and return deterministic findings."""

    issues: list[dict[str, str]] = []
    if not isinstance(record, dict):
        return {"status": FAIL_STATUS, "warning_count": 0, "issues": [_issue("record_shape", "", "must be an object")]}
    missing = sorted(REQUIRED_TOP_LEVEL - set(record))
    unexpected = sorted(set(record) - REQUIRED_TOP_LEVEL)
    for field in missing:
        issues.append(_issue("required_field", field, "missing required field"))
    for field in unexpected:
        issues.append(_issue("unexpected_field", field, "unexpected top-level field"))
    if record.get("schema_id") != RECORD_SCHEMA_ID:
        issues.append(_issue("schema_id", "schema_id", f"must be {RECORD_SCHEMA_ID}"))

    subject = record.get("subject")
    if not isinstance(subject, dict) or set(subject) != {"theorem_id", "theorem_scope", "claim_status"}:
        issues.append(
            _issue(
                "subject_shape",
                "subject",
                "must contain exactly theorem_id, theorem_scope, and claim_status",
            )
        )
    elif subject.get("claim_status") not in {"draft/control", "proposal-only", "source-extension data"}:
        issues.append(
            _issue(
                "subject_claim_status",
                "subject.claim_status",
                "must remain non-promotional",
            )
        )

    theorem = record.get("theorem_statement")
    if not isinstance(theorem, dict) or set(theorem) != {"path", "sha256", "authority_status"}:
        issues.append(
            _issue(
                "theorem_statement_shape",
                "theorem_statement",
                "must contain exactly path, sha256, and authority_status",
            )
        )
    else:
        if theorem.get("authority_status") not in {"registered_canonical_science", "tracked_task_science"}:
            issues.append(
                _issue(
                    "theorem_authority",
                    "theorem_statement.authority_status",
                    "must identify tracked science authority without promoting it",
                )
            )
        if verify_live_files:
            _check_live_hash(issues, theorem.get("path"), theorem.get("sha256"), "theorem_statement")
        else:
            _check_hash_field(issues, theorem.get("sha256"), "theorem_statement.sha256")

    proof_sources = record.get("proof_sources")
    if not isinstance(proof_sources, list) or not proof_sources:
        issues.append(_issue("proof_sources", "proof_sources", "must be a nonempty list"))
    else:
        for index, source in enumerate(proof_sources):
            field = f"proof_sources.{index}"
            if not isinstance(source, dict) or set(source) != {"path", "sha256", "language", "role"}:
                issues.append(_issue("proof_source_shape", field, "invalid proof-source shape"))
                continue
            if verify_live_files:
                _check_live_hash(issues, source.get("path"), source.get("sha256"), field)
            else:
                _check_hash_field(issues, source.get("sha256"), f"{field}.sha256")

    proof_objects = record.get("proof_objects")
    if not isinstance(proof_objects, list) or not proof_objects:
        issues.append(_issue("proof_objects", "proof_objects", "must be a nonempty list"))
        proof_objects = []
    for index, proof_object in enumerate(proof_objects):
        field = f"proof_objects.{index}"
        required = {
            "artifact_id",
            "format",
            "sha256",
            "retained_path",
            "retention_status",
            "reproducible",
            "clean_build_count",
        }
        if not isinstance(proof_object, dict) or set(proof_object) != required:
            issues.append(_issue("proof_object_shape", field, "invalid proof-object shape"))
            continue
        _check_hash_field(issues, proof_object.get("sha256"), f"{field}.sha256")
        if proof_object.get("retention_status") not in {
            "tracked_artifact",
            "hashed_untracked_build_output",
        }:
            issues.append(_issue("proof_object_retention", field, "unknown retention status"))
        if proof_object.get("retention_status") == "tracked_artifact":
            if verify_live_files:
                _check_live_hash(
                    issues,
                    proof_object.get("retained_path"),
                    proof_object.get("sha256"),
                    field,
                )
        elif proof_object.get("retained_path") != "":
            issues.append(
                _issue(
                    "untracked_proof_object_path",
                    f"{field}.retained_path",
                    "hashed untracked output must not claim a tracked path",
                )
            )
        count = proof_object.get("clean_build_count")
        reproducible = proof_object.get("reproducible")
        if not isinstance(count, int) or count < 1:
            issues.append(_issue("clean_build_count", field, "must be a positive integer"))
        if not isinstance(reproducible, bool):
            issues.append(_issue("reproducible_type", field, "must be boolean"))
        elif reproducible and isinstance(count, int) and count < 2:
            issues.append(
                _issue(
                    "reproducible_build_count",
                    field,
                    "byte reproducibility requires at least two clean builds",
                )
            )

    _validate_toolchain(record, issues, verify_live_files)
    warning = _validate_trusted_foundation(record, issues)

    build = record.get("build")
    required_build = {
        "adapter_id",
        "script_path",
        "script_sha256",
        "result_status",
        "clean_build_count",
        "proof_object_byte_reproducible",
        "proof_object_sha256",
        "validation_receipt_path",
        "validation_receipt_sha256",
        "source_hash_verified",
        "proof_object_hash_verified",
    }
    if not isinstance(build, dict) or set(build) != required_build:
        issues.append(_issue("build_shape", "build", f"must contain exactly {sorted(required_build)}"))
    else:
        for name in ("source_hash_verified", "proof_object_hash_verified", "proof_object_byte_reproducible"):
            if build.get(name) is not True:
                issues.append(_issue("build_boolean", f"build.{name}", "must be true for this record"))
        if build.get("result_status") != "PASS":
            issues.append(_issue("build_status", "build.result_status", "must be PASS"))
        if verify_live_files:
            _check_live_hash(issues, build.get("script_path"), build.get("script_sha256"), "build.script_path")
            _check_live_hash(
                issues,
                build.get("validation_receipt_path"),
                build.get("validation_receipt_sha256"),
                "build.validation_receipt_path",
            )
        else:
            _check_hash_field(issues, build.get("script_sha256"), "build.script_sha256")
            _check_hash_field(issues, build.get("validation_receipt_sha256"), "build.validation_receipt_sha256")
        _check_hash_field(issues, build.get("proof_object_sha256"), "build.proof_object_sha256")
        if proof_objects and isinstance(proof_objects[0], dict):
            if build.get("proof_object_sha256") != proof_objects[0].get("sha256"):
                issues.append(
                    _issue(
                        "proof_object_hash_parity",
                        "build.proof_object_sha256",
                        "must match the first proof-object hash",
                    )
                )
            if build.get("clean_build_count") != proof_objects[0].get("clean_build_count"):
                issues.append(
                    _issue(
                        "clean_build_parity",
                        "build.clean_build_count",
                        "must match the proof-object clean-build count",
                    )
                )
        receipt_path = REPO_ROOT / str(build.get("validation_receipt_path", ""))
        if verify_live_files and receipt_path.is_file():
            try:
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                checks = {
                    item.get("check_id"): item
                    for item in receipt.get("checks", [])
                    if isinstance(item, dict) and isinstance(item.get("check_id"), str)
                }
                if receipt.get("status") != "PASS" or receipt.get("failure_count") != 0:
                    issues.append(
                        _issue(
                            "validation_receipt_status",
                            "build.validation_receipt_path",
                            "receipt must record PASS with zero failures",
                        )
                    )
                proof_hash_evidence = [
                    item.get("evidence")
                    for item in receipt.get("checks", [])
                    if item.get("check_id") == "proof_object_sha256"
                    and item.get("status") == "PASS"
                ]
                if build.get("proof_object_sha256") not in proof_hash_evidence:
                    issues.append(
                        _issue(
                            "validation_receipt_proof_hash",
                            "build.validation_receipt_path",
                            "receipt does not carry the registered proof-object hash",
                        )
                    )
                source_check = checks.get("source_sha256", {})
                if proof_sources and isinstance(proof_sources[0], dict):
                    if source_check.get("status") != "PASS" or source_check.get("evidence") != proof_sources[0].get("sha256"):
                        issues.append(
                            _issue(
                                "validation_receipt_source_hash",
                                "build.validation_receipt_path",
                                "receipt does not carry the registered formal-source hash",
                            )
                        )
                theorem_check = checks.get("p2_t03_source_sha256", {})
                theorem_evidence = theorem_check.get("evidence")
                if isinstance(theorem, dict):
                    if (
                        theorem_check.get("status") != "PASS"
                        or not isinstance(theorem_evidence, dict)
                        or theorem_evidence.get(theorem.get("path")) != theorem.get("sha256")
                    ):
                        issues.append(
                            _issue(
                                "validation_receipt_theorem_hash",
                                "build.validation_receipt_path",
                                "receipt does not carry the registered theorem-source hash",
                            )
                        )
                lean_version = checks.get("lean_version", {})
                lean_evidence = lean_version.get("evidence")
                toolchain = record.get("toolchain", {})
                if (
                    lean_version.get("status") != "PASS"
                    or not isinstance(lean_evidence, str)
                    or f"version {toolchain.get('version')}" not in lean_evidence
                    or f"commit {toolchain.get('release_commit')}" not in lean_evidence
                ):
                    issues.append(
                        _issue(
                            "validation_receipt_toolchain_identity",
                            "build.validation_receipt_path",
                            "receipt does not match the registered tool version and release commit",
                        )
                    )
                trust = record.get("trusted_foundation", {})
                axiom_report = checks.get("axiom_report_count", {})
                axiom_evidence = axiom_report.get("evidence")
                if (
                    axiom_report.get("status") != "PASS"
                    or not isinstance(axiom_evidence, list)
                    or len(axiom_evidence) != trust.get("theorem_axiom_report_count")
                ):
                    issues.append(
                        _issue(
                            "validation_receipt_axiom_report_count",
                            "build.validation_receipt_path",
                            "receipt axiom-report count does not match the trust declaration",
                        )
                    )
                no_dependencies = checks.get("no_reported_axiom_dependencies", {})
                dependency_evidence = no_dependencies.get("evidence")
                if (
                    no_dependencies.get("status") != "PASS"
                    or not isinstance(dependency_evidence, list)
                    or any("does not depend on any axioms" not in item for item in dependency_evidence)
                    or trust.get("theorem_with_axiom_dependency_count") != 0
                ):
                    issues.append(
                        _issue(
                            "validation_receipt_axiom_dependency",
                            "build.validation_receipt_path",
                            "receipt and trust declaration must report zero theorem axiom dependencies",
                        )
                    )
                for check_id in (
                    "no_sorry",
                    "no_admit",
                    "no_axiom_declaration",
                    "no_unsafe_declaration",
                ):
                    if checks.get(check_id, {}).get("status") != "PASS":
                        issues.append(
                            _issue(
                                "validation_receipt_forbidden_declaration_scan",
                                "build.validation_receipt_path",
                                f"receipt check {check_id} must PASS",
                            )
                        )
            except (OSError, json.JSONDecodeError) as exc:
                issues.append(_issue("validation_receipt_parse", "build.validation_receipt_path", str(exc)))

    claim = record.get("claim_boundary")
    if not isinstance(claim, dict):
        issues.append(_issue("claim_boundary_shape", "claim_boundary", "must be an object"))
    else:
        for field in sorted(REQUIRED_CLAIM_BOUNDARY_FALSE_FIELDS):
            if claim.get(field) is not False:
                issues.append(
                    _issue(
                        "claim_boundary_false",
                        f"claim_boundary.{field}",
                        "must be exactly false",
                    )
                )
        if claim.get("mathematical_status") not in {
            "machine_checked_scoped",
            "machine_checked_with_formal_assumption_warning",
        }:
            issues.append(
                _issue(
                    "mathematical_status",
                    "claim_boundary.mathematical_status",
                    "unknown scoped mathematical status",
                )
            )
        expected_math_status = (
            "machine_checked_with_formal_assumption_warning"
            if warning
            else "machine_checked_scoped"
        )
        if claim.get("mathematical_status") != expected_math_status:
            issues.append(
                _issue(
                    "mathematical_status_warning_parity",
                    "claim_boundary.mathematical_status",
                    f"must be {expected_math_status}",
                )
            )
        if claim.get("authority_status") not in {"control_only", "proposal_only"}:
            issues.append(
                _issue(
                    "authority_status",
                    "claim_boundary.authority_status",
                    "must remain control_only or proposal_only",
                )
            )

    authorization = record.get("authorization_layers")
    if not isinstance(authorization, dict) or set(authorization) != REQUIRED_AUTHORIZATION_FIELDS:
        issues.append(
            _issue(
                "authorization_shape",
                "authorization_layers",
                f"must contain exactly {sorted(REQUIRED_AUTHORIZATION_FIELDS)}",
            )
        )
    elif any(value is not False for value in authorization.values()):
        issues.append(
            _issue(
                "authorization_false",
                "authorization_layers",
                "every protected authorization must be exactly false",
            )
        )

    conclusions = record.get("forbidden_conclusions")
    if not isinstance(conclusions, list) or any(not isinstance(item, str) or not item for item in conclusions):
        issues.append(
            _issue(
                "forbidden_conclusions_shape",
                "forbidden_conclusions",
                "must be a list of nonempty strings",
            )
        )
    else:
        missing_tokens = sorted(REQUIRED_FORBIDDEN_CONCLUSION_TOKENS - set(conclusions))
        if missing_tokens:
            issues.append(
                _issue(
                    "forbidden_conclusions_required",
                    "forbidden_conclusions",
                    f"missing exact guards: {missing_tokens}",
                )
            )

    status = FAIL_STATUS if issues else (WARNING_STATUS if warning else PASS_STATUS)
    return {
        "status": status,
        "warning_count": 1 if status == WARNING_STATUS else 0,
        "issue_count": len(issues),
        "issues": issues,
    }


def build_report(fixtures_path: Path = DEFAULT_FIXTURES) -> dict[str, Any]:
    suite = json.loads(fixtures_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if suite.get("schema_id") != FIXTURE_SCHEMA_ID:
        errors.append(f"fixture schema_id must be {FIXTURE_SCHEMA_ID}")
    base_record = suite.get("base_record")
    cases = suite.get("cases")
    if not isinstance(base_record, dict):
        errors.append("base_record must be an object")
        base_record = {}
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a nonempty list")
        cases = []

    case_results: list[dict[str, Any]] = []
    seen_case_ids: set[str] = set()
    for case in cases:
        case_id = case.get("case_id") if isinstance(case, dict) else None
        if not isinstance(case_id, str) or not case_id:
            errors.append("every fixture case requires a nonempty case_id")
            continue
        if case_id in seen_case_ids:
            errors.append(f"duplicate fixture case_id: {case_id}")
            continue
        seen_case_ids.add(case_id)
        try:
            record = apply_mutations(base_record, case.get("mutations", []))
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"{case_id}: invalid mutation: {exc}")
            continue
        result = validate_record(record, verify_live_files=case.get("verify_live_files") is True)
        expected_status = case.get("expected_status")
        matched = result["status"] == expected_status
        case_results.append(
            {
                "case_id": case_id,
                "expected_status": expected_status,
                "observed_status": result["status"],
                "status_matched": matched,
                "warning_count": result["warning_count"],
                "issue_count": result["issue_count"],
                "issues": result["issues"],
            }
        )

    unexpected = sum(not item["status_matched"] for item in case_results)
    observed_counts = {
        PASS_STATUS: sum(item["observed_status"] == PASS_STATUS for item in case_results),
        WARNING_STATUS: sum(item["observed_status"] == WARNING_STATUS for item in case_results),
        FAIL_STATUS: sum(item["observed_status"] == FAIL_STATUS for item in case_results),
    }
    report_status = "PASS" if not errors and unexpected == 0 else "FAIL"
    return {
        "schema_id": "v21_proof_evidence_validation_report_v1",
        "task_id": "RT-20260722-009",
        "plan_task_id": "P11-T03",
        "status": report_status,
        "record_schema_id": RECORD_SCHEMA_ID,
        "fixture_schema_id": FIXTURE_SCHEMA_ID,
        "fixture_count": len(case_results),
        "unexpected_fixture_result_count": unexpected,
        "observed_status_counts": observed_counts,
        "formal_failure_visible": observed_counts[FAIL_STATUS] > 0,
        "formal_assumption_warning_visible": observed_counts[WARNING_STATUS] > 0,
        "p2_t05_migration_status": next(
            (
                item["observed_status"]
                for item in case_results
                if item["case_id"] == "p2_t05_migration_pass"
            ),
            "missing",
        ),
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "ontology_adoption_authorized": False,
        "external_review_completed": False,
        "independent_replication_completed": False,
        "input_hashes": {
            "fixtures": _sha256_path(fixtures_path),
            "schema": _sha256_path(SCHEMA_PATH),
            "trusted_foundation_policy": _sha256_path(POLICY_PATH),
            "adapter": _sha256_path(Path(__file__).resolve()),
        },
        "errors": errors,
        "case_results": case_results,
        "claim_boundary_summary": (
            "Mechanized build evidence is queryable project-control metadata. "
            "Adapter PASS is not theorem truth, proof authority, physical "
            "interpretation, ontology adoption, external review, or promotion."
        ),
    }


def build_compact_receipt(report: dict[str, Any], report_bytes: bytes) -> dict[str, Any]:
    return {
        "schema_id": "v21_proof_evidence_compact_receipt_v1",
        "task_id": report["task_id"],
        "plan_task_id": report["plan_task_id"],
        "status": report["status"],
        "record_schema_id": report["record_schema_id"],
        "fixture_count": report["fixture_count"],
        "unexpected_fixture_result_count": report["unexpected_fixture_result_count"],
        "observed_status_counts": report["observed_status_counts"],
        "formal_failure_visible": report["formal_failure_visible"],
        "formal_assumption_warning_visible": report["formal_assumption_warning_visible"],
        "p2_t05_migration_status": report["p2_t05_migration_status"],
        "report_sha256": _sha256_bytes(report_bytes),
        "input_hashes": report["input_hashes"],
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "claim_boundary_summary": report["claim_boundary_summary"],
    }


def _write_or_check(path: Path, content: bytes, check: bool) -> bool:
    if check:
        return path.is_file() and path.read_bytes() == content
    path.write_bytes(content)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write report and compact receipt")
    mode.add_argument("--check", action="store_true", help="verify report and compact receipt are fresh")
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--compact", type=Path, default=DEFAULT_COMPACT)
    parser.add_argument("--json", action="store_true", help="emit compact JSON summary")
    args = parser.parse_args(argv)

    report = build_report(args.fixtures)
    report_bytes = _canonical_json_bytes(report)
    compact = build_compact_receipt(report, report_bytes)
    compact_bytes = _canonical_json_bytes(compact)

    fresh = True
    if args.write or args.check:
        fresh &= _write_or_check(args.report, report_bytes, args.check)
        fresh &= _write_or_check(args.compact, compact_bytes, args.check)
    summary = {
        "status": report["status"] if fresh else "FAIL_STALE_OUTPUT",
        "fresh": fresh,
        "fixture_count": report["fixture_count"],
        "unexpected_fixture_result_count": report["unexpected_fixture_result_count"],
        "observed_status_counts": report["observed_status_counts"],
        "p2_t05_migration_status": report["p2_t05_migration_status"],
        "proof_authority": False,
        "physics_promotion_authorized": False,
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" and fresh else 1


if __name__ == "__main__":
    sys.exit(main())
