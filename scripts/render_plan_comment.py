import argparse
import json
import sys
from typing import Any


SAMPLE_PLAN = {
    "resource_changes": [
        {"change": {"actions": ["create"]}},
        {"change": {"actions": ["update"]}},
        {"change": {"actions": ["delete"]}},
        {"change": {"actions": ["no-op"]}},
    ]
}


def summarize(plan: dict[str, Any]) -> dict[str, int]:
    """Summarize known Terraform actions; reject malformed or unrecognized plans."""
    if not isinstance(plan, dict):
        raise ValueError("plan must be a JSON object")
    resources = plan.get("resource_changes", [])
    if not isinstance(resources, list):
        raise ValueError("resource_changes must be a list")
    counts = dict.fromkeys(("create", "read", "update", "delete", "replace", "no-op"), 0)
    actions_to_count = {
        ("create",): "create", ("read",): "read", ("update",): "update",
        ("delete",): "delete", ("no-op",): "no-op",
        ("delete", "create"): "replace", ("create", "delete"): "replace",
    }
    for index, resource in enumerate(resources):
        change = resource.get("change") if isinstance(resource, dict) else None
        actions = change.get("actions") if isinstance(change, dict) else None
        if not isinstance(actions, list) or not all(isinstance(a, str) for a in actions):
            raise ValueError(f"resource_changes[{index}]: actions must be a list of strings")
        key = actions_to_count.get(tuple(actions))
        if key is None:
            raise ValueError(f"resource_changes[{index}]: unsupported action sequence {actions!r}")
        counts[key] += 1
    return counts


def render_markdown(counts: dict[str, int]) -> str:
    return "\n".join(
        [
            "## Terraform Plan Summary",
            "",
            "| Action | Count |",
            "| --- | ---: |",
            f"| Create | {counts['create']} |",
            f"| Read | {counts.get('read', 0)} |",
            f"| Update | {counts['update']} |",
            f"| Delete | {counts['delete']} |",
            f"| Replace | {counts['replace']} |",
            f"| No-op | {counts['no-op']} |",
            "",
            "Review deletes and replacements carefully before apply.",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Terraform plan JSON as a PR comment.")
    parser.add_argument("--sample", action="store_true", help="Render a sample comment.")
    parser.add_argument("--file", help="Path to Terraform plan JSON. Reads stdin if omitted.")
    args = parser.parse_args()

    try:
        if args.sample:
            plan = SAMPLE_PLAN
        elif args.file:
            with open(args.file, "r", encoding="utf-8") as fh:
                plan = json.load(fh)
        else:
            plan = json.load(sys.stdin)
        print(render_markdown(summarize(plan)))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Cannot summarize Terraform plan: {exc}\n")



if __name__ == "__main__":
    main()
