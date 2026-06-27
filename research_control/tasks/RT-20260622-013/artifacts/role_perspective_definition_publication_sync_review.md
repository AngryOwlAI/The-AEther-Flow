<!-- authority: control -->

# Role-Perspective Definition Publication Sync Review

Task: `RT-20260622-013`
Job: `AJ-RT-20260622-013-001`

## Scope

This packet adds two descriptive perspective definitions and synchronizes them
through project-control guidance and three source-backed reader surfaces:

- Project-System Improvement Loop;
- Documentation Curator Publication Process; and
- Roles And Skills Catalog.

## Before

The project already separated Project-Control Maintainer, Documentation
Curator, `improve-project-system`, publication briefs, source specs, and
generated reader surfaces. The reader-facing pages described responsibilities
and boundaries, but they did not explicitly answer what professional
perspective each named workflow was closest to.

## After

The updated sources state:

- improve-project-system is best understood as a project-system reliability and
  governance perspective. It is closest to system engineer plus software
  engineer plus process auditor.
- Documentation Curator is best understood as a source-backed publication and
  technical-documentation perspective. It is closest to technical editor,
  science communicator, information architect, and provenance auditor.

The same surfaces also state that these are descriptive definitions only. They
do not change role authority, role semantics, routing behavior, validator
behavior, write permissions, checkpoint behavior, generated-output authority,
or physics claim status.

## Review Notes

- `.agents/roles/**` was not modified.
- `registries/AGENT_ROLE_REGISTRY.csv` was not modified.
- The three tracked HTML pages were updated with matching source-spec hashes.
- The publication brief registry rows were updated to point to this packet's
  screenshot and before/after review evidence.

## Screenshot Evidence

- `research_control/tasks/RT-20260622-013/artifacts/screenshots/project-system-improvement-desktop.png`
- `research_control/tasks/RT-20260622-013/artifacts/screenshots/project-system-improvement-mobile.png`
- `research_control/tasks/RT-20260622-013/artifacts/screenshots/documentation-curator-publication-process-desktop.png`
- `research_control/tasks/RT-20260622-013/artifacts/screenshots/documentation-curator-publication-process-mobile.png`
- `research_control/tasks/RT-20260622-013/artifacts/screenshots/roles-and-skills-desktop.png`
- `research_control/tasks/RT-20260622-013/artifacts/screenshots/roles-and-skills-mobile.png`

## Remaining Risk

The update is intentionally descriptive. Any future desire to make these
perspectives executable role semantics would require separate human-gated
role-contract and registry work.
