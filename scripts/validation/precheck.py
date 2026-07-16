#!/usr/bin/env python3
"""Run cheap read-only working-tree checks before governed checkpointing.

Receipts from this command are working-tree editing evidence only. They cannot
be reused as staged PASS evidence or satisfy repository acceptance.
"""

from __future__ import annotations

import argparse
import ast
import csv
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import time
import tomllib
from typing import Callable, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.project_control.classify_project_changes import (  # noqa: E402
    changed_paths_from_git,
    classify_paths,
)
from scripts.project_control.validate_claim_language import (  # noqa: E402
    claim_language_gate_paths,
)
from scripts.research_control.strict_yaml import load as load_strict_yaml  # noqa: E402
from scripts.validation.plan import load_manifest  # noqa: E402
from scripts.validation.profiles import ProfileError, resolve_profile  # noqa: E402


DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
DEFAULT_RECEIPT_ROOT = Path(".local/validation-receipts")
TARGET_SECONDS = (5.0, 30.0)
HARD_GUARD_SECONDS = 45
GATES = (
    "classify_changes",
    "path_policy_sanity",
    "syntax_schema",
    "changed_claim_language",
    "git_diff_check",
    "affected_fast_tests",
    "shadow_legacy_equivalence",
)
DIRECT_MANIFEST_GATES = {"classify_changes", "git_diff_check"}
CAPABILITY_GATES = {
    "path_policy_sanity": "classify_changes",
    "syntax_schema": "syntax_compilation",
    "changed_claim_language": "changed_claim_validation",
    "affected_fast_tests": "affected_unit_tests",
}
TEST_OVERRIDES = {
    "scripts/project_control/classify_project_changes.py": (
        "tests/test_project_change_classifier.py"
    )
}


class PrecheckError(RuntimeError):
    """A fail-closed precheck configuration error."""


@dataclass(frozen=True, slots=True)
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str


Runner = Callable[..., CommandResult]
Classifier = Callable[..., dict[str, object]]


def _run(
    command: tuple[str, ...],
    *,
    cwd: Path,
    timeout_seconds: int,
    env: dict[str, str] | None = None,
) -> CommandResult:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        return CommandResult(completed.returncode, completed.stdout, completed.stderr)
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout if isinstance(error.stdout, str) else ""
        stderr = error.stderr if isinstance(error.stderr, str) else ""
        return CommandResult(124, stdout, stderr or "command timed out")
    except OSError as error:
        return CommandResult(127, "", str(error))


def _finding(gate: str, code: str, message: str, path: str = "") -> dict[str, str]:
    digest = hashlib.sha256(f"{gate}\0{path}\0{code}".encode()).hexdigest()[:12]
    return {
        "finding_id": f"PRECHECK-{gate.replace('_', '-').upper()}-{digest.upper()}",
        "code": code,
        "message": " ".join(message.split()),
        "path": path,
    }


def _result(
    gate: str,
    *,
    status: str = "PASS",
    exit_code: int = 0,
    findings: Iterable[dict[str, str]] = (),
    stdout: str = "",
    stderr: str = "",
    details: Mapping[str, object] | None = None,
    duration: float = 0.0,
    subprocesses: int = 0,
) -> dict[str, object]:
    ordered = sorted(findings, key=lambda item: (item["path"], item["code"]))
    return {
        "gate_id": gate,
        "status": status,
        "exit_code": exit_code,
        "duration_seconds": round(duration, 6),
        "subprocess_count": subprocesses,
        "finding_count": len(ordered),
        "findings": ordered,
        "stdout": stdout,
        "stderr": stderr,
        "details": dict(details or {}),
    }


def _skip(gate: str, reason: str) -> dict[str, object]:
    return _result(gate, status="SKIP_NOT_APPLICABLE", details={"reason": reason})


