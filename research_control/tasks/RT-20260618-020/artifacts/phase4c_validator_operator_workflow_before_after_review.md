<!-- authority: control -->

# Phase 4C Validator And Operator Workflow Review

## Scope

Task `RT-20260618-020` migrated one public Documentation Curator publication
page:

- `validator-operator-workflow-explainer`

The packet did not edit canonical science, ontology, role contracts, schemas,
validators, routing behavior, signal registries, checkpoint behavior, command
semantics, tests, or physics claim status.

## Before

The active publication-process corpus had project-system improvement and
publication-process coverage, but no public operator guide explained which
checks to run for documentation, memory, project-control, research-control,
script, test, and tracked HTML work. Operators had to infer the chain from
root guidance, skill contracts, folder READMEs, validator scripts, and prior
task receipts.

## After

| Page | Improvement | Boundary Preserved |
| --- | --- | --- |
| Validator And Operator Workflow | Explains command selection by change type, bootstrap versus validate-only, publication checks, documentation-impact checks, research-control checks and `--check-diff`, unit-test triggers, screenshot evidence, troubleshooting, and PASS-result limits. | Does not change validator behavior, command semantics, schemas, routing, checkpoint gates, role authority, generated-output authority, or physics claim status. |

## Review Findings

- The page opens with the operator decision problem rather than source
  metadata.
- The page states generated noncanonical status early.
- The GitHub-facing Markdown reads as a native operator guide rather than an
  HTML transcript.
- The HTML derivative uses an annotated command matrix, decision path,
  troubleshooting guide, and evidence checklist.
- The page distinguishes bootstrap from validate-only and explains when each
  is insufficient by itself.
- The page states that PASS is deterministic evidence, not proof of scientific
  truth, ontology adoption, benchmark promotion, completed derivation, or
  publication taste.
- Source materials are named visibly in APA 7 style.
- HTML is standalone, no-network, and readable without JavaScript.

## Remaining Risks

- `.local` Obsidian and memory-index freshness warnings may remain after
  bootstrap. These are retrieval-layer warnings and not source authority.
- This page explains existing command behavior; it intentionally does not
  repair future validator implementation or test gaps.

## Recommendation

Seek explicit approval before Phase 5A:
`memory-system-explainer`.
