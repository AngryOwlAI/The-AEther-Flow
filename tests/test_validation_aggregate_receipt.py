from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.validation.aggregate import (
    AggregateReceiptError,
    aggregate_transaction_receipt,
    canonical_json,
    render_console_summary,
)


TREE_HASH = "git-tree-sha1:0123456789abcdef0123456789abcdef01234567"
ALL_OBLIGATIONS = (
    "role:validator",
    "skill:improve-project-system",
    "profile:checkpoint",
    "checkpoint:staged",
)


def gate_result(
    gate_id: str,
    *,
    status: str = "PASS",
    obligations: tuple[str, ...] = ALL_OBLIGATIONS,
    duration_seconds: float = 0.01,
    raw_artifact_ids: tuple[str, ...] = (),
) -> dict[str, object]:
    return {
        "gate_id": gate_id,
        "status": status,
        "severity": "blocking",
        "reason": "test_fixture",
        "exit_code": 0 if status not in {"FAIL", "BLOCKED_CONFIGURATION"} else 1,
        "duration_seconds": duration_seconds,
        "stdout_bytes": 8,
        "stderr_bytes": 2,
        "child_gates": [],
        "dependencies": [],
        "satisfied_obligations": list(obligations),
        "plan_reasons": ["profile:checkpoint"],
        "raw_artifact_ids": list(raw_artifact_ids),
        "cache_status": "HIT" if status == "CACHE_HIT" else "NOT_ELIGIBLE",
    }


def child_receipt(
    receipt_id: str,
    gates: list[dict[str, object]],
    *,
    status: str = "PASS",
    cancelled: bool = False,
) -> dict[str, object]:
    return {
        "receipt_id": receipt_id,
        "path": f".local/validation-receipts/{receipt_id}/receipt.json",
        "receipt": {
            "schema_id": "validation_execution_receipt_v1",
            "schema_version": 1,
            "run_id": receipt_id,
            "status": status,
            "cancelled": cancelled,
            "gate_results": gates,
        },
    }


def validation_plan(
    selected: tuple[str, ...] = ("gate_a",),
    *,
    skipped: tuple[str, ...] = ("gate_optional",),
    superseded: tuple[str, ...] = (),
) -> dict[str, object]:
    entries = [
        {
            "gate_id": gate_id,
            "status": "selected",
            "reasons": ["profile:checkpoint"],
            "satisfies_obligations": list(ALL_OBLIGATIONS),
        }
        for gate_id in selected
    ]
    entries.extend(
        {
            "gate_id": gate_id,
            "status": "skipped_not_applicable",
            "reasons": ["selection_predicate_not_satisfied"],
            "satisfies_obligations": [],
        }
        for gate_id in skipped
    )
    return {
        "schema_id": "validation_plan_v1",
        "manifest_hash": "sha256:" + "a" * 64,
        "requested_profile": "checkpoint",
        "effective_profile": "checkpoint",
        "changed_paths": ["scripts/validation/aggregate.py"],
        "blocked_paths": [],
        "path_tags": ["validation_runtime"],
        "ordered_gate_ids": list(selected),
        "selected_gate_ids": list(selected),
        "superseded_gate_ids": list(superseded),
        "skipped_gate_ids": list(skipped),
        "entries": entries,
        "execution_authority": "legacy",
        "status": "READY",
    }


def obligation_table(
    *,
    role_required: bool = True,
    role_condition_false: bool = False,
) -> list[dict[str, object]]:
    result = []
    for obligation_id in ALL_OBLIGATIONS:
        source_kind = obligation_id.split(":", 1)[0]
        required = role_required if source_kind == "role" else True
        result.append(
            {
                "obligation_id": obligation_id,
                "source_kind": source_kind,
                "required": required,
                "candidate_gate_ids": ["gate_a"],
                "condition_proven_false": (
                    role_condition_false if source_kind == "role" else False
                ),
                "condition_evidence": (
                    "The declared role condition evaluated false."
                    if source_kind == "role" and role_condition_false
                    else ""
                ),
            }
        )
    return result


