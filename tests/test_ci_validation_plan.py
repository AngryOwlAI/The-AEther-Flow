#!/usr/bin/env python3
"""Validate and exercise the bounded P11-T02 planner-driven CI shard contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml


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
        ):
            self.assertIn(fragment, text)
        for shard in SHARDS:
            self.assertIn(f"- {shard}", text)

    def test_scheduled_workflow_is_unfiltered_and_cache_audit_capable(self) -> None:
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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command")
    run = subcommands.add_parser("run-shard")
    run.add_argument("--plan", required=True, type=Path)
    run.add_argument("--shard", required=True, choices=SHARDS)
    run.add_argument("--output-dir", required=True, type=Path)
    run.add_argument("--scheduled-full", action="store_true")
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
    program = unittest.main(argv=[sys.argv[0]], exit=False)
    return 0 if program.result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
