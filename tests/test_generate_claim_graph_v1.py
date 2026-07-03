from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module():
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(
        "generate_claim_graph_v1",
        SCRIPT_DIR / "generate_claim_graph_v1.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ClaimGraphV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph_module = load_module()

    def test_graph_includes_required_p12_t02_nodes(self) -> None:
        graph = self.graph_module.build_claim_graph(REPO_ROOT)
        labels = {node["label"] for node in graph["nodes"]}

        for required in (
            "M_src",
            "g_eff",
            "Resp_lc",
            "matter_coupling",
            "PositiveMSProfile_v1",
            "RR_ETransportCompletenessOrInvarianceLaw_v1",
            "RR_E separation obstruction",
            "Einstein equations",
            "benchmark promotion",
            "NarrowMSCertEq_v1",
        ):
            self.assertIn(required, labels)

    def test_high_risk_overreads_are_negative_or_guarded(self) -> None:
        graph = self.graph_module.build_claim_graph(REPO_ROOT)
        nodes_by_id = {node["node_id"]: node for node in graph["nodes"]}
        physical_targets = {
            "blocked-target-matter-coupling",
            "blocked-target-einstein-equations",
            "blocked-target-benchmark-promotion",
        }

        for target_id in physical_targets:
            target_node = nodes_by_id[target_id]
            self.assertTrue(target_node["overread_guards"])
            incoming = [
                edge
                for edge in graph["edges"]
                if edge["target_node_id"] == target_id
                and edge["edge_type"] in {"does_not_establish", "blocks", "requires_human_gate"}
            ]
            self.assertTrue(incoming, target_id)

        for node in graph["nodes"]:
            self.assertFalse(node["scientific_proof_authority"])

        self.assertFalse(graph["claim_boundary"]["graph_is_proof_authority"])
        self.assertFalse(graph["claim_boundary"]["graph_changes_scientific_claims"])
        self.assertFalse(graph["claim_boundary"]["graph_promotes_status"])

    def test_rendering_is_deterministic_for_unchanged_sources(self) -> None:
        graph_one = self.graph_module.build_claim_graph(REPO_ROOT)
        graph_two = self.graph_module.build_claim_graph(REPO_ROOT)
        payload_one = json.dumps(graph_one, indent=2, sort_keys=True)
        payload_two = json.dumps(graph_two, indent=2, sort_keys=True)
        self.assertEqual(
            hashlib.sha256(payload_one.encode("utf-8")).hexdigest(),
            hashlib.sha256(payload_two.encode("utf-8")).hexdigest(),
        )

    def test_cli_writes_declared_outputs_and_check_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            json_path = tmp_path / "claim_graph.json"
            dot_path = tmp_path / "claim_graph.dot"
            markdown_path = tmp_path / "claim_graph.md"

            exit_code = self.graph_module.main(
                [
                    "--json",
                    json_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                ]
            )
            self.assertEqual(exit_code, 0)
            self.assertEqual(
                json.loads(json_path.read_text(encoding="utf-8"))["claim_graph_schema_id"],
                "claim_graph_schema_v1",
            )
            self.assertIn("digraph claim_graph_v1", dot_path.read_text(encoding="utf-8"))
            self.assertIn("High-Risk Non-Establishment", markdown_path.read_text(encoding="utf-8"))

            check_code = self.graph_module.main(
                [
                    "--check",
                    "--json",
                    json_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                ]
            )
            self.assertEqual(check_code, 0)


if __name__ == "__main__":
    unittest.main()
