from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
FIXTURE_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260614-095"
    / "artifacts"
    / "finite_source_witness.yaml"
)


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FiniteSourceCoverModelCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checker = load_module(
            "finite_source_cover_model_checker",
            "finite_source_cover_model_checker.py",
        )
        cls.fixture = cls.checker.load_input(FIXTURE_PATH)

    def check(self, data):
        return self.checker.check_finite_source_cover(data)

    def test_clean_finite_local_witness_passes_candidate_local(self) -> None:
        result = self.check(copy.deepcopy(self.fixture))
        self.assertEqual(result.status, "pass_candidate_local")
        self.assertEqual(result.failures, [])
        self.assertIn("Sep_src", result.checked_objects)
        self.assertGreaterEqual(result.bottom_demonstrations_checked, 1)

    def test_nonseparation_fails(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["quotient_support"]["classes"][1]["members"] = list(
            data["quotient_support"]["classes"][0]["members"]
        )
        result = self.check(data)
        self.assertEqual(result.status, "fail_nonseparation")
        self.assertTrue(any(failure.check == "check_sep_src" for failure in result.failures))

    def test_transition_inverse_failure_is_reported(self) -> None:
        data = copy.deepcopy(self.fixture)
        for token in data["transition_tokens"]:
            if token["id"] == "tau_VU":
                token["relation"] = [["q0", "q1"], ["q1", "q0"]]
        result = self.check(data)
        self.assertEqual(result.status, "fail_transition_incoherent")
        self.assertTrue(
            any(failure.check == "check_inverse_tokens" for failure in result.failures)
        )

    def test_transition_cocycle_failure_is_reported(self) -> None:
        data = copy.deepcopy(self.fixture)
        for token in data["transition_tokens"]:
            if token["id"] == "tau_UW":
                token["relation"] = [["q0", "q1"], ["q1", "q0"]]
        result = self.check(data)
        self.assertEqual(result.status, "fail_transition_incoherent")
        self.assertTrue(
            any(failure.check == "check_cocycle_tokens" for failure in result.failures)
        )

    def test_soldering_nonuniqueness_fails(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["soldering"]["candidates"].append(
            {"resp_token": "r0", "chart_id": "chi_U_src", "support": ["q1"]}
        )
        result = self.check(data)
        self.assertEqual(result.status, "fail_soldering_nonunique")
        self.assertTrue(
            any(failure.check == "check_soldering_uniqueness" for failure in result.failures)
        )

    def test_variation_fragility_fails(self) -> None:
        data = copy.deepcopy(self.fixture)
        for variation in data["finite_variations"]:
            if variation["id"] == "var_merge_q0_q1":
                variation["result"] = "preserved_equivalently"
                variation["preserved_objects"] = ["Sep_src"]
        result = self.check(data)
        self.assertEqual(result.status, "fail_variation_fragile")
        self.assertTrue(
            any(failure.check == "check_variation_preservation" for failure in result.failures)
        )

    def test_target_metric_field_rejected(self) -> None:
        data = copy.deepcopy(self.fixture)
        data["soldering"]["target_metric_id"] = "g_eff"
        result = self.check(data)
        self.assertEqual(result.status, "fail_target_import")
        self.assertTrue(
            any(failure.check == "check_target_import_flags" for failure in result.failures)
        )

    def test_no_false_promotion_flags(self) -> None:
        result = self.check(copy.deepcopy(self.fixture))
        output = result.to_dict()
        self.assertEqual(
            output["checker_id"],
            "finite_source_cover_structural_support_checker",
        )
        self.assertEqual(
            output["checker_display_name"],
            "Finite source-cover structural support checker",
        )
        self.assertEqual(
            output["legacy_compatibility_ids"],
            ["finite_source_cover_model_checker"],
        )
        self.assertTrue(output["support_only"])
        self.assertFalse(output["proof_authority"])
        self.assertFalse(output["physics_claim_authority"])
        self.assertFalse(output["source_law_adoption_authority"])
        self.assertFalse(output["m_src_adoption_authority"])
        self.assertFalse(output["g_eff_authority"])
        self.assertFalse(output["benchmark_promotion_authority"])
        self.assertIn("proof_authority=false", output["boundary_statement"])

    def test_human_facing_name_is_support_calibrated(self) -> None:
        self.assertIn("structural support checker", self.checker.__doc__ or "")
        self.assertNotIn("model checker for", self.checker.__doc__ or "")
        self.assertEqual(
            self.checker.LEGACY_COMPATIBILITY_IDS,
            ("finite_source_cover_model_checker",),
        )


if __name__ == "__main__":
    unittest.main()
