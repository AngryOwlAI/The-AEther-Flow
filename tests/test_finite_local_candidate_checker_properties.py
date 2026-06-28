from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / "scripts"
    / "research_control"
    / "mechanized_checks"
    / "check_finite_local_candidate.py"
)
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "research_control" / "finite_local_candidate"
VALID_FIXTURE = FIXTURE_DIR / "valid_support_only.yaml"


def load_module():
    spec = importlib.util.spec_from_file_location("check_finite_local_candidate", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FiniteLocalCandidateCheckerPropertyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checker = load_module()
        cls.fixture = cls.checker.load_fixture(VALID_FIXTURE)

    def check(self, data):
        return self.checker.check_fixture(copy.deepcopy(data))

    def generated_fixture(self, size: int) -> dict:
        tokens = [f"tau_{index}" for index in range(size)]
        states = [f"sigma_{index}" for index in range(size)]
        sectors = [f"sector_{index}" for index in range(size)]
        return {
            "metadata": {
                "fixture_id": f"generated_support_only_{size}",
                "fixture_version": "0.1.0",
                "source_task_ids": ["RT-20260614-271"],
                "source_artifact_paths": [
                    "research_control/tasks/RT-20260614-270/artifacts/p5_t01_support_only_mechanization_boundary_design.md"
                ],
                "scope": "finite_local_source_side_support_only",
                "boundary_statement": self.checker.BOUNDARY_STATEMENT,
            },
            "source_family": {
                "parameters": [f"n={size}"],
                "sectors": sectors,
                "finite_local": True,
                "bottom_behavior": "fail_closed",
            },
            "source_objects": {
                "tokens": [
                    {"id": token, "sector": sector}
                    for token, sector in zip(tokens, sectors, strict=True)
                ],
                "states": [
                    {"id": state, "token": token}
                    for state, token in zip(states, tokens, strict=True)
                ],
                "carriers": [
                    {
                        "id": "carrier_all",
                        "tokens": tokens,
                        "states": states,
                    }
                ],
            },
            "relations": {
                "balance_predicates": [
                    {
                        "id": "balance_all",
                        "support_tokens": tokens,
                        "result": "balanced",
                    }
                ],
                "flux_ledger": [
                    {
                        "id": f"flux_{index}",
                        "source_state": states[index],
                        "target_state": states[(index + 1) % size],
                        "token": tokens[index],
                        "balance_id": "balance_all",
                    }
                    for index in range(size)
                ],
                "restriction_maps": [
                    {
                        "id": "restrict_all",
                        "domain": "carrier_all",
                        "codomain": "carrier_all",
                        "maps": [
                            *[{"from": token, "to": token} for token in tokens],
                            *[{"from": state, "to": state} for state in states],
                        ],
                    }
                ],
                "bottom_results": [
                    {
                        "id": "bottom_hidden_target",
                        "trigger": "hidden_target_import",
                        "result": "bottom",
                        "obstruction_label": "bottom",
                        "blocked_overread": [
                            "target_import_as_source_law",
                            "checker_failure_as_global_theorem",
                        ],
                    }
                ],
            },
            "boundary_markers": {
                "no_target_import": True,
                "bridge_compatibility": "scoped_source_extension_evidence_precondition_only",
                "scoped_geff_boundary": "no_adoption_no_scope_expansion",
                "evidence_not_adoption": True,
                "process_authority_not_proof": True,
            },
            "candidate": {
                "candidate_map": {
                    "id": "candidate_all",
                    "domain": tokens,
                    "codomain": states,
                },
                "certificate_object": {
                    "id": "certificate_all",
                    "references": ["candidate_all", "carrier_all"],
                },
                "obstruction_labels": ["none"],
            },
            "variation_relabeling": {
                "relabelings": [
                    {
                        "id": "cycle_all",
                        "domain": tokens,
                        "codomain": tokens,
                        "map": [
                            {"from": token, "to": tokens[(index + 1) % size]}
                            for index, token in enumerate(tokens)
                        ],
                    }
                ],
                "finite_variations": [
                    {
                        "id": "cycle_variation",
                        "relabeling_id": "cycle_all",
                        "result": "preserved",
                        "preserves": ["balance_all", "candidate_all"],
                    }
                ],
            },
            "forbidden_imports": {
                "target_metric": False,
                "target_atlas": False,
                "target_topology": False,
                "lorentzian_signature": False,
                "proper_time": False,
                "stress_energy_semantics": False,
                "stress_energy_tensor": False,
                "matter_action": False,
                "detector_semantics": False,
                "einstein_equations": False,
                "benchmark_success": False,
                "source_law_adoption": False,
                "MetricData_E_adoption": False,
                "g_eff_adoption": False,
            },
        }

    def test_generated_finite_families_remain_support_only(self) -> None:
        for size in range(1, 5):
            with self.subTest(size=size):
                report = self.check(self.generated_fixture(size))
                self.assertEqual(report.status, "pass_support_only")
                self.assertEqual(report.boundary_statement, self.checker.BOUNDARY_STATEMENT)
                self.assertEqual(report.forbidden_overread_flags, [])
                self.assertFalse(report.tooling_error)
                self.assertEqual(report.physics_obstruction, "")

    def test_permuting_finite_rows_preserves_status_and_predicates(self) -> None:
        data = copy.deepcopy(self.fixture)
        permuted = copy.deepcopy(self.fixture)
        permuted["source_family"]["sectors"] = list(reversed(permuted["source_family"]["sectors"]))
        permuted["source_objects"]["tokens"] = list(reversed(permuted["source_objects"]["tokens"]))
        permuted["source_objects"]["states"] = list(reversed(permuted["source_objects"]["states"]))
        permuted["relations"]["flux_ledger"] = list(reversed(permuted["relations"]["flux_ledger"]))
        permuted["candidate"]["candidate_map"]["domain"] = list(
            reversed(permuted["candidate"]["candidate_map"]["domain"])
        )
        permuted["candidate"]["candidate_map"]["codomain"] = list(
            reversed(permuted["candidate"]["candidate_map"]["codomain"])
        )

        original = self.check(data)
        shuffled = self.check(permuted)

        self.assertEqual(original.status, shuffled.status)
        self.assertEqual(
            [(result.predicate, result.status, result.status_code) for result in original.predicate_results],
            [(result.predicate, result.status, result.status_code) for result in shuffled.predicate_results],
        )
        self.assertEqual(original.forbidden_overread_flags, shuffled.forbidden_overread_flags)
        self.assertEqual(original.obstruction_labels, shuffled.obstruction_labels)

    def test_forbidden_import_surface_scan_fails_closed(self) -> None:
        forbidden_keys = [
            "target_metric",
            "target_atlas",
            "target_topology",
            "proper_time",
            "stress_energy_tensor",
            "matter_action",
            "detector_semantics",
            "einstein_equations",
            "benchmark_success",
            "MetricData_E_adoption",
            "g_eff_adoption",
            "matter_coupling",
        ]
        for key in forbidden_keys:
            with self.subTest(key=key):
                data = copy.deepcopy(self.fixture)
                data["candidate"][key] = "overread"
                report = self.check(data)
                self.assertEqual(report.status, "fail_target_import")
                self.assertTrue(report.forbidden_overread_flags)
                self.assertEqual(report.physics_obstruction, "")

    def test_status_priority_is_fail_closed_for_combined_overreads(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["candidate"]["target_metric"] = "g_eff"
        data["boundary_markers"]["scoped_geff_boundary"] = "adopted"
        data["boundary_markers"]["process_authority_not_proof"] = False
        report = self.check(data)
        self.assertEqual(report.status, "fail_target_import")
        self.assertIn("target_metric", report.forbidden_overread_flags)
        self.assertIn("geff_overread", report.forbidden_overread_flags)
        self.assertIn("process_authority_as_proof", report.forbidden_overread_flags)

    def test_malformed_references_take_priority_over_target_imports(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["source_objects"]["states"][0]["token"] = "missing_token"
        data["candidate"]["target_metric"] = "g_eff"
        report = self.check(data)
        self.assertEqual(report.status, "fail_malformed_fixture")
        self.assertIn("target_metric", report.forbidden_overread_flags)
        self.assertEqual(report.physics_obstruction, "")

    def test_bottom_branch_closes_empty_sector_without_promotion(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["source_family"]["sectors"].append("empty")
        data["relations"]["bottom_results"].append(
            {
                "id": "bottom_empty_sector",
                "trigger": "empty_sector:empty",
                "result": "bottom",
                "obstruction_label": "bottom",
                "blocked_overread": [
                    "bottom_branch_as_global_theorem",
                    "checker_failure_as_physics_obstruction",
                ],
            }
        )
        report = self.check(data)
        self.assertEqual(report.status, "pass_support_only")
        self.assertEqual(report.physics_obstruction, "")
        self.assertIn("bottom", report.obstruction_labels)

    def test_allowed_finite_variation_outcomes_are_closed(self) -> None:
        cases = [
            ("preserved", {"preserves": ["balance_pair"]}),
            ("bottom", {"obstruction_label": "bottom"}),
            ("controlled_obstruction", {"obstruction_label": "source_side_obstruction"}),
        ]
        for result, extra_fields in cases:
            with self.subTest(result=result):
                data = copy.deepcopy(self.fixture)
                variation = data["variation_relabeling"]["finite_variations"][0]
                variation["result"] = result
                variation.pop("preserves", None)
                variation.pop("obstruction_label", None)
                variation.update(extra_fields)
                report = self.check(data)
                predicate = next(
                    item
                    for item in report.predicate_results
                    if item.predicate == "finite_variations_have_allowed_results"
                )
                self.assertEqual(predicate.status, "pass")
                self.assertEqual(report.status, "pass_support_only")

    def test_generated_json_fixtures_have_byte_stable_cli_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            for size in range(1, 5):
                fixture_path = temp_path / f"generated_{size}.json"
                fixture_path.write_text(
                    json.dumps(self.generated_fixture(size), indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--fixture",
                    str(fixture_path),
                    "--json",
                ]
                first = subprocess.run(
                    command,
                    cwd=REPO_ROOT,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                second = subprocess.run(
                    command,
                    cwd=REPO_ROOT,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(first.stdout, second.stdout)
                parsed = json.loads(first.stdout)
                self.assertEqual(parsed["status"], "pass_support_only")
                self.assertEqual(parsed["boundary_statement"], self.checker.BOUNDARY_STATEMENT)


if __name__ == "__main__":
    unittest.main()
