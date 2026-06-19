<!-- authority: control -->

# Reader Scope Footer Relocation Phase 1 Guardrail

## Analysis

Phase 1 resolves the pattern ambiguity identified by Phase 0. The public page
corpus is not migrated in this packet.

The locked Markdown target is:

```markdown
## Reader Scope

Reader scope: ...

<!-- explainer-control: authority_footer -->
## Source Binding And Authority
```

The locked HTML target is:

```html
<section class="reader-scope" data-explainer-control="reader_scope" aria-labelledby="reader-scope-title">
  <h2 id="reader-scope-title">Reader Scope</h2>
  <p>Reader scope: ...</p>
</section>
</main>

<footer data-explainer-control="authority_footer">
```

## Decisions

- GitHub-facing Markdown must use an explicit `## Reader Scope` section on
  every page once that page enters the relocation migration.
- The Markdown `## Reader Scope` section must immediately precede
  `<!-- explainer-control: authority_footer -->`.
- The HTML `reader_scope` hook must be on a `section` element immediately above
  `footer[data-explainer-control="authority_footer"]`, with only optional
  `</main>` between the section and footer.
- The bottom Reader Scope block is a final boundary check, not a primary
  section-navigation destination. Navigation should omit it unless a
  page-specific source spec explicitly requires a visible route to the final
  boundary.
- The validator guard is opt-in during staged migration: legacy pages without
  `## Reader Scope` or `data-explainer-control="reader_scope"` remain valid
  until their migration phase declares the hook.

## Changes Made

- `research_control/design/github_facing_explainer_contract.md` now documents
  the bottom Markdown Reader Scope section and duplicate-top-scope guard.
- `research_control/design/html_explainer_flexible_presentation_contract.md`
  now documents the HTML `reader_scope` section hook and validator scope.
- `scripts/validate_publication_process.py` now validates the Markdown and HTML
  Reader Scope hook when a migrated page declares it.
- `scripts/project_control/audit_documentation_surfaces.py` mirrors the same
  guardrail for documentation-surface audits.
- `tests/test_publication_process_validation.py` and
  `tests/test_documentation_surface_audit.py` add focused acceptance and
  rejection coverage.

## Guardrail Semantics

The guard catches these regressions after a page opts into the new hook:

- more than one Markdown `## Reader Scope` section;
- a Markdown Reader Scope section without the authority-footer marker;
- a Markdown Reader Scope section that is not immediately above the
  authority-footer marker;
- top-positioned duplicate `Reader scope:` text above the declared Markdown
  Reader Scope section;
- an HTML `reader_scope` control placed on a non-section element;
- an HTML `reader_scope` section not immediately above the authority footer;
- a missing visible `Reader Scope` `h2` or `Reader scope:` boundary text; and
- duplicate visible `Reader scope:` text outside the HTML `reader_scope`
  section.

## Verification

Focused tests passed:

```zsh
.venv/bin/python -m unittest tests.test_publication_process_validation tests.test_documentation_surface_audit
```

Live publication validation passed before memory-registry refresh:

```zsh
.venv/bin/python scripts/validate_publication_process.py --root . --strict
```

The pre-refresh documentation-surface audit failed only on expected stale
hashes for the two edited control contracts. That is the expected state before
`bootstrap_memory_system.py` refreshes generated registry metadata.

## Boundaries Preserved

No publication briefs, source specs, GitHub-facing Markdown pages, tracked HTML
pages, role contracts, schema contracts, routing behavior, checkpoint behavior,
canonical science sources, ontology claims, benchmark claims, derivation
claims, or Gate Chair claims were modified.

## Logical Next Step

Phase 2 should migrate only the pilot pair, `project-overview` and
`source-authority`, to the explicit bottom Reader Scope hook and then run
screenshot QA.

## Source Materials

AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy and
generated-output boundaries].

AEther-Flow Project. (2026). `research_control/AGENTS.md` [Research-control
editing rules].

AEther-Flow Project. (2026).
`research_control/design/documentation_curator_reader_scope_footer_relocation_plan.md`
[Reader Scope footer relocation plan].

AEther-Flow Project. (2026).
`research_control/tasks/RT-20260619-011/artifacts/reader_scope_footer_relocation_phase0_audit.md`
[Phase 0 page-by-page audit].

AEther-Flow Project. (2026). `scripts/validate_publication_process.py`
[Publication-process validator].

AEther-Flow Project. (2026).
`scripts/project_control/audit_documentation_surfaces.py`
[Documentation-surface audit].
