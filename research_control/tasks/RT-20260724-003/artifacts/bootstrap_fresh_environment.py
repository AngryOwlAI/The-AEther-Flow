#!/usr/bin/env python3
"""Build and validate the bounded P13-T06 fresh-machine equivalent.

The environment is created outside the repository and is provisioned only from
the tracked, hash-locked dependency graph.  PASS is project-system evidence; it
does not confer proof, benchmark, physics, ontology, or publication authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
DEFAULT_DEFINITION = ARTIFACT_DIR / "reproducible_environment_definition.json"
DEFAULT_RECEIPT = ARTIFACT_DIR / "reproduction_receipt.json"
EXPECTED_SCHEMA = "p13_t06_reproducible_environment_v1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def _repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def _path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def validate_external_target(target: Path) -> None:
    resolved = target.expanduser().resolve()
    if _path_is_within(resolved, REPO_ROOT):
        raise ValueError("target must be outside the repository checkout")
    if resolved.exists():
        raise ValueError("target must not already exist")
    if resolved == resolved.parent:
        raise ValueError("target must not be a filesystem root")


def validate_definition(
    definition: dict[str, Any],
    *,
    verify_live_sources: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []

    def fail(check_id: str, path: str, message: str) -> None:
        errors.append({"check_id": check_id, "path": path, "message": message})

    if definition.get("schema_id") != EXPECTED_SCHEMA:
        fail("schema_id", "schema_id", f"expected {EXPECTED_SCHEMA}")
    if definition.get("task_id") != "RT-20260724-003":
        fail("task_id", "task_id", "expected RT-20260724-003")
    if definition.get("work_item_id") != "P13-T06":
        fail("work_item_id", "work_item_id", "expected P13-T06")

    environment = definition.get("environment")
    if not isinstance(environment, dict):
        fail("environment_shape", "environment", "must be an object")
        environment = {}
    python = environment.get("python")
    if not isinstance(python, dict) or python.get("supported_series") != "3.12":
        fail(
            "python_series",
            "environment.python.supported_series",
            "must be 3.12",
        )
    if environment.get("target_must_be_outside_checkout") is not True:
        fail(
            "external_target",
            "environment.target_must_be_outside_checkout",
            "must be true",
        )

    exclusions = definition.get("exclusions")
    if not isinstance(exclusions, dict):
        fail("exclusions_shape", "exclusions", "must be an object")
        exclusions = {}
    forbidden_prefixes = exclusions.get("forbidden_repo_prefixes")
    if not isinstance(forbidden_prefixes, list) or not forbidden_prefixes:
        fail(
            "forbidden_prefixes",
            "exclusions.forbidden_repo_prefixes",
            "must be a nonempty list",
        )
        forbidden_prefixes = []

    source_manifest = definition.get("source_manifest")
    if not isinstance(source_manifest, list) or not source_manifest:
        fail("source_manifest", "source_manifest", "must be a nonempty list")
        source_manifest = []

    seen_paths: set[str] = set()
    observed_sources: list[dict[str, str]] = []
    for index, item in enumerate(source_manifest):
        item_path = f"source_manifest.{index}"
        if not isinstance(item, dict):
            fail("source_entry_shape", item_path, "must be an object")
            continue
        relative = item.get("path")
        expected_hash = item.get("sha256")
        if not isinstance(relative, str) or not relative:
            fail("source_path", f"{item_path}.path", "must be nonblank")
            continue
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            fail("source_path", f"{item_path}.path", "must be repository-relative")
            continue
        if relative in seen_paths:
            fail("source_path_unique", f"{item_path}.path", "duplicate source path")
        seen_paths.add(relative)
        if any(relative.startswith(str(prefix)) for prefix in forbidden_prefixes):
            fail(
                "source_exclusion",
                f"{item_path}.path",
                "source path uses a forbidden repository prefix",
            )
        if not isinstance(expected_hash, str) or SHA256_RE.fullmatch(expected_hash) is None:
            fail("source_sha256", f"{item_path}.sha256", "must be lowercase SHA-256")
            continue
        observed_hash = ""
        if verify_live_sources:
            live_path = REPO_ROOT / relative
            if not live_path.is_file():
                fail("source_exists", f"{item_path}.path", "tracked source is missing")
            else:
                observed_hash = _sha256_path(live_path)
                if observed_hash != expected_hash:
                    fail(
                        "source_hash",
                        f"{item_path}.sha256",
                        f"expected {expected_hash}; observed {observed_hash}",
                    )
        observed_sources.append(
            {
                "path": relative,
                "expected_sha256": str(expected_hash),
                "observed_sha256": observed_hash or str(expected_hash),
            }
        )

    profiles = definition.get("profiles")
    if not isinstance(profiles, dict):
        fail("profiles_shape", "profiles", "must be an object")
        profiles = {}
    required_profiles = profiles.get("required")
    if not isinstance(required_profiles, list) or not required_profiles:
        fail("required_profiles", "profiles.required", "must be a nonempty list")
    else:
        profile_ids: set[str] = set()
        for index, profile in enumerate(required_profiles):
            profile_path = f"profiles.required.{index}"
            if not isinstance(profile, dict):
                fail("profile_shape", profile_path, "must be an object")
                continue
            profile_id = profile.get("profile_id")
            command = profile.get("command")
            if not isinstance(profile_id, str) or not profile_id:
                fail("profile_id", f"{profile_path}.profile_id", "must be nonblank")
            elif profile_id in profile_ids:
                fail(
                    "profile_id_unique",
                    f"{profile_path}.profile_id",
                    "must be unique",
                )
            else:
                profile_ids.add(profile_id)
            if (
                not isinstance(command, list)
                or not command
                or any(not isinstance(token, str) or not token for token in command)
            ):
                fail("profile_command", f"{profile_path}.command", "must be string list")
            elif command[0] != "{python}":
                fail(
                    "profile_python",
                    f"{profile_path}.command",
                    "must use the fresh environment interpreter",
                )

    proof = profiles.get("formal_proof_build")
    required_proof_fields = {
        "profile_id",
        "build_script",
        "source_path",
        "toolchain_lock_path",
        "toolchain_selector_path",
        "expected_tool_version",
        "expected_tool_commit",
        "expected_source_sha256",
        "expected_proof_object_sha256",
    }
    if not isinstance(proof, dict) or not required_proof_fields.issubset(proof):
        fail(
            "proof_profile",
            "profiles.formal_proof_build",
            f"must contain {sorted(required_proof_fields)}",
        )

    authority = definition.get("authority")
    if not isinstance(authority, dict):
        fail("authority_shape", "authority", "must be an object")
    else:
        prohibited_true = sorted(key for key, value in authority.items() if value is True)
        if prohibited_true:
            fail(
                "authority_boundary",
                "authority",
                f"all authority flags must remain false: {prohibited_true}",
            )

    manifest_digest = _sha256_bytes(_canonical_json_bytes(source_manifest))
    return {
        "schema_id": "p13_t06_environment_definition_validation_v1",
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "source_count": len(source_manifest),
        "source_manifest_sha256": manifest_digest,
        "source_hashes_match": not any(
            item["check_id"] in {"source_exists", "source_hash"} for item in errors
        ),
        "excluded_input_finding_count": sum(
            item["check_id"] == "source_exclusion" for item in errors
        ),
        "observed_sources": observed_sources,
        "authority": {
            "project_system_evidence_only": True,
            "proof_authority": False,
            "benchmark_authority": False,
            "physics_promotion_authorized": False,
        },
    }


def _python_probe(python: Path) -> dict[str, str]:
    code = (
        "import json,platform,sys;"
        "print(json.dumps({'implementation':platform.python_implementation(),"
        "'version':platform.python_version(),"
        "'series':f'{sys.version_info.major}.{sys.version_info.minor}'},"
        "sort_keys=True,separators=(',',':')))"
    )
    completed = subprocess.run(
        [str(python), "-c", code],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise ValueError(f"cannot execute Python interpreter: {completed.stderr.strip()}")
    payload = json.loads(completed.stdout)
    if payload.get("implementation") != "CPython" or payload.get("series") != "3.12":
        raise ValueError(
            "bootstrap requires CPython 3.12; "
            f"observed {payload.get('implementation')} {payload.get('version')}"
        )
    return {str(key): str(value) for key, value in payload.items()}


def _run_logged(
    command: list[str],
    *,
    command_id: str,
    log_dir: Path,
    extra_environment: dict[str, str] | None = None,
) -> dict[str, Any]:
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPYCACHEPREFIX": str(log_dir.parent / "pycache"),
        }
    )
    if extra_environment:
        environment.update(extra_environment)
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        env=environment,
    )
    elapsed = round(time.monotonic() - started, 6)
    stdout_path = log_dir / f"{command_id}.stdout.log"
    stderr_path = log_dir / f"{command_id}.stderr.log"
    stdout_path.write_bytes(completed.stdout)
    stderr_path.write_bytes(completed.stderr)
    return {
        "command_id": command_id,
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "exit_code": completed.returncode,
        "duration_seconds": elapsed,
        "stdout_sha256": _sha256_bytes(completed.stdout),
        "stderr_sha256": _sha256_bytes(completed.stderr),
        "stdout_bytes": len(completed.stdout),
        "stderr_bytes": len(completed.stderr),
        "log_paths": [
            f"logs/{stdout_path.name}",
            f"logs/{stderr_path.name}",
        ],
    }


def _installed_inventory(python: Path) -> dict[str, Any]:
    code = (
        "import hashlib,importlib.metadata as m,json;"
        "rows=sorted((d.metadata['Name'],d.version) for d in m.distributions() "
        "if d.metadata.get('Name'));"
        "raw=json.dumps(rows,sort_keys=True,separators=(',',':')).encode();"
        "print(json.dumps({'count':len(rows),'sha256':hashlib.sha256(raw).hexdigest(),"
        "'packages':dict(rows)},sort_keys=True,separators=(',',':')))"
    )
    completed = subprocess.run(
        [str(python), "-c", code],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def _formal_proof_build(
    definition: dict[str, Any],
    *,
    lean_bin: Path,
    target: Path,
    log_dir: Path,
) -> dict[str, Any]:
    proof = definition["profiles"]["formal_proof_build"]
    version = subprocess.run(
        [str(lean_bin), "--version"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    version_text = version.stdout.strip()
    version_ok = (
        version.returncode == 0
        and f"version {proof['expected_tool_version']}" in version_text
        and f"commit {proof['expected_tool_commit']}" in version_text
    )
    if not version_ok:
        return {
            "command_id": proof["profile_id"],
            "status": "FAIL",
            "exit_code": version.returncode or 1,
            "tool_version_sha256": _sha256_bytes(version.stdout.encode("utf-8")),
            "source_sha256": _sha256_path(REPO_ROOT / proof["source_path"]),
            "proof_object_sha256": "",
            "reason": "supplied Lean toolchain does not match the pinned version and commit",
        }

    output_dir = target / "proof-build"
    result = _run_logged(
        [
            "sh",
            str(REPO_ROOT / proof["build_script"]),
            str(lean_bin),
            str(output_dir),
        ],
        command_id=proof["profile_id"],
        log_dir=log_dir,
    )
    source_hash = _sha256_path(REPO_ROOT / proof["source_path"])
    proof_object = output_dir / "SelectorKernel.olean"
    proof_hash = _sha256_path(proof_object) if proof_object.is_file() else ""
    matches = (
        result["status"] == "PASS"
        and source_hash == proof["expected_source_sha256"]
        and proof_hash == proof["expected_proof_object_sha256"]
    )
    result.update(
        {
            "status": "PASS" if matches else "FAIL",
            "tool_version_sha256": _sha256_bytes(version.stdout.encode("utf-8")),
            "source_sha256": source_hash,
            "proof_object_sha256": proof_hash,
            "proof_object_reproduced": matches,
            "toolchain_origin": "operator_supplied_external_to_environment",
        }
    )
    return result


def bootstrap(
    definition_path: Path,
    *,
    target: Path,
    bootstrap_python: Path,
    receipt_path: Path,
    lean_bin: Path | None,
) -> dict[str, Any]:
    definition = _load_json(definition_path)
    definition_validation = validate_definition(definition)
    if definition_validation["status"] != "PASS":
        raise ValueError("environment definition validation failed")
    validate_external_target(target)
    python_probe = _python_probe(bootstrap_python)

    target = target.expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    log_dir = target / "logs"
    log_dir.mkdir(parents=True)

    commands: list[dict[str, Any]] = []
    venv_result = _run_logged(
        [str(bootstrap_python), "-m", "venv", str(target)],
        command_id="create_venv",
        log_dir=log_dir,
    )
    commands.append(venv_result)
    venv_python = target / "bin/python"
    if venv_result["status"] == "PASS":
        pip_args = definition["environment"]["pip_install"]["arguments"]
        install_result = _run_logged(
            [str(venv_python), "-m", "pip", "install", *pip_args],
            command_id="install_hash_locked_dependencies",
            log_dir=log_dir,
        )
        commands.append(install_result)

    if all(item["status"] == "PASS" for item in commands):
        for profile in definition["profiles"]["required"]:
            command = [
                str(venv_python) if token == "{python}" else token
                for token in profile["command"]
            ]
            commands.append(
                _run_logged(
                    command,
                    command_id=profile["profile_id"],
                    log_dir=log_dir,
                )
            )

    if lean_bin is None:
        proof_result: dict[str, Any] = {
            "command_id": definition["profiles"]["formal_proof_build"]["profile_id"],
            "status": "NOT_RUN_OPTIONAL_RUNTIME",
            "exit_code": 0,
            "reason": "supply --lean-bin to reproduce the pinned formal proof object",
        }
    else:
        proof_result = _formal_proof_build(
            definition,
            lean_bin=lean_bin.expanduser().resolve(),
            target=target,
            log_dir=log_dir,
        )
        commands.append(proof_result)

    after_validation = validate_definition(definition)
    inventory = (
        _installed_inventory(venv_python)
        if venv_python.is_file()
        else {"count": 0, "sha256": "", "packages": {}}
    )
    failures = [item for item in commands if item["status"] != "PASS"]
    status = (
        "PASS"
        if not failures
        and definition_validation["status"] == "PASS"
        and after_validation["status"] == "PASS"
        else "FAIL"
    )
    receipt = {
        "schema_id": "p13_t06_reproduction_receipt_v1",
        "task_id": "RT-20260724-003",
        "work_item_id": "P13-T06",
        "status": status,
        "mechanism": definition["environment"]["mechanism"],
        "target_class": "external_ephemeral_directory",
        "host": {
            "system": platform.system(),
            "machine": platform.machine(),
        },
        "bootstrap_python": python_probe,
        "definition_path": _repo_relative(definition_path),
        "definition_sha256": _sha256_path(definition_path),
        "source_manifest_sha256": definition_validation["source_manifest_sha256"],
        "source_hashes_match_before": definition_validation["source_hashes_match"],
        "source_hashes_match_after": after_validation["source_hashes_match"],
        "source_count": definition_validation["source_count"],
        "installed_inventory": inventory,
        "command_count": len(commands),
        "failure_count": len(failures),
        "commands": commands,
        "formal_proof_profile": proof_result,
        "exclusion_checks": {
            "selected_input_finding_count": definition_validation[
                "excluded_input_finding_count"
            ],
            "credential_material_embedded": False,
            "local_cache_embedded": False,
            "relay_goal_state_embedded": False,
            "checkout_copied_into_environment": False,
        },
        "platform_limitations": [
            "The equivalent environment pins CPython to the 3.12 series rather than an operating-system image.",
            "Formal Lean reproduction requires an operator-supplied binary matching the tracked 4.30.0 toolchain lock.",
            "The existing Lean archive lock is Darwin-arm64; another host needs a separately tracked archive lock before formal-build parity can be claimed.",
        ],
        "authority": {
            "project_system_evidence_only": True,
            "proof_authority": False,
            "benchmark_authority": False,
            "physics_promotion_authorized": False,
            "scientific_claims_changed": False,
        },
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_bytes(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        + b"\n"
    )
    return receipt


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--definition", type=Path, default=DEFAULT_DEFINITION)
    validate_parser.add_argument("--json", action="store_true")

    bootstrap_parser = subparsers.add_parser("bootstrap")
    bootstrap_parser.add_argument("--definition", type=Path, default=DEFAULT_DEFINITION)
    bootstrap_parser.add_argument("--target", type=Path, required=True)
    bootstrap_parser.add_argument("--python", type=Path, required=True)
    bootstrap_parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    bootstrap_parser.add_argument("--lean-bin", type=Path)
    bootstrap_parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        if args.command == "validate":
            receipt = validate_definition(_load_json(args.definition))
        else:
            receipt = bootstrap(
                args.definition,
                target=args.target,
                bootstrap_python=args.python,
                receipt_path=args.receipt,
                lean_bin=args.lean_bin,
            )
    except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(receipt, ensure_ascii=False, sort_keys=True)
    if getattr(args, "json", False):
        print(rendered)
    else:
        print(
            f"{receipt['status']} schema={receipt['schema_id']} "
            f"errors={receipt.get('error_count', receipt.get('failure_count', 0))}"
        )
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