def _normalize(paths: Iterable[str]) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    valid: set[str] = set()
    findings: list[dict[str, str]] = []
    for raw in paths:
        path = str(raw)
        pure = PurePosixPath(path)
        invalid = (
            not path
            or path.startswith("/")
            or "\\" in path
            or "\0" in path
            or any(part in {"", ".", ".."} for part in pure.parts)
            or pure.as_posix() != path
        )
        if invalid:
            findings.append(
                _finding(
                    "path_policy_sanity",
                    "invalid_path",
                    "path must be normalized and repository-relative",
                    path,
                )
            )
        else:
            valid.add(path)
    return tuple(sorted(valid)), findings


def _classify(
    repo: Path, paths: tuple[str, ...], classifier: Classifier
) -> tuple[dict[str, object], dict[str, object] | None]:
    started = time.monotonic()
    try:
        payload = classifier(paths, registry_root=repo)
        if not isinstance(payload, dict):
            raise TypeError("classifier did not return an object")
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        finding = _finding("classify_changes", "classification_error", str(error))
        return (
            _result(
                "classify_changes",
                status="BLOCKED_CONFIGURATION",
                exit_code=2,
                findings=[finding],
                duration=time.monotonic() - started,
            ),
            None,
        )
    details = {
        "legacy_result_authoritative": True,
        "changed_path_count": len(payload.get("changed_paths", [])),
        "recommended_validation_profile": payload.get(
            "recommended_validation_profile", ""
        ),
        "path_family_tags": payload.get("path_family_tags", []),
    }
    return _result(
        "classify_changes", details=details, duration=time.monotonic() - started
    ), payload


def _path_policy(
    classification: Mapping[str, object], invalid: Sequence[dict[str, str]]
) -> dict[str, object]:
    findings = list(invalid)
    blocked = [str(path) for path in classification.get("blocked_paths", [])]
    unknown: set[str] = set()
    for detail in classification.get("path_family_details", []):
        if isinstance(detail, dict) and "unknown_governed_path" in detail.get("tags", []):
            unknown.add(str(detail.get("path", "")))
    findings.extend(
        _finding(
            "path_policy_sanity",
            "blocked_path",
            "classifier marks this governed path as blocked",
            path,
        )
        for path in blocked
    )
    findings.extend(
        _finding(
            "path_policy_sanity",
            "unknown_governed_path",
            "unknown governed paths require the full fail-closed route",
            path,
        )
        for path in sorted(unknown)
        if path
    )
    return _result(
        "path_policy_sanity",
        status="FAIL" if findings else "PASS",
        exit_code=1 if findings else 0,
        findings=findings,
        details={"blocked_paths": sorted(blocked), "unknown_paths": sorted(unknown)},
    )


def _parse_structured(path: Path, relative: str) -> None:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix == ".py":
        ast.parse(text, filename=relative)
    elif suffix == ".json" or (
        suffix in {".yaml", ".yml"} and text.lstrip().startswith(("{", "["))
    ):
        json.loads(text)
    elif suffix in {".yaml", ".yml"}:
        if relative.startswith(("research_control/", ".agents/")):
            load_strict_yaml(path)
        else:
            try:
                import yaml  # type: ignore[import-not-found]
            except ImportError as error:
                raise ValueError("PyYAML is required for general YAML checks") from error
            try:
                yaml.safe_load(text)
            except yaml.YAMLError as error:
                raise ValueError(str(error)) from error
    elif suffix == ".toml":
        tomllib.loads(text)
    elif suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or any(not name for name in reader.fieldnames):
                raise ValueError("CSV header is missing or has a blank column")
            for line, row in enumerate(reader, 2):
                if None in row or any(value is None for value in row.values()):
                    raise ValueError(f"CSV row {line} does not match its header")


def _syntax(repo: Path, paths: Sequence[str]) -> dict[str, object]:
    started = time.monotonic()
    suffixes = {".py", ".json", ".yaml", ".yml", ".toml", ".csv"}
    checked: list[str] = []
    findings: list[dict[str, str]] = []
    for relative in paths:
        path = repo / relative
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        checked.append(relative)
        try:
            _parse_structured(path, relative)
        except (OSError, SyntaxError, UnicodeDecodeError, ValueError) as error:
            findings.append(
                _finding(
                    "syntax_schema", "syntax_or_schema_error", str(error), relative
                )
            )
    return _result(
        "syntax_schema",
        status="FAIL" if findings else "PASS",
        exit_code=1 if findings else 0,
        findings=findings,
        details={"checked_paths": checked, "checked_path_count": len(checked)},
        duration=time.monotonic() - started,
    )


