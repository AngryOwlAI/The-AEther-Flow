<!-- authority: explanatory -->

# Phase 3 Research-Control Operation Footer-Authority Review

## Scope

This review covers the four Phase 3 post-migration quality pages:

- `github-facing/research-agent-workflow-explainer.md`
- `github-facing/director-agentjob-lifecycle-explainer.md`
- `github-facing/parent-child-synthesis-explainer.md`
- `github-facing/role-routing-explainer.md`
- `html/research-agent-workflow-explainer.html`
- `html/director-agentjob-lifecycle-explainer.html`
- `html/parent-child-synthesis-explainer.html`
- `html/role-routing-explainer.html`

## Review Findings

The GitHub-facing openings now foreground page-specific research-control
operation before authority metadata. The pages teach request-to-job routing,
durable control-record lifecycle, parent-child synthesis inside one physics
AgentJob, and role-routing authority boundaries before presenting the full
generated-output disclaimer.

The full generated-noncanonical authority paragraph was moved into a marked
`Source Binding And Authority` footer section for each GitHub-facing page.
The tracked HTML pages use `<footer data-explainer-control="authority_footer">`
for the same full authority paragraph. Top notices now use shorter
reader-scope language and do not carry the full generated-noncanonical
paragraph.

The three workflow or lifecycle pages include page-specific process, lifecycle,
or parent-child diagrams as native Markdown tables and local HTML visual
structures. The tracked HTML uses no browser-side Mermaid, CDN script, remote
font, or external runtime. The role-routing page uses a role matrix and
decision table because the post-migration plan identified that as clearer than
a graph.

## Claim-Boundary Result

No page changes routing behavior, role authority, schema behavior, validator
behavior, checkpoint behavior, write permissions, generated-output authority,
or physics claim status. The parent-child synthesis page preserves the one
Director decision, one outer AgentJob, one execution-role record, one
completion record, one fused output invariant; states that child outputs are
`draft/control` support artifacts; and states that unresolved declared
blocking conflicts prevent PASS completion.

## Screenshot Evidence

- Desktop: `research_control/tasks/RT-20260619-006/artifacts/screenshots/research-agent-workflow-desktop.png`
- Mobile: `research_control/tasks/RT-20260619-006/artifacts/screenshots/research-agent-workflow-mobile.png`
- Desktop: `research_control/tasks/RT-20260619-006/artifacts/screenshots/director-agentjob-lifecycle-desktop.png`
- Mobile: `research_control/tasks/RT-20260619-006/artifacts/screenshots/director-agentjob-lifecycle-mobile.png`
- Desktop: `research_control/tasks/RT-20260619-006/artifacts/screenshots/parent-child-synthesis-desktop.png`
- Mobile: `research_control/tasks/RT-20260619-006/artifacts/screenshots/parent-child-synthesis-mobile.png`
- Desktop: `research_control/tasks/RT-20260619-006/artifacts/screenshots/role-routing-desktop.png`
- Mobile: `research_control/tasks/RT-20260619-006/artifacts/screenshots/role-routing-mobile.png`

The local browser run served pages from `http://127.0.0.1:8766/`. Page HTML
requests returned `200`, the favicon is a local data URL, and screenshots were
captured at `1440px` desktop width and `390px` mobile width.

## Conclusion

Phase 3 satisfies the post-migration footer-authority requirement for the
approved research-control operation page family. Remaining publication corpus
pages stay outside this packet.
