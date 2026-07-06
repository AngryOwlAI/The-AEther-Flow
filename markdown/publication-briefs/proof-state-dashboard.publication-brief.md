---
brief_id: "PB-PROOF-STATE-DASHBOARD"
subject: "Proof-State Dashboard"
reader: "External technical reader, maintainer, reviewer, or summarizing AI that needs the current proof state without overreading scoped objects as GR derivation."
reader_job: "See what is positively established, the exact scope of each status, what may be used next, and which downstream claims remain blocked."
document_type: "visual_brief"
reading_experience: "A concise dashboard brief centered on one annotated status table with positive-first language, visible source paths, and explicit non-authoritative derivative boundaries."
narrative_structure:
  - "Open by stating that the dashboard is a reader-facing derivative and that GR has not been derived."
  - "Render the required rows: Resp_lc, M_src, g_eff, matter_coupling, Einstein equations, benchmark promotion, and finite toy metric response."
  - "Use the required columns: Object, Positive status, Exact scope, Allowed use, Blocked overread, and Next lawful route."
  - "Close by naming the authority hierarchy and the claims the dashboard cannot establish."
visual_strategy: "annotated_table"
source_basis:
  - "research_control/current_frontier.md"
  - "output/compact_current_frontier_v16.yaml"
  - "registries/DISTANCE_TO_GR_LEDGER.csv"
  - "registries/METRIC_USE_LEDGER.csv"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "research_control/design/distance_to_gr_status_aliases.yaml"
  - "research_control/design/accepted_status_calibration_v1.yaml"
  - "research_control/design/public_status_exists_does_not_exist_source_spec.md"
  - "research_control/handoffs/handoff-0652.yaml"
authority_boundaries:
  - "The dashboard may summarize calibrated status cards but cannot promote physics claims, certify proof authority, or update the Distance-to-GR ledger."
  - "The dashboard must state that matter coupling, Einstein equations, benchmark promotion, Gate Chair closure, and completed derivation remain unestablished."
  - "The generated GitHub Markdown and HTML derivatives remain noncanonical reader surfaces."
output_surfaces:
  - "github-facing/proof-state-dashboard-explainer.md"
  - "html/proof-state-dashboard-explainer.html"
acceptance_criteria:
  - "Includes every required dashboard row and required dashboard column from v17 P9-T01."
  - "Uses positive-first scoped status for Resp_lc, M_src, g_eff, and matter_coupling."
  - "States that Einstein equations are not started, benchmark promotion remains blocked, and finite toy metric response is a frozen local route rather than global rejection."
  - "Names the source basis for each row or for the table as a whole."
  - "States that GR has not been derived and that generated public outputs are noncanonical derivatives."
  - "Leaves GitHub Markdown, tracked HTML, screenshots, and HTML registry synchronization to P9-T02."
forbidden_patterns:
  - "Calling the dashboard a proof, derivation, certification, or Gate Chair verdict."
  - "Rendering accepted scoped evidence/preconditions as source-law adoption, detector semantics, coupling-law adoption, matter coupling, or Einstein equations."
  - "Rendering g_eff as an unscoped Lorentzian metric or physical metric authority."
  - "Rendering finite toy metric response as a program-wide no-go, global theory rejection, or future source-extension impossibility."
migration_status: "publication_pilot"
---

# Publication Brief: Proof-State Dashboard

The page is a compact proof-state dashboard for readers who need the present
research status without reading the full control registry stack. Its purpose is
not to simplify the claim boundary away. Its purpose is to keep positive status,
exact scope, allowed use, blocked overread, and next route visible at the same
time.

P9-T02 renders the GitHub Markdown and standalone HTML surfaces as a
publication pilot. The surfaces remain generated noncanonical reader outputs;
they do not change proof authority, source authority, the Distance-to-GR
ledger, or physics claim status.
