#!/usr/bin/env python3
"""
visualize_workflows.py

Generate Mermaid diagrams for each workflow YAML and write them
to diagrams/<workflow_id>.mmd

Usage:
    python scripts/visualize_workflows.py

Requires:
    pip install pyyaml
"""

import os
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS_DIR = os.path.join(ROOT, "workflows")
DIAGRAMS_DIR = os.path.join(ROOT, "diagrams")


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def workflow_to_mermaid(data):
    """
    Very simple flowchart:

    trigger --> step1 --> step2 --> ... --> stepN
    With component labels.
    """
    wf_id = data.get("id", "workflow")
    title = data.get("name", wf_id)
    trigger = data.get("trigger", {})

    lines = []
    lines.append("flowchart LR")
    lines.append(f"  %% {title}")

    # trigger node
    trig_label = trigger.get("event", trigger.get("type", "trigger"))
    trig_node_id = "trigger"
    lines.append(f'  {trig_node_id}(["Trigger: {trig_label}"])')

    steps = data.get("steps", [])
    prev_node_id = trig_node_id

    for i, step in enumerate(steps):
        sid = step.get("id", f"s{i+1}")
        comp = step.get("component", "component")
        name = step.get("name", sid)
        node_id = sid.replace("-", "_")
        label = f"{name}\\n[{comp}]"
        lines.append(f'  {node_id}["{label}"]')
        lines.append(f"  {prev_node_id} --> {node_id}")
        prev_node_id = node_id

    return "\n".join(lines)


def main():
    ensure_dir(DIAGRAMS_DIR)

    for fname in os.listdir(WORKFLOWS_DIR):
        if not fname.endswith(".yaml"):
            continue
        path = os.path.join(WORKFLOWS_DIR, fname)
        data = load_yaml(path)
        wf_id = data.get("id", os.path.splitext(fname)[0])
        mmd = workflow_to_mermaid(data)
        out_path = os.path.join(DIAGRAMS_DIR, f"{wf_id}.mmd")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(mmd)
        print(f"[visualize] Wrote {out_path}")


if __name__ == "__main__":
    main()
