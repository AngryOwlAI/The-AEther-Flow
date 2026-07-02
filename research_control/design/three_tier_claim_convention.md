<!-- authority: control -->

# Three-Tier Claim Convention

## Scope

This policy defines the required three-tier claim convention for completions,
handoffs, current-frontier summaries, public status surfaces, and final audits.
It is project-control guidance. It is not a physics proof surface, not a
registry override, and not authority to promote any scoped evidence into a
source law, physical target, benchmark result, or completed derivation.

The convention exists to keep three different facts visibly separate:

1. source-side objects with scoped object status;
2. accepted evidence or preconditions;
3. open or blocked physical targets.

If a summary cannot distinguish these three tiers, it must use the stricter
lower-authority wording and cite the controlling source path.

## Authority Order

When this policy is used, the tracked authority order remains:

1. registered TeX sources for scientific derivation claims;
2. `registries/DISTANCE_TO_GR_LEDGER.csv` for Distance-to-GR burden status;
3. `research_control/design/distance_to_gr_status_aliases.yaml` for
   subordinate reader-facing aliases;
4. row-specific Gate Chair or task artifacts for scoped evidence status;
5. `research_control/current_frontier.md` as a synchronized snapshot only;
6. this policy as the reporting convention for tiered summaries.

Generated wiki notes, HTML, PDFs, local caches, semantic extracts, validator
output, role records, handoffs, commits, and checkpoints are not independent
scientific authority.

## Required Tiers

Every nontrivial completion, handoff, current-frontier summary, public status
surface, and final audit that mentions high-risk project status must include
the three tiers below, either as explicit headings or as equivalent fields with
the same meaning.

### Tier 1: Adopted Objects

Use this tier only for scoped source-side objects whose object status is
already supported by tracked authority. The summary must name the exact scope
and the blocked downstream readings.

Required fields:

- object name;
- exact scoped status phrase;
- authority path;
- scope qualifier;
- blocked overread;
- downstream promotion status.

Required examples:

| Object | Required tier wording | Scope qualifier | Blocked overread |
| --- | --- | --- | --- |
| `M_src` | scoped source-only object | Not a target manifold, not a metric, and not a GR derivation. | No `MetricData(E)`, `g_eff` scope expansion, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows. |
| `g_eff` | scoped source-extension object | Not an unscoped Lorentzian metric and not matter coupling or Einstein-equation evidence. | No `MetricData(E)`, unscoped `g_eff`, matter coupling, Einstein equations, benchmark promotion, or completed derivation follows. |

Tier 1 must not be used for matter semantics, detector semantics, universal
coupling, stress-energy semantics, stress-energy tensor, matter action,
Einstein equations, benchmark promotion, or completed derivation unless a
later tracked source explicitly establishes the relevant protected authority.

### Tier 2: Accepted Evidence Or Preconditions

Use this tier for scoped evidence, certificates, profiles, witness
preconditions, readiness material, or bridge evidence that can support later
work but does not itself adopt an object or solve a physical target.

Required fields:

- evidence or precondition name;
- exact evidence/precondition status phrase;
- authority path;
- scope qualifier;
- target it may support;
- target it does not establish.

Required examples:

| Evidence or precondition | Required tier wording | Scope qualifier | Target not established |
| --- | --- | --- | --- |
| `SourceMatterSemanticsAdoptionReadinessLaw_v1` | scoped readiness evidence/precondition or proposal-only law target unless a later gate changes status | Not source-law adoption, not matter semantics, not detector semantics, and not coupling law. | Matter semantics, detector semantics, universal coupling, Einstein equations, benchmark promotion, and completed derivation remain open or blocked. |
| `PositiveMSProfile_v1` | accepted only as scoped positive source-semantics evidence/precondition | Not adopted matter semantics, detector semantics, stress-energy, or matter action. | Matter semantics, detector semantics, stress-energy semantics, matter action, matter coupling, Einstein equations, benchmark promotion, and completed derivation remain open or blocked. |
| `RR_ETransportCompletenessOrInvarianceLaw_v1` | accepted only as certificate-indexed `RR_E` transport-completeness or invariance evidence/precondition | Not source-law adoption, not object adoption, not unrestricted `RR_E` theorem, not detector semantics, and not matter coupling. | `RR_E` unrestricted irrelevance, detector collapse, matter semantics, coupling law, matter coupling, `MetricData(E)`, `g_eff`, Einstein equations, benchmark promotion, and completed derivation remain open or blocked. |
| stable matter-semantics bridge evidence/precondition | scoped bridge evidence/precondition only | Not matter-semantics adoption and not detector-semantics adoption. | Matter semantics, detector semantics, coupling law, and downstream GR promotion remain open or blocked. |
| MCPA evidence/precondition | scoped matter-coupling precondition evidence only | Not universal coupling and not stress-energy semantics. | Matter coupling, stress-energy tensor, matter action, Einstein equations, and benchmark promotion remain open or blocked. |
| coupling-law-candidate evidence/precondition | scoped candidate evidence/precondition only | Not coupling-law adoption. | Universal coupling, matter action, Einstein equations, benchmark promotion, and completed derivation remain open or blocked. |

