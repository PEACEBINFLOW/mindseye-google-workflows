#!/usr/bin/env python3
"""
validate_workflows.py

Validate all YAML workflows against a minimal schema and
ensure portals referenced in steps exist in portal_routes.yaml.

Requires:
    pip install pyyaml
"""

import os
import sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS_DIR = os.path.join(ROOT, "workflows")

PORTAL_FILE = os.path.join(WORKFLOWS_DIR, "portal_routes.yaml")


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_known_portals():
    if not os.path.exists(PORTAL_FILE):
        return set()
    data = load_yaml(PORTAL_FILE)
    portals = data.get("portals", [])
    names = {p.get("name") for p in portals if isinstance(p, dict)}
    return {n for n in names if n}


def validate_workflow(path, known_portals):
    rel = os.path.relpath(path, ROOT)
    data = load_yaml(path)
    errors = []

    def require(field):
        if field not in data:
            errors.append(f"missing required field '{field}'")

    # basic required fields
    for field in ["id", "name", "description", "version", "trigger", "steps"]:
        require(field)

    # validate steps
    steps = data.get("steps", [])
    if not isinstance(steps, list) or len(steps) == 0:
        errors.append("steps must be a non-empty list")
    else:
        for i, step in enumerate(steps):
            prefix = f"steps[{i}]"
            if not isinstance(step, dict):
                errors.append(f"{prefix} must be a dict")
                continue
            for sf in ["id", "name", "component", "action"]:
                if sf not in step:
                    errors.append(f"{prefix}: missing '{sf}'")
            # validate portal references
            uses = step.get("uses")
            if isinstance(uses, dict):
                portal = uses.get("portal")
                if portal and portal not in known_portals:
                    errors.append(
                        f"{prefix}: uses.portal '{portal}' not found in portal_routes.yaml"
                    )

    return rel, errors


def main():
    known_portals = get_known_portals()
    print(f"[validate] Known portals: {sorted(known_portals)}")

    workflow_files = [
      os.path.join(WORKFLOWS_DIR, f)
      for f in os.listdir(WORKFLOWS_DIR)
      if f.endswith(".yaml")
    ]

    all_errors = []
    for wf in workflow_files:
        rel, errors = validate_workflow(wf, known_portals)
        if errors:
            print(f"[validate] ❌ {rel}")
            for e in errors:
                print(f"  - {e}")
            all_errors.extend((rel, e) for e in errors)
        else:
            print(f"[validate] ✅ {rel}")

    if all_errors:
        print(f"\n[validate] Found {len(all_errors)} issues.")
        sys.exit(1)
    else:
        print("\n[validate] All workflows look good.")
        sys.exit(0)


if __name__ == "__main__":
    main()
