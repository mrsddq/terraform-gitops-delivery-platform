import unittest
from pathlib import Path

from scripts.render_plan_comment import render_markdown, summarize


ROOT = Path(__file__).resolve().parents[1]


class DeliveryPlatformTest(unittest.TestCase):
    def test_all_environments_exist(self):
        for env in ("dev", "stage", "prod"):
            self.assertTrue((ROOT / "terraform" / "envs" / env / "main.tf").exists())
            self.assertTrue((ROOT / "kubernetes" / "overlays" / env / "kustomization.yaml").exists())
            self.assertTrue((ROOT / "argocd" / "applications" / f"{env}.yaml").exists())

    def test_plan_summary_counts_replace(self):
        counts = summarize({"resource_changes": [{"change": {"actions": ["delete", "create"]}}]})
        self.assertEqual(counts["replace"], 1)

    def test_markdown_contains_review_warning(self):
        markdown = render_markdown({"create": 1, "update": 0, "delete": 0, "replace": 0, "no-op": 0})
        self.assertIn("Terraform Plan Summary", markdown)
        self.assertIn("Review deletes", markdown)


if __name__ == "__main__":
    unittest.main()
