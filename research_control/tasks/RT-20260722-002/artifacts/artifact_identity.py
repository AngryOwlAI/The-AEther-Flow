#!/usr/bin/env python3
"""Prospective portable-path linter and content-addressed P10-T07 pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import unicodedata
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ROOT = REPO_ROOT / "research_control/tasks/RT-20260722-002"
ARTIFACT_ROOT = TASK_ROOT / "artifacts"
CA_ROOT = ARTIFACT_ROOT / "ca"
MANIFEST_PATH = ARTIFACT_ROOT / "artifact_refs.json"
VALIDATION_PATH = ARTIFACT_ROOT / "validation.json"
COMPACT_RECEIPT_PATH = ARTIFACT_ROOT / "compact_receipt.json"
POLICY_PATH = ARTIFACT_ROOT / "artifact_path_policy.md"
MIGRATION_PATH = ARTIFACT_ROOT / "migration_guidance.md"

POLICY = {
    "schema_id": "artifact_path_policy_v1",
    "max_relative_path_chars": 180,
    "max_relative_path_utf8_bytes": 220,
    "max_component_chars": 96,
    "max_component_utf8_bytes": 120,
    "max_filename_chars": 96,
    "max_filename_utf8_bytes": 120,
    "max_stable_alias_chars": 48,
    "normalization": "NFC",
    "separator": "/",
    "digest_algorithm": "sha256",
    "digest_hex_chars": 64,
}

SOURCE_SPECS = (
    {
        "stable_alias": "event-architecture-v1",
        "title": "V21 canonical event-store architecture contract",
        "media_type": "application/json",
        "source_path": "research_control/tasks/RT-20260721-007/artifacts/v21_event_store_architecture_contract.json",
    },
    {
        "stable_alias": "event-schema-v1",
        "title": "V21 project-control event schema",
        "media_type": "text/markdown",
        "source_path": "research_control/tasks/RT-20260721-007/artifacts/v21_event_store_schema.md",
    },
    {
        "stable_alias": "generated-view-v1",
        "title": "V21 deterministic generated-view contract",
        "media_type": "text/markdown",
        "source_path": "research_control/tasks/RT-20260721-007/artifacts/v21_generated_view_contract.md",
    },
)

ALIAS_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,47}$")
HEX_RE = re.compile(r"^[0-9a-f]{64}$")
WINDOWS_RESERVED = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}
WINDOWS_FORBIDDEN = set('<>:"\\|?*')


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def rel_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def path_finding(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def lint_relative_path(path_text: str) -> list[dict[str, str]]:
    """Return deterministic portability findings for one repository-relative path."""
    findings: list[dict[str, str]] = []
    if not isinstance(path_text, str) or not path_text:
        return [path_finding("empty_path", str(path_text), "path must be a nonempty string")]
    if path_text.startswith("/") or re.match(r"^[A-Za-z]:", path_text):
        findings.append(path_finding("absolute_path", path_text, "path must be repository-relative"))
    if "\\" in path_text:
        findings.append(path_finding("backslash_separator", path_text, "use POSIX forward slashes"))
    if unicodedata.normalize("NFC", path_text) != path_text:
        findings.append(path_finding("non_nfc", path_text, "path must be Unicode NFC"))
    if len(path_text) > POLICY["max_relative_path_chars"]:
        findings.append(path_finding("relative_path_chars", path_text, "repository-relative path is too long"))
    if len(path_text.encode("utf-8")) > POLICY["max_relative_path_utf8_bytes"]:
        findings.append(path_finding("relative_path_bytes", path_text, "repository-relative UTF-8 path is too long"))

    components = path_text.split("/")
    for component in components:
        if component in {"", ".", ".."}:
            findings.append(path_finding("unsafe_segment", path_text, f"unsafe path segment: {component!r}"))
            continue
        if len(component) > POLICY["max_component_chars"]:
            findings.append(path_finding("component_chars", path_text, f"component is too long: {component[:24]}"))
        if len(component.encode("utf-8")) > POLICY["max_component_utf8_bytes"]:
            findings.append(path_finding("component_bytes", path_text, f"component UTF-8 encoding is too long: {component[:24]}"))
        if component.endswith((" ", ".")):
            findings.append(path_finding("trailing_space_or_period", path_text, f"component has unsafe trailing character: {component!r}"))
        if any(ord(char) < 32 or ord(char) == 127 for char in component):
            findings.append(path_finding("control_character", path_text, "component contains a control character"))
        forbidden = sorted({char for char in component if char in WINDOWS_FORBIDDEN})
        if forbidden:
            findings.append(path_finding("windows_forbidden_character", path_text, f"component contains forbidden characters: {''.join(forbidden)}"))
        stem = component.split(".", 1)[0].casefold()
        if stem in WINDOWS_RESERVED:
            findings.append(path_finding("windows_reserved_name", path_text, f"reserved Windows device name: {component}"))

    filename = components[-1] if components else ""
    if len(filename) > POLICY["max_filename_chars"]:
        findings.append(path_finding("filename_chars", path_text, "filename is too long"))
    if len(filename.encode("utf-8")) > POLICY["max_filename_utf8_bytes"]:
        findings.append(path_finding("filename_bytes", path_text, "filename UTF-8 encoding is too long"))
    return sorted(findings, key=lambda item: (item["code"], item["path"], item["message"]))


def casefold_collisions(paths: Iterable[str]) -> list[dict[str, Any]]:
    buckets: dict[str, list[str]] = {}
    for path_text in paths:
        key = unicodedata.normalize("NFC", path_text).casefold()
        buckets.setdefault(key, []).append(path_text)
    return [
        {"code": "casefold_collision", "paths": sorted(values)}
        for _, values in sorted(buckets.items())
        if len(set(values)) > 1
    ]


def build_reference(spec: dict[str, str]) -> tuple[dict[str, Any], bytes]:
    source_rel = spec["source_path"]
    source_path = REPO_ROOT / source_rel
    source_bytes = source_path.read_bytes()
    digest = sha256_bytes(source_bytes)
    suffix = source_path.suffix.lower()
    content_rel = f"research_control/tasks/RT-20260722-002/artifacts/ca/{digest}{suffix}"
    reference = {
        "aliases_are_authority": False,
        "content_path": content_rel,
        "content_sha256": digest,
        "historical_source_path_changed": False,
        "identity": f"sha256:{digest}",
        "media_type": spec["media_type"],
        "source_path": source_rel,
        "source_sha256": digest,
        "stable_alias": spec["stable_alias"],
        "title": spec["title"],
    }
    return reference, source_bytes


def build_manifest() -> tuple[dict[str, Any], dict[str, bytes]]:
    references: list[dict[str, Any]] = []
    copies: dict[str, bytes] = {}
    for spec in SOURCE_SPECS:
        reference, source_bytes = build_reference(spec)
        references.append(reference)
        copies[reference["content_path"]] = source_bytes
    references.sort(key=lambda item: item["stable_alias"])
    manifest = {
        "aliases_are_authority": False,
        "event_store_cutover_authorized": False,
        "historical_paths_changed": False,
        "manifest_authority": "generated_noncanonical",
        "physics_promotion_authorized": False,
        "policy_schema_id": POLICY["schema_id"],
        "proof_authority": False,
        "references": references,
        "schema_id": "artifact_reference_manifest_v1",
        "scientific_claims_changed": False,
    }
    return manifest, copies


def validate_manifest(manifest: dict[str, Any], copies: dict[str, bytes]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    checks: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []

    def record(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        if not passed:
            findings.append({"finding_id": check_id, "detail": detail})

    references = manifest.get("references", [])
    aliases = [item.get("stable_alias", "") for item in references]
    paths = [item.get("content_path", "") for item in references]
    record("reference_count", len(references) == 3, f"references={len(references)}")
    record("stable_alias_unique", len(aliases) == len(set(aliases)), f"aliases={len(aliases)} unique={len(set(aliases))}")
    record("stable_alias_syntax", all(ALIAS_RE.fullmatch(alias) for alias in aliases), "all aliases use the bounded portable syntax")
    record("portable_content_paths", not any(lint_relative_path(path) for path in paths), "all content paths pass prospective portability policy")
    record("casefold_unique", not casefold_collisions(paths), "content paths are unique after NFC casefold")

    identity_ok = True
    source_ok = True
    copy_ok = True
    for item in references:
        digest = item.get("content_sha256", "")
        source_path = REPO_ROOT / item.get("source_path", "")
        copy_bytes = copies.get(item.get("content_path", ""), b"")
        identity_ok &= bool(HEX_RE.fullmatch(digest)) and item.get("identity") == f"sha256:{digest}"
        source_ok &= source_path.is_file() and file_sha256(source_path) == item.get("source_sha256") == digest
        copy_ok &= sha256_bytes(copy_bytes) == digest
    record("full_sha256_identity", identity_ok, "every identity carries one exact full SHA-256 digest")
    record("historical_source_integrity", source_ok, "every historical source exists at its original path with its pinned digest")
    record("content_copy_integrity", copy_ok, "every task-local copy resolves to the full recorded digest")
    record("historical_paths_preserved", manifest.get("historical_paths_changed") is False, "manifest records no historical path mutation")
    record("alias_non_authority", manifest.get("aliases_are_authority") is False, "aliases remain non-authoritative manifest keys")
    record("science_non_authority", manifest.get("scientific_claims_changed") is False and manifest.get("physics_promotion_authorized") is False and manifest.get("proof_authority") is False, "pilot creates no scientific or promotion authority")

    fixtures = {
        "absolute": "/tmp/artifact.json",
        "backslash": r"artifacts\unsafe.json",
        "reserved": "artifacts/CON.md",
        "trailing": "artifacts/report. ",
        "parent": "artifacts/../report.md",
        "non_nfc": "artifacts/cafe\u0301.md",
        "component_too_long": f"artifacts/{'a' * 97}.md",
        "relative_too_long": "/".join(["segment" * 5] * 6) + ".md",
    }
    fixture_codes = {name: {item["code"] for item in lint_relative_path(path)} for name, path in fixtures.items()}
    expected_codes = {
        "absolute": "absolute_path",
        "backslash": "backslash_separator",
        "reserved": "windows_reserved_name",
        "trailing": "trailing_space_or_period",
        "parent": "unsafe_segment",
        "non_nfc": "non_nfc",
        "component_too_long": "component_chars",
        "relative_too_long": "relative_path_chars",
    }
    record("cross_platform_negative_fixtures", all(code in fixture_codes[name] for name, code in expected_codes.items()), f"fixtures={len(fixtures)}")
    collision_fixture = casefold_collisions(["artifacts/Report.md", "artifacts/report.md"])
    record("casefold_collision_fixture", len(collision_fixture) == 1, "case-insensitive collision fails closed")
    return checks, findings


def build_validation(manifest: dict[str, Any], copies: dict[str, bytes]) -> dict[str, Any]:
    checks, findings = validate_manifest(manifest, copies)
    return {
        "aliases_are_authority": False,
        "check_count": len(checks),
        "checks": checks,
        "cross_platform_profiles": {
            "linux": "bounded UTF-8 component and repository-relative path fixtures",
            "macos": "NFC and casefold collision fixtures plus bounded UTF-8 components",
            "windows": "legacy path budget reserved names forbidden characters separators and trailing-character fixtures",
        },
        "failed_check_count": len(findings),
        "findings": findings,
        "historical_paths_changed": False,
        "physics_promotion_authorized": False,
        "policy": POLICY,
        "proof_authority": False,
        "reference_count": len(manifest["references"]),
        "schema_id": "artifact_identity_validation_v1",
        "scientific_claims_changed": False,
        "status": "PASS" if not findings else "FAIL",
    }


def build_compact_receipt(manifest_bytes: bytes, validation_bytes: bytes) -> dict[str, Any]:
    return {
        "aliases_are_authority": False,
        "content_reference_count": 3,
        "event_store_cutover_authorized": False,
        "historical_paths_changed": False,
        "manifest_path": rel_path(MANIFEST_PATH),
        "manifest_sha256": sha256_bytes(manifest_bytes),
        "migration_guidance_path": rel_path(MIGRATION_PATH),
        "migration_guidance_sha256": file_sha256(MIGRATION_PATH),
        "path_policy_path": rel_path(POLICY_PATH),
        "path_policy_sha256": file_sha256(POLICY_PATH),
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "schema_id": "artifact_identity_compact_receipt_v1",
        "scientific_claims_changed": False,
        "status": "PASS",
        "tool_path": rel_path(Path(__file__).resolve()),
        "tool_sha256": file_sha256(Path(__file__).resolve()),
        "validation_path": rel_path(VALIDATION_PATH),
        "validation_sha256": sha256_bytes(validation_bytes),
    }


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def expected_outputs() -> tuple[dict[str, bytes], dict[str, Any]]:
    manifest, copies = build_manifest()
    validation = build_validation(manifest, copies)
    manifest_bytes = canonical_json_bytes(manifest)
    validation_bytes = canonical_json_bytes(validation)
    receipt = build_compact_receipt(manifest_bytes, validation_bytes)
    outputs = {**copies}
    outputs[rel_path(MANIFEST_PATH)] = manifest_bytes
    outputs[rel_path(VALIDATION_PATH)] = validation_bytes
    outputs[rel_path(COMPACT_RECEIPT_PATH)] = canonical_json_bytes(receipt)
    return outputs, validation


def write_outputs(outputs: dict[str, bytes]) -> None:
    for path_text, data in sorted(outputs.items()):
        atomic_write(REPO_ROOT / path_text, data)


def drift_paths(outputs: dict[str, bytes]) -> list[str]:
    drift: list[str] = []
    for path_text, expected in sorted(outputs.items()):
        path = REPO_ROOT / path_text
        if not path.is_file() or path.read_bytes() != expected:
            drift.append(path_text)
    return drift


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write deterministic pilot outputs")
    mode.add_argument("--check", action="store_true", help="check deterministic pilot outputs")
    parser.add_argument("--lint-path", action="append", default=[], help="lint one repository-relative path; may be repeated")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    if args.lint_path:
        findings = [item for path_text in args.lint_path for item in lint_relative_path(path_text)]
        collisions = casefold_collisions(args.lint_path)
        payload = {
            "collision_count": len(collisions),
            "collisions": collisions,
            "finding_count": len(findings),
            "findings": findings,
            "path_count": len(args.lint_path),
            "policy_schema_id": POLICY["schema_id"],
            "status": "PASS" if not findings and not collisions else "FAIL",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["status"] == "PASS" else 1

    outputs, validation = expected_outputs()
    if args.write:
        write_outputs(outputs)
    drift = drift_paths(outputs)
    payload = {
        "check_count": validation["check_count"],
        "drift_count": len(drift),
        "drift_paths": drift,
        "failed_check_count": validation["failed_check_count"],
        "reference_count": validation["reference_count"],
        "status": "PASS" if validation["status"] == "PASS" and not drift else "FAIL",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
