<!-- authority: control -->

# P7-T06 source-kernel variational receipt

Task: `RT-20260728-005`
AgentJob: `AJ-RT-20260728-005-001`
Plan task: `P7-T06`
Candidate: `SourceKernelDirichletVariationalCandidate_v1`
Source-flux record: `SourceVariationalFluxRecord_v1`
Obstruction: `OBST-P7T06-DIRECTIONAL-KERNEL-NONVARIATIONAL-001`
Status: `draft/control`, `proposal-only`, `source-extension data`
Adoption: `blocked_adoption_open_continuation`

## Exact result

For each separately declared finite rational P7-T02 row kernel \(P\), the
task-local symmetric record \(C=(P+P^\mathsf T)/2\) defines
\[
\mathcal V_{\rm src}(q)
=\frac14\sum_{x,y}C_{xy}(q_y-q_x)^2.
\]
Its exact first variation is
\(L_Cq\), where \(L_C=\operatorname{Diag}(C\mathbf1)-C\). The edge record
\(J_{xy}=C_{xy}(q_x-q_y)\) is antisymmetric and gives exact total-cancellation
and finite-cut identities.

The fixed P7-T02 forward kernel has nonsymmetric \(I-P\), so the full
directional operator is not the standard-coordinate gradient of a scalar
quadratic on the same variables. This is a precise obstruction only in that
declared class. In general \(L_C\neq\operatorname{Sym}(I-P)\); the functional
also omits directional residue, diagonal holding weights, and degree
imbalance.

## Source hashes

| Source | SHA-256 |
| --- | --- |
| P7-T02 candidate TeX | `65ac095f5cdf4c2e319365c8b0e024d031b19d9fc2b8102e59997afa1e8f9129` |
| P7-T02 specification | `936d2aa6dfea3d263675468ff581190240efde84c1241ad971a8c1383a065a97` |
| P7-T02 controls | `af7fc976590b4ca82fca5c34c6f30091f6599428b8005cf3932ce03f92f7d779` |
| P7-T05 candidate TeX | `5a9a8f5542a7c8b714bbff7ec06c06449b0c66c0196266051562caf9ce602c6b` |
| P7-T05 specification | `75a3564fc0ea37ac776b2602c5f260514e5f48ae861ac049f87f9d92532f85db` |
| P7-T05 controls | `d8f8ceabbba294be8f268367d573e028774845f7d022e1b6c61a5e16623352dd` |
| P7-T05 completion | `8260dd09df7df6074e7c6990db86558ae4fe0fc9ea5d431edc09210e6d5386f7` |
| Handoff 0894 | `ad535ab39069b0d35845c3de0051b02ce55d4096e28b0f7ce48b434a90ba1d45` |
| P7-T06 candidate TeX | `386769e40167c35604625ef7250c027dc1712c82db4790e2895e0b31ac3cfbf7` |
| P7-T06 specification | `6d478d839aebad0d3a8ee74513f4de02a6c6a298a37a776bffe361adaa1377fb` |
| P7-T06 controls | `1c45bf7d031d040f33454f2508f2566ebbdb2bf62820ed5706089b12465a4a0e` |
| P7-T06 assumption table | `d004c7bbe2639daa021a25065455b7a73997f521b1e0c83457576285dcc4116f` |
| Mathematical child | `7dc4a3ff6200672d6a73e411d165542957d1a57dfaea5b1ad6af236fef8c98f3` |
| Philosophical child | `a8960a1d2cf3556524fbf31ec5e1506ac2800301ba711207f7e12cd0dd9b3cf4` |
| Parent conflict review | `8b115db1aee461ea7839948a97961bd54891c46a7a1a9eaf872f6f1bc7443ca2` |
| Parent fusion notes | `e08e6ca26e66540b70a15ef912b182d2c2ef6060ee1fe1a754215c2353c48926` |
| Task-local validation report | `ac2205324fc8e94c4f5155469b458ac46b32c2775c2585d4176bfe8b2bc0665c` |
| Compact receipt | `975b11749b2b5dd02bd3946203d9f4b2c18b2b932e0fc783d21b3bc52b61cd5d` |

## Validation

- Exact rational task-local checks: `PASS`, 164 of 164.
- Parent-child synthesis: two completed same-context reviews, ten resolved
  conflicts, zero unresolved conflicts.
- Scratch TeX build: bundled Tectonic `PASS`, six pages, references resolved,
  zero overfull boxes in the final run.
- Physical action claims: zero.
- Stress-energy claims: zero.
- Physical conservation-law claims: zero.
- Global no-go claims: zero.

Validation and compilation are operational evidence only. They do not create
theorem truth, physical interpretation, canonical ontology, source-law or
coupling-law adoption, proof, publication, benchmark promotion, checkpoint,
or completed-derivation authority.

## Remaining burden and route

Current ontology does not derive the variational selection rule, a lawful
treatment of the full directional residue, physical matter variables,
source-derived geometry, metric variation, stress energy, or a physical
symmetry/conservation theorem. P7-T05's universal selector obstruction also
remains open.

After one successful governed checkpoint, the bounded next route is P7-T07:
`smuggling-auditor@0.2.0` under `ontology-law-research-packet`, strategy
`audit_source_variational_matter_package_v1`.
