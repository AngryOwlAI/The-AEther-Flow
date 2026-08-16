#!/usr/bin/env python3
"""Validate the exact RT003 write-allowlist parity recovery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
REPORT = ROOT / "research_control/tasks/RT-20260816-004/artifacts/rt003_allowlist_parity_checkpoint_recovery_receipt.json"
JOB_ID = "AJ-RT-20260816-003-001"
ROLE_REF = "smuggling-auditor@0.2.0--RT-20260816-003"

EXPECTED = [
    "FOLDER_MAP.md",
    "output/**",
    "registries/**",
    "research_control/current_frontier.md",
    "research_control/design/v22_recommendation_backlog.yaml",
    "research_control/handoffs/handoff-1046.yaml",
    "research_control/handoffs/handoff-1046.md",
    "research_control/program_state.yaml",
    "research_control/tasks/RT-20260721-009/artifacts/v21_burden_status_migration_receipt.json",
    "research_control/tasks/RT-20260721-009/artifacts/v21_current_burden_status.md",
    "research_control/tasks/RT-20260721-009/artifacts/v21_current_burden_status_compact_receipt.json",
    "research_control/tasks/RT-20260721-009/artifacts/v21_current_burden_status_validation.json",
    "research_control/tasks/RT-20260816-003/**",
    "research_control/tasks/TASK_INDEX.csv",
    "research_control/tasks/TASK_INDEX.md",
    "wiki/indexes/**",
    "wiki/markdown/**",
    "wiki/tex/**",
]

OLD = EXPECTED[:8] + ["research_control/tasks/RT-20260721-009/artifacts/**"] + EXPECTED[12:]

PROTECTED_HASHES = {
    "research_control/tasks/RT-20260816-003/jobs/AJ-RT-20260816-003-001.yaml": "683e16df5df6f21fcca978ba0cb524edd4c656328e3ee5cc16f72a0d6001d2b1",
    "research_control/tasks/RT-20260816-003/jobs/completions/AJC-AJ-RT-20260816-003-001.yaml": "d57a38bc92da622a962caf97d773e267a2385a34a085acb235a2973bb40c9a92",
    "research_control/tasks/RT-20260816-003/00_TASK.yaml": "5f9fba8ea445c118826f7cb896a054cf408320c13ede2ea1be8e3922d6c5b03c",
    "research_control/tasks/RT-20260816-003/DDR-20260816-003.md": "17db099c0c3023a0518c10557d28edaecd1ff0ea2720e90231d3f9a5c417296a",
    "research_control/tasks/RT-20260816-003/artifacts/v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_audit_v1.tex": "97eb186301e5600dbda55fdc3663a604f7380c9beb38eebee2419f706d8b212c",
    "research_control/tasks/RT-20260816-003/artifacts/v22_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_disposition_v1.yaml": "8cd3ebddce439157273a8d35afb52101060f872dfa3d268b10d2a493e791fbd2",
    "research_control/tasks/RT-20260816-003/artifacts/parent_fusion_notes_p4_t02_b2_proposal_only_measurable_fiber_occurrence_law_smuggling_audit.md": "0d8adbd8f0954131e045224f4e56c32c242ea80d916987df6ca17925099798d6",
    "research_control/handoffs/handoff-1046.yaml": "55ae7fa9e3ad39b6ab9a9ae630655834ace10c3026816fae357458859a9c8657",
    "research_control/handoffs/handoff-1046.md": "d02928b5179c32930bf832c5f4cb13edc5330c0895b0fe65a78e4b91a23875ce",
}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping in {path}")
    return data


def row(path: Path, key: str, value: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return next(item for item in csv.DictReader(handle) if item[key] == value)


def semantic_digest(data: dict[str, str], excluded: str) -> str:
    copy = dict(data)
    copy.pop(excluded)
    payload = json.dumps(copy, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    job_path = ROOT / "research_control/tasks/RT-20260816-003/jobs/AJ-RT-20260816-003-001.yaml"
    role_path = ROOT / "research_control/tasks/RT-20260816-003/roles/smuggling-auditor@0.2.0--RT-20260816-003.yaml"
    job = load_yaml(job_path)
    role = load_yaml(role_path)
    job_registry = row(ROOT / "registries/AGENT_JOB_REGISTRY.csv", "job_id", JOB_ID)
    role_registry = row(ROOT / "registries/ROLE_EXECUTION_REGISTRY.csv", "execution_role_ref", ROLE_REF)

    exact = {
        "job": job["allowed_write_paths"],
        "role": role["allowed_write_paths"],
        "agent_job_registry": job_registry["allowed_write_paths"].split(";"),
        "role_execution_registry": role_registry["allowed_write_paths"].split(";"),
    }

    checks: list[dict[str, Any]] = []

    def check(name: str, ok: bool, detail: Any) -> None:
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})

    for name, values in exact.items():
        check(f"{name}_ordered_allowlist", values == EXPECTED, {"count": len(values), "expected_count": 18})
    check("four_way_ordered_parity", len({tuple(values) for values in exact.values()}) == 1, "all four representations equal")
    check("immutable_agentjob_hash", sha(job_path) == PROTECTED_HASHES[str(job_path.relative_to(ROOT))], sha(job_path))
    check("corrected_role_hash", sha(role_path) == "aafa43d2b5b26f08f88f13a0691a507e3c74596e81af38da12bb4d5eac5a9738", sha(role_path))

    current_role = role_path.read_text(encoding="utf-8")
    exact_block = "".join(f'  - "{item}"\n' for item in EXPECTED[8:12])
    old_block = '  - "research_control/tasks/RT-20260721-009/artifacts/**"\n'
    reconstructed = current_role.replace(exact_block, old_block)
    check(
        "role_non_allowlist_bytes_preserved",
        hashlib.sha256(reconstructed.encode()).hexdigest() == "70f7c77e5d8ddd16df80feb874eadfa85fba752c935f561307fe6df43a5ddbbc",
        hashlib.sha256(reconstructed.encode()).hexdigest(),
    )
    check(
        "agentjob_registry_non_allowlist_fields_preserved",
        semantic_digest(job_registry, "allowed_write_paths") == "86e2079023c3f0fcc0b488b4f92df54e2612a335980b289a78a64b1d44fd8f3b",
        semantic_digest(job_registry, "allowed_write_paths"),
    )
    check(
        "role_registry_non_allowlist_fields_preserved",
        semantic_digest(role_registry, "allowed_write_paths") == "54729a7104c12fac326e644dda184ea6f385cd1d1ac6ca29422d6bddc95f36f5",
        semantic_digest(role_registry, "allowed_write_paths"),
    )
    check("wildcard_removed_from_repaired_representations", all("research_control/tasks/RT-20260721-009/artifacts/**" not in values for values in exact.values()), "permission narrowing only")

    for relative, expected_hash in PROTECTED_HASHES.items():
        actual = sha(ROOT / relative)
        check(f"protected::{relative}", actual == expected_hash, actual)

    adjacent = []
    for task_id in ("RT-20260815-007", "RT-20260815-009", "RT-20260816-001"):
        candidate = next((ROOT / "research_control/tasks" / task_id / "jobs").glob("AJ-*.yaml"))
        values = load_yaml(candidate)["allowed_write_paths"]
        adjacent.append(values[8:12] == EXPECTED[8:12])
    check("adjacent_current_v22_exact_path_controls", all(adjacent), {"controls": 3, "pass": sum(adjacent)})

    failed = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_id": "rt003_allowlist_parity_checkpoint_recovery_receipt_v1",
        "task_id": "RT-20260816-004",
        "job_id": "AJ-RT-20260816-004-001",
        "status": "PASS" if not failed else "FAIL",
        "source_head": "1aea0cbe89bdc37cf9f9630e51057833360fb18e",
        "source_tree": "445493a55d3593f6186d2233d4f6f50dc54a9de4",
        "expected_allowed_write_path_count": 18,
        "corrected_representation_count": 3,
        "protected_source_count": len(PROTECTED_HASHES),
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "failure_count": len(failed),
        "checks": checks,
        "science_changed": False,
        "refuter_stress_executed": False,
        "permission_broadened": False,
        "checkpoint_status": "PENDING_FRESH_RECOVERY_CHECKPOINT",
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
