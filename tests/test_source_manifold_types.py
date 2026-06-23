from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SourceManifoldTypesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.types = load_module("source_manifold_types", "source_manifold_types.py")

    def build_valid_law(self):
        t = self.types
        source = t.SourceToken("src-0")
        support = t.QuotientSupport("support-0", ("class-0",))
        carrier = t.SourceCarrier("carrier-0", (source,), (support,))
        chart = t.ChartCandidate("U0", support)
        cover = t.SourceCover("cover-0", carrier, (chart,))
        chart_support = t.ChartSupport(chart, support)
        transition = t.TransitionToken(
            "tau-0",
            chart_support,
            chart_support,
            inverse_check=t.InverseCheck("inverse-0", passes=True),
            cocycle_check=t.CocycleCheck("cocycle-0", passes=True),
        )
        regularity = t.make_regularity_certificate(
            certificate_id="reg-0",
            cover=cover,
            transitions=(transition,),
            evidence=(t.EvidenceKind.SOURCE_REGULARITY,),
        )
        readout = t.RespReadoutToken("resp-0", source)
        soldering_relation = t.SolderingRelation("solder-0", chart_support, readout)
        soldering = t.SolderingCertificate("solder-cert-0", soldering_relation)
        source_relation = t.SourceRelation(
            "eq-0",
            source,
            source,
            evidence=(t.EvidenceKind.SOURCE_EQUIVALENCE,),
        )
        variations = t.VariationFamily("var-0", cover, (source_relation,))
        return t.RegSoldLaw("RegSold-src-GSC-draft", regularity, soldering, variations)

    def test_required_abstract_interfaces_exist(self) -> None:
        required = [
            "SourceToken",
            "SourceCarrier",
            "SourceRelation",
            "SourceCover",
            "QuotientSupport",
            "ChartCandidate",
            "ChartSupport",
            "TransitionToken",
            "InverseCheck",
            "CocycleCheck",
            "RespReadoutToken",
            "SolderingRelation",
            "VariationFamily",
            "RegularityCertificate",
            "SolderingCertificate",
            "BottomCondition",
            "RegSoldLaw",
        ]
        for name in required:
            self.assertTrue(hasattr(self.types, name), name)

    def test_valid_reg_sold_law_reports_phase9_invariants(self) -> None:
        law = self.build_valid_law()
        self.assertEqual(law.claim_status, "proposal-only")
        self.assertFalse(law.adoption_authorized)
        self.assertEqual(
            set(self.types.check_reg_sold_law(law)),
            {
                "SepSrcNoTargetTopology",
                "ChartNamesAreNotCoordinates",
                "TransitionTokensAreNotSmoothMaps",
                "SolderingNoTargetMetric",
                "ValidationIsNotProof",
            },
        )

    def test_sep_src_rejects_target_topology(self) -> None:
        t = self.types
        source = t.SourceToken("src-1")
        support = t.QuotientSupport("support-1", ("class-1",))
        carrier = t.SourceCarrier("carrier-1", (source,), (support,))
        chart = t.ChartCandidate("U1", support)
        with self.assertRaisesRegex(t.SpecInvariantError, "SepSrcNoTargetTopology"):
            t.SourceCover(
                "bad-cover",
                carrier,
                (chart,),
                separation_evidence=(t.EvidenceKind.TARGET_TOPOLOGY,),
            )

    def test_chart_names_are_not_coordinates(self) -> None:
        t = self.types
        support = t.QuotientSupport("support-2", ("class-2",))
        chart = t.ChartCandidate("x", support)
        self.assertFalse(chart.is_coordinate_chart)
        with self.assertRaisesRegex(t.SpecInvariantError, "ChartNamesAreNotCoordinates"):
            t.ChartCandidate("x", support, coordinate_symbols=("x",))

    def test_transition_tokens_are_not_smooth_maps(self) -> None:
        t = self.types
        law = self.build_valid_law()
        transition = law.regularity.transitions[0]
        self.assertFalse(transition.implies_smooth_map)
        with self.assertRaisesRegex(t.SpecInvariantError, "TransitionTokensAreNotSmoothMaps"):
            t.TransitionToken(
                "tau-bad",
                transition.source,
                transition.target,
                differentiability_claim="C1",
            )

    def test_soldering_rejects_target_metric_inputs(self) -> None:
        t = self.types
        law = self.build_valid_law()
        with self.assertRaisesRegex(t.SpecInvariantError, "SolderingNoTargetMetric"):
            t.SolderingRelation(
                "solder-bad",
                law.soldering.soldering.support,
                law.soldering.soldering.readout,
                target_metric_id="g-eff",
            )
        with self.assertRaisesRegex(t.SpecInvariantError, "SolderingNoTargetMetric"):
            t.SolderingRelation(
                "solder-bad-2",
                law.soldering.soldering.support,
                law.soldering.soldering.readout,
                evidence=(t.EvidenceKind.PROPER_TIME,),
            )

    def test_validation_is_not_proof(self) -> None:
        t = self.types
        law = self.build_valid_law()
        self.assertFalse(t.validator_pass_can_instantiate_regularization(True))
        with self.assertRaisesRegex(t.SpecInvariantError, "ValidationIsNotProof"):
            t.regularity_certificate_from_validator_pass(
                certificate_id="reg-from-validator",
                cover=law.regularity.cover,
                transitions=law.regularity.transitions,
                validator_pass=True,
            )
        with self.assertRaisesRegex(t.SpecInvariantError, "ValidationIsNotProof"):
            t.make_regularity_certificate(
                certificate_id="reg-bad",
                cover=law.regularity.cover,
                transitions=law.regularity.transitions,
                evidence=(t.EvidenceKind.VALIDATOR_PASS,),
            )


if __name__ == "__main__":
    unittest.main()
