# Governed Markdown Mermaid Example

Visual grammar:

- source nodes use `source`;
- validation and transformation steps use `control`;
- final reader-facing output uses `target`;
- default arrows show required provenance flow.

```yaml
mermaid_diagrams:
  required: true
  ids:
    - authority-ladder
```

<!-- mermaid-diagram-id: authority-ladder -->
```mermaid
flowchart TD
  source["Registered Markdown source"]:::source
  registry["Registry row"]:::source
  html["Tracked HTML derivative"]:::target
  validator["Bootstrap validation"]:::control

  source --> registry
  source --> html
  registry --> validator
  html --> validator

  classDef source fill:#0f364d,stroke:#48a0c0,color:#fff8ef,stroke-width:2px;
  classDef control fill:#270b01,stroke:#f87800,color:#fff8ef,stroke-width:2px;
  classDef target fill:#2d7ea0,stroke:#f4d6a1,color:#ffffff,stroke-width:2px;
  linkStyle default stroke:#d6c3b4,stroke-width:2.25px;
```
