#!/usr/bin/env python3
"""Support-only finite/local witness schema skeleton formalization.

This module encodes the v12 P6-T03 finite/local source-side witness schema as
deterministic project-control tooling. It has proof_authority=false. A passing
report is not canonical ontology, not source-law adoption, not MetricData(E),
not g_eff adoption or scope expansion, not matter coupling, not stress-energy
semantics, not Einstein equations, not benchmark promotion, and not completed
derivation.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


CHECKER_ID = "finite_local_witness_schema_support_formalization"
CHECKER_VERSION = "0.1.0"
PROOF_AUTHORITY = False
SUPPORT_ONLY = True

CURRENT_CHECKER_PATH = (
    "scripts/research_control/support_formalization/finite_toy_tag_obstruction.py"
)
CURRENT_CHECKER_HASH = (
    "f7a162ebf6ca259c27ab1d2e3e8f497038ce97d12e4a6a416b3231a091861444"
)
PARAMETERIZED_TARGET_PATH = (
    "research_control/tasks/RT-20260614-264/artifacts/"
    "293_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_P4_PARAMETERIZED_FINITE_LOCAL_"
    "SOURCE_FAMILY_TARGET_V1_FORMALIZATION.tex"
)
PARAMETERIZED_TARGET_OBJECT_ID = (
    "TEX-RESEARCH-CONTROL-NONBOTTOM-METRICDATA-WITNESS-SRC-GSC-P4-"
    "PARAMETERIZED-FINITE-LOCAL-SOURCE-FAMILY-TARGET-V1-FORMALIZATION"
)
PARAMETERIZED_TARGET_HASH = (
    "c58eeaa7d3c5f196003a95483aded24f4f6c06a37fb7b4ed4cfd3f81cebee59f"
)
PARAMETERIZED_WITNESS_PATH = (
    "research_control/tasks/RT-20260614-265/artifacts/"
    "294_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_P4_PARAMETERIZED_FINITE_LOCAL_"
    "SOURCE_FAMILY_WITNESS_V1.tex"
)
PARAMETERIZED_WITNESS_OBJECT_ID = (
    "TEX-RESEARCH-CONTROL-NONBOTTOM-METRICDATA-WITNESS-SRC-GSC-P4-"
    "PARAMETERIZED-FINITE-LOCAL-SOURCE-FAMILY-WITNESS-V1"
)
PARAMETERIZED_WITNESS_HASH = (
    "2c7b03be73dd23b6cdacdff4ce0ae078d10b3382c7bc2d71b4403713caa5f112"
)
PARAMETERIZED_GATE_REVIEW_PATH = (
    "research_control/tasks/RT-20260614-269/artifacts/"
    "298_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_P4_PARAMETERIZED_FINITE_LOCAL_"
    "SOURCE_FAMILY_WITNESS_V1_SOURCE_EXTENSION_EVIDENCE_GATE_CHAIR_REVIEW.tex"
)
PARAMETERIZED_GATE_REVIEW_OBJECT_ID = (
    "TEX-RESEARCH-CONTROL-NONBOTTOM-METRICDATA-WITNESS-SRC-GSC-P4-"
    "PARAMETERIZED-FINITE-LOCAL-SOURCE-FAMILY-WITNESS-V1-SOURCE-EXTENSION-"
    "EVIDENCE-GATE-CHAIR-REVIEW"
)
PARAMETERIZED_GATE_REVIEW_HASH = (
    "3c42fe6e5eae3bf6e26e29a2cfe341d72e873f71ca596edd0ba6c59ebd276fcd"
)

BOUNDARY_STATEMENT = (
    "This finite/local witness schema skeleton has proof_authority=false. It "
    "is support-only tooling and not canonical ontology adoption, not "
    "source-law adoption, not MetricData(E) adoption, not g_eff adoption or "
    "scope expansion, not coupling-law adoption, not matter coupling, not "
    "stress-energy semantics, not a stress-energy tensor, not detector "
    "semantics, not a matter action, not Einstein equations, not benchmark "
    "promotion, and not completed derivation."
)

FORMAL_OBJECTS = (
    "FiniteSourceIndexGraph",
    "SectorAssignment",
    "SourceTokenAssignment",
    "RelabelingMap",
    "RestrictionMap",
    "bridge_slot_compatibility_predicate",
    "no_target_import_certificate_predicate",
    "FailClosedBottomLabel",
    "SupportOnlyPassFailReport",
)

FAIL_CLOSED_BOTTOM_LABELS = (
    "OB-SCHEMA-NONUNIFORM-SECTOR-BEHAVIOR",
    "OB-SCHEMA-RELABELING-FAILURE",
    "OB-SCHEMA-VARIATION-INSTABILITY",
    "OB-SCHEMA-MISSING-MORPHISM-BEHAVIOR",
    "OB-SCHEMA-TARGET-IMPORT",
    "OB-SCHEMA-EVIDENCE-AS-ADOPTION",
)

FORBIDDEN_TARGET_IMPORT_TERMS = (
    "target topology",
    "target atlas",
    "target metric",
    "lorentzian signature",
    "proper time",
    "detector calibration",
    "empirical matter field",
    "stress-energy tensor",
    "stress-energy semantics",
    "matter action",
    "bianchi identity",
    "einstein equation",
    "benchmark fit",
    "generated derivative authority",
    "registry authority",
    "validator status as proof",
    "role authority as proof",
    "handoff status as proof",
    "approval status as proof",
    "local cache state as proof",
    "file order as proof",
    "commit status as proof",
)


@dataclass(frozen=True)
class FiniteSourceIndexGraph:
    """Finite source index graph, never a target topology or metric scaffold."""

    vertices: tuple[str, ...]
    arrows: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not self.vertices:
            raise ValueError("vertices must be nonempty")
        if len(set(self.vertices)) != len(self.vertices):
            raise ValueError("vertices must be unique")
        vertex_set = set(self.vertices)
        for source, target in self.arrows:
            if source not in vertex_set or target not in vertex_set:
                raise ValueError("arrows must use declared vertices")

    @classmethod
    def cycle(cls, size: int) -> "FiniteSourceIndexGraph":
        if size < 3:
            raise ValueError("cycle witness schema requires size >= 3")
        vertices = tuple(f"v{i}" for i in range(size))
        arrows = tuple((f"v{i}", f"v{(i + 1) % size}") for i in range(size))
        return cls(vertices=vertices, arrows=arrows)

    def to_dict(self) -> dict[str, Any]:
        return {
            "arrows": [list(arrow) for arrow in self.arrows],
            "vertices": list(self.vertices),
        }


@dataclass(frozen=True)
class SectorAssignment:
    """Assign exactly one source sector to every graph vertex."""

    by_vertex: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        vertices = [vertex for vertex, _sector in self.by_vertex]
        sectors = [sector for _vertex, sector in self.by_vertex]
        if len(set(vertices)) != len(vertices):
            raise ValueError("sector assignment vertices must be unique")
        if len(set(sectors)) != len(sectors):
            raise ValueError("sector labels must be unique")

    @classmethod
    def from_graph(cls, graph: FiniteSourceIndexGraph) -> "SectorAssignment":
        return cls(tuple((vertex, f"S_{vertex}") for vertex in graph.vertices))

    def sector_for(self, vertex: str) -> str:
        mapping = dict(self.by_vertex)
        if vertex not in mapping:
            raise KeyError(vertex)
        return mapping[vertex]

    def covers(self, graph: FiniteSourceIndexGraph) -> bool:
        return {vertex for vertex, _sector in self.by_vertex} == set(graph.vertices)

    def restrict(self, vertices: tuple[str, ...]) -> "SectorAssignment":
        wanted = set(vertices)
        return SectorAssignment(tuple(item for item in self.by_vertex if item[0] in wanted))

    def to_dict(self) -> dict[str, str]:
        return dict(self.by_vertex)


@dataclass(frozen=True)
class SourceTokenAssignment:
    """Finite source-token assignment by sector."""

    by_sector: tuple[tuple[str, tuple[str, ...]], ...]

    def __post_init__(self) -> None:
        sectors = [sector for sector, _tokens in self.by_sector]
        if len(set(sectors)) != len(sectors):
            raise ValueError("token assignment sectors must be unique")
        for sector, tokens in self.by_sector:
            if not tokens:
                raise ValueError(f"{sector} must have nonempty source tokens")

    @classmethod
    def from_sectors(cls, sectors: SectorAssignment) -> "SourceTokenAssignment":
        return cls(
            tuple(
                (
                    sector,
                    (
                        f"alpha_{vertex}",
                        f"beta_{vertex}",
                        f"flux_{vertex}",
                        f"quality_{vertex}",
                    ),
                )
                for vertex, sector in sectors.by_vertex
            )
        )

    def tokens_for_sector(self, sector: str) -> tuple[str, ...]:
        mapping = dict(self.by_sector)
        if sector not in mapping:
            raise KeyError(sector)
        return mapping[sector]

    def covers(self, sectors: SectorAssignment) -> bool:
        return {sector for sector, _tokens in self.by_sector} == {
            sector for _vertex, sector in sectors.by_vertex
        }

    def restrict(self, sectors: SectorAssignment) -> "SourceTokenAssignment":
        wanted = {sector for _vertex, sector in sectors.by_vertex}
        return SourceTokenAssignment(
            tuple(item for item in self.by_sector if item[0] in wanted)
        )

    def to_dict(self) -> dict[str, list[str]]:
        return {sector: list(tokens) for sector, tokens in self.by_sector}


@dataclass(frozen=True)
class RelabelingMap:
    """Declared source relabeling over vertices."""

    vertex_map: tuple[tuple[str, str], ...]

    @classmethod
    def cyclic_shift(cls, graph: FiniteSourceIndexGraph, shift: int = 1) -> "RelabelingMap":
        size = len(graph.vertices)
        return cls(
            tuple(
                (vertex, graph.vertices[(index + shift) % size])
                for index, vertex in enumerate(graph.vertices)
            )
        )

    def image_vertex(self, vertex: str) -> str:
        mapping = dict(self.vertex_map)
        if vertex not in mapping:
            raise KeyError(vertex)
        return mapping[vertex]

    def image_vertices(self, vertices: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(self.image_vertex(vertex) for vertex in vertices)

    def preserves_graph(self, graph: FiniteSourceIndexGraph) -> bool:
        vertex_set = set(graph.vertices)
        image_set = {target for _source, target in self.vertex_map}
        arrow_set = set(graph.arrows)
        mapped_arrows = {
            (self.image_vertex(source), self.image_vertex(target))
            for source, target in graph.arrows
        }
        return image_set == vertex_set and mapped_arrows == arrow_set

    def to_dict(self) -> dict[str, str]:
        return dict(self.vertex_map)


@dataclass(frozen=True)
class RestrictionMap:
    """Finite subgraph restriction map."""

    kept_vertices: tuple[str, ...]

    def restrict_graph(self, graph: FiniteSourceIndexGraph) -> FiniteSourceIndexGraph:
        wanted = set(self.kept_vertices)
        if not wanted <= set(graph.vertices):
            raise ValueError("restriction vertices must be graph vertices")
        return FiniteSourceIndexGraph(
            vertices=tuple(vertex for vertex in graph.vertices if vertex in wanted),
            arrows=tuple(
                arrow for arrow in graph.arrows if arrow[0] in wanted and arrow[1] in wanted
            ),
        )

    def relabeled(self, relabeling: RelabelingMap) -> "RestrictionMap":
        return RestrictionMap(relabeling.image_vertices(self.kept_vertices))

    def to_dict(self) -> dict[str, list[str]]:
        return {"kept_vertices": list(self.kept_vertices)}


@dataclass(frozen=True)
class NoTargetImportCertificate:
    """Predicate input naming the premises used by support-only schema checks."""

    premises: tuple[str, ...]

    def forbidden_hits(self) -> tuple[str, ...]:
        haystack = " ".join(self.premises).lower().replace("_", " ")
        return tuple(term for term in FORBIDDEN_TARGET_IMPORT_TERMS if term in haystack)

    def passes(self) -> bool:
        return not self.forbidden_hits()

    def to_dict(self) -> dict[str, Any]:
        return {
            "forbidden_hits": list(self.forbidden_hits()),
            "passes": self.passes(),
            "premises": list(self.premises),
        }


@dataclass(frozen=True)
class BridgeSlot:
    """Source-side bridge-slot compatibility skeleton."""

    interface_records: tuple[tuple[str, str], ...]
    quality_ledger_vertices: tuple[str, ...]
    finite_support: tuple[str, ...]
    relabeling_witness: str
    uniformity_witness: str
    source_balance_ledger: tuple[str, ...]
    no_target_import_certificate: NoTargetImportCertificate
    failure_labels: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "failure_labels": list(self.failure_labels),
            "finite_support": list(self.finite_support),
            "interface_records": [list(record) for record in self.interface_records],
            "no_target_import_certificate": self.no_target_import_certificate.to_dict(),
            "quality_ledger_vertices": list(self.quality_ledger_vertices),
            "relabeling_witness": self.relabeling_witness,
            "source_balance_ledger": list(self.source_balance_ledger),
            "uniformity_witness": self.uniformity_witness,
        }


@dataclass(frozen=True)
class FiniteLocalWitnessSchema:
    graph: FiniteSourceIndexGraph
    sector_assignment: SectorAssignment
    token_assignment: SourceTokenAssignment
    relabeling_map: RelabelingMap
    restriction_map: RestrictionMap
    bridge_slot: BridgeSlot

    def to_dict(self) -> dict[str, Any]:
        return {
            "bridge_slot": self.bridge_slot.to_dict(),
            "graph": self.graph.to_dict(),
            "relabeling_map": self.relabeling_map.to_dict(),
            "restriction_map": self.restriction_map.to_dict(),
            "sector_assignment": self.sector_assignment.to_dict(),
            "token_assignment": self.token_assignment.to_dict(),
        }


@dataclass(frozen=True)
class PropositionResult:
    proposition_id: str
    status: str
    message: str
    proof_authority: bool = PROOF_AUTHORITY
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence": self.evidence,
            "message": self.message,
            "proof_authority": self.proof_authority,
            "proposition_id": self.proposition_id,
            "status": self.status,
        }


@dataclass(frozen=True)
class SupportOnlyPassFailReport:
    checker_id: str
    checker_version: str
    status: str
    proposition_results: tuple[PropositionResult, ...]
    proof_authority: bool = PROOF_AUTHORITY
    support_only: bool = SUPPORT_ONLY
    boundary_statement: str = BOUNDARY_STATEMENT
    formal_objects: tuple[str, ...] = FORMAL_OBJECTS
    source_artifacts: tuple[dict[str, str], ...] = (
        {
            "object_id": "PY-SUPPORT-FORMALIZATION-FINITE-TOY-TAG-OBSTRUCTION",
            "path": CURRENT_CHECKER_PATH,
            "source_hash": CURRENT_CHECKER_HASH,
        },
        {
            "object_id": PARAMETERIZED_TARGET_OBJECT_ID,
            "path": PARAMETERIZED_TARGET_PATH,
            "source_hash": PARAMETERIZED_TARGET_HASH,
        },
        {
            "object_id": PARAMETERIZED_WITNESS_OBJECT_ID,
            "path": PARAMETERIZED_WITNESS_PATH,
            "source_hash": PARAMETERIZED_WITNESS_HASH,
        },
        {
            "object_id": PARAMETERIZED_GATE_REVIEW_OBJECT_ID,
            "path": PARAMETERIZED_GATE_REVIEW_PATH,
            "source_hash": PARAMETERIZED_GATE_REVIEW_HASH,
        },
    )
    forbidden_authority_flags: dict[str, bool] = field(
        default_factory=lambda: {
            "benchmark_promotion_authority": False,
            "canonical_ontology_adoption": False,
            "completed_derivation_claimed": False,
            "coupling_law_adopted": False,
            "downstream_gr_promotion_authorized": False,
            "einstein_equations_derived": False,
            "future_source_extension_impossibility_claimed": False,
            "g_eff_adopted": False,
            "geff_scope_changed": False,
            "global_theory_rejected": False,
            "matter_action_imported": False,
            "matter_coupling_adopted": False,
            "matter_coupling_derived": False,
            "metric_data_adopted": False,
            "source_law_adopted": False,
            "stress_energy_semantics_imported": False,
            "stress_energy_tensor_constructed": False,
            "target_metric_imported": False,
        }
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "boundary_statement": self.boundary_statement,
            "checker_id": self.checker_id,
            "checker_version": self.checker_version,
            "forbidden_authority_flags": self.forbidden_authority_flags,
            "formal_objects": list(self.formal_objects),
            "proof_authority": self.proof_authority,
            "proposition_results": [
                proposition.to_dict() for proposition in self.proposition_results
            ],
            "source_artifacts": list(self.source_artifacts),
            "status": self.status,
            "support_only": self.support_only,
        }


def sample_schema(size: int = 4) -> FiniteLocalWitnessSchema:
    graph = FiniteSourceIndexGraph.cycle(size)
    sectors = SectorAssignment.from_graph(graph)
    tokens = SourceTokenAssignment.from_sectors(sectors)
    relabeling = RelabelingMap.cyclic_shift(graph)
    restriction = RestrictionMap(("v0", "v1"))
    certificate = NoTargetImportCertificate(
        (
            "finite source index graph",
            "sector assignment",
            "source token assignment",
            "declared source relabeling map",
            "finite subgraph restriction map",
            "source bridge slot interface records",
            "no target import certificate",
            "fail closed bottom labels",
        )
    )
    bridge_slot = BridgeSlot(
        interface_records=graph.arrows,
        quality_ledger_vertices=graph.vertices,
        finite_support=("v0", "v1"),
        relabeling_witness="cyclic_shift_tau_1",
        uniformity_witness="one_source_rule_schema_for_all_sectors",
        source_balance_ledger=tuple(f"balance_{vertex}" for vertex in graph.vertices),
        no_target_import_certificate=certificate,
        failure_labels=FAIL_CLOSED_BOTTOM_LABELS,
    )
    return FiniteLocalWitnessSchema(
        graph=graph,
        sector_assignment=sectors,
        token_assignment=tokens,
        relabeling_map=relabeling,
        restriction_map=restriction,
        bridge_slot=bridge_slot,
    )


def finite_graph_schema_invariant(schema: FiniteLocalWitnessSchema) -> PropositionResult:
    graph = schema.graph
    if not schema.sector_assignment.covers(graph):
        return PropositionResult(
            proposition_id="finite_graph_schema_invariant",
            status="fail_sector_coverage",
            message="Sector assignment does not cover the graph vertices.",
        )
    if not schema.token_assignment.covers(schema.sector_assignment):
        return PropositionResult(
            proposition_id="finite_graph_schema_invariant",
            status="fail_token_coverage",
            message="Source token assignment does not cover declared sectors.",
        )
    return PropositionResult(
        proposition_id="finite_graph_schema_invariant",
        status="pass",
        message="Finite graph, sector assignment, and token assignment are coherent.",
        evidence={
            "arrow_count": len(graph.arrows),
            "sector_count": len(schema.sector_assignment.by_vertex),
            "token_assignment_count": len(schema.token_assignment.by_sector),
            "vertex_count": len(graph.vertices),
        },
    )


def relabeling_and_restriction_invariant(
    schema: FiniteLocalWitnessSchema,
) -> PropositionResult:
    if not schema.relabeling_map.preserves_graph(schema.graph):
        return PropositionResult(
            proposition_id="relabeling_and_restriction_invariant",
            status="fail_relabeling_not_graph_automorphism",
            message="Declared relabeling does not preserve graph arrows.",
        )
    restricted = schema.restriction_map.restrict_graph(schema.graph)
    relabeled_restriction = schema.restriction_map.relabeled(schema.relabeling_map)
    shifted = relabeled_restriction.restrict_graph(schema.graph)
    if len(restricted.vertices) != len(shifted.vertices):
        return PropositionResult(
            proposition_id="relabeling_and_restriction_invariant",
            status="fail_restriction_cardinality",
            message="Relabeled restriction changed finite subgraph cardinality.",
        )
    return PropositionResult(
        proposition_id="relabeling_and_restriction_invariant",
        status="pass",
        message="Relabeling preserves the graph and restriction remains finite/local.",
        evidence={
            "relabeled_restriction_vertices": list(shifted.vertices),
            "restriction_vertices": list(restricted.vertices),
        },
    )


def no_target_import_certificate_predicate(
    certificate: NoTargetImportCertificate,
) -> PropositionResult:
    hits = certificate.forbidden_hits()
    if hits:
        return PropositionResult(
            proposition_id="no_target_import_certificate_predicate",
            status="fail_target_import_detected",
            message="Certificate contains forbidden target or process-authority terms.",
            evidence={"forbidden_hits": list(hits)},
        )
    return PropositionResult(
        proposition_id="no_target_import_certificate_predicate",
        status="pass",
        message="Certificate premises contain no forbidden target-import terms.",
        evidence={"premise_count": len(certificate.premises)},
    )


def bridge_slot_compatibility_predicate(
    schema: FiniteLocalWitnessSchema,
) -> PropositionResult:
    slot = schema.bridge_slot
    graph = schema.graph
    certificate_result = no_target_import_certificate_predicate(
        slot.no_target_import_certificate
    )
    if certificate_result.status != "pass":
        return PropositionResult(
            proposition_id="bridge_slot_compatibility_predicate",
            status="fail_no_target_import_certificate",
            message="Bridge slot failed the no-target-import certificate predicate.",
            evidence=certificate_result.evidence,
        )
    if not set(slot.finite_support) <= set(graph.vertices):
        return PropositionResult(
            proposition_id="bridge_slot_compatibility_predicate",
            status="fail_support_outside_graph",
            message="Finite support includes vertices outside the source graph.",
            evidence={"finite_support": list(slot.finite_support)},
        )
    if set(slot.interface_records) != set(graph.arrows):
        return PropositionResult(
            proposition_id="bridge_slot_compatibility_predicate",
            status="fail_interface_records_mismatch",
            message="Interface records must match the declared source arrows.",
        )
    if set(slot.quality_ledger_vertices) != set(graph.vertices):
        return PropositionResult(
            proposition_id="bridge_slot_compatibility_predicate",
            status="fail_quality_ledger_mismatch",
            message="Quality ledger must cover every source vertex exactly once.",
        )
    if not set(slot.failure_labels) <= set(FAIL_CLOSED_BOTTOM_LABELS):
        return PropositionResult(
            proposition_id="bridge_slot_compatibility_predicate",
            status="fail_unknown_bottom_label",
            message="Bridge slot contains an unknown fail-closed label.",
        )
    return PropositionResult(
        proposition_id="bridge_slot_compatibility_predicate",
        status="pass",
        message="Bridge slot is source-local, certificate-backed, and fail-closed.",
        evidence={
            "failure_label_count": len(slot.failure_labels),
            "finite_support": list(slot.finite_support),
            "interface_record_count": len(slot.interface_records),
        },
    )


def run_formalization() -> SupportOnlyPassFailReport:
    schema = sample_schema()
    propositions = (
        finite_graph_schema_invariant(schema),
        relabeling_and_restriction_invariant(schema),
        no_target_import_certificate_predicate(
            schema.bridge_slot.no_target_import_certificate
        ),
        bridge_slot_compatibility_predicate(schema),
    )
    status = (
        "pass_support_only"
        if all(proposition.status == "pass" for proposition in propositions)
        else "fail_support_only"
    )
    return SupportOnlyPassFailReport(
        checker_id=CHECKER_ID,
        checker_version=CHECKER_VERSION,
        status=status,
        proposition_results=propositions,
    )


def write_json(path: Path, report: SupportOnlyPassFailReport) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the support-only finite/local witness schema formalization."
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    parser.add_argument("--json-output", type=Path, help="write JSON report to this path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_formalization()
    if args.json_output:
        write_json(args.json_output, report)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"{CHECKER_ID}: {report.status}")
    return 0 if report.status == "pass_support_only" else 1


if __name__ == "__main__":
    raise SystemExit(main())
