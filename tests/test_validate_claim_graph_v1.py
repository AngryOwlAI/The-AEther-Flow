from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
SCRIPT_PATH = SCRIPT_DIR / "validate_claim_graph_v1.py"
CURRENT_GRAPH = REPO_ROOT / "output" / "claim_graph_v1.json"
BAD_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "research_control" / "claim_graph_v1_bad_missing_guards.json"


def load_module():
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location("validate_claim_graph_v1", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ClaimGraphV1ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_current_claim_graph_passes_validation_rules(self) -> None:
        report = self.module.validate_claim_graph_path(CURRENT_GRAPH)

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["error_count"], 0)
        self.assertTrue(report["no_physics_delta"])
        for result in report["rule_results"].values():
            self.assertEqual(result["status"], "PASS")

    def test_bad_fixture_fails_required_p12_t03_rules(self) -> None:
        report = self.module.validate_claim_graph_path(BAD_FIXTURE)
        codes = {error["code"] for error in report["errors"]}

        self.assertEqual(report["status"], "FAIL")
        self.assertIn("high_risk_positive_node_lacks_blocked_overread_edges", codes)
        self.assertIn("accepted_evidence_precondition_lacks_downstream_non_establishment", codes)
        self.assertIn("generated_derivative_lacks_is_derivative_of", codes)
        self.assertIn("gate_chair_node_lacks_exact_authority_path", codes)
        self.assertIn("benchmark_promotion_edge_lacks_protected_authority", codes)
        self.assertIn(
            "scoped_evidence_path_to_completed_derivation_lacks_required_intermediate_nodes",
            codes,
        )

    def test_cli_writes_report_for_current_graph(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "claim_graph_validation_report.json"
            code = self.module.main(["--graph", str(CURRENT_GRAPH), "--output", str(output)])

            self.assertEqual(code, 0)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["schema_id"], "claim_graph_validation_report_v1")

    def test_cli_expect_fail_accepts_bad_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "bad_fixture_report.json"
            code = self.module.main(
                [
                    "--graph",
                    str(BAD_FIXTURE),
                    "--output",
                    str(output),
                    "--expect-fail",
                ]
            )

            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