def aggregate(
    *,
    plan: dict[str, object] | None = None,
    children: list[dict[str, object]] | None = None,
    obligations: list[dict[str, object]] | None = None,
    raw_artifacts: list[dict[str, object]] | None = None,
    artifact_root: Path = Path("."),
    residue: dict[str, object] | None = None,
    rollback: dict[str, object] | None = None,
    shadow: dict[str, object] | None = None,
) -> dict[str, object]:
    return aggregate_transaction_receipt(
        transaction_id="TX-P6-T08-TEST",
        mode="shadow",
        profile="checkpoint",
        scope="staged",
        base_ref="HEAD",
        staged_tree_hash=TREE_HASH,
        classification={
            "changed_paths": ["scripts/validation/aggregate.py"],
            "path_family_tags": ["validation_runtime"],
            "blocked_paths": [],
        },
        plan=plan or validation_plan(),
        child_receipts=children
        or [child_receipt("RUN-A", [gate_result("gate_a")])],
        obligations=obligations or obligation_table(),
        generator_changes=[
            {
                "generator_id": "memory_sync",
                "status": "UNCHANGED",
                "changed_paths": [],
                "before_tree_hash": TREE_HASH,
                "after_tree_hash": TREE_HASH,
            }
        ],
        raw_artifacts=raw_artifacts or [],
        artifact_root=artifact_root,
        residue=residue or {"status": "CLEAN", "paths": [], "evidence": "exact diff"},
        rollback=rollback
        or {
            "required": False,
            "performed": False,
            "authority": "legacy_checkpoint_index_owner",
            "changed_paths": [],
        },
        shadow_comparison=shadow
        or {
            "status": "MATCH",
            "legacy_status": "PASS",
            "planner_status": "PASS",
            "affected_blocking_gate_ids": ["gate_a"],
            "unexplained_mismatch": False,
            "evidence": "paired status fixture",
        },
    )


