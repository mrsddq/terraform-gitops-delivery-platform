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
    counts = {"create": 0, "update": 0, "delete": 0, "replace": 0, "no-op": 0}
    for resource in plan.get("resource_changes", []):
        actions = resource.get("change", {}).get("actions", [])
        if actions == ["delete", "create"] or actions == ["create", "delete"]:
            counts["replace"] += 1
            continue
        for action in actions:
            if action in counts:
                counts[action] += 1
    return counts


def render_markdown(counts: dict[str, int]) -> str:
    return "\n".join(
        [
            "## Terraform Plan Summary",
            "",
            "| Action | Count |",
            "| --- | ---: |",
            f"| Create | {counts['create']} |",
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

    if args.sample:
        plan = SAMPLE_PLAN
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            plan = json.load(fh)
    else:
        plan = json.load(sys.stdin)

    print(render_markdown(summarize(plan)))


if __name__ == "__main__":
    main()
