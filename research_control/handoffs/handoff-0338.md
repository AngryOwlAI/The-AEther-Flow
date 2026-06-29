<!-- authority: control -->

# Handoff 0338

V12 P4-T01 source-extension dependency extraction is complete.

The packet extracted and classified the dependency stack used by `Resp_lc`,
`M_src`, scoped `g_eff`, and matter-coupling precondition evidence under the
`matter_coupling` milestone. The task produced:

- `research_control/tasks/RT-20260629-043/artifacts/source_extension_dependency_extraction_v1.md`
- `research_control/tasks/RT-20260629-043/artifacts/source_extension_dependency_table_v1.yaml`

The extraction contains 22 dependency rows. The present categories are
`conditional_theorem_input`, `conservative_source_extension`,
`support_only_tooling_artifact`, and
`forbidden_target_import_if_used_physically`. No row is currently classified
as derived solely from current source ontology, a new source-law candidate, a
new ontology-primitive candidate, or unknown.

No compression, adoption, rejection, source-law adoption, `MetricData(E)`,
`g_eff` scope change, matter coupling, stress-energy semantics, Einstein
equations, benchmark promotion, or completed derivation is authorized by this
handoff.

The logical next step is P4-T02: one bounded `ontology-formalizer@0.2.0`
transaction to formalize the minimization target:

- `SourceExtensionStack_v1`
- `ExtensionDatum(E)`
- `DerivableDatum(E)`
- `ConservativeExtension(E)`
- `IrreduciblePrimitiveCandidate(E)`
- `TargetImportRisk(E)`
- `CompressionMap_v1`
- `MinimalSourceLawPackage_v1`
- `NoTargetImportPreservingCompression_v1`
- `CompressionFailureObstruction_v1`

P4-T02 must remain target formalization only. It must not decide compression,
construct a candidate, issue a Gate Chair verdict, or promote downstream GR
claims.
