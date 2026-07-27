"""Fail-closed ownership for the research-control test shards."""

from __future__ import annotations

from collections import Counter
import hashlib
import unittest

from tests import test_research_control
from tests import test_validate_research_control


EXPECTED_SOURCE_TEST_COUNT = 149
EXPECTED_SOURCE_TEST_SHA256 = "368163a3e8cc797da6e7b8ff96da0cddc40c75d84ae5533cb19a28529499b38e"
EXPECTED_SHARD_COUNTS = {
    "policy": 106,
    "active_state": 11,
    "continuation": 7,
    "checkpoint": 12,
    "metrics": 10,
    "live_integration": 3,
}
SHARD_NAMES = tuple(EXPECTED_SHARD_COUNTS)

SOURCE_CASES = (
    (
        "tests.test_research_control",
        test_research_control.ResearchControlTests,
    ),
    (
        "tests.test_validate_research_control",
        test_validate_research_control.ActiveStateSidecarValidatorTests,
    ),
)
CASE_BY_ID_PREFIX = {
    f"{module_name}.{case_type.__name__}": case_type
    for module_name, case_type in SOURCE_CASES
}


def _test_id(module_name: str, case_type: type[unittest.TestCase], method_name: str) -> str:
    return f"{module_name}.{case_type.__name__}.{method_name}"


def _research_control_id(method_name: str) -> str:
    return _test_id(
        "tests.test_research_control",
        test_research_control.ResearchControlTests,
        method_name,
    )


def _source_test_ids() -> tuple[str, ...]:
    return tuple(
        sorted(
            _test_id(module_name, case_type, method_name)
            for module_name, case_type in SOURCE_CASES
            for method_name, value in vars(case_type).items()
            if method_name.startswith("test_") and callable(value)
        )
    )


def _inventory_fingerprint(test_ids: tuple[str, ...]) -> str:
    return hashlib.sha256("\n".join(test_ids).encode("utf-8")).hexdigest()


SOURCE_TEST_IDS = _source_test_ids()
SOURCE_TEST_ID_SET = frozenset(SOURCE_TEST_IDS)
SOURCE_TEST_SHA256 = _inventory_fingerprint(SOURCE_TEST_IDS)

METRICS_TEST_IDS = frozenset(
    _research_control_id(name)
    for name in (
        "test_ai_methodology_dashboard_is_support_only_and_not_truth_ranking",
        "test_ai_methodology_metrics_are_support_only_and_separate",
        "test_payload_density_and_route_orbit_metrics_are_operational_only",
        "test_payload_density_warnings_are_advisory",
        "test_physics_progress_integration_metrics_count_required_packet_types",
        "test_physics_progress_metrics_markdown_renders_diagnostic_sections",
        "test_physics_progress_metrics_report_reads_tracked_completions",
        "test_physics_progress_metrics_separate_operational_and_scientific_scoreboards",
        "test_support_only_checker_metrics_are_operational_only",
        "test_support_only_checker_parse_errors_are_tooling_metrics",
    )
)

CONTINUATION_TEST_IDS = frozenset(
    _research_control_id(name)
    for name in (
        "test_continue_research_context_warnings_do_not_block_gate_chair_route",
        "test_continue_research_dependency_graph_summary_is_support_only",
        "test_continue_research_memory_preflight_refreshes_local_cache_warning",
        "test_continue_research_memory_preflight_skips_refresh_when_fresh",
        "test_continue_research_reports_director_context_packet",
        "test_continue_research_route_orbit_diagnostics_are_advisory",
        "test_resolve_latest_handoff",
    )
)

CHECKPOINT_TEST_IDS = frozenset(
    test_id
    for test_id in SOURCE_TEST_IDS
    if test_id.startswith(
        "tests.test_research_control.ResearchControlTests.test_checkpoint_"
    )
) | {
    _research_control_id("test_commit_message_uses_execution_role_ref"),
}

ACTIVE_STATE_TEST_IDS = frozenset(
    _research_control_id(name)
    for name in (
        "test_current_frontier_sync_accepts_synchronized_fixture",
        "test_current_frontier_sync_rejects_stale_active_burden_status",
        "test_current_frontier_sync_rejects_stale_active_task_snapshot",
        "test_role_registry_accepts_distinct_role_versions",
    )
) | frozenset(
    test_id
    for test_id in SOURCE_TEST_IDS
    if test_id.startswith(
        "tests.test_validate_research_control.ActiveStateSidecarValidatorTests."
    )
)

LIVE_INTEGRATION_TEST_IDS = frozenset(
    _research_control_id(name)
    for name in (
        "test_distance_to_gr_ledger_is_static_validated",
        "test_frontier_inventory_validator_accepts_live_inventory",
        "test_static_research_control_validation_passes",
    )
)

