from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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

    def test_snapshot_is_immutable_and_loads_each_source_once(self) -> None:
        instrumentation = self.graph_module.GraphInstrumentation()
        snapshot = self.graph_module.load_graph_input_snapshot(
            REPO_ROOT,
            registry_paths=(
                f"registries/{name}" for name in self.graph_module.REGISTRY_SPECS
            ),
            instrumentation=instrumentation,
        )

        self.assertEqual(instrumentation.source_loads, len(snapshot.sources))
        self.assertTrue(instrumentation.source_loads_by_path)
        self.assertEqual(set(instrumentation.source_loads_by_path.values()), {1})
        with self.assertRaises(TypeError):
            snapshot.sources["new"] = object()
        with self.assertRaises(TypeError):
            snapshot.source_hashes["new"] = "not-allowed"
        program_state = snapshot.sources["research_control/program_state.yaml"].payload
        with self.assertRaises(TypeError):
            program_state["active_task_id"] = "not-allowed"

    def test_snapshot_build_and_repeated_rendering_perform_no_file_reads(self) -> None:
        instrumentation = self.graph_module.GraphInstrumentation()
        snapshot = self.graph_module.load_graph_input_snapshot(
            REPO_ROOT,
            registry_paths=(
                f"registries/{name}" for name in self.graph_module.REGISTRY_SPECS
            ),
            instrumentation=instrumentation,
        )
        loads_after_snapshot = instrumentation.source_loads

        with (
            mock.patch.object(Path, "read_bytes", side_effect=AssertionError("unexpected read_bytes")),
            mock.patch.object(Path, "read_text", side_effect=AssertionError("unexpected read_text")),
            mock.patch.object(Path, "open", side_effect=AssertionError("unexpected open")),
        ):
            graph = self.graph_module.build_graph(
                REPO_ROOT,
                snapshot=snapshot,
                instrumentation=instrumentation,
            )
            first = (
                self.graph_module.render_json(graph, instrumentation),
                self.graph_module.render_markdown(graph, instrumentation),
                self.graph_module.render_dot(graph, instrumentation),
            )
            second = (
                self.graph_module.render_json(graph, instrumentation),
                self.graph_module.render_markdown(graph, instrumentation),
                self.graph_module.render_dot(graph, instrumentation),
            )

        self.assertEqual(first, second)
        self.assertEqual(instrumentation.source_loads, loads_after_snapshot)
        self.assertEqual(instrumentation.graph_builds, 1)
        self.assertEqual(instrumentation.render_calls, 6)
        self.assertEqual(
            instrumentation.renders_by_format,
            {"json": 2, "markdown": 2, "dot": 2},
        )

    def test_implicit_and_explicit_snapshot_apis_are_byte_identical(self) -> None:
        snapshot = self.graph_module.load_graph_input_snapshot(
            REPO_ROOT,
            registry_paths=(
                f"registries/{name}" for name in self.graph_module.REGISTRY_SPECS
            ),
        )
        implicit_graph = self.graph_module.build_graph(REPO_ROOT)
        snapshot_graph = self.graph_module.build_graph(REPO_ROOT, snapshot=snapshot)

        self.assertEqual(implicit_graph, snapshot_graph)
        self.assertEqual(
            self.graph_module.render_json(implicit_graph),
            self.graph_module.render_json(snapshot_graph),
        )
        self.assertEqual(
            self.graph_module.render_markdown(implicit_graph),
            self.graph_module.render_markdown(snapshot_graph),
        )
        self.assertEqual(
            self.graph_module.render_dot(implicit_graph),
            self.graph_module.render_dot(snapshot_graph),
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