Tier 2 summaries must never render the word `accepted` without the immediate
qualifier `only as scoped evidence/precondition` or a stricter equivalent
phrase.

### Tier 3: Open Or Blocked Physical Targets

Use this tier for physical, benchmark, or completed-derivation targets that
remain unproved, not started, blocked by missing burdens, or protected by a
future gate.

Required fields:

- target name;
- current open or blocked status;
- missing burden or protected authority;
- evidence that must not be overread;
- next lawful route, if known.

Required examples:

| Target | Required tier wording | Missing burden or authority | Evidence that must not be overread |
| --- | --- | --- | --- |
| matter semantics | open or blocked physical target | Protected adoption route and source-side semantics remain missing. | Tier 2 matter-semantics evidence/preconditions are not adoption. |
| detector semantics | open or blocked physical target | Detector-semantics adoption remains missing. | `RR_E` certificate-indexed evidence is not detector collapse. |
| universal coupling | open or blocked physical target | Coupling law and matter-coupling derivation remain missing. | Scoped matter-coupling preconditions are not universal coupling. |
| stress-energy semantics | open or blocked physical target | Stress-energy semantics and stress-energy tensor are not derived. | Positive source-semantics evidence does not define stress-energy. |
| stress-energy tensor | open or blocked physical target | Tensor definition and derivation remain missing. | No Tier 1 or Tier 2 item establishes this tensor. |
| matter action | open or blocked physical target | Matter action or variation principle remains missing. | Matter-coupling evidence/preconditions do not supply an action. |
| Einstein equations | open or blocked physical target | Dynamics, action, variation, matter coupling, and protected benchmark authority remain missing. | Scoped source-side objects and evidence/preconditions do not derive Einstein equations. |
| benchmark promotion | open or blocked protected target | Protected benchmark authority remains missing. | Validation, public status rendering, and scoped evidence do not promote benchmark status. |
| completed derivation | open or blocked protected target | Upstream derivation burdens and protected promotion authority remain missing. | No current scoped object, evidence/precondition, validator, or generated surface establishes completion. |

Tier 3 summaries must preserve open-continuation language unless a tracked
no-go theorem exists. A local frozen route is not a program-wide rejection.

## Required Summary Form

Use this compact form for completions and handoffs:

```yaml
three_tier_claim_summary:
  adopted_objects:
    - object: ""
      status: ""
      authority_path: ""
      scope_qualifier: ""
      blocked_overread: []
      downstream_promotion_authorized: false
  accepted_evidence_preconditions:
    - object: ""
      status: ""
      authority_path: ""
      supports_target: ""
      does_not_establish: []
  open_or_blocked_physical_targets:
    - target: ""
      status: ""
      missing_burden_or_authority: ""
      evidence_not_to_overread: []
      next_lawful_route: ""
  forbidden_overread: []
```

This field is a reporting field only. It cannot promote a claim beyond the
underlying source authority.

## Minimal Public-Surface Form

When a public surface has limited space, it may use this shorter form:

```text
Adopted scoped source-side objects: [Tier 1]. Accepted evidence/preconditions:
[Tier 2]. Open or blocked physical targets: [Tier 3]. No downstream promotion
follows unless the cited tracked authority explicitly grants it.
```

The shorter form is valid only when each item still carries enough scope and
blocked-overread language to prevent a reader from confusing tiers.

## Forbidden Conversions

The following conversions are forbidden unless a later tracked source and
protected authority explicitly change the status:

- Tier 1 source-side object status into physical target completion;
- Tier 1 source-extension object status into unscoped metric status;
- Tier 2 evidence/precondition status into object adoption;
- Tier 2 evidence/precondition status into source-law adoption;
- Tier 2 evidence/precondition status into matter semantics or detector
  semantics;
- Tier 2 evidence/precondition status into universal matter coupling;
- any validator PASS, renderer output, registry row, handoff, commit, or
  generated derivative into scientific proof authority;
- any local frozen negative route into future source-extension impossibility
  or a program-wide no-go conclusion.

## Checklist

Before closing a packet, check:

- each high-risk object appears in the correct tier;
- every positive status phrase names its scope;
- every evidence/precondition phrase says what target it does not establish;
- every physical target remains open or blocked unless tracked authority says
  otherwise;
- no bare `accepted` or bare `adopted` wording appears near high-risk objects;
- no generated artifact or validator receipt is treated as scientific proof;
- the next route is bounded and uses tracked continue-research state.

## Source Materials

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan continue task v14* [Internal implementation plan].

The AEther-Flow Research Project. (2026, July 1). *Distance-to-GR status
aliases* [Internal control data].

The AEther-Flow Research Project. (2026, July 1). *Scoped claim language
examples* [Internal control note].

The AEther-Flow Research Project. (2026, July 2). *Public status table source
spec* [Internal control source spec].

The AEther-Flow Research Project. (2026, July 2). *Current research frontier*
[Internal control snapshot].