def _claims(repo: Path, paths: Sequence[str], runner: Runner) -> dict[str, object]:
    started = time.monotonic()
    selected = claim_language_gate_paths(paths, repo_root=repo)
    details: dict[str, object] = {
        "selected_paths": selected,
        "legacy_result_authoritative": True,
    }
    if not selected:
        return _result(
            "changed_claim_language",
            details=details,
            duration=time.monotonic() - started,
        )
    command = (
        sys.executable,
        str(REPO_ROOT / "scripts/project_control/validate_claim_language.py"),
        "--repo-root",
        str(repo),
        "--json",
        "--paths",
        *selected,
    )
    child = runner(command, cwd=repo, timeout_seconds=HARD_GUARD_SECONDS)
    try:
        parsed = json.loads(child.stdout) if child.stdout.strip() else {}
        if not isinstance(parsed, dict):
            raise ValueError("legacy claim result is not an object")
    except (json.JSONDecodeError, ValueError) as error:
        finding = _finding("changed_claim_language", "legacy_output_error", str(error))
        return _result(
            "changed_claim_language",
            status="BLOCKED_CONFIGURATION",
            exit_code=2,
            findings=[finding],
            stdout=child.stdout,
            stderr=child.stderr,
            details=details,
            duration=time.monotonic() - started,
            subprocesses=1,
        )
    details.update(
        hard_fail_count=parsed.get("hard_fail_count", 0),
        warning_count=parsed.get("warning_count", 0),
    )
    failed = child.exit_code != 0 or parsed.get("status") != "PASS"
    findings = [
        _finding(
            "changed_claim_language",
            str(item.get("class_id", "claim_language_failure")),
            f"legacy claim-language finding at line {item.get('line', '?')}",
            str(item.get("path", "")),
        )
        for item in parsed.get("findings", [])
        if isinstance(item, dict)
    ] if failed else []
    if failed and not findings:
        findings.append(
            _finding(
                "changed_claim_language",
                "legacy_claim_validator_failed",
                child.stderr or f"legacy claim validator exited {child.exit_code}",
            )
        )
    return _result(
        "changed_claim_language",
        status="FAIL" if failed else "PASS",
        exit_code=child.exit_code or (1 if failed else 0),
        findings=findings,
        stdout=child.stdout,
        stderr=child.stderr,
        details=details,
        duration=time.monotonic() - started,
        subprocesses=1,
    )


def _whitespace(repo: Path, paths: Sequence[str], runner: Runner) -> dict[str, object]:
    started = time.monotonic()
    diff = runner(
        ("git", "diff", "--check", "HEAD", "--"), cwd=repo, timeout_seconds=15
    )
    untracked = runner(
        ("git", "ls-files", "--others", "--exclude-standard", "-z"),
        cwd=repo,
        timeout_seconds=15,
    )
    selected_untracked = sorted(set(paths) & set(untracked.stdout.split("\0")))
    findings: list[dict[str, str]] = []
    if diff.exit_code:
        findings.append(
            _finding(
                "git_diff_check",
                "git_diff_check_failed",
                diff.stdout or diff.stderr or f"git diff --check exited {diff.exit_code}",
            )
        )
    for relative in selected_untracked:
        path = repo / relative
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for line_number, line in enumerate(lines, 1):
            if line.endswith((" ", "\t")):
                findings.append(
                    _finding(
                        "git_diff_check",
                        "untracked_trailing_whitespace",
                        f"untracked line {line_number} has trailing whitespace",
                        relative,
                    )
                )
    blocked = untracked.exit_code != 0
    if blocked:
        findings.append(
            _finding(
                "git_diff_check",
                "untracked_query_failed",
                untracked.stderr or f"git ls-files exited {untracked.exit_code}",
            )
        )
    return _result(
        "git_diff_check",
        status="BLOCKED_CONFIGURATION" if blocked else ("FAIL" if findings else "PASS"),
        exit_code=2 if blocked else (diff.exit_code or (1 if findings else 0)),
        findings=findings,
        stdout=diff.stdout,
        stderr="\n".join(part for part in (diff.stderr, untracked.stderr) if part),
        details={
            "legacy_result_authoritative": True,
            "untracked_paths_checked": selected_untracked,
        },
        duration=time.monotonic() - started,
        subprocesses=2,
    )


