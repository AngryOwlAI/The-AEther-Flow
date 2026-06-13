<!-- authority: explanatory -->

# Source Manifest

This manifest records the source basis for the GitHub-facing Markdown layer. It preserves traceability without turning the pages into generated copies of the HTML explainer specs.

Authority boundary: this manifest is canonical for GitHub-facing page-to-source traceability. It is non-authoritative for physics claims and control decisions.

| Page | Purpose | Primary source materials | Source-backed scope | Authority boundary | Related HTML explainer |
| --- | --- | --- | --- | --- | --- |
| [README.md](README.md) | Hub and reading paths. | [../../README.md](../../README.md); [../../AGENTS.md](../../AGENTS.md); [../../markdown/html-explainer-specs/project-overview-explainer.md](../../markdown/html-explainer-specs/project-overview-explainer.md) | Navigation layer for GitHub readers and external agents. | Explains; does not promote claims or alter control routing. | [../../html/project-overview-explainer.html](../../html/project-overview-explainer.html) |
| [start-here.md](start-here.md) | Newcomer route. | [../../README.md](../../README.md); [../../AGENTS.md](../../AGENTS.md); [../../research_control/README.md](../../research_control/README.md) | First-read path across project identity, authority, and validation. | Orientation only; not scientific or control authority. | [../../html/project-overview-explainer.html](../../html/project-overview-explainer.html) |
| [project-overview.md](project-overview.md) | Project map. | [../../markdown/html-explainer-specs/project-overview-explainer.md](../../markdown/html-explainer-specs/project-overview-explainer.md); [../../README.md](../../README.md); [../../AGENTS.md](../../AGENTS.md) | Dual physics and AI research-agent program overview. | Summarizes existing boundaries; does not assert derivation success. | [../../html/project-overview-explainer.html](../../html/project-overview-explainer.html) |
| [source-authority.md](source-authority.md) | File authority ladder. | [../../markdown/html-explainer-specs/source-authority-explainer.md](../../markdown/html-explainer-specs/source-authority-explainer.md); [../../registries/MARKDOWN_SOURCE_REGISTRY.csv](../../registries/MARKDOWN_SOURCE_REGISTRY.csv); [../../registries/HTML_EXPLAINER_REGISTRY.csv](../../registries/HTML_EXPLAINER_REGISTRY.csv) | TeX, registries, Markdown, HTML, wiki, PDF, and `.local` boundaries. | Explains existing authority; does not change registry status. | [../../html/source-authority-explainer.html](../../html/source-authority-explainer.html) |
| [research-system.md](research-system.md) | Research and project-control workflow. | [../../markdown/html-explainer-specs/research-agent-workflow-explainer.md](../../markdown/html-explainer-specs/research-agent-workflow-explainer.md); [../../markdown/html-explainer-specs/research-control-system-explainer.md](../../markdown/html-explainer-specs/research-control-system-explainer.md); [../../research_control/README.md](../../research_control/README.md) | Bounded jobs, Director decisions, validators, receipts, and handoffs. | Descriptive only; validators and control records remain authoritative. | [../../html/research-agent-workflow-explainer.html](../../html/research-agent-workflow-explainer.html); [../../html/research-control-system-explainer.html](../../html/research-control-system-explainer.html) |
| [claim-gates.md](claim-gates.md) | Claim boundary model. | [../../markdown/html-explainer-specs/claim-gates-explainer.md](../../markdown/html-explainer-specs/claim-gates-explainer.md); [../../registries/CLAIM_BOUNDARY_REGISTRY.csv](../../registries/CLAIM_BOUNDARY_REGISTRY.csv); [../../registries/TEX_SOURCE_REGISTRY.csv](../../registries/TEX_SOURCE_REGISTRY.csv) | Claim statuses, negative results, blocked promotions, and review boundaries. | Does not accept, reject, or promote physics claims. | [../../html/claim-gates-explainer.html](../../html/claim-gates-explainer.html) |
| [roles-and-skills.md](roles-and-skills.md) | Role and skill map. | [../../markdown/html-explainer-specs/roles-and-skills-explainer.md](../../markdown/html-explainer-specs/roles-and-skills-explainer.md); [../../registries/AGENT_ROLE_REGISTRY.csv](../../registries/AGENT_ROLE_REGISTRY.csv); [../../registries/ROLE_EXECUTION_REGISTRY.csv](../../registries/ROLE_EXECUTION_REGISTRY.csv) | Registered roles, task overlays, repo-local skills, and operator aids. | Does not register roles or change permissions. | [../../html/roles-and-skills-explainer.html](../../html/roles-and-skills-explainer.html) |
| [technical-requirements.md](technical-requirements.md) | Validation and regeneration guide. | [../../markdown/html-explainer-specs/technical-requirements-explainer.md](../../markdown/html-explainer-specs/technical-requirements-explainer.md); [../../requirements.txt](../../requirements.txt); [../../Makefile](../../Makefile) | Read-only inspection, Python validators, memory refresh, Mermaid rendering, local retrieval, and PDF refresh. | Describes commands; scripts and control records own requirements. | [../../html/technical-requirements-explainer.html](../../html/technical-requirements-explainer.html) |

## Registry Metadata

The Markdown source registry should treat this layer with the following metadata:

- `role`: `github_facing_documentation`
- `authority_status`: `canonical_markdown_source`
- `audience`: `humans_and_agents`
- `owner_skill`: `documentation-curator`
- `github_facing`: `true`
- `agent_documentation`: `true`
- `notes`: `GitHub-facing explanatory documentation; non-authoritative for physics claims and control decisions.`

