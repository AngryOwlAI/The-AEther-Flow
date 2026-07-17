#!/usr/bin/env python3
"""Validate P9-T01 raw-input injection and minimal fixture equivalence."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control import strict_yaml  # noqa: E402
from scripts.research_control.support_formalization import (  # noqa: E402
    validate_traceability_registry as v1_validator,
)
from scripts.research_control.support_formalization import (  # noqa: E402
    validate_traceability_registry_v18 as v18_validator,
)
from scripts.research_control.support_formalization.traceability_io import (  # noqa: E402
    TraceabilityInputs,
)
from tests.support.traceability_fixture_builder import (  # noqa: E402
    PNF_REGISTRY_PATH,
    V1_REGISTRY_PATH,
    V18_REGISTRY_PATH,
    TraceabilityFixtureBuilder,
    dump_fixture_yaml,
)


REPORT_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260717-013"
    / "artifacts"
    / "traceability_injection_equivalence.json"
)


def timed(call: Callable[[], Any]) -> tuple[Any, float]:
    started = time.perf_counter()
    return call(), time.perf_counter() - started


def capture_error(call: Callable[[], Any]) -> dict[str, str]:
    try:
        call()
    except (v1_validator.TraceabilityRegistryError, v18_validator.V18TraceabilityError) as exc:
        return {"class": type(exc).__name__, "message": str(exc)}
    raise AssertionError("expected validation failure")


def read_pnf_rows(root: Path) -> dict[str, dict[str, str]]:
    with (root / PNF_REGISTRY_PATH).open(newline="", encoding="utf-8") as handle:
        return {
            row["proof_normal_form_row_id"]: {
                key: value or "" for key, value in row.items()
            }
            for row in csv.DictReader(handle)
        }


def instrumented_inputs(
    root: Path,
    registry: dict[str, Any],
    *,
    pnf_rows: dict[str, dict[str, str]] | None = None,
) -> tuple[TraceabilityInputs, dict[str, Any]]:
    evidence: dict[str, Any] = {"file_reads": [], "hash_calls": 0}

    def load(path: Path) -> bytes:
        evidence["file_reads"].append(path.relative_to(root).as_posix())
        return path.read_bytes()

    def hash_bytes(payload: bytes) -> str:
        evidence["hash_calls"] += 1
        return hashlib.sha256(payload).hexdigest()

    return (
        TraceabilityInputs(
            repo_root=root,
            registry=registry,
            file_loader=load,
            hash_provider=hash_bytes,
            proof_normal_form_rows=pnf_rows,
        ),
        evidence,
    )


def write_registry(root: Path, rel_path: str, registry: dict[str, Any]) -> None:
    path = root / rel_path
    path.write_text(dump_fixture_yaml(registry), encoding="utf-8")


def compare_v1_failure(
    base_root: Path,
    base_registry: dict[str, Any],
    case_id: str,
    mutate: Callable[[dict[str, Any]], None],
    expected_message: str,
) -> dict[str, Any]:
    registry = copy.deepcopy(base_registry)
    mutate(registry)
    with tempfile.TemporaryDirectory() as temp_dir:
        disk_root = Path(temp_dir) / "repo"
        shutil.copytree(base_root, disk_root)
        write_registry(disk_root, V1_REGISTRY_PATH, registry)
        default_error = capture_error(
            lambda: v1_validator.validate_registry(repo_root=disk_root)
        )
    injected_error = capture_error(
        lambda: v1_validator.validate_registry(
            dependencies=TraceabilityInputs(
                repo_root=base_root,
                registry=registry,
            )
        )
    )
    if default_error != injected_error:
        raise AssertionError(
            f"{case_id} exception drift: {default_error} != {injected_error}"
        )
    if expected_message not in injected_error["message"]:
        raise AssertionError(
            f"{case_id} missing expected message {expected_message!r}: {injected_error}"
        )
    return {
        "case_id": case_id,
        "default_error": default_error,
        "injected_error": injected_error,
        "status": "PASS",
    }


def compare_v18_missing_pnf(
    base_root: Path,
    base_registry: dict[str, Any],
    pnf_rows: dict[str, dict[str, str]],
) -> dict[str, Any]:
    registry = copy.deepcopy(base_registry)
    registry["entries"][0]["proof_normal_form_row_id"] = "PNF-MISSING"
    with tempfile.TemporaryDirectory() as temp_dir:
        disk_root = Path(temp_dir) / "repo"
        shutil.copytree(base_root, disk_root)
        write_registry(disk_root, V18_REGISTRY_PATH, registry)
        default_error = capture_error(
            lambda: v18_validator.validate_registry(repo_root=disk_root)
        )
    injected_error = capture_error(
        lambda: v18_validator.validate_registry(
            dependencies=TraceabilityInputs(
                repo_root=base_root,
                registry=registry,
                proof_normal_form_rows=pnf_rows,
            )
        )
    )
    if default_error != injected_error:
        raise AssertionError(
            f"missing PNF exception drift: {default_error} != {injected_error}"
        )
    if "missing proof-normal-form row: PNF-MISSING" not in injected_error["message"]:
        raise AssertionError(f"unexpected missing-PNF error: {injected_error}")
    return {
        "case_id": "missing_pnf_row",
        "default_error": default_error,
        "injected_error": injected_error,
        "status": "PASS",
    }


def main() -> int:
    live_v1, live_v1_seconds = timed(v1_validator.validate_registry)
    live_v18, live_v18_seconds = timed(v18_validator.validate_registry)

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        v1_root = root / "v1"
        v18_root = root / "v18"
        v1_entry_id = "SFR-V12-P6-T02-FINITE-TOY-TAG-REMOVAL"
        v1_build = TraceabilityFixtureBuilder(REPO_ROOT, v1_root).build_v1(
            [v1_entry_id]
        )
        v18_build = TraceabilityFixtureBuilder(REPO_ROOT, v18_root).build_v18()

        v1_registry = strict_yaml.load(v1_root / V1_REGISTRY_PATH)
        v18_registry = strict_yaml.load(v18_root / V18_REGISTRY_PATH)
        pnf_rows = read_pnf_rows(v18_root)

        v1_inputs, v1_injection = instrumented_inputs(v1_root, v1_registry)
        v18_inputs, v18_injection = instrumented_inputs(
            v18_root,
            v18_registry,
            pnf_rows=pnf_rows,
        )
        fixture_v1, fixture_v1_seconds = timed(
            lambda: v1_validator.validate_registry(dependencies=v1_inputs)
        )
        fixture_v18, fixture_v18_seconds = timed(
            lambda: v18_validator.validate_registry(dependencies=v18_inputs)
        )

        if V1_REGISTRY_PATH in v1_injection["file_reads"]:
            raise AssertionError("injected v1 registry object was read from disk")
        if V18_REGISTRY_PATH in v18_injection["file_reads"]:
            raise AssertionError("injected v18 registry object was read from disk")
        if PNF_REGISTRY_PATH in v18_injection["file_reads"]:
            raise AssertionError("injected PNF rows were read from disk")
        if v1_injection["hash_calls"] == 0 or v18_injection["hash_calls"] == 0:
            raise AssertionError("injected hash provider was not exercised")
        if (v1_root / "README.md").exists() or (v18_root / "README.md").exists():
            raise AssertionError("minimal fixture copied unrelated repository files")

        failure_cases = [
            compare_v1_failure(
                v1_root,
                v1_registry,
                "missing_file",
                lambda registry: registry["entries"][0]["formalization_files"].append(
                    "missing/formalization.tex"
                ),
                "missing path: missing/formalization.tex",
            ),
            compare_v1_failure(
                v1_root,
                v1_registry,
                "hash_mismatch",
                lambda registry: registry["entries"][0][
                    "canonical_source_artifacts"
                ][0].update({"source_hash": "0" * 64}),
                "artifact hash mismatch",
            ),
            compare_v1_failure(
                v1_root,
                v1_registry,
                "generated_authority_path",
                lambda registry: registry["entries"][0][
                    "canonical_source_artifacts"
                ][0].update(
                    {
                        "path": "wiki/forbidden-authority.md",
                        "source_hash": "0" * 64,
                    }
                ),
                "uses generated or local path as authority",
            ),
            compare_v1_failure(
                v1_root,
                v1_registry,
                "proof_authority",
                lambda registry: registry["entries"][0].update(
                    {"proof_authority": True}
                ),
                "proof_authority is not false",
            ),
            compare_v18_missing_pnf(v18_root, v18_registry, pnf_rows),
        ]

        report = {
            "authority_boundary": {
                "ordinary_research_handoff_preserved": "handoff-0740",
                "physics_promotion_authorized": False,
                "proof_authority": False,
                "scientific_claims_changed": False,
            },
            "baseline": {
                "full_copy_test_count": 9,
                "full_copy_test_runtime_seconds": 83.731,
                "live_v1_entry_count": live_v1["checked_entry_count"],
                "live_v1_runtime_seconds": round(live_v1_seconds, 6),
                "live_v18_entry_count": live_v18["entry_count"],
                "live_v18_runtime_seconds": round(live_v18_seconds, 6),
            },
            "dependency_injection": {
                "injectable_raw_inputs": [
                    "repo_root",
                    "registry",
                    "file_loader",
                    "hash_provider",
                    "proof_normal_form_rows",
                ],
                "prevalidated_results_injectable": False,
                "v1": v1_injection,
                "v18": v18_injection,
            },
            "failure_equivalence": failure_cases,
            "fixture_builds": {
                "v1": v1_build.as_dict(),
                "v18": v18_build.as_dict(),
            },
            "fixture_validation": {
                "v1_entry_count": fixture_v1["checked_entry_count"],
                "v1_runtime_seconds": round(fixture_v1_seconds, 6),
                "v1_status": fixture_v1["status"],
                "v18_entry_count": fixture_v18["entry_count"],
                "v18_runtime_seconds": round(fixture_v18_seconds, 6),
                "v18_status": fixture_v18["status"],
            },
            "plan_task_id": "P9-T01",
            "recommendation_ids": ["V19-R18", "V19-R19"],
            "status": "PASS",
        }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