def select_affected_tests(repo: Path, paths: Sequence[str]) -> tuple[str, ...]:
    """Return only directly mapped, present fast unittest paths."""

    selected: set[str] = set()
    for relative in paths:
        candidate = TEST_OVERRIDES.get(relative, "")
        if relative.startswith("tests/test_") and relative.endswith(".py"):
            candidate = relative
        elif relative.startswith("scripts/validation/") and relative.endswith(".py"):
            candidate = f"tests/test_validation_{Path(relative).stem}.py"
        elif relative.startswith(("scripts/project_control/", "scripts/research_control/")) and relative.endswith(".py"):
            candidate = candidate or f"tests/test_{Path(relative).stem}.py"
        elif relative.startswith(".codex/skills/") and "/scripts/" in relative and relative.endswith(".py"):
            candidate = f"tests/test_{Path(relative).stem}.py"
        if candidate and (repo / candidate).is_file():
            selected.add(candidate)
    return tuple(sorted(selected))


def _tests(repo: Path, paths: Sequence[str], runner: Runner) -> dict[str, object]:
    selected = select_affected_tests(repo, paths)
    if not selected:
        return _skip("affected_fast_tests", "no directly affected fast tests")
    started = time.monotonic()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    child = runner(
        (sys.executable, "-m", "unittest", *selected),
        cwd=repo,
        timeout_seconds=HARD_GUARD_SECONDS,
        env=env,
    )
    findings = [] if child.exit_code == 0 else [
        _finding(
            "affected_fast_tests",
            "affected_tests_failed",
            child.stderr or child.stdout or f"unittest exited {child.exit_code}",
        )
    ]
    return _result(
        "affected_fast_tests",
        status="FAIL" if findings else "PASS",
        exit_code=child.exit_code,
        findings=findings,
        stdout=child.stdout,
        stderr=child.stderr,
        details={"selected_tests": list(selected), "full_test_suite_selected": False},
        duration=time.monotonic() - started,
        subprocesses=1,
    )