class AggregateTransactionReceiptTests(unittest.TestCase):
    def test_complete_receipt_covers_all_obligations_and_boundaries(self) -> None:
        receipt = aggregate()

        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["outcome"], "complete")
        self.assertEqual(receipt["counts"]["selected_gate_count"], 1)
        self.assertEqual(receipt["counts"]["executed_gate_count"], 1)
        self.assertEqual(receipt["obligation_coverage"]["counts"]["satisfied"], 4)
        self.assertEqual(
            receipt["obligation_coverage"]["counts"]["by_source_kind"],
            {"role": 1, "skill": 1, "profile": 1, "checkpoint": 1},
        )
        self.assertFalse(receipt["authority"]["physics_claim_authority"])
        self.assertFalse(receipt["authority"]["source_authoritative"])
        self.assertFalse(receipt["output_policy"]["raw_stdout_stderr_embedded"])

    def test_partial_receipt_fails_closed_when_selected_gate_is_unaccounted(self) -> None:
        plan = validation_plan(selected=("gate_a", "gate_b"))
        receipt = aggregate(
            plan=plan,
            children=[child_receipt("RUN-A", [gate_result("gate_a")])],
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["outcome"], "partial")
        self.assertEqual(receipt["plan"]["unaccounted_gate_ids"], ["gate_b"])
        self.assertIn(
            "SELECTED_GATE_UNACCOUNTED",
            {item["code"] for item in receipt["blockers"]},
        )

    def test_failed_child_controls_aggregate_status(self) -> None:
        plan = validation_plan(selected=("gate_a", "gate_b"))
        receipt = aggregate(
            plan=plan,
            children=[
                child_receipt(
                    "RUN-FAIL",
                    [
                        gate_result("gate_a"),
                        gate_result("gate_b", status="FAIL", obligations=()),
                    ],
                    status="FAIL",
                )
            ]
        )

        self.assertEqual(receipt["status"], "FAIL")
        self.assertEqual(receipt["outcome"], "failed")
        self.assertEqual(receipt["gate_results"][1]["status"], "FAIL")
        self.assertEqual(receipt["obligation_coverage"]["counts"]["blocked"], 0)

    def test_cancelled_child_is_explicit_and_blocking(self) -> None:
        receipt = aggregate(
            children=[
                child_receipt(
                    "RUN-CANCELLED",
                    [
                        gate_result(
                            "gate_a",
                            status="BLOCKED_CONFIGURATION",
                            obligations=(),
                        )
                    ],
                    status="BLOCKED_CONFIGURATION",
                    cancelled=True,
                )
            ]
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["outcome"], "cancelled")

    def test_cache_hit_is_successful_provider_and_counted(self) -> None:
        receipt = aggregate(
            children=[
                child_receipt(
                    "RUN-CACHE",
                    [gate_result("gate_a", status="CACHE_HIT")],
                )
            ]
        )

        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["outcome"], "complete")
        self.assertEqual(receipt["performance"]["cache_hits"], 1)
        self.assertEqual(receipt["obligation_coverage"]["counts"]["satisfied"], 4)

    def test_performed_rollback_is_preserved_and_blocks_completion(self) -> None:
        receipt = aggregate(
            rollback={
                "required": True,
                "performed": True,
                "authority": "legacy_checkpoint_index_owner",
                "reason": "scope_violation",
                "before_tree_hash": TREE_HASH,
                "after_tree_hash": TREE_HASH,
                "changed_paths": ["outside.txt"],
            }
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["outcome"], "rolled_back")
        self.assertTrue(receipt["rollback"]["performed"])
        self.assertEqual(receipt["rollback"]["changed_paths"], ["outside.txt"])

    def test_skipped_gate_cannot_satisfy_applicable_obligation(self) -> None:
        receipt = aggregate(
            children=[
                child_receipt(
                    "RUN-SKIP",
                    [
                        gate_result(
                            "gate_a",
                            status="SKIP_NOT_APPLICABLE",
                            obligations=ALL_OBLIGATIONS,
                        )
                    ],
                )
            ]
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(receipt["obligation_coverage"]["counts"]["satisfied"], 0)
        self.assertEqual(receipt["obligation_coverage"]["counts"]["blocked"], 4)
        self.assertIn(
            "OBLIGATION_INVALID_PROVIDER",
            {item["code"] for item in receipt["blockers"]},
        )

    def test_non_applicability_requires_condition_false_evidence(self) -> None:
        obligations = obligation_table(
            role_required=False,
            role_condition_false=True,
        )
        reduced = tuple(item for item in ALL_OBLIGATIONS if not item.startswith("role:"))
        receipt = aggregate(
            children=[
                child_receipt(
                    "RUN-CONDITION",
                    [gate_result("gate_a", obligations=reduced)],
                )
            ],
            obligations=obligations,
        )
        role_row = next(
            row
            for row in receipt["obligation_coverage"]["rows"]
            if row["source_kind"] == "role"
        )

        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(role_row["coverage_status"], "NOT_APPLICABLE_PROVEN")
        self.assertTrue(role_row["condition_proven_false"])

    def test_declared_supersedence_is_preserved_without_execution(self) -> None:
        plan = validation_plan(
            selected=("gate_a", "gate_old"),
            skipped=(),
            superseded=("gate_old",),
        )
        receipt = aggregate(
            plan=plan,
            children=[
                child_receipt(
                    "RUN-SUPERSEDED",
                    [
                        gate_result("gate_a"),
                        gate_result(
                            "gate_old",
                            status="SKIP_SUPERSEDED",
                            obligations=(),
                        ),
                    ],
                )
            ],
        )

        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["plan"]["superseded_gate_ids"], ["gate_old"])
        self.assertEqual(receipt["plan"]["executed_gate_ids"], ["gate_a"])
        self.assertIn("gate_old", receipt["plan"]["skipped_gate_ids"])

    def test_affected_shadow_mismatch_fails_closed(self) -> None:
        receipt = aggregate(
            shadow={
                "status": "MISMATCH",
                "legacy_status": "FAIL",
                "planner_status": "PASS",
                "affected_blocking_gate_ids": ["gate_a"],
                "unexplained_mismatch": True,
                "evidence": "paired comparison",
            }
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertIn(
            "SHADOW_BLOCKING_MISMATCH",
            {item["code"] for item in receipt["blockers"]},
        )

    def test_aggregation_is_independent_of_child_completion_order(self) -> None:
        plan = validation_plan(selected=("gate_a", "gate_b"))
        obligations = obligation_table()
        gate_a = gate_result("gate_a")
        gate_b = gate_result("gate_b", obligations=())
        first = aggregate(
            plan=plan,
            children=[
                child_receipt("RUN-B", [gate_b]),
                child_receipt("RUN-A", [gate_a]),
            ],
            obligations=obligations,
        )
        second = aggregate(
            plan=plan,
            children=[
                child_receipt("RUN-A", [gate_a]),
                child_receipt("RUN-B", [gate_b]),
            ],
            obligations=obligations,
        )

        self.assertEqual(canonical_json(first), canonical_json(second))
        self.assertEqual(
            [row["gate_id"] for row in first["gate_results"]],
            ["gate_a", "gate_b"],
        )
        self.assertEqual(
            [row["artifact_id"] for row in first["artifacts"]],
            ["child-receipt:RUN-A", "child-receipt:RUN-B"],
        )

    def test_child_and_raw_evidence_are_hashed_but_not_embedded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = Path("logs/gate-a.stdout")
            (root / path).parent.mkdir(parents=True)
            raw_content = b"raw validation stream content"
            (root / path).write_bytes(raw_content)
            child = child_receipt(
                "RUN-HASH",
                [
                    gate_result(
                        "gate_a",
                        raw_artifact_ids=("raw:gate_a:stdout",),
                    )
                ],
            )
            receipt = aggregate(
                children=[child],
                raw_artifacts=[
                    {
                        "artifact_id": "raw:gate_a:stdout",
                        "kind": "stdout_log",
                        "path": path.as_posix(),
                        "local_only": True,
                        "description": "Full raw stdout for gate_a.",
                    }
                ],
                artifact_root=root,
            )

        artifacts = {
            item["artifact_id"]: item for item in receipt["artifacts"]
        }
        self.assertEqual(
            artifacts["raw:gate_a:stdout"]["content_hash"],
            f"sha256:{hashlib.sha256(raw_content).hexdigest()}",
        )
        child_payload = child["receipt"]
        child_bytes = json.dumps(
            child_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        self.assertEqual(
            artifacts["child-receipt:RUN-HASH"]["content_hash"],
            f"sha256:{hashlib.sha256(child_bytes).hexdigest()}",
        )
        rendered = canonical_json(receipt)
        self.assertNotIn(raw_content.decode("utf-8"), rendered)
        self.assertNotIn('"receipt":', rendered)

    def test_blocking_child_cannot_be_overridden_by_declared_pass(self) -> None:
        receipt = aggregate(
            children=[
                child_receipt(
                    "RUN-MISMATCH",
                    [
                        gate_result(
                            "gate_a",
                            status="BLOCKED_CONFIGURATION",
                            obligations=(),
                        )
                    ],
                    status="PASS",
                )
            ]
        )

        self.assertEqual(receipt["status"], "BLOCKED_CONFIGURATION")
        self.assertIn(
            "CHILD_STATUS_MISMATCH",
            {item["code"] for item in receipt["blockers"]},
        )

    def test_console_is_bounded_and_complete_json_is_deterministic(self) -> None:
        receipt = aggregate(
            obligations=[
                {
                    "obligation_id": f"role:missing-{index}",
                    "source_kind": "role",
                    "required": True,
                    "candidate_gate_ids": ["gate_a"],
                    "condition_proven_false": False,
                    "condition_evidence": "",
                }
                for index in range(20)
            ]
        )
        output = render_console_summary(
            receipt,
            max_blockers=10,
            byte_budget=512,
        )

        self.assertLessEqual(len(output.encode("utf-8")), 512)
        self.assertEqual(canonical_json(receipt), canonical_json(receipt))
        self.assertIn('"schema_id":"validation_transaction_aggregate_receipt_v1"', canonical_json(receipt))

    def test_embedded_raw_stream_is_rejected_before_hashing(self) -> None:
        child = child_receipt("RUN-RAW", [gate_result("gate_a")])
        child["receipt"]["stdout"] = "forbidden raw stream"

        with self.assertRaisesRegex(AggregateReceiptError, "forbidden raw output"):
            aggregate(children=[child])

    def test_unknown_child_schema_is_rejected_fail_closed(self) -> None:
        child = child_receipt("RUN-UNKNOWN", [gate_result("gate_a")])
        child["receipt"]["schema_id"] = "unknown_receipt_v1"

        with self.assertRaisesRegex(AggregateReceiptError, "unsupported child receipt"):
            aggregate(children=[child])


if __name__ == "__main__":
    unittest.main()
