from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.research_control.support_formalization import (
    finite_local_witness_schema as schema,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / "scripts"
    / "research_control"
    / "support_formalization"
    / "finite_local_witness_schema.py"
)


class FiniteLocalWitnessSchemaTests(unittest.TestCase):
    def test_sample_schema_contains_required_formal_objects(self) -> None:
        report = schema.run_formalization().to_dict()
        self.assertEqual(report["status"], "pass_support_only")
        self.assertFalse(report["proof_authority"])
        self.assertTrue(report["support_only"])
        for required in (
            "FiniteSourceIndexGraph",
            "SectorAssignment",
            "SourceTokenAssignment",
            "RelabelingMap",
            "RestrictionMap",
            "bridge_slot_compatibility_predicate",
            "no_target_import_certificate_predicate",
            "FailClosedBottomLabel",
            "SupportOnlyPassFailReport",
        ):
            self.assertIn(required, report["formal_objects"])

    def test_graph_sector_and_token_assignments_are_coherent(self) -> None:
        sample = schema.sample_schema(size=4)
        self.assertEqual(sample.graph.vertices, ("v0", "v1", "v2", "v3"))
        self.assertEqual(len(sample.graph.arrows), 4)
        self.assertTrue(sample.sector_assignment.covers(sample.graph))
        self.assertTrue(sample.token_assignment.covers(sample.sector_assignment))
        self.assertEqual(
            sample.token_assignment.tokens_for_sector("S_v0"),
            ("alpha_v0", "beta_v0", "flux_v0", "quality_v0"),
        )

    def test_relabeling_is_nontrivial_graph_automorphism(self) -> None:
        sample = schema.sample_schema(size=5)
        relabeling = sample.relabeling_map
        self.assertEqual(relabeling.image_vertex("v0"), "v1")
        self.assertTrue(relabeling.preserves_graph(sample.graph))
        self.assertNotEqual(relabeling.to_dict()["v0"], "v0")

    def test_restriction_remains_finite_and_relabels_locally(self) -> None:
        sample = schema.sample_schema(size=4)
        restricted = sample.restriction_map.restrict_graph(sample.graph)
        shifted = sample.restriction_map.relabeled(sample.relabeling_map).restrict_graph(
            sample.graph
        )
        self.assertEqual(restricted.vertices, ("v0", "v1"))
        self.assertEqual(restricted.arrows, (("v0", "v1"),))
        self.assertEqual(shifted.vertices, ("v1", "v2"))
        self.assertEqual(shifted.arrows, (("v1", "v2"),))

    def test_no_target_import_certificate_predicate_fails_closed(self) -> None:
        passing = schema.NoTargetImportCertificate(("source token", "source graph"))
        failing = schema.NoTargetImportCertificate(("source token", "target metric"))
        self.assertEqual(
            schema.no_target_import_certificate_predicate(passing).status,
            "pass",
        )
        failed = schema.no_target_import_certificate_predicate(failing)
        self.assertEqual(failed.status, "fail_target_import_detected")
        self.assertIn("target metric", failed.evidence["forbidden_hits"])

    def test_bridge_slot_compatibility_fails_closed_for_bad_support(self) -> None:
        sample = schema.sample_schema(size=4)
        bad_slot = schema.BridgeSlot(
            interface_records=sample.bridge_slot.interface_records,
            quality_ledger_vertices=sample.bridge_slot.quality_ledger_vertices,
            finite_support=("v0", "v_missing"),
            relabeling_witness=sample.bridge_slot.relabeling_witness,
            uniformity_witness=sample.bridge_slot.uniformity_witness,
            source_balance_ledger=sample.bridge_slot.source_balance_ledger,
            no_target_import_certificate=sample.bridge_slot.no_target_import_certificate,
            failure_labels=sample.bridge_slot.failure_labels,
        )
        bad_schema = schema.FiniteLocalWitnessSchema(
            graph=sample.graph,
            sector_assignment=sample.sector_assignment,
            token_assignment=sample.token_assignment,
            relabeling_map=sample.relabeling_map,
            restriction_map=sample.restriction_map,
            bridge_slot=bad_slot,
        )
        self.assertEqual(
            schema.bridge_slot_compatibility_predicate(bad_schema).status,
            "fail_support_outside_graph",
        )

    def test_report_blocks_authority_overread(self) -> None:
        output = schema.run_formalization().to_dict()
        self.assertIn("proof_authority=false", output["boundary_statement"])
        self.assertTrue(output["forbidden_authority_flags"])
        self.assertFalse(any(output["forbidden_authority_flags"].values()))
        self.assertEqual(len(output["source_artifacts"]), 4)
        paths = {artifact["path"] for artifact in output["source_artifacts"]}
        self.assertIn(schema.CURRENT_CHECKER_PATH, paths)
        self.assertIn(schema.PARAMETERIZED_WITNESS_PATH, paths)
        self.assertIn(schema.PARAMETERIZED_GATE_REVIEW_PATH, paths)

    def test_cli_json_output_is_deterministic(self) -> None:
        command = [sys.executable, str(SCRIPT_PATH), "--json"]
        first = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        second = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        self.assertEqual(first.stdout, second.stdout)
        parsed = json.loads(first.stdout)
        self.assertEqual(parsed["status"], "pass_support_only")

    def test_cli_json_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.json"
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--json-output",
                    str(report_path),
                    "--json",
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            parsed = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(parsed["checker_id"], schema.CHECKER_ID)
        self.assertEqual(parsed["status"], "pass_support_only")


if __name__ == "__main__":
    unittest.main()