def _shadow_comparison(
    manifest: Mapping[str, object], classification: Mapping[str, object]
) -> dict[str, object]:
    """Compare the fast shadow plan with this precheck's read-only gate set."""

    try:
        resolution = resolve_profile(
            manifest,
            classification,
            requested_profile="fast",
            scopes=("working",),
            shadow=True,
        )
    except (ProfileError, TypeError, ValueError) as error:
        return {
            "status": "BLOCKED_CONFIGURATION",
            "planner_gate_ids": [],
            "legacy_read_only_gate_ids": sorted(DIRECT_MANIFEST_GATES),
            "excluded_gate_ids": [],
            "capability_gate_explanations": [],
            "unexplained_mismatch_gate_ids": [],
            "configuration_error": str(error),
        }
    gates = {
        str(gate["gate_id"]): gate
        for gate in manifest.get("gates", [])
        if isinstance(gate, dict) and gate.get("gate_id")
    }
    selected: list[str] = []
    excluded: list[dict[str, str]] = []
    mismatch: set[str] = set()
    for gate_id in resolution.plan.selected_gate_ids:
        gate = gates.get(gate_id)
        if gate is None or gate.get("severity") != "blocking":
            continue
        selected.append(gate_id)
        valid_legacy = (
            str(gate.get("adapter", "")).startswith("legacy:")
            and bool(gate.get("command_compatibility"))
        )
        if not valid_legacy:
            mismatch.add(gate_id)
        elif gate.get("mutating") is True:
            excluded.append(
                {"gate_id": gate_id, "reason": "precheck_forbids_mutating_gates"}
            )
        elif gate_id not in DIRECT_MANIFEST_GATES:
            mismatch.add(gate_id)
    mismatch.update(DIRECT_MANIFEST_GATES - set(selected))
    if resolution.effective_profile != "fast":
        mismatch.add(f"effective_profile:{resolution.effective_profile}")
    if manifest.get("execution_authority") != "legacy":
        mismatch.add("execution_authority:not_legacy")
    return {
        "status": "PASS" if not mismatch else "BLOCKED_CONFIGURATION",
        "planner_gate_ids": sorted(selected),
        "legacy_read_only_gate_ids": sorted(DIRECT_MANIFEST_GATES),
        "excluded_gate_ids": sorted(excluded, key=lambda item: item["gate_id"]),
        "capability_gate_explanations": [
            {
                "gate_id": gate,
                "profile_capability": capability,
                "reason": "fast_profile_capability_pending_manifest_gate",
            }
            for gate, capability in sorted(CAPABILITY_GATES.items())
        ],
        "unexplained_mismatch_gate_ids": sorted(mismatch),
        "effective_profile": resolution.effective_profile,
        "legacy_execution_authority": True,
    }


def _shadow(
    manifest: Mapping[str, object], classification: Mapping[str, object]
) -> dict[str, object]:
    started = time.monotonic()
    comparison = _shadow_comparison(manifest, classification)
    passed = comparison["status"] == "PASS"
    findings = [] if passed else [
        _finding(
            "shadow_legacy_equivalence",
            "unexplained_shadow_mismatch",
            json.dumps(comparison.get("unexplained_mismatch_gate_ids", [])),
        )
    ]
    return _result(
        "shadow_legacy_equivalence",
        status="PASS" if passed else "BLOCKED_CONFIGURATION",
        exit_code=0 if passed else 2,
        findings=findings,
        details=comparison,
        duration=time.monotonic() - started,
    )


def _git(repo: Path, *command: str) -> bytes:
    child = subprocess.run(command, cwd=repo, capture_output=True, check=False)
    if child.returncode:
        raise PrecheckError(child.stderr.decode(errors="replace").strip() or "git failed")
    return child.stdout


def working_tree_hash(repo: Path) -> str:
    """Hash HEAD, tracked changes, path state, and untracked contents."""

    digest = hashlib.sha256()
    head = _git(repo, "git", "rev-parse", "HEAD")
    status = _git(repo, "git", "status", "--porcelain=v1", "-z")
    diff = _git(repo, "git", "diff", "--binary", "HEAD", "--")
    untracked = _git(repo, "git", "ls-files", "--others", "--exclude-standard", "-z")
    for label, payload in ((b"head", head), (b"status", status), (b"diff", diff), (b"untracked", untracked)):
        digest.update(label + b"\0" + payload)
    for raw in sorted(value for value in untracked.split(b"\0") if value):
        path = repo / raw.decode(errors="surrogateescape")
        if path.is_file():
            digest.update(b"content\0" + raw + b"\0" + path.read_bytes())
    return f"working-sha256:{digest.hexdigest()}"


def _requested(only_gate: str | None) -> tuple[str, ...]:
    if only_gate is None:
        return GATES
    if only_gate == "classify_changes":
        return (only_gate,)
    if only_gate == "path_policy_sanity":
        return ("classify_changes", only_gate)
    return ("classify_changes", "path_policy_sanity", only_gate)


