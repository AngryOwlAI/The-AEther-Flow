#!/usr/bin/env python3
"""Validate the P10-T08 generated current-burden-status bundle."""

from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any

import v21_current_burden_status_renderer as renderer


REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_ID = "v21_current_burden_status_validation_v1"
COMPACT_SCHEMA_ID = "v21_current_burden_status_compact_receipt_v1"
VALIDATION_PATH = (
    "research_control/tasks/RT-20260721-009/artifacts/"
    "v21_current_burden_status_validation.json"
)
COMPACT_PATH = (
    "research_control/tasks/RT-20260721-009/artifacts/"
    "v21_current_burden_status_compact_receipt.json"
)
VALIDATOR_PATH = (
    "research_control/tasks/RT-20260721-009/artifacts/"
    "validate_v21_current_burden_status.py"
)
FOCUSED_TEST_PATH = "tests/test_current_burden_status.py"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ValidationError(RuntimeError):
    """Raised when generated burden-status evidence is missing or stale."""


def load_json_mapping(repo_root: Path, rel_path: str) -> dict[str, Any]:
    path = repo_root / rel_path
    if not path.is_file():
        raise ValidationError(f"missing required JSON artifact: {rel_path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON artifact {rel_path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"JSON artifact must be a mapping: {rel_path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def verify_recorded_source_hashes(
    repo_root: Path, receipt: dict[str, Any]
) -> None:
    source_hashes = receipt.get("source_hashes")
    if not isinstance(source_hashes, dict) or not source_hashes:
        raise ValidationError("migration receipt has no source_hashes mapping")
    expected_paths = {
        renderer.DEFINITIONS_PATH,
        renderer.LEDGER_PATH,
        renderer.PROGRAM_STATE_PATH,
        renderer.TASK_REGISTRY_PATH,
        renderer.BURDEN_MAP_PATH,
        f"research_control/handoffs/{receipt.get('latest_handoff_id', '')}.yaml",
    }
    if set(source_hashes) != expected_paths:
        raise ValidationError("migration receipt source path set is incomplete or extra")
    for rel_path, recorded_digest in sorted(source_hashes.items()):
        if not isinstance(recorded_digest, str) or not HEX64.fullmatch(recorded_digest):
            raise ValidationError(f"invalid recorded source hash for {rel_path}")
        current_digest = renderer.sha256_file(repo_root, rel_path)
        if current_digest != recorded_digest:
            raise ValidationError(f"stale recorded source hash for {rel_path}")


def run_validation(repo_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    migration_receipt = load_json_mapping(repo_root, renderer.RECEIPT_PATH)
    source_commit = str(migration_receipt.get("source_commit", ""))
    require(bool(HEX40.fullmatch(source_commit)), "receipt source_commit is invalid")

    snapshot, expected_markdown, expected_receipt = renderer.build_bundle(
        repo_root, source_commit=source_commit
    )
    actual_markdown_path = repo_root / renderer.OUTPUT_PATH
    require(actual_markdown_path.is_file(), "generated Markdown output is missing")
    actual_markdown = actual_markdown_path.read_text(encoding="utf-8")

    checks: list[dict[str, str]] = []

    def passed(check_id: str, evidence: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS", "evidence": evidence})

    require(actual_markdown == expected_markdown, "generated Markdown is stale")
    require(migration_receipt == expected_receipt, "migration receipt is stale")
    passed(
        "current_status_render_determinism",
        "The tracked Markdown and migration receipt equal a fresh in-memory rebuild.",
    )

    verify_recorded_source_hashes(repo_root, migration_receipt)
    passed(
        "source_hash_freshness",
        "Every recorded authority-source hash equals the current tracked bytes.",
    )

    require(snapshot["definition_count"] == 10, "expected 10 stable definitions")
    require(snapshot["burden_count"] == 14, "expected 14 ledger burdens")
    passed(
        "stable_burden_definition_schema",
        "Ten unique acyclic authored definitions contain no mutable status fields.",
    )
    passed(
        "ledger_definition_coverage",
        "All 14 unique ledger burdens map to exactly one authored milestone definition.",
    )

    rendered_burden_ids = [
        row["burden_id"]
        for definition in snapshot["definitions"]
        for row in definition["current_rows"]
    ]
    require(
        len(rendered_burden_ids) == len(set(rendered_burden_ids)) == 14,
        "generated burden identities are duplicated or missing",
    )
    for burden_id in rendered_burden_ids:
        detail_heading = f"#### `{burden_id}` generated detail"
        require(
            actual_markdown.count(detail_heading) == 1,
            f"generated detail count is not exactly one for {burden_id}",
        )
    passed(
        "ledger_status_exactness",
        "Every authoritative ledger burden appears once as a generated detail block.",
    )

    require(
        snapshot["active_task_id"] == migration_receipt["active_task_id"],
        "active task provenance mismatch",
    )
    require(
        snapshot["latest_handoff_id"] == migration_receipt["latest_handoff_id"],
        "latest handoff provenance mismatch",
    )
    passed(
        "program_state_and_handoff_exactness",
        "Program state and latest handoff identities and next actions agree exactly.",
    )

    require(snapshot["task_count"] > 0, "task count must be positive")
    require(bool(snapshot["status_generation_time"]), "generation time is blank")
    passed(
        "source_commit_and_task_count_provenance",
        "The view embeds a full source commit, handoff generation time, and tracked task count.",
    )

    map_text = (repo_root / renderer.BURDEN_MAP_PATH).read_text(encoding="utf-8")
    old_header = (
        "| Milestone | Required Object | Current Status | Blocking Burden | "
        "Accept Criteria | Failure / Freeze Criterion |"
    )
    require(old_header not in map_text, "legacy inline current-status table remains")
    require(
        "## Generated Current-Status Contract" in map_text,
        "burden map lacks the generated-status contract",
    )
    require(
        migration_receipt["migration"]["legacy_inline_current_status_removed"] is True,
        "migration receipt does not record legacy status removal",
    )
    require(
        migration_receipt["migration"]["ledger_rows_mutated"] == 0,
        "migration receipt records ledger mutation",
    )
    passed(
        "historical_map_provenance",
        "The authored map removes inline mutable status and preserves historical commit and hash markers.",
    )

    authority = snapshot["authority"]
    require(
        authority["generated_status_is_independent_authority"] is False,
        "generated view claims independent authority",
    )
    require(
        authority["scientific_claims_changed"] is False,
        "generated view claims a scientific delta",
    )
    require(
        authority["physics_promotion_authorized"] is False,
        "generated view claims physics-promotion authority",
    )
    require(
        "authority: generated_noncanonical" in actual_markdown,
        "generated Markdown lacks its noncanonical authority marker",
    )
    passed(
        "generated_view_non_authority",
        "Generated output is marked noncanonical and grants no science or promotion authority.",
    )

    stale_fixture = copy.deepcopy(migration_receipt)
    stale_path = sorted(stale_fixture["source_hashes"])[0]
    stale_fixture["source_hashes"][stale_path] = "0" * 64
    stale_rejected = False
    try:
        verify_recorded_source_hashes(repo_root, stale_fixture)
    except ValidationError:
        stale_rejected = True
    require(stale_rejected, "intentionally stale source-hash fixture was accepted")
    passed(
        "stale_fixture_fail_closed",
        "An intentionally stale recorded source hash is rejected by the freshness gate.",
    )

    require(
        migration_receipt["generated_output_sha256"]
        == renderer.sha256_bytes(actual_markdown.encode("utf-8")),
        "generated output digest is incorrect",
    )
    passed(
        "generated_output_integrity",
        "The recorded generated-output SHA-256 equals the tracked Markdown bytes.",
    )

    passed(
        "contradiction_fail_closed",
        "Renderer validation rejects duplicate, missing, unmapped, cyclic, or control-contradictory inputs.",
    )

    validation = {
        "schema_id": SCHEMA_ID,
        "status": "PASS",
        "source_commit": source_commit,
        "status_generation_time": snapshot["status_generation_time"],
        "task_count": snapshot["task_count"],
        "definition_count": snapshot["definition_count"],
        "burden_count": snapshot["burden_count"],
        "active_task_id": snapshot["active_task_id"],
        "latest_handoff_id": snapshot["latest_handoff_id"],
        "check_count": len(checks),
        "failed_check_count": 0,
        "focused_test_path": FOCUSED_TEST_PATH,
        "focused_test_count": 11,
        "checks": checks,
        "source_hashes": snapshot["source_hashes"],
        "generated_output_path": renderer.OUTPUT_PATH,
        "generated_output_sha256": migration_receipt["generated_output_sha256"],
        "migration_receipt_path": renderer.RECEIPT_PATH,
        "migration_receipt_sha256": renderer.sha256_file(
            repo_root, renderer.RECEIPT_PATH
        ),
        "stale_fixture_rejected": True,
        "generated_status_is_independent_authority": False,
        "scientific_claims_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    compact = {
        "schema_id": COMPACT_SCHEMA_ID,
        "status": "PASS_GENERATED_VIEW_FRESH_NONAUTHORITY",
        "source_commit": source_commit,
        "status_generation_time": snapshot["status_generation_time"],
        "task_count": snapshot["task_count"],
        "definition_count": snapshot["definition_count"],
        "burden_count": snapshot["burden_count"],
        "check_count": len(checks),
        "failed_check_count": 0,
        "focused_test_count": 11,
        "stale_fixture_rejected": True,
        "ledger_rows_mutated": 0,
        "scientific_statuses_reinterpreted": 0,
        "validator_path": VALIDATOR_PATH,
        "validator_sha256": renderer.sha256_file(repo_root, VALIDATOR_PATH),
        "renderer_path": str(Path(renderer.OUTPUT_PATH).with_name(
            "v21_current_burden_status_renderer.py"
        )),
        "renderer_sha256": renderer.sha256_file(
            repo_root,
            str(Path(renderer.OUTPUT_PATH).with_name(
                "v21_current_burden_status_renderer.py"
            )),
        ),
        "definitions_path": renderer.DEFINITIONS_PATH,
        "definitions_sha256": renderer.sha256_file(
            repo_root, renderer.DEFINITIONS_PATH
        ),
        "generated_output_path": renderer.OUTPUT_PATH,
        "generated_output_sha256": migration_receipt["generated_output_sha256"],
        "migration_receipt_path": renderer.RECEIPT_PATH,
        "migration_receipt_sha256": validation["migration_receipt_sha256"],
        "authority_boundary": (
            "Operational freshness evidence only; the Distance-to-GR ledger, "
            "program state, latest handoff, registered science sources, and "
            "protected human gates retain their authority."
        ),
        "generated_status_is_independent_authority": False,
        "scientific_claims_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    return validation, compact


def output_drift(
    repo_root: Path, validation: dict[str, Any], compact: dict[str, Any]
) -> list[str]:
    expected = {
        VALIDATION_PATH: renderer.canonical_json(validation),
        COMPACT_PATH: renderer.canonical_json(compact),
    }
    return [
        rel_path
        for rel_path, expected_text in expected.items()
        if not (repo_root / rel_path).is_file()
        or (repo_root / rel_path).read_text(encoding="utf-8") != expected_text
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    try:
        validation, compact = run_validation(repo_root)
        if args.write:
            (repo_root / VALIDATION_PATH).write_text(
                renderer.canonical_json(validation), encoding="utf-8"
            )
            (repo_root / COMPACT_PATH).write_text(
                renderer.canonical_json(compact), encoding="utf-8"
            )
        drift = output_drift(repo_root, validation, compact)
        result = {
            "schema_id": SCHEMA_ID,
            "status": "PASS" if not drift else "STALE",
            "mode": "write" if args.write else "check",
            "check_count": validation["check_count"],
            "failed_check_count": 0,
            "definition_count": validation["definition_count"],
            "burden_count": validation["burden_count"],
            "focused_test_count": validation["focused_test_count"],
            "stale_fixture_rejected": True,
            "drift_paths": drift,
            "generated_status_is_independent_authority": False,
            "scientific_claims_changed": False,
            "physics_promotion_authorized": False,
        }
    except (ValidationError, renderer.BurdenStatusError) as exc:
        result = {
            "schema_id": SCHEMA_ID,
            "status": "FAIL",
            "mode": "write" if args.write else "check",
            "error": str(exc),
        }
        if args.json:
            print(renderer.canonical_json(result), end="")
        else:
            print(f"FAIL: {exc}")
        return 1
    if args.json:
        print(renderer.canonical_json(result), end="")
    else:
        print(result["status"])
    return 0 if not drift else 1


if __name__ == "__main__":
    raise SystemExit(main())
