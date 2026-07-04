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
        "render_dependency_graph",
        SCRIPT_DIR / "render_dependency_graph.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class DependencyGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph_module = load_module()

    def test_graph_includes_required_frontier_items_and_authority_boundary(self) -> None:
        graph = self.graph_module.build_graph(REPO_ROOT)
        labels = {node["label"] for node in graph["nodes"]}

        for required in (
            "Resp_lc",
            "M_src",
            "g_eff",
            "matter-coupling burden",
            "Einstein-equations burden",
            "benchmark-promotion burden",
            "finite toy metric response",
        ):
            self.assertIn(required, labels)

        self.assertTrue(any("B_E" in label for label in labels))
        self.assertTrue(any("BridgeCert" in label for label in labels))
        self.assertTrue(any("SEI-MC" in label for label in labels))
        self.assertTrue(any("SEI_src" in label for label in labels))
        self.assertTrue(graph["authority_boundary"]["navigational_support_only"])
        self.assertFalse(graph["authority_boundary"]["physics_claim_authority"])
        self.assertFalse(graph["authority_boundary"]["generated_graph_can_promote_claims"])

    def test_graph_edges_reference_existing_nodes(self) -> None:
        graph = self.graph_module.build_graph(REPO_ROOT)
        node_ids = {node["node_id"] for node in graph["nodes"]}
        for edge in graph["edges"]:
            self.assertIn(edge["source_id"], node_ids)
            self.assertIn(edge["target_id"], node_ids)
            self.assertIn(edge["edge_class"], self.graph_module.EDGE_CLASSES)
            self.assertTrue(edge["source_path"])
            self.assertTrue(edge["source_field"])

    def test_graph_rendering_is_deterministic_for_unchanged_state(self) -> None:
        graph_one = self.graph_module.build_graph(REPO_ROOT)
        graph_two = self.graph_module.build_graph(REPO_ROOT)
        payload_one = json.dumps(graph_one, indent=2, sort_keys=True)
        payload_two = json.dumps(graph_two, indent=2, sort_keys=True)
        self.assertEqual(
            hashlib.sha256(payload_one.encode("utf-8")).hexdigest(),
            hashlib.sha256(payload_two.encode("utf-8")).hexdigest(),
        )

    def test_freeze_summary_scopes_high_risk_accepted_label(self) -> None:
        summary = self.graph_module.freeze_criteria_summary(
            {
                "repeated_burden": True,
                "freeze_evaluation_required": True,
                "active_freeze_label": "COUPLING-LAW-CANDIDATE-EVIDENCE-ACCEPTED",
                "candidate_freeze_label": "COUPLING-LAW-CANDIDATE-POST-EVIDENCE-CRITERIA-MISSING",
                "prior_attempts_considered": ["RT-20260614-230", "RT-20260614-231"],
                "freeze_decision": "not_frozen",
                "next_allowed_route": "ontology_formalizer_positive_success_criteria",
            },
            "RT-20260614-235",
        )

        self.assertIn("scoped evidence/precondition status", summary)
        self.assertIn("not_frozen", summary)
        self.assertNotIn("EVIDENCE-ACCEPTED", summary)
        self.assertNotIn("True True", summary)

    def test_cli_writes_all_declared_formats(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            json_path = tmp_path / "graph.json"
            markdown_path = tmp_path / "graph.md"
            dot_path = tmp_path / "graph.dot"
            exit_code = self.graph_module.main(
                [
                    "--json",
                    json_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertIn("navigational support only", markdown_path.read_text(encoding="utf-8"))
            self.assertIn("navigational_support_only", dot_path.read_text(encoding="utf-8"))
            self.assertEqual(json.loads(json_path.read_text(encoding="utf-8"))["schema_id"], "research_dependency_graph_v1")

    def test_cli_check_passes_for_fresh_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            json_path = tmp_path / "graph.json"
            markdown_path = tmp_path / "graph.md"
            dot_path = tmp_path / "graph.dot"
            self.graph_module.main(
                [
                    "--json",
                    json_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                ]
            )

            exit_code = self.graph_module.main(
                [
                    "--check",
                    "--json",
                    json_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                ]
            )

            self.assertEqual(exit_code, 0)

    def test_cli_check_fails_for_stale_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            json_path = tmp_path / "graph.json"
            markdown_path = tmp_path / "graph.md"
            dot_path = tmp_path / "graph.dot"
            self.graph_module.main(
                [
                    "--json",
                    json_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                ]
            )
            markdown_path.write_text(
                markdown_path.read_text(encoding="utf-8") + "\nstale fixture\n",
                encoding="utf-8",
            )

            exit_code = self.graph_module.main(
                [
                    "--check",
                    "--json",
                    json_path.as_posix(),
                    "--markdown",
                    markdown_path.as_posix(),
                    "--dot",
                    dot_path.as_posix(),
                ]
            )

            self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