def run_precheck(
    repo_root: Path,
    paths: Sequence[str],
    *,
    only_gate: str | None = None,
    manifest: Mapping[str, object] | None = None,
    command_runner: Runner = _run,
    classifier: Classifier = classify_paths,
    tree_hash: str | None = None,
) -> dict[str, object]:
    """Execute one bounded precheck and return its complete local receipt."""

    if only_gate is not None and only_gate not in GATES:
        raise PrecheckError(f"unsupported precheck gate: {only_gate}")
    repo = repo_root.resolve()
    started = time.monotonic()
    selected, invalid = _normalize(paths)
    selected_manifest = manifest or load_manifest(DEFAULT_MANIFEST)
    identity = tree_hash or working_tree_hash(repo)
    if not identity.startswith("working-sha256:"):
        raise PrecheckError("precheck requires a working-sha256 identity")
    requested = _requested(only_gate)
    results: list[dict[str, object]] = []
    classification_gate, classification = _classify(repo, selected, classifier)
    results.append(classification_gate)
    if classification is None:
        results.extend(_skip(gate, "classification_failed") for gate in requested[1:])
    else:
        path_gate = None
        if "path_policy_sanity" in requested:
            path_gate = _path_policy(classification, invalid)
            results.append(path_gate)
        path_failed = bool(path_gate and path_gate["status"] != "PASS")
        cheap_failed = path_failed
        for gate in requested[2:]:
            if path_failed:
                current = _skip(gate, "path_policy_failed")
            elif gate == "syntax_schema":
                current = _syntax(repo, selected)
            elif gate == "changed_claim_language":
                current = _claims(repo, selected, command_runner)
            elif gate == "git_diff_check":
                current = _whitespace(repo, selected, command_runner)
            elif gate == "affected_fast_tests":
                current = (
                    _skip(gate, "earlier_fast_gate_failed")
                    if cheap_failed
                    else _tests(repo, selected, command_runner)
                )
            elif gate == "shadow_legacy_equivalence":
                current = _shadow(selected_manifest, classification)
            else:
                raise PrecheckError(f"unhandled precheck gate: {gate}")
            results.append(current)
            if gate in {"syntax_schema", "changed_claim_language", "git_diff_check"}:
                cheap_failed = cheap_failed or current["status"] != "PASS"
    statuses = {str(result["status"]) for result in results}
    status, exit_code = (
        ("BLOCKED_CONFIGURATION", 2)
        if "BLOCKED_CONFIGURATION" in statuses
        else ("FAIL", 1)
        if "FAIL" in statuses
        else ("PASS", 0)
    )
    duration = time.monotonic() - started
    assessment = (
        "below_target_range"
        if duration < TARGET_SECONDS[0]
        else "within_target_range"
        if duration <= TARGET_SECONDS[1]
        else "above_target_range"
    )
    run_digest = hashlib.sha256(f"{identity}\0{only_gate or 'all'}".encode()).hexdigest()
    return {
        "schema_id": "validation_working_precheck_receipt_v1",
        "run_id": f"WORKING-PRECHECK-{run_digest[:16].upper()}",
        "status": status,
        "exit_code": exit_code,
        "scope": "working",
        "tree_hash": identity,
        "requested_gate": only_gate or "all",
        "selected_paths": list(selected),
        "gate_results": results,
        "counts": {
            "gate_count": len(results),
            "failed_gate_count": sum(
                item["status"] in {"FAIL", "BLOCKED_CONFIGURATION"} for item in results
            ),
            "finding_count": sum(int(item["finding_count"]) for item in results),
            "selected_path_count": len(selected),
            "subprocess_count": sum(int(item["subprocess_count"]) for item in results),
            "registry_parse_count": 3 if classifier is classify_paths else 0,
            "graph_build_count": 0,
            "cache_hit_count": 0,
            "cache_miss_count": 0,
            "console_output_bytes": 0,
        },
        "performance": {
            "budget_id": "V19-PERF-AFFECTED-001",
            "duration_seconds": round(duration, 6),
            "target_seconds": list(TARGET_SECONDS),
            "hard_guard_seconds": HARD_GUARD_SECONDS,
            "assessment": assessment,
            "within_hard_guard": duration <= HARD_GUARD_SECONDS,
            "provisional_nonblocking": True,
        },
        "evidence_reuse": {
            "checkpoint_acceptance": False,
            "staged_pass_reusable": False,
            "reason": "working-tree evidence is not final staged-tree acceptance",
        },
        "mutation_boundary": {
            "tracked_state_mutation": False,
            "generator_execution": False,
            "local_receipt_write": True,
        },
        "authority": {
            "operational_validation_only": True,
            "legacy_results_authoritative": True,
            "repository_acceptance": False,
            "human_gate": False,
            "physics_claim": False,
            "ontology": False,
            "benchmark": False,
            "proof": False,
            "gate_chair": False,
        },
    }


