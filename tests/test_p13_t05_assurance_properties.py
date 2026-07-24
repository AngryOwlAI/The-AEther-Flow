from __future__ import annotations

import importlib.util
import json
import string
import sys
import unittest
from pathlib import Path
from typing import Any

from hypothesis import given, settings
from hypothesis import strategies as st

from scripts.validation import assurance, portability

REPO_ROOT = Path(__file__).resolve().parents[1]
GOAL_STATE_PATH = (
    REPO_ROOT / ".codex/skills/continue-research-goal/scripts/goal_state.py"
)
GOAL_STATE_SPEC = importlib.util.spec_from_file_location(
    "p13_t05_goal_state_properties",
    GOAL_STATE_PATH,
)
assert GOAL_STATE_SPEC is not None and GOAL_STATE_SPEC.loader is not None
goal_state = importlib.util.module_from_spec(GOAL_STATE_SPEC)
sys.modules[GOAL_STATE_SPEC.name] = goal_state
GOAL_STATE_SPEC.loader.exec_module(goal_state)

PROPERTY_SETTINGS = settings(max_examples=80, deadline=None, derandomize=True)
JSON_SCALARS = st.none() | st.booleans() | st.integers() | st.text(max_size=24)
JSON_VALUES: st.SearchStrategy[Any] = st.recursive(
    JSON_SCALARS,
    lambda children: st.lists(children, max_size=5)
    | st.dictionaries(st.text(max_size=16), children, max_size=5),
    max_leaves=20,
)
SAFE_COMPONENTS = st.text(
    alphabet=string.ascii_letters + string.digits + "_-",
    min_size=1,
    max_size=24,
).filter(lambda value: value.casefold() not in portability.WINDOWS_RESERVED)


class P13T05AssurancePropertyTests(unittest.TestCase):
    @PROPERTY_SETTINGS
    @given(JSON_VALUES)
    def test_goal_state_canonical_json_round_trip_is_stable(self, value: Any) -> None:
        encoded = goal_state.canonical_json_bytes(value)
        decoded = json.loads(encoded)
        self.assertEqual(goal_state.canonical_json_bytes(decoded), encoded)
        self.assertEqual(goal_state.sha256_json(decoded), goal_state.sha256_json(value))

    @PROPERTY_SETTINGS
    @given(
        st.dictionaries(st.text(min_size=1, max_size=12), JSON_SCALARS, max_size=8)
    )
    def test_goal_state_hash_is_invariant_to_mapping_insertion_order(
        self,
        value: dict[str, Any],
    ) -> None:
        reversed_value = dict(reversed(list(value.items())))
        self.assertEqual(
            goal_state.canonical_json_bytes(value),
            goal_state.canonical_json_bytes(reversed_value),
        )
        self.assertEqual(goal_state.sha256_json(value), goal_state.sha256_json(reversed_value))

    @PROPERTY_SETTINGS
    @given(
        st.lists(
            st.text(alphabet=string.hexdigits.lower(), min_size=64, max_size=64),
            max_size=12,
        ),
        st.text(alphabet=string.hexdigits.lower(), min_size=64, max_size=64),
    )
    def test_fingerprint_status_matches_ordered_history_contract(
        self,
        history: list[str],
        candidate: str,
    ) -> None:
        observed = goal_state.fingerprint_status(history, candidate)
        if history and history[-1] == candidate:
            expected = "unchanged"
        elif candidate in history:
            expected = "repeated"
        else:
            expected = "new"
        self.assertEqual(observed, expected)

    @PROPERTY_SETTINGS
    @given(st.lists(SAFE_COMPONENTS, min_size=1, max_size=4))
    def test_generated_bounded_relative_paths_are_portable(
        self,
        components: list[str],
    ) -> None:
        path = "/".join(components)
        self.assertLessEqual(len(path), portability.MAX_RELATIVE_PATH_CHARS)
        self.assertEqual(portability.lint_relative_path(path), ())

    @PROPERTY_SETTINGS
    @given(
        SAFE_COMPONENTS,
        st.sampled_from(sorted(portability.WINDOWS_FORBIDDEN)),
        SAFE_COMPONENTS,
    )
    def test_every_windows_forbidden_character_is_detected(
        self,
        prefix: str,
        forbidden: str,
        suffix: str,
    ) -> None:
        findings = portability.lint_relative_path(
            f"artifacts/{prefix}{forbidden}{suffix}.json"
        )
        self.assertIn(
            "windows_forbidden_character",
            {finding.code for finding in findings},
        )

    @PROPERTY_SETTINGS
    @given(SAFE_COMPONENTS)
    def test_casefold_collision_is_order_independent(self, component: str) -> None:
        upper = f"artifacts/{component.upper()}.json"
        lower = f"artifacts/{component.lower()}.json"
        if upper == lower:
            self.skipTest("generated spelling has no case distinction")
        forward = portability.casefold_collisions((upper, lower))
        reverse = portability.casefold_collisions((lower, upper))
        self.assertEqual(forward, reverse)
        self.assertEqual(len(forward), 1)

    @PROPERTY_SETTINGS
    @given(
        st.integers(min_value=1, max_value=10_000),
        st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    )
    def test_coverage_gate_is_exactly_monotone_at_its_floor(
        self,
        statements: int,
        observed: float,
        floor: float,
    ) -> None:
        report = {
            "totals": {
                "num_statements": statements,
                "num_branches": 0,
                "percent_covered": observed,
            }
        }
        result = assurance.evaluate_coverage(report, minimum_percent=floor)
        self.assertEqual(result["status"], "PASS" if observed >= floor else "FAIL")


if __name__ == "__main__":
    unittest.main()
