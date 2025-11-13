# Workflow Schema – MindsEye Google Workflows

All `workflows/*.yaml` files should follow this schema.

This repo doesn’t enforce everything at runtime, but  
`scripts/validate_workflows.py` will check the **core shape**.

---

## 1. Top-level fields

Required:

- `id` — unique string ID (`wf_...`)
- `name` — human-readable title
- `description` — multi-line description
- `version` — semver-like string, e.g. `0.1.0`
- `trigger` — object describing what starts the workflow
- `steps` — ordered list of step objects

Optional:

- `domains` — e.g. `["ledger", "orchestrator", "workspace_automation"]`
- `conditions` — list of preconditions
- `ports` — list of portal definitions (for that workflow)

---

## 2. Trigger

```yaml
trigger:
  type: <trigger_type>
  event: <event_name_or_pattern>
  # optional
  source_component: <component_name>
  schedule: <cronish_or_human_schedule>
  payload:
    expected:
      - ...
