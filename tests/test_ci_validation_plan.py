#!/usr/bin/env python3
"""Validate and exercise the bounded P11-T02/P11-T03 CI contracts."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
COVERAGE_PATH = (
    ROOT
    / "research_control/tasks/RT-20260718-003/artifacts/ci_shard_coverage_report.json"
)
PROJECT_WORKFLOW_PATH = ROOT / ".github/workflows/project-control-validation.yml"
SCHEDULED_WORKFLOW_PATH = ROOT / ".github/workflows/scheduled-full-validation.yml"
RUNNER_PATH = Path(__file__).resolve()
MEMORY_SCRIPT_PATH = (
    ROOT
    / ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py"
)
REQUIREMENT_PATHS = (
    ROOT / "pyproject.toml",
    ROOT / "research_control/tasks/RT-20260723-019/artifacts/requirements.lock",
    ROOT / "requirements.txt",
    ROOT / "requirements-dev.txt",
)
MEMORY_IMPLEMENTATION_PATHS = (
    ROOT / "Makefile",
    RUNNER_PATH,
    *sorted(MEMORY_SCRIPT_PATH.parent.rglob("*.py")),
)
MEMORY_CONFIGURATION_PATHS = (
    PROJECT_WORKFLOW_PATH,
    MANIFEST_PATH,
    *REQUIREMENT_PATHS,
)

SHARDS = (
    "policy-fast",
    "research-control-integration",
    "dependency-graph",
    "memory-core",
    "publication",
    "scientific-support",
    "local-retrieval",
    "orchestration-equivalence",
)

# These are test-responsibility shards, not hidden validator command lists.
# Gate selection continues to come only from the emitted validation plan.
SHARD_TEST_MODULES = {
    "policy-fast": (
        "tests.test_project_change_classifier",
        "tests.test_validation_change_matrix",
        "tests.test_validation_profiles",
    ),
    "research-control-integration": (
        "tests.test_checkpoint_validation_planner",
        "tests.test_research_control_policy",
        "tests.test_validation_precheck",
    ),
    "dependency-graph": (
        "tests.test_dependency_graph_determinism",
        "tests.test_render_dependency_graph",
    ),
    "memory-core": (
        "tests.test_memory_cli_modes",
        "tests.test_memory_system_unit",
    ),
    "publication": (
        "tests.test_documentation_surface_audit",
        "tests.test_publication_process_validation",
        "tests.test_spec_depth_lint",
    ),
    "scientific-support": (
        "tests.test_validate_claim_graph_v1",
        "tests.test_validate_claim_language",
        "tests.test_validation_executor",
    ),
    "local-retrieval": (
        "tests.test_obsidian_wiki_unit",
        "tests.test_route_orbit_validator",
        "tests.test_validation_doctor",
    ),
    "orchestration-equivalence": (
        "tests.test_validation_deduplication",
        "tests.test_validation_equivalence",
        "tests.test_validation_orchestration",
    ),
}


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def digest_files(paths: tuple[Path, ...]) -> str:
    hasher = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        hasher.update(relative.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(path.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def source_tree() -> str:
    github_sha = os.environ.get("GITHUB_SHA", "").strip()
    if github_sha:
        return github_sha
    process = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        raise ValueError("unable to resolve source tree")
    return process.stdout.strip()


def manifest_hash() -> str:
    return canonical_hash(load_json(MANIFEST_PATH))


def installed_distribution_digest() -> str:
    distributions = sorted(
        f"{distribution.metadata.get('Name', '').lower()}=={distribution.version}"
        for distribution in importlib.metadata.distributions()
    )
    return hashlib.sha256("\n".join(distributions).encode("utf-8")).hexdigest()


def legacy_evidence_identity() -> dict[str, object]:
    environment = {
        "schema_id": "ci_legacy_environment_v1",
        "python_implementation": platform.python_implementation(),
        "python_series": f"{sys.version_info.major}.{sys.version_info.minor}",
        "platform_system": platform.system(),
        "platform_machine": platform.machine(),
        "dependency_lock_digest": digest_files(REQUIREMENT_PATHS),
        "installed_distribution_digest": installed_distribution_digest(),
    }
    return {
        "gate_id": "memory_core",
        "implementation_digest": f"sha256:{digest_files(MEMORY_IMPLEMENTATION_PATHS)}",
        "environment": environment,
        "environment_digest": f"sha256:{canonical_hash(environment)}",
        "config_digest": f"sha256:{digest_files(MEMORY_CONFIGURATION_PATHS)}",
        "scope": "tree_state=commit;scope=repository",
        "tree_hash": f"git:{source_tree()}",
        "manifest_hash": manifest_hash(),
    }


def build_legacy_project_control_receipt(
    *,
    exit_code: int,
    full_output: bytes,
    duration_seconds: float,
) -> dict[str, object]:
    status = "PASS" if exit_code == 0 else "FAIL"
    return {
        "schema_id": "ci_legacy_project_control_receipt_v1",
        "status": status,
        "aggregate_exit_code": exit_code,
        "evidence_identity": legacy_evidence_identity(),
        "producer": {
            "workflow_run_id": os.environ.get("GITHUB_RUN_ID", ""),
            "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", ""),
            "job": os.environ.get("GITHUB_JOB", ""),
        },
        "gate_results": [
            {
                "gate_id": "memory_core",
                "status": status,
                "evidence_basis": "validate-project-control-legacy sequential aggregate",
                "command": (
                    ".venv/bin/python "
                    ".codex/skills/project-memory-system/scripts/"
                    "bootstrap_memory_system.py --validate-only"
                ),
            }
        ],
        "duration_seconds": round(duration_seconds, 6),
        "full_output": {
            "path": "full-output.log",
            "sha256": hashlib.sha256(full_output).hexdigest(),
            "bytes": len(full_output),
        },
        "authority": {
            "operational_validation_only": True,
            "legacy_ci_authoritative": True,
            "planner_authoritative": False,
            "physics_claim_authority": False,
            "proof_authority": False,
        },
    }


def write_legacy_project_control_receipt(
    output_dir: Path,
    full_output_path: Path,
    *,
    exit_code: int,
    duration_seconds: float,
) -> int:
    output = full_output_path.read_bytes()
    receipt = build_legacy_project_control_receipt(
        exit_code=exit_code,
        full_output=output,
        duration_seconds=duration_seconds,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = output_dir / "legacy-project-control-receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"{receipt['status']} legacy-project-control "
        f"memory_core={receipt['gate_results'][0]['status']} "
        f"receipt={receipt_path}"
    )
    return exit_code


def memory_input_globs() -> tuple[str, ...]:
    manifest = load_json(MANIFEST_PATH)
    gates = manifest.get("gates")
    if not isinstance(gates, list):
        raise ValueError("validation manifest gates are missing")
    globs: set[str] = set()
    for gate in gates:
        if not isinstance(gate, dict) or gate.get("gate_id") not in {
            "memory_sync",
            "memory_core",
        }:
            continue
        input_globs = gate.get("input_globs")
        if not isinstance(input_globs, list) or any(
            not isinstance(pattern, str) for pattern in input_globs
        ):
            raise ValueError("memory gate input globs are invalid")
        globs.update(input_globs)
    if not globs:
        raise ValueError("memory gate input globs are empty")
    return tuple(sorted(globs))


def build_memory_signal_selection(
    plan: dict[str, object],
    *,
    scheduled_full: bool = False,
) -> dict[str, object]:
    if plan.get("schema_id") != "validation_plan_v1":
        raise ValueError("unsupported validation plan")
    if plan.get("status") != "READY":
        raise ValueError("memory signal requires a READY plan")
    if plan.get("execution_authority") != "legacy":
        raise ValueError("memory signal requires legacy execution authority")
    if plan.get("manifest_hash") != manifest_hash():
        raise ValueError("validation plan manifest hash mismatch")
    selected_gate_ids = plan.get("selected_gate_ids")
    changed_paths = plan.get("changed_paths")
    if not isinstance(selected_gate_ids, list) or any(
        not isinstance(gate_id, str) for gate_id in selected_gate_ids
    ):
        raise ValueError("plan selected gate IDs are invalid")
    if not isinstance(changed_paths, list) or any(
        not isinstance(path, str) for path in changed_paths
    ):
        raise ValueError("plan changed paths are invalid")
    selected = "memory_core" in selected_gate_ids
    full_profile = plan.get("effective_profile") == "full"
    changed_memory_input = any(
        fnmatch.fnmatchcase(path, pattern)
        for path in changed_paths
        for pattern in memory_input_globs()
    )
    applicable = scheduled_full or full_profile or changed_memory_input
    if applicable and not selected:
        raise ValueError("applicable memory input lacks planner-selected memory_core")
    if scheduled_full:
        reason = "scheduled_full"
    elif full_profile:
        reason = "full_profile"
    elif changed_memory_input:
        reason = "memory_input_changed"
    else:
        reason = "unrelated_change"
    return {
        "schema_id": "ci_memory_signal_selection_v1",
        "status": "READY",
        "mode": "reuse" if applicable else "skip",
        "reason": reason,
        "plan_hash": canonical_hash(plan),
        "manifest_hash": plan.get("manifest_hash"),
        "tree_hash": f"git:{source_tree()}",
        "changed_path_count": len(changed_paths),
        "memory_core_selected": selected,
        "scheduled_full": scheduled_full,
    }


def prepare_memory_signal(
    plan_path: Path,
    output_dir: Path,
    *,
    scheduled_full: bool = False,
) -> int:
    if plan_path.exists():
        selection = build_memory_signal_selection(
            load_json(plan_path),
            scheduled_full=scheduled_full,
        )
    else:
        selection = {
            "schema_id": "ci_memory_signal_selection_v1",
            "status": "READY",
            "mode": "fallback",
            "reason": "planner_artifact_unavailable",
            "plan_hash": None,
            "manifest_hash": manifest_hash(),
            "tree_hash": f"git:{source_tree()}",
            "changed_path_count": None,
            "memory_core_selected": None,
            "scheduled_full": scheduled_full,
        }
    output_dir.mkdir(parents=True, exist_ok=True)
    selection_path = output_dir / "memory-signal-selection.json"
    selection_path.write_text(
        json.dumps(selection, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    github_output = os.environ.get("GITHUB_OUTPUT", "")
    if github_output:
        with Path(github_output).open("a", encoding="utf-8") as stream:
            stream.write(f"mode={selection['mode']}\n")
    print(
        f"READY memory-signal mode={selection['mode']} "
        f"reason={selection['reason']} selection={selection_path}"
    )
    return 0


def verify_reused_memory_receipt(
    receipt: dict[str, object],
    receipt_path: Path,
) -> dict[str, object]:
    if receipt.get("schema_id") != "ci_legacy_project_control_receipt_v1":
        raise ValueError("unsupported legacy project-control receipt")
    identity = receipt.get("evidence_identity")
    if not isinstance(identity, dict):
        raise ValueError("legacy receipt evidence identity is missing")
    expected = legacy_evidence_identity()
    for field in (
        "gate_id",
        "manifest_hash",
        "implementation_digest",
        "config_digest",
        "scope",
        "tree_hash",
    ):
        if identity.get(field) != expected[field]:
            raise ValueError(f"legacy receipt {field} mismatch")
    environment = identity.get("environment")
    if not isinstance(environment, dict):
        raise ValueError("legacy receipt environment is missing")
    if identity.get("environment_digest") != f"sha256:{canonical_hash(environment)}":
        raise ValueError("legacy receipt environment digest mismatch")
    if environment.get("dependency_lock_digest") != digest_files(REQUIREMENT_PATHS):
        raise ValueError("legacy receipt dependency lock mismatch")
    if environment.get("python_series") != "3.12":
        raise ValueError("legacy receipt Python series mismatch")
    distribution_digest = environment.get("installed_distribution_digest")
    if (
        not isinstance(distribution_digest, str)
        or len(distribution_digest) != 64
        or any(character not in "0123456789abcdef" for character in distribution_digest)
    ):
        raise ValueError("legacy receipt installed distribution digest is invalid")
    producer = receipt.get("producer")
    if not isinstance(producer, dict):
        raise ValueError("legacy receipt producer is missing")
    for field, variable in (
        ("workflow_run_id", "GITHUB_RUN_ID"),
        ("workflow_run_attempt", "GITHUB_RUN_ATTEMPT"),
    ):
        current = os.environ.get(variable, "")
        if current and producer.get(field) != current:
            raise ValueError(f"legacy receipt producer {field} mismatch")
    gate_results = receipt.get("gate_results")
    if not isinstance(gate_results, list):
        raise ValueError("legacy receipt gate results are missing")
    memory = [
        result
        for result in gate_results
        if isinstance(result, dict) and result.get("gate_id") == "memory_core"
    ]
    if len(memory) != 1 or memory[0].get("status") != "PASS":
        raise ValueError("legacy receipt does not prove memory_core PASS")
    if receipt.get("status") != "PASS" or receipt.get("aggregate_exit_code") != 0:
        raise ValueError("legacy project-control aggregate did not pass")
    return {
        "evidence_identity": identity,
        "source_receipt": {
            "path": receipt_path.name,
            "sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        },
        "authority": receipt.get("authority"),
    }


def finalize_memory_signal(
    selection_path: Path,
    output_dir: Path,
    *,
    legacy_receipt_path: Path | None = None,
    fallback_output_path: Path | None = None,
    fallback_exit_code: int | None = None,
) -> int:
    selection = load_json(selection_path)
    if selection.get("schema_id") != "ci_memory_signal_selection_v1":
        raise ValueError("unsupported memory signal selection")
    mode = selection.get("mode")
    if mode not in {"reuse", "skip", "fallback"}:
        raise ValueError("unsupported memory signal mode")
    execution = {
        "reuse": "REUSED_SAME_TREE_LEGACY_RECEIPT",
        "skip": "SKIP_NOT_APPLICABLE",
        "fallback": "FALLBACK_DIRECT_EXECUTION",
    }[mode]
    status = "PASS"
    signal: dict[str, object] = {
        "schema_id": "ci_memory_signal_receipt_v1",
        "status": status,
        "gate_id": "memory_core",
        "execution": execution,
        "selection": selection,
        "duplicate_environment_provisioned": mode == "fallback",
        "duplicate_memory_command_executed": mode == "fallback",
        "authority": {
            "operational_validation_only": True,
            "legacy_ci_authoritative": True,
            "planner_authoritative": False,
            "physics_claim_authority": False,
            "proof_authority": False,
        },
    }
    if mode == "reuse":
        if legacy_receipt_path is None:
            raise ValueError("reuse mode requires a legacy receipt")
        reused = verify_reused_memory_receipt(
            load_json(legacy_receipt_path),
            legacy_receipt_path,
        )
        identity = reused["evidence_identity"]
        if identity["tree_hash"] != selection.get("tree_hash"):
            raise ValueError("selection and legacy receipt tree hash mismatch")
        if identity["manifest_hash"] != selection.get("manifest_hash"):
            raise ValueError("selection and legacy receipt manifest hash mismatch")
        signal.update(reused)
    elif mode == "fallback":
        if fallback_output_path is None or fallback_exit_code is None:
            raise ValueError("fallback mode requires direct execution evidence")
        fallback_bytes = fallback_output_path.read_bytes()
        status = "PASS" if fallback_exit_code == 0 else "FAIL"
        signal["status"] = status
        signal["fallback_execution"] = {
            "exit_code": fallback_exit_code,
            "full_output_path": fallback_output_path.name,
            "full_output_sha256": hashlib.sha256(fallback_bytes).hexdigest(),
            "full_output_bytes": len(fallback_bytes),
        }
    output_dir.mkdir(parents=True, exist_ok=True)
    signal_path = output_dir / "memory-signal-receipt.json"
    signal_path.write_text(
        json.dumps(signal, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"{status} memory-signal execution={execution} "
        f"receipt={signal_path}"
    )
    return 0 if status == "PASS" else 1


def validate_plan_document(plan: dict[str, object]) -> None:
    from scripts.validation.run import load_plan

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "plan.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        loaded = load_plan(path)
    if loaded.status != "READY":
        raise ValueError(f"plan status is not READY: {loaded.status}")
    if loaded.execution_authority != "legacy":
        raise ValueError("shadow shards require legacy execution authority")


def shard_owners() -> dict[str, tuple[str, ...]]:
    coverage = load_json(COVERAGE_PATH)
    raw = coverage.get("primary_owners")
    if not isinstance(raw, dict) or set(raw) != set(SHARDS):
        raise ValueError("P11-T01 primary owner map does not match the CI shard set")
    owners: dict[str, tuple[str, ...]] = {}
    for shard, gate_ids in raw.items():
        if (
            not isinstance(shard, str)
            or not isinstance(gate_ids, list)
            or any(not isinstance(gate_id, str) for gate_id in gate_ids)
        ):
            raise ValueError("primary owner map contains an invalid entry")
        owners[shard] = tuple(gate_ids)
    flattened = [gate_id for values in owners.values() for gate_id in values]
    if len(flattened) != len(set(flattened)):
        raise ValueError("a gate has more than one primary CI owner")
    return owners


def build_shard_receipt(
    plan: dict[str, object],
    shard: str,
    *,
    scheduled_full: bool = False,
) -> dict[str, object]:
    validate_plan_document(plan)
    owners = shard_owners()
    if shard not in owners:
        raise ValueError(f"unknown shard: {shard}")
    selected = plan.get("selected_gate_ids")
    entries = plan.get("entries")
    if (
        not isinstance(selected, list)
        or any(not isinstance(gate_id, str) for gate_id in selected)
        or not isinstance(entries, list)
    ):
        raise ValueError("plan selection fields are invalid")
    selected_set = set(selected)
    selected_gate_ids = [
        gate_id for gate_id in owners[shard] if gate_id in selected_set
    ]
    entries_by_id = {
        str(entry.get("gate_id")): entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("gate_id"), str)
    }
    missing_entries = [
        gate_id for gate_id in selected_gate_ids if gate_id not in entries_by_id
    ]
    if missing_entries:
        raise ValueError(f"selected gates lack plan entries: {missing_entries}")
    plan_hash = hashlib.sha256(
        json.dumps(
            plan, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()
    gate_results = [
        {
            "gate_id": gate_id,
            "status": (
                "SHADOW_TEST_PENDING"
                if gate_id in selected_set
                else "SKIP_NOT_APPLICABLE"
            ),
            "selection_reasons": (
                list(entries_by_id[gate_id].get("reasons", []))
                if gate_id in entries_by_id
                else ["not_selected_by_plan"]
            ),
        }
        for gate_id in owners[shard]
    ]
    return {
        "schema_id": "ci_validation_shard_receipt_v1",
        "status": "PASS",
        "shard_id": shard,
        "plan_hash": plan_hash,
        "manifest_hash": plan.get("manifest_hash"),
        "requested_profile": plan.get("requested_profile"),
        "effective_profile": plan.get("effective_profile"),
        "scheduled_full": scheduled_full,
        "cache_mode": os.environ.get("VALIDATION_CACHE_MODE", "off"),
        "selected_gate_count": len(selected_gate_ids),
        "selected_gate_ids": selected_gate_ids,
        "primary_gate_ids": list(owners[shard]),
        "gate_results": gate_results,
        "test_modules": list(SHARD_TEST_MODULES[shard]),
        "test_execution": {
            "status": (
                "PENDING" if selected_gate_ids else "SKIP_NOT_APPLICABLE"
            ),
            "exit_code": None,
            "full_output_path": None,
            "full_output_sha256": None,
            "full_output_bytes": 0,
        },
        "authority": {
            "operational_validation_only": True,
            "legacy_ci_authoritative": True,
            "planner_authoritative": False,
            "physics_claim_authority": False,
            "proof_authority": False,
        },
    }


def run_shard(
    plan_path: Path,
    shard: str,
    output_dir: Path,
    *,
    scheduled_full: bool,
) -> int:
    plan = load_json(plan_path)
    receipt = build_shard_receipt(plan, shard, scheduled_full=scheduled_full)
    output_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = output_dir / "shard-receipt.json"
    log_path = output_dir / "full-output.log"
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if receipt["selected_gate_count"] == 0:
        log_path.write_text("", encoding="utf-8")
        print(f"PASS shard={shard} selected=0 status=SKIP_NOT_APPLICABLE")
        return 0

    command = [
        sys.executable,
        "-m",
        "unittest",
        "-v",
        *SHARD_TEST_MODULES[shard],
    ]
    process = subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=False,
        check=False,
    )
    output = process.stdout or b""
    log_path.write_bytes(output)
    receipt["status"] = "PASS" if process.returncode == 0 else "FAIL"
    for gate_result in receipt["gate_results"]:
        if gate_result["status"] == "SHADOW_TEST_PENDING":
            gate_result["status"] = (
                "SHADOW_TEST_PASS" if process.returncode == 0 else "SHADOW_TEST_FAIL"
            )
    receipt["test_execution"] = {
        "status": "PASS" if process.returncode == 0 else "FAIL",
        "exit_code": process.returncode,
        "full_output_path": log_path.name,
        "full_output_sha256": hashlib.sha256(output).hexdigest(),
        "full_output_bytes": len(output),
    }
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"{receipt['status']} shard={shard} "
        f"selected={receipt['selected_gate_count']} tests={len(SHARD_TEST_MODULES[shard])} "
        f"receipt={receipt_path}"
    )
    return process.returncode


class CIValidationPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from scripts.validation.plan import load_manifest

        cls.manifest = load_manifest(MANIFEST_PATH)

    def plan_for(self, paths: list[str], profile: str = "affected") -> dict[str, object]:
        from scripts.project_control.classify_project_changes import classify_paths
        from scripts.validation.plan import build_plan

        return build_plan(
            self.manifest,
            classify_paths(paths),
            profile=profile,
            scopes=("working",),
        ).to_dict()

    def test_primary_ownership_is_complete_and_nonoverlapping(self) -> None:
        owners = shard_owners()
        flattened = [gate_id for values in owners.values() for gate_id in values]
        manifest_ids = {str(gate["gate_id"]) for gate in self.manifest["gates"]}
        self.assertEqual(set(flattened), manifest_ids)
        self.assertEqual(len(flattened), len(set(flattened)))
        self.assertEqual(set(SHARD_TEST_MODULES), set(SHARDS))

    def test_affected_plan_selects_shards_from_gate_ids_not_path_globs(self) -> None:
        plan = self.plan_for([".github/workflows/project-control-validation.yml"])
        selected = set(plan["selected_gate_ids"])
        expected_active = {
            shard
            for shard, gate_ids in shard_owners().items()
            if selected.intersection(gate_ids)
        }
        actual_active = {
            shard
            for shard in SHARDS
            if build_shard_receipt(plan, shard)["selected_gate_count"] > 0
        }
        self.assertEqual(actual_active, expected_active)

    def test_inapplicable_shard_stays_visible_with_explicit_receipt(self) -> None:
        plan = self.plan_for([".github/workflows/project-control-validation.yml"])
        receipt = build_shard_receipt(plan, "dependency-graph")
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["selected_gate_count"], 0)
        self.assertTrue(
            all(
                result["status"] == "SKIP_NOT_APPLICABLE"
                for result in receipt["gate_results"]
            )
        )

    def test_project_workflow_keeps_legacy_authority_and_stable_shards(self) -> None:
        import yaml

        text = PROJECT_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIsNotNone(yaml.compose(text))
        for fragment in (
            "validation_plan_shadow:",
            "validation_shards_shadow:",
            "needs: validation_plan_shadow",
            "continue-on-error: true",
            "tests/test_ci_validation_plan.py run-shard",
            "actions/download-artifact@v4",
            "actions/upload-artifact@v4",
            "validate_project_control:",
            "validate_memory_read_only:",
            "write-legacy-receipt",
            "prepare-memory-signal",
            "finalize-memory-signal",
            "if: always()",
            "legacy-project-control-${{ github.run_id }}-${{ github.run_attempt }}",
        ):
            self.assertIn(fragment, text)
        for shard in SHARDS:
            self.assertIn(f"- {shard}", text)
        project_job = text.split("  validate_project_control:", 1)[1].split(
            "  validate_memory_read_only:", 1
        )[0]
        self.assertNotIn("needs: validation_plan_shadow", project_job)
        self.assertIn("fetch-depth: 0", project_job)
        self.assertIn(
            "pip install --require-hashes -r requirements-dev.txt",
            project_job,
        )
        self.assertNotIn(
            "pip install --require-hashes -r requirements.txt",
            project_job,
        )
        memory_job = text.split("  validate_memory_read_only:", 1)[1]
        self.assertIn("steps.memory_selection.outputs.mode == 'fallback'", memory_job)
        self.assertIn("steps.memory_selection.outputs.mode == 'reuse'", memory_job)
        self.assertIn("continue-on-error: true", memory_job)

    def test_scheduled_workflow_is_unfiltered_and_cache_audit_capable(self) -> None:
        import yaml

        text = SCHEDULED_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIsNotNone(yaml.compose(text))
        self.assertIn("schedule:", text)
        self.assertIn("--profile full", text)
        self.assertIn("--scope repository", text)
        self.assertIn("--profile doctor", text)
        self.assertIn("VALIDATION_CACHE_MODE: audit", text)
        self.assertIn("scheduled_validation_shards:", text)
        self.assertNotIn("paths-ignore:", text)
        self.assertNotIn("branches-ignore:", text)
        for shard in SHARDS:
            self.assertIn(f"- {shard}", text)

    def test_full_plus_doctor_plans_cover_every_scheduled_shard(self) -> None:
        from scripts.project_control.classify_project_changes import classify_paths
        from scripts.validation.plan import build_plan

        full = build_plan(
            self.manifest,
            classify_paths([]),
            profile="full",
            scopes=("repository",),
        ).to_dict()
        doctor = build_plan(
            self.manifest,
            classify_paths([".local/scheduled-health"]),
            profile="doctor",
            scopes=("local_retrieval",),
        ).to_dict()
        selected = set(full["selected_gate_ids"]) | set(doctor["selected_gate_ids"])
        scheduled_shards = {
            shard
            for shard, gate_ids in shard_owners().items()
            if selected.intersection(gate_ids)
        }
        self.assertEqual(scheduled_shards, set(SHARDS))

    def test_script_mode_writes_inapplicable_receipt_without_running_tests(self) -> None:
        plan = self.plan_for([".github/workflows/project-control-validation.yml"])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path = root / "plan.json"
            output_dir = root / "output"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "run-shard",
                    "--plan",
                    str(plan_path),
                    "--shard",
                    "dependency-graph",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            receipt = load_json(output_dir / "shard-receipt.json")
            self.assertEqual(receipt["selected_gate_count"], 0)
            self.assertEqual(
                receipt["test_execution"]["status"], "SKIP_NOT_APPLICABLE"
            )

    def test_shard_receipt_rejects_unknown_identity(self) -> None:
        plan = self.plan_for(["README.md"])
        with self.assertRaisesRegex(ValueError, "unknown shard"):
            build_shard_receipt(plan, "unknown")

    def test_memory_signal_selects_affected_unrelated_full_and_scheduled(self) -> None:
        affected = build_memory_signal_selection(
            self.plan_for(["registries/FILE_OBJECT_REGISTRY.csv"])
        )
        unrelated = build_memory_signal_selection(self.plan_for(["README.md"]))
        full = build_memory_signal_selection(self.plan_for(["README.md"], profile="full"))
        scheduled = build_memory_signal_selection(
            self.plan_for(["README.md"]),
            scheduled_full=True,
        )
        self.assertEqual((affected["mode"], affected["reason"]), ("reuse", "memory_input_changed"))
        self.assertEqual((unrelated["mode"], unrelated["reason"]), ("skip", "unrelated_change"))
        self.assertEqual((full["mode"], full["reason"]), ("reuse", "full_profile"))
        self.assertEqual((scheduled["mode"], scheduled["reason"]), ("reuse", "scheduled_full"))

    def test_unrelated_memory_signal_skips_without_receipt_or_provisioning(self) -> None:
        selection = build_memory_signal_selection(self.plan_for(["README.md"]))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            selection_path = root / "selection.json"
            selection_path.write_text(json.dumps(selection), encoding="utf-8")
            self.assertEqual(
                finalize_memory_signal(
                    selection_path,
                    root / "signal",
                    legacy_receipt_path=root / "missing-receipt.json",
                ),
                0,
            )
            signal = load_json(root / "signal/memory-signal-receipt.json")
        self.assertEqual(signal["execution"], "SKIP_NOT_APPLICABLE")
        self.assertFalse(signal["duplicate_environment_provisioned"])
        self.assertFalse(signal["duplicate_memory_command_executed"])

    def test_memory_signal_reuses_same_tree_legacy_receipt(self) -> None:
        plan = self.plan_for(["registries/FILE_OBJECT_REGISTRY.csv"])
        environment = {
            "GITHUB_SHA": "a" * 40,
            "GITHUB_RUN_ID": "101",
            "GITHUB_RUN_ATTEMPT": "2",
            "GITHUB_JOB": "validate_project_control",
        }
        with mock.patch.dict(os.environ, environment):
            receipt = build_legacy_project_control_receipt(
                exit_code=0,
                full_output=b"PASS\n",
                duration_seconds=1.25,
            )
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                selection_path = root / "selection.json"
                legacy_path = root / "legacy-project-control-receipt.json"
                selection_path.write_text(
                    json.dumps(build_memory_signal_selection(plan)),
                    encoding="utf-8",
                )
                legacy_path.write_text(json.dumps(receipt), encoding="utf-8")
                self.assertEqual(
                    finalize_memory_signal(
                        selection_path,
                        root / "signal",
                        legacy_receipt_path=legacy_path,
                    ),
                    0,
                )
                signal = load_json(root / "signal/memory-signal-receipt.json")
        self.assertEqual(signal["execution"], "REUSED_SAME_TREE_LEGACY_RECEIPT")
        self.assertFalse(signal["duplicate_environment_provisioned"])
        self.assertFalse(signal["duplicate_memory_command_executed"])

    def test_memory_signal_rejects_each_identity_mismatch(self) -> None:
        plan = self.plan_for(["registries/FILE_OBJECT_REGISTRY.csv"])
        fields = (
            "tree_hash",
            "manifest_hash",
            "implementation_digest",
            "config_digest",
            "scope",
        )
        with mock.patch.dict(os.environ, {"GITHUB_SHA": "b" * 40}):
            baseline = build_legacy_project_control_receipt(
                exit_code=0,
                full_output=b"PASS\n",
                duration_seconds=1.0,
            )
            for field in fields:
                receipt = json.loads(json.dumps(baseline))
                receipt["evidence_identity"][field] = "mismatch"
                with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    receipt_path = root / "receipt.json"
                    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "mismatch"):
                        verify_reused_memory_receipt(
                            load_json(receipt_path),
                            receipt_path,
                        )

    def test_memory_signal_rejects_failed_or_environment_mismatched_receipt(self) -> None:
        environment = {"GITHUB_SHA": "c" * 40, "GITHUB_RUN_ID": "202"}
        with mock.patch.dict(os.environ, environment):
            failed = build_legacy_project_control_receipt(
                exit_code=1,
                full_output=b"FAIL\n",
                duration_seconds=1.0,
            )
            mismatched = build_legacy_project_control_receipt(
                exit_code=0,
                full_output=b"PASS\n",
                duration_seconds=1.0,
            )
            mismatched["evidence_identity"]["environment"]["python_series"] = "3.11"
            wrong_run = build_legacy_project_control_receipt(
                exit_code=0,
                full_output=b"PASS\n",
                duration_seconds=1.0,
            )
            wrong_run["producer"]["workflow_run_id"] = "different-run"
            cases = (failed, mismatched, wrong_run)
            for receipt in cases:
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    receipt_path = root / "receipt.json"
                    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        verify_reused_memory_receipt(
                            load_json(receipt_path),
                            receipt_path,
                        )

    def test_missing_plan_uses_explicit_direct_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(
                prepare_memory_signal(root / "missing-plan.json", root / "selection"),
                0,
            )
            selection_path = root / "selection/memory-signal-selection.json"
            output_path = root / "fallback-output.log"
            output_path.write_text("PASS\n", encoding="utf-8")
            self.assertEqual(
                finalize_memory_signal(
                    selection_path,
                    root / "signal",
                    fallback_output_path=output_path,
                    fallback_exit_code=0,
                ),
                0,
            )
            signal = load_json(root / "signal/memory-signal-receipt.json")
        self.assertEqual(signal["execution"], "FALLBACK_DIRECT_EXECUTION")
        self.assertTrue(signal["duplicate_environment_provisioned"])
        self.assertTrue(signal["duplicate_memory_command_executed"])


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command")
    run = subcommands.add_parser("run-shard")
    run.add_argument("--plan", required=True, type=Path)
    run.add_argument("--shard", required=True, choices=SHARDS)
    run.add_argument("--output-dir", required=True, type=Path)
    run.add_argument("--scheduled-full", action="store_true")
    legacy = subcommands.add_parser("write-legacy-receipt")
    legacy.add_argument("--output-dir", required=True, type=Path)
    legacy.add_argument("--full-output", required=True, type=Path)
    legacy.add_argument("--exit-code", required=True, type=int)
    legacy.add_argument("--duration-seconds", required=True, type=float)
    prepare = subcommands.add_parser("prepare-memory-signal")
    prepare.add_argument("--plan", required=True, type=Path)
    prepare.add_argument("--output-dir", required=True, type=Path)
    prepare.add_argument("--scheduled-full", action="store_true")
    finalize = subcommands.add_parser("finalize-memory-signal")
    finalize.add_argument("--selection", required=True, type=Path)
    finalize.add_argument("--output-dir", required=True, type=Path)
    finalize.add_argument("--legacy-receipt", type=Path)
    finalize.add_argument("--fallback-output", type=Path)
    finalize.add_argument("--fallback-exit-code", type=int)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.command == "run-shard":
        try:
            return run_shard(
                args.plan,
                args.shard,
                args.output_dir,
                scheduled_full=args.scheduled_full,
            )
        except (OSError, TypeError, ValueError) as error:
            print(f"BLOCKED_CONFIGURATION: {error}", file=sys.stderr)
            return 2
    if args.command == "write-legacy-receipt":
        try:
            return write_legacy_project_control_receipt(
                args.output_dir,
                args.full_output,
                exit_code=args.exit_code,
                duration_seconds=args.duration_seconds,
            )
        except (OSError, TypeError, ValueError) as error:
            print(f"BLOCKED_CONFIGURATION: {error}", file=sys.stderr)
            return 2
    if args.command == "prepare-memory-signal":
        try:
            return prepare_memory_signal(
                args.plan,
                args.output_dir,
                scheduled_full=args.scheduled_full,
            )
        except (OSError, TypeError, ValueError) as error:
            print(f"BLOCKED_CONFIGURATION: {error}", file=sys.stderr)
            return 2
    if args.command == "finalize-memory-signal":
        try:
            return finalize_memory_signal(
                args.selection,
                args.output_dir,
                legacy_receipt_path=args.legacy_receipt,
                fallback_output_path=args.fallback_output,
                fallback_exit_code=args.fallback_exit_code,
            )
        except (OSError, TypeError, ValueError) as error:
            print(f"BLOCKED_CONFIGURATION: {error}", file=sys.stderr)
            return 2
    program = unittest.main(argv=[sys.argv[0]], exit=False)
    return 0 if program.result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
