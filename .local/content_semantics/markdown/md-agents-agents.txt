# AGENTS.md

Scoped guidance for `.agents/`.

## Authority

Versioned role contracts and reusable schemas live here. They constrain
execution but do not authorize scientific claim promotion by themselves.

## Editing Rules

- Keep behavior-bearing role contracts versioned in filenames.
- Do not change a registered role version's authority, mission, validators, or
  forbidden actions in place. Create a new version instead.
- Use `.agents/schemas/` for abstract schemas and `research_control/templates/`
  for concrete task or job templates.
- Run ` .venv/bin/python scripts/research_control/validate_research_control.py`
  after role or schema changes.
