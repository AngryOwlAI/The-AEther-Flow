#!/usr/bin/env python3
"""Validate the bounded v19 P10-T02 cache contract and review evidence."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
CONTRACT_PATH = ROOT / "research_control/design/validation_cache_contract_v1.md"
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
REVIEW_PATH = (
    ROOT
    / "research_control/tasks/RT-20260717-021/artifacts/cache_contract_review.yaml"
)

EXACT_TREE = {
    "classify_changes",
    "resolve_project_improvement",
    "project_improvement_signals",
    "documentation_impact",
    "documentation_surface_audit",
    "spec_depth",
    "publication_validation",
    "current_frontier_freshness",
    "compact_frontier_freshness",
    "dependency_graph_freshness",
    "task_index_freshness",
    "claim_graph_validation",
    "mermaid_sources",
}
SCHEDULED_BYPASS = {
    "memory_core",
    "research_control_core",
    "research_control_diff",
    "test_shard_repository",
    "claim_language_changed",
}
REQUIRED_THREATS = {
    "working_to_staged_reuse",
    "environment_drift",
    "implementation_change",
    "manifest_or_configuration_change",
    "corrupt_receipt",
    "partial_write",
    "missing_input_closure",
    "symlink_or_path_traversal",
    "final_safeguard_reuse",
}
REQUIRED_NEGATIVE_KEYS = {
    "working_to_staged",
    "environment_drift",
    "implementation_change",
    "manifest_change",
    "configuration_change",
    "dependency_change",
    "base_ref_change",
    "repository_change",
}
REQUIRED_CONTRACT_TEXT = (
    "# Validation cache contract v1",
    "active-contract-runtime-disabled",
    "cache_mode=off",
    "validation_cache_key_v1",
    "Working and staged scopes are different",
    "complete original `PASS` may be stored",
    "`git_diff_check` and `checkpoint_transaction` are unconditionally ineligible",
    ".local/validation-cache/v1/objects/",
    "maximum entry size: 16 MiB",
    "maximum entry count: 2,048",
    "maximum aggregate entry size: 512 MiB",
    "status: CACHE_HIT",
    "cache_status: HIT",
    "P10-T03 owns storage, lookup, integrity, and eviction implementation",
    "Physics, proof, benchmark, ontology, or Gate Chair authority created: `false`",
)


class ValidationError(RuntimeError):
    """Raised for one bounded contract-review failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=no_duplicate_object,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"{path.relative_to(ROOT)}: {exc}") from exc
    require(isinstance(payload, dict), f"{path.relative_to(ROOT)} must be an object")
    return payload


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def apply_overrides(payload: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    changed = copy.deepcopy(payload)
    for dotted_path, value in overrides.items():
        parts = dotted_path.split(".")
        target: dict[str, Any] = changed
        for part in parts[:-1]:
            child = target.get(part)
            require(isinstance(child, dict), f"override parent is not an object: {dotted_path}")
            target = child
        target[parts[-1]] = value
    return changed


def validate_sources(review: dict[str, Any]) -> dict[str, str]:
    rows = review.get("source_fingerprints")
    require(isinstance(rows, list) and rows, "source_fingerprints must be nonempty")
    observed: dict[str, str] = {}
    for row in rows:
        require(isinstance(row, dict), "source fingerprint row must be an object")
        path_text = row.get("path")
        expected = row.get("sha256")
        require(isinstance(path_text, str) and path_text, "source path must be nonblank")
        require(
            isinstance(expected, str) and len(expected) == 64,
            f"{path_text}: invalid SHA-256",
        )
        require(path_text not in observed, f"duplicate source fingerprint: {path_text}")
        path = ROOT / path_text
        require(path.is_file(), f"missing source fingerprint path: {path_text}")
        actual = sha256_path(path)
        require(actual == expected, f"{path_text}: source hash drift")
        observed[path_text] = actual
    require(
        "research_control/design/validation_cache_contract_v1.md" in observed,
        "contract source fingerprint is required",
    )
    require(
        "research_control/design/validation_gate_manifest_v1.yaml" in observed,
        "manifest source fingerprint is required",
    )
    return observed


def validate_gate_review(
    manifest: dict[str, Any], review: dict[str, Any]
) -> Counter[str]:
    gates = manifest.get("gates")
    rows = review.get("gate_reviews")
    require(isinstance(gates, list) and len(gates) == 37, "manifest must contain 37 gates")
    require(isinstance(rows, list) and len(rows) == 37, "review must contain 37 gates")

    manifest_ids = [gate.get("gate_id") for gate in gates]
    require(len(set(manifest_ids)) == 37, "manifest gate IDs must be unique")
    require(
        all(gate.get("cache_policy") == "ineligible" for gate in gates),
        "P10-T02 must leave every live manifest gate ineligible",
    )

    expected_policy = {
        gate_id: (
            "exact_tree"
            if gate_id in EXACT_TREE
            else "scheduled_bypass"
            if gate_id in SCHEDULED_BYPASS
            else "ineligible"
        )
        for gate_id in manifest_ids
    }
    counts: Counter[str] = Counter()
    for index, (gate, row) in enumerate(zip(gates, rows, strict=True)):
        require(row.get("manifest_index") == index, f"gate row {index}: wrong index")
        gate_id = gate["gate_id"]
        require(row.get("gate_id") == gate_id, f"gate row {index}: wrong gate ID")
        require(
            row.get("current_cache_policy") == gate["cache_policy"],
            f"{gate_id}: live cache policy mismatch",
        )
        policy = row.get("provisional_cache_policy")
        require(policy == expected_policy[gate_id], f"{gate_id}: wrong provisional policy")
        counts[policy] += 1
        require(isinstance(row.get("reason_code"), str), f"{gate_id}: missing reason")
        requirements = row.get("activation_requirements")
        require(isinstance(requirements, list), f"{gate_id}: requirements must be a list")

        if gate.get("mutating"):
            require(policy == "ineligible", f"{gate_id}: mutator cannot be cached")
        if "local_retrieval" in gate.get("scopes", []):
            require(policy == "ineligible", f"{gate_id}: local retrieval cannot be cached")
        if gate_id.startswith("profile_"):
            require(policy == "ineligible", f"{gate_id}: wrapper aggregate cannot be cached")
        if gate_id in {"git_diff_check", "checkpoint_transaction"}:
            require(policy == "ineligible", f"{gate_id}: final safeguard must be ineligible")

        if policy == "ineligible":
            require(
                row.get("determination") == "ineligible" and not requirements,
                f"{gate_id}: ineligible row cannot have activation requirements",
            )
        else:
            require(
                row.get("determination") == "candidate_not_activated",
                f"{gate_id}: candidate must remain not activated",
            )
            require(
                "later_manifest_activation" in requirements,
                f"{gate_id}: later manifest activation must be explicit",
            )
            require(not gate.get("mutating"), f"{gate_id}: candidate must be read-only")

    require(
        counts == Counter({"ineligible": 19, "exact_tree": 13, "scheduled_bypass": 5}),
        f"unexpected provisional counts: {dict(counts)}",
    )
    require(
        review.get("live_manifest_policy_count")
        == {"exact_tree": 0, "ineligible": 37, "scheduled_bypass": 0},
        "live manifest policy counts are wrong",
    )
    require(
        review.get("provisional_policy_count") == dict(counts),
        "provisional policy count receipt mismatch",
    )
    return counts


def validate_key_examples(review: dict[str, Any]) -> int:
    examples = review.get("key_examples")
    require(isinstance(examples, dict), "key_examples must be an object")
    baseline = examples.get("baseline")
    require(isinstance(baseline, dict), "baseline key example is required")
    material = baseline.get("key_material")
    require(isinstance(material, dict), "baseline key material must be an object")
    baseline_hash = canonical_hash(material)
    require(baseline.get("cache_key") == baseline_hash, "baseline key hash mismatch")

    positive = examples.get("positive_same_identity")
    require(isinstance(positive, dict), "positive key example is required")
    require(
        positive.get("copy_of") == "baseline"
        and positive.get("expected_relation") == "equal"
        and positive.get("cache_key") == baseline_hash,
        "positive same-identity example must preserve the key",
    )

    negative_rows = examples.get("negative_examples")
    require(isinstance(negative_rows, list), "negative key examples must be a list")
    observed_ids: set[str] = set()
    observed_hashes: set[str] = {baseline_hash}
    for row in negative_rows:
        require(isinstance(row, dict), "negative key row must be an object")
        example_id = row.get("example_id")
        require(isinstance(example_id, str), "negative key example ID is required")
        require(example_id not in observed_ids, f"duplicate negative example: {example_id}")
        observed_ids.add(example_id)
        overrides = row.get("overrides")
        require(isinstance(overrides, dict) and overrides, f"{example_id}: overrides required")
        variant_hash = canonical_hash(apply_overrides(material, overrides))
        require(row.get("cache_key") == variant_hash, f"{example_id}: key hash mismatch")
        require(
            row.get("expected_relation") == "different" and variant_hash != baseline_hash,
            f"{example_id}: variant must differ from baseline",
        )
        require(variant_hash not in observed_hashes, f"{example_id}: duplicate variant hash")
        observed_hashes.add(variant_hash)
    require(observed_ids == REQUIRED_NEGATIVE_KEYS, "negative key coverage is incomplete")
    return 2 + len(negative_rows)


def validate_threats(review: dict[str, Any]) -> int:
    rows = review.get("threat_analysis")
    require(isinstance(rows, list), "threat_analysis must be a list")
    ids: set[str] = set()
    for row in rows:
        require(isinstance(row, dict), "threat row must be an object")
        threat_id = row.get("threat_id")
        require(isinstance(threat_id, str), "threat ID is required")
        require(threat_id not in ids, f"duplicate threat ID: {threat_id}")
        ids.add(threat_id)
        require(row.get("status") == "PASS", f"{threat_id}: threat analysis did not pass")
        require(
            isinstance(row.get("prevented_by"), list) and row["prevented_by"],
            f"{threat_id}: prevention fields required",
        )
        require(
            isinstance(row.get("required_response"), str) and row["required_response"],
            f"{threat_id}: response required",
        )
    require(ids == REQUIRED_THREATS, "threat-analysis coverage is incomplete")
    return len(rows)


def main() -> int:
    manifest = load_json(MANIFEST_PATH)
    review = load_json(REVIEW_PATH)
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")

    require(review.get("schema_id") == "validation_cache_contract_review_v1", "bad review schema")
    require(review.get("schema_version") == 1, "bad review schema version")
    require(review.get("status") == "PASS", "review status must be PASS")
    require(review.get("live_manifest_mutated") is False, "live manifest mutation is forbidden")
    require(
        review.get("live_manifest_execution_authority") == "legacy",
        "legacy execution authority must remain active",
    )
    require(
        manifest.get("execution_authority") == "legacy",
        "manifest execution authority changed",
    )
    require(review.get("scientific_claims_changed") is False, "scientific claim change forbidden")
    require(
        review.get("physics_promotion_authorized") is False,
        "physics promotion is forbidden",
    )
    require(
        review.get("distance_to_gr_delta_changed") is False,
        "Distance-to-GR delta is forbidden",
    )
    require(review.get("next_plan_task_not_executed") == "P10-T03", "P10-T03 boundary missing")

    authority = review.get("authority")
    require(isinstance(authority, dict), "authority object required")
    require(authority.get("operational_validation_only") is True, "operational boundary required")
    require(
        all(value is False for key, value in authority.items() if key != "operational_validation_only"),
        "all authority flags except operational_validation_only must be false",
    )

    sources = validate_sources(review)
    counts = validate_gate_review(manifest, review)
    key_example_count = validate_key_examples(review)
    threat_count = validate_threats(review)

    for text in REQUIRED_CONTRACT_TEXT:
        require(text in contract_text, f"contract text missing: {text}")

    shadow = review.get("shadow_comparison")
    require(isinstance(shadow, dict), "shadow comparison object required")
    require(shadow.get("status") == "PASS", "shadow comparison must pass")
    require(shadow.get("unexplained_mismatch_count") == 0, "shadow mismatch must be zero")
    require(
        shadow.get("legacy_compatible_blocking_gate_count")
        == shadow.get("planner_blocking_gate_count"),
        "legacy and planner blocking counts must match",
    )

    result = {
        "schema_id": "validation_cache_contract_validation_v1",
        "schema_version": 1,
        "status": "PASS",
        "task_id": "RT-20260717-021",
        "job_id": "AJ-RT-20260717-021-001",
        "gate_count": 37,
        "live_manifest_cache_policy_counts": {
            "exact_tree": 0,
            "ineligible": 37,
            "scheduled_bypass": 0,
        },
        "provisional_cache_policy_counts": dict(sorted(counts.items())),
        "source_fingerprint_count": len(sources),
        "key_example_count": key_example_count,
        "threat_case_count": threat_count,
        "manifest_sha256": sha256_path(MANIFEST_PATH),
        "contract_sha256": sha256_path(CONTRACT_PATH),
        "review_sha256": sha256_path(REVIEW_PATH),
        "legacy_compatible_blocking_gate_count": shadow[
            "legacy_compatible_blocking_gate_count"
        ],
        "planner_blocking_gate_count": shadow["planner_blocking_gate_count"],
        "unexplained_mismatch_count": 0,
        "live_manifest_mutated": False,
        "cache_runtime_implemented": False,
        "cache_runtime_activated": False,
        "ordinary_research_handoff_preserved": "handoff-0740",
        "scientific_claims_changed": False,
        "physics_promotion_authorized": False,
        "distance_to_gr_delta_changed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        raise SystemExit(1) from exc