def receipt_path(receipt: Mapping[str, object], root: Path) -> Path:
    tree = str(receipt["tree_hash"]).replace(":", "-")
    return root / tree / str(receipt["run_id"]) / "full.json"


def write_receipt(receipt: dict[str, object], root: Path) -> Path:
    path = receipt_path(receipt, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as handle:
            temporary = Path(handle.name)
            json.dump(receipt, handle, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return path


def _shown_findings(receipt: Mapping[str, object]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for gate in receipt["gate_results"]:  # type: ignore[index]
        if isinstance(gate, dict):
            findings.extend(
                {"gate_id": gate["gate_id"], **item}
                for item in gate.get("findings", [])
                if isinstance(item, dict)
            )
    return findings[:5]


def render_json_summary(receipt: Mapping[str, object], full_receipt: Path) -> str:
    payload = {
        "schema_id": "validation_working_precheck_summary_v1",
        "run_id": receipt["run_id"],
        "status": receipt["status"],
        "exit_code": receipt["exit_code"],
        "scope": "working",
        "tree_hash": receipt["tree_hash"],
        "requested_gate": receipt["requested_gate"],
        "counts": receipt["counts"],
        "gate_statuses": [
            {"gate_id": gate["gate_id"], "status": gate["status"]}
            for gate in receipt["gate_results"]  # type: ignore[index]
            if isinstance(gate, dict)
        ],
        "shown_findings": _shown_findings(receipt),
        "checkpoint_acceptance": False,
        "staged_pass_reusable": False,
        "full_receipt": str(full_receipt),
        "authority": "operational_validation_only",
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def render_summary(receipt: Mapping[str, object], full_receipt: Path) -> str:
    counts = receipt["counts"]
    assert isinstance(counts, dict)
    lines = [
        f"{receipt['status']} scope=working gates={counts['gate_count']} "
        f"findings={counts['finding_count']} checkpoint_acceptance=false "
        f"staged_pass_reusable=false receipt={full_receipt}"
    ]
    lines.extend(
        f"ERROR {item['gate_id']} {item['finding_id']} {item['code']}: {item['message']}"
        for item in _shown_findings(receipt)
    )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit compact summary JSON")
    parser.add_argument("--paths", nargs="*", help="explicit working-tree paths")
    parser.add_argument("--gate", choices=GATES, help="rerun one gate and prerequisites")
    parser.add_argument(
        "--receipt-root",
        default=DEFAULT_RECEIPT_ROOT.as_posix(),
        help="ignored local full-receipt root",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        paths = args.paths if args.paths is not None else changed_paths_from_git()
        receipt = run_precheck(REPO_ROOT, paths, only_gate=args.gate)
        root = Path(args.receipt_root)
        root = root if root.is_absolute() else REPO_ROOT / root
        path = receipt_path(receipt, root)
        render = render_json_summary if args.json else render_summary
        counts = receipt["counts"]
        assert isinstance(counts, dict)
        for _ in range(4):
            output = render(receipt, path)
            measured = len(output.encode())
            if counts["console_output_bytes"] == measured:
                break
            counts["console_output_bytes"] = measured
        output = render(receipt, path)
        write_receipt(receipt, root)
    except (OSError, PrecheckError, ProfileError, ValueError) as error:
        print(
            f"BLOCKED_CONFIGURATION precheck_error: {' '.join(str(error).split())}",
            file=sys.stderr,
        )
        return 2
    (sys.stdout if receipt["exit_code"] == 0 else sys.stderr).write(output)
    return int(receipt["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
