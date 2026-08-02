#!/usr/bin/env python3
"""Shared deterministic provenance and commit-lag helpers for live reports."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Mapping

from strict_yaml import StrictYamlError, load as load_yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ID = "generated_report_provenance_v1"
POLICY_PATH = (
    "research_control/tasks/RT-20260801-011/artifacts/"
    "generated_report_freshness_metadata_schema_v1.yaml"
)
HELPER_PATH = "scripts/research_control/generated_report_provenance.py"
MARKER_PREFIX = "<!-- generated-report-provenance: "
MARKER_SUFFIX = " -->"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
RFC3339_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
FIXTURE_SOURCE_COMMIT = "0" * 40


class GeneratedReportProvenanceError(RuntimeError):
    """Raised when live report provenance is absent, malformed, or stale."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(repo_root: Path, rel_path: str) -> str:
    path = repo_root / rel_path
    if not path.is_file():
        raise GeneratedReportProvenanceError(f"missing provenance source: {rel_path}")
    return sha256_bytes(path.read_bytes())


def canonical_json(value: Any, *, compact: bool = False) -> str:
    if compact:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _load_policy_from(repo_root: Path) -> dict[str, Any]:
    path = repo_root / POLICY_PATH
    if not path.is_file():
        raise GeneratedReportProvenanceError(f"missing freshness policy: {POLICY_PATH}")
    try:
        value = load_yaml(path)
    except StrictYamlError as exc:
        raise GeneratedReportProvenanceError(f"invalid freshness policy: {exc}") from exc
    if not isinstance(value, dict):
        raise GeneratedReportProvenanceError("freshness policy must be a mapping")
    if value.get("schema_id") != "generated_report_freshness_metadata_schema_v1":
        raise GeneratedReportProvenanceError("unexpected freshness-policy schema_id")
    if value.get("status") != "active":
        raise GeneratedReportProvenanceError("freshness policy is not active")
    return value


POLICY = _load_policy_from(REPO_ROOT)
POLICY_SHA256 = sha256_file(REPO_ROOT, POLICY_PATH)
HELPER_SHA256 = sha256_file(REPO_ROOT, HELPER_PATH)


def report_policy(report_class: str) -> dict[str, Any]:
    report_classes = POLICY.get("report_classes")
    if not isinstance(report_classes, dict):
        raise GeneratedReportProvenanceError("freshness policy lacks report_classes")
    value = report_classes.get(report_class)
    if not isinstance(value, dict):
        raise GeneratedReportProvenanceError(f"unknown live report class: {report_class}")
    if value.get("live_authoritative_facing") is not True:
        raise GeneratedReportProvenanceError(f"report class is not live: {report_class}")
    try:
        maximum_lag = int(str(value.get("maximum_commit_lag", "")))
    except ValueError:
        raise GeneratedReportProvenanceError(f"invalid maximum lag for {report_class}")
    if maximum_lag < 0:
        raise GeneratedReportProvenanceError(f"invalid maximum lag for {report_class}")
    return {**value, "maximum_commit_lag": maximum_lag}