EXPLICIT_TEST_IDS = frozenset().union(
    ACTIVE_STATE_TEST_IDS,
    CONTINUATION_TEST_IDS,
    CHECKPOINT_TEST_IDS,
    METRICS_TEST_IDS,
    LIVE_INTEGRATION_TEST_IDS,
)
POLICY_TEST_IDS = SOURCE_TEST_ID_SET - EXPLICIT_TEST_IDS

SHARD_TEST_IDS = {
    "policy": tuple(sorted(POLICY_TEST_IDS)),
    "active_state": tuple(sorted(ACTIVE_STATE_TEST_IDS)),
    "continuation": tuple(sorted(CONTINUATION_TEST_IDS)),
    "checkpoint": tuple(sorted(CHECKPOINT_TEST_IDS)),
    "metrics": tuple(sorted(METRICS_TEST_IDS)),
    "live_integration": tuple(sorted(LIVE_INTEGRATION_TEST_IDS)),
}


def _validate_inventory() -> None:
    errors: list[str] = []
    if len(SOURCE_TEST_IDS) != EXPECTED_SOURCE_TEST_COUNT:
        errors.append(
            "source test count changed: "
            f"expected {EXPECTED_SOURCE_TEST_COUNT}, observed {len(SOURCE_TEST_IDS)}"
        )
    if SOURCE_TEST_SHA256 != EXPECTED_SOURCE_TEST_SHA256:
        errors.append(
            "source test fingerprint changed: "
            f"expected {EXPECTED_SOURCE_TEST_SHA256}, observed {SOURCE_TEST_SHA256}"
        )

    unknown_explicit = EXPLICIT_TEST_IDS - SOURCE_TEST_ID_SET
    if unknown_explicit:
        errors.append(f"shard map names unknown tests: {sorted(unknown_explicit)}")

    assigned_ids = [
        test_id
        for shard_name in SHARD_NAMES
        for test_id in SHARD_TEST_IDS[shard_name]
    ]
    duplicate_ids = sorted(
        test_id
        for test_id, count in Counter(assigned_ids).items()
        if count != 1
    )
    if duplicate_ids:
        errors.append(f"shard map has duplicate ownership: {duplicate_ids}")

    assigned_set = frozenset(assigned_ids)
    if assigned_set != SOURCE_TEST_ID_SET:
        errors.append(
            "shard map does not match the source inventory: "
            f"missing={sorted(SOURCE_TEST_ID_SET - assigned_set)} "
            f"extra={sorted(assigned_set - SOURCE_TEST_ID_SET)}"
        )

    observed_counts = {
        shard_name: len(test_ids)
        for shard_name, test_ids in SHARD_TEST_IDS.items()
    }
    if observed_counts != EXPECTED_SHARD_COUNTS:
        errors.append(
            "shard counts changed: "
            f"expected {EXPECTED_SHARD_COUNTS}, observed {observed_counts}"
        )

    if errors:
        raise RuntimeError("research-control shard inventory invalid: " + "; ".join(errors))


_validate_inventory()


def load_shard(
    loader: unittest.TestLoader,
    shard_name: str,
) -> unittest.TestSuite:
    """Build one shard from its exact frozen source-method ownership."""
    if shard_name not in SHARD_TEST_IDS:
        raise ValueError(f"unknown research-control shard: {shard_name}")
    suite = unittest.TestSuite()
    for test_id in SHARD_TEST_IDS[shard_name]:
        case_prefix, method_name = test_id.rsplit(".", 1)
        case_type = CASE_BY_ID_PREFIX[case_prefix]
        suite.addTest(case_type(method_name))
    return suite


def split_map() -> dict[str, object]:
    """Return the durable ownership payload used by task-local audit evidence."""
    return {
        "schema_id": "research_control_test_split_map_v1",
        "source_modules": [
            "tests.test_research_control",
            "tests.test_validate_research_control",
        ],
        "source_test_count": len(SOURCE_TEST_IDS),
        "source_test_sha256": SOURCE_TEST_SHA256,
        "shard_counts": {
            shard_name: len(test_ids)
            for shard_name, test_ids in SHARD_TEST_IDS.items()
        },
        "shards": {
            shard_name: list(test_ids)
            for shard_name, test_ids in SHARD_TEST_IDS.items()
        },
        "coverage": {
            "assigned_test_count": sum(
                len(test_ids) for test_ids in SHARD_TEST_IDS.values()
            ),
            "duplicate_test_count": 0,
            "missing_test_count": 0,
        },
    }
