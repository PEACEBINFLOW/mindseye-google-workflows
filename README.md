# MindsEye Google Workflows

Central workflow hub for the MindsEye Google ecosystem —  
“**portal maps**” that explain how data moves across:

- Repos: ledger, orchestrator, workspace automation, devlog, analytics
- Google apps: Sheets, Docs, Gmail, Drive, Forms, Calendar, etc.

This repo is mostly **YAML specs + docs**.  
It doesn’t run workflows itself — it defines them as:

> source event → conditions → ordered steps → portals between apps/repos

Other repos (`orchestrator`, `workspace-automation`, etc.) use these YAMLs as the **source of truth** when you build actual automations.

---

## 📁 Structure

```text
mindseye-google-workflows/
├─ README.md
├─ LICENSE
├─ workflows/
│  ├─ 00_overview.yaml                # High-level system map
│  ├─ ledger_to_gemini.yaml           # Node → run → log
│  ├─ workspace_event_to_ledger.yaml  # Gmail/Docs/Drive → ledger node
│  ├─ devlog_generation.yaml          # Ledger → Devlog → Docs/Dev.to
│  ├─ analytics_refresh.yaml          # Runs → exports → dashboards
│  └─ portal_routes.yaml              # “Portal” definitions between apps
├─ specs/
│  ├─ workflow_schema.md              # What a workflow YAML must contain
│  └─ event_types.md                  # All valid events / triggers
├─ mappings/
│  ├─ repos.yaml                      # Map logical components → repos
│  └─ google_apps.yaml                # Map logical roles → Google apps
├─ scripts/
│  ├─ validate_workflows.py           # Lint + schema-validate YAML
│  └─ visualize_workflows.py          # Output Mermaid diagrams
└─ docs/
   └─ SYSTEM_FLOW.md                  # Narrative: how data traverses everything