def git_head(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    value = result.stdout.strip()
    if result.returncode != 0 or not HEX40.fullmatch(value):
        return FIXTURE_SOURCE_COMMIT
    return value


def source_manifest_sha256(source_hashes: Mapping[str, str]) -> str:
    if not source_hashes:
        raise GeneratedReportProvenanceError("source hash mapping is empty")
    lines: list[str] = []
    for rel_path, digest in sorted(source_hashes.items()):
        if not rel_path or rel_path.startswith("/") or ".." in Path(rel_path).parts:
            raise GeneratedReportProvenanceError(f"unsafe provenance path: {rel_path!r}")
        if rel_path == ".local" or rel_path.startswith(".local/"):
            raise GeneratedReportProvenanceError(f"local cache cannot be a report source: {rel_path}")
        if not HEX64.fullmatch(str(digest)):
            raise GeneratedReportProvenanceError(f"invalid source hash for {rel_path}")
        lines.append(f"{rel_path}={digest}")
    return sha256_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def build_metadata(
    *,
    report_class: str,
    source_commit: str,
    source_hashes: Mapping[str, str],
    primary_source_paths: list[str],
    generation_time: str,
    task_count: int,
    renderer_path: str,
    renderer_sha256: str,
    strict: bool,
) -> dict[str, Any]:
    policy = report_policy(report_class)
    if not HEX40.fullmatch(source_commit):
        raise GeneratedReportProvenanceError("source_commit is not a full lowercase Git hash")
    if strict and source_commit == FIXTURE_SOURCE_COMMIT:
        raise GeneratedReportProvenanceError("live report cannot use the fixture source commit")
    if not isinstance(task_count, int) or task_count < 0:
        raise GeneratedReportProvenanceError("task_count must be a nonnegative integer")
    if strict and task_count == 0:
        raise GeneratedReportProvenanceError("live report task_count must be positive")
    if not RFC3339_Z.fullmatch(generation_time):
        if strict:
            raise GeneratedReportProvenanceError("generation_time must be a source-derived RFC3339 Z timestamp")
        generation_time = "1970-01-01T00:00:00Z"
    if not HEX64.fullmatch(renderer_sha256):
        raise GeneratedReportProvenanceError("renderer_sha256 is invalid")

    normalized_hashes = {str(path): str(digest) for path, digest in source_hashes.items()}
    normalized_hashes[POLICY_PATH] = POLICY_SHA256
    normalized_hashes[HELPER_PATH] = HELPER_SHA256
    normalized_hashes[renderer_path] = renderer_sha256
    manifest = source_manifest_sha256(normalized_hashes)

    primary_paths = sorted(set(primary_source_paths + [POLICY_PATH, HELPER_PATH, renderer_path]))
    missing_primary = [path for path in primary_paths if path not in normalized_hashes]
    if missing_primary:
        raise GeneratedReportProvenanceError(
            f"primary provenance paths missing from manifest: {missing_primary}"
        )
    primary_hashes = [
        {"path": path, "sha256": normalized_hashes[path]}
        for path in primary_paths
    ]
    return {
        "schema_id": SCHEMA_ID,
        "policy_id": str(POLICY["policy_id"]),
        "report_class": report_class,
        "source_commit": source_commit,
        "source_hashes": primary_hashes,
        "source_manifest_sha256": manifest,
        "source_path_count": str(len(normalized_hashes)),
        "generation_time": generation_time,
        "task_count": str(task_count),
        "maximum_commit_lag": str(policy["maximum_commit_lag"]),
        "freshness_status": "fresh_at_generation",
        "generated_view_is_authority": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def metadata_comment(metadata: Mapping[str, Any]) -> str:
    return f"{MARKER_PREFIX}{canonical_json(dict(metadata), compact=True)}{MARKER_SUFFIX}"


def parse_metadata_comment(text: str) -> dict[str, Any] | None:
    for line in text.splitlines():
        if line.startswith(MARKER_PREFIX) and line.endswith(MARKER_SUFFIX):
            payload = line[len(MARKER_PREFIX) : -len(MARKER_SUFFIX)]
            try:
                value = json.loads(payload)
            except json.JSONDecodeError as exc:
                raise GeneratedReportProvenanceError(
                    f"invalid generated-report provenance marker: {exc}"
                ) from exc
            if not isinstance(value, dict):
                raise GeneratedReportProvenanceError("provenance marker must contain a mapping")
            return value
    return None


def metadata_from_json_file(repo_root: Path, rel_path: str) -> dict[str, Any] | None:
    path = repo_root / rel_path
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GeneratedReportProvenanceError(f"invalid JSON report {rel_path}: {exc}") from exc
    if not isinstance(value, dict):
        return None
    metadata = value.get("report_provenance")
    return metadata if isinstance(metadata, dict) else None


def metadata_from_markdown_file(repo_root: Path, rel_path: str) -> dict[str, Any] | None:
    path = repo_root / rel_path
    if not path.is_file():
        return None
    return parse_metadata_comment(path.read_text(encoding="utf-8"))


def source_commit_from_metadata(metadata: Mapping[str, Any] | None, fallback: str) -> str:
    value = str((metadata or {}).get("source_commit", ""))
    return value if HEX40.fullmatch(value) else fallback


def markdown_provenance_lines(metadata: Mapping[str, Any]) -> list[str]:
    lines = [
        metadata_comment(metadata),
        "",
        "## Generated-Report Provenance",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Provenance schema | `{metadata['schema_id']}` |",
        f"| Freshness policy | `{metadata['policy_id']}` |",
        f"| Report class | `{metadata['report_class']}` |",
        f"| Source commit | `{metadata['source_commit']}` |",
        f"| Source-derived generation time | `{metadata['generation_time']}` |",
        f"| Tracked task count | {metadata['task_count']} |",
        f"| Exact source-path count | {metadata['source_path_count']} |",
        f"| Source manifest SHA-256 | `{metadata['source_manifest_sha256']}` |",
        f"| Maximum commit lag | {metadata['maximum_commit_lag']} |",
        f"| Freshness status at generation | `{metadata['freshness_status']}` |",
        f"| Generated view is authority | `{str(metadata['generated_view_is_authority']).lower()}` |",
        "",
        "Exact primary source hashes:",
        "",
    ]
    for item in metadata["source_hashes"]:
        lines.append(f"- `{item['path']}`: `{item['sha256']}`")
    lines.extend(
        [
            "",
            "Live validation recomputes the full source manifest and commit lag.",
            "Freshness PASS is operational evidence only; it is not physics proof",
            "or claim-promotion authority.",
            "",
        ]
    )
    return lines


def commit_lag(repo_root: Path, source_commit: str) -> tuple[int | None, str]:
    if source_commit == FIXTURE_SOURCE_COMMIT:
        return 0, "fixture"
    exists = subprocess.run(
        ["git", "-C", str(repo_root), "cat-file", "-e", f"{source_commit}^{{commit}}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if exists.returncode != 0:
        return None, "source_commit_missing"
    ancestor = subprocess.run(
        ["git", "-C", str(repo_root), "merge-base", "--is-ancestor", source_commit, "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        return None, "source_commit_not_ancestor"
    count = subprocess.run(
        ["git", "-C", str(repo_root), "rev-list", "--count", f"{source_commit}..HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        lag = int(count.stdout.strip())
    except ValueError:
        return None, "commit_lag_unavailable"
    return lag, "ok"


def validate_metadata(
    *,
    repo_root: Path,
    observed: Mapping[str, Any],
    expected: Mapping[str, Any],
    strict: bool,
) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    if dict(observed) != dict(expected):
        findings.append(
            {
                "finding_id": "generated_report_source_metadata_stale",
                "message": "Embedded provenance does not match current exact source bytes or metadata fields.",
            }
        )
    source_commit = str(observed.get("source_commit", ""))
    raw_maximum_lag = observed.get("maximum_commit_lag")
    try:
        maximum_lag = int(str(raw_maximum_lag))
    except ValueError:
        maximum_lag = None
    lag, lag_status = commit_lag(repo_root, source_commit)
    if strict and source_commit == FIXTURE_SOURCE_COMMIT:
        findings.append(
            {
                "finding_id": "generated_report_fixture_commit_forbidden",
                "message": "A live report embeds the fixture-only source commit.",
            }
        )
    if lag is None:
        findings.append(
            {
                "finding_id": "generated_report_source_commit_invalid",
                "message": f"Source commit could not be compared with HEAD: {lag_status}.",
            }
        )
    elif maximum_lag is None or lag > maximum_lag:
        findings.append(
            {
                "finding_id": "generated_report_commit_lag_exceeded",
                "message": f"Observed commit lag {lag} exceeds maximum {raw_maximum_lag}.",
            }
        )
    return {
        "report_class": observed.get("report_class", ""),
        "status": "PASS" if not findings else "FAIL",
        "source_commit": source_commit,
        "observed_commit_lag": lag,
        "maximum_commit_lag": maximum_lag,
        "source_manifest_sha256": observed.get("source_manifest_sha256", ""),
        "source_path_count": observed.get("source_path_count", 0),
        "task_count": observed.get("task_count", 0),
        "generation_time": observed.get("generation_time", ""),
        "findings": findings,
    }
