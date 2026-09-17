import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.render_plan_comment import summarize
from scripts.validate_gitops_layout import ROOT, validate_env


class RoutingRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("terraform", "kubernetes", "argocd"):
            shutil.copytree(ROOT / name, self.root / name)

    def change(self, relative, mutate):
        path = self.root / relative
        data = yaml.safe_load(path.read_text())
        mutate(data)
        path.write_text(yaml.safe_dump(data))

    def test_all_environments(self):
        for env in ("dev", "stage", "prod"):
            validate_env(env, self.root)

    def test_production_cannot_auto_sync(self):
        self.change("argocd/applications/prod.yaml", lambda d: d["spec"]["syncPolicy"].update(automated={}))
        with self.assertRaisesRegex(ValueError, "automated sync"):
            validate_env("prod", self.root)

    def test_namespace_mismatch_fails(self):
        self.change("argocd/applications/stage.yaml", lambda d: d["spec"]["destination"].update(namespace="delivery-prod"))
        with self.assertRaisesRegex(ValueError, "destination namespace"):
            validate_env("stage", self.root)

    def test_overlay_namespace_mismatch_fails(self):
        self.change("kubernetes/overlays/dev/kustomization.yaml", lambda d: d.update(namespace="delivery-prod"))
        with self.assertRaisesRegex(ValueError, "overlay namespace"):
            validate_env("dev", self.root)

    def test_comment_cannot_mask_wrong_source(self):
        path = self.root / "argocd/applications/dev.yaml"
        self.change("argocd/applications/dev.yaml", lambda d: d["spec"]["source"].update(path="kubernetes/overlays/prod"))
        path.write_text(path.read_text() + "\n# kubernetes/overlays/dev\n")
        with self.assertRaisesRegex(ValueError, "source.path"):
            validate_env("dev", self.root)

    def test_wrong_repository_fails(self):
        self.change("argocd/applications/dev.yaml", lambda d: d["spec"]["source"].update(repoURL="https://example.org/wrong.git"))
        with self.assertRaisesRegex(ValueError, "repoURL"):
            validate_env("dev", self.root)


class PlanSummaryRegressionTests(unittest.TestCase):
    def test_both_replacement_orders_count_once(self):
        result = summarize({"resource_changes": [{"change": {"actions": a}} for a in
                            [["create", "delete"], ["delete", "create"], ["read"]]]})
        self.assertEqual(result["replace"], 2)
        self.assertEqual(result["read"], 1)
        self.assertEqual(result["create"], 0)
        self.assertEqual(result["delete"], 0)

    def test_bad_actions_fail_instead_of_showing_zero_changes(self):
        for actions in ([], ["delete", "unknown"], "delete", [None], ["create", "create"]):
            with self.subTest(actions=actions), self.assertRaises(ValueError):
                summarize({"resource_changes": [{"change": {"actions": actions}}]})

    def test_malformed_plan_fails(self):
        for plan in ([], {"resource_changes": {}}, {"resource_changes": [None]}):
            with self.subTest(plan=plan), self.assertRaises(ValueError):
                summarize(plan)

    def test_empty_plan_is_valid(self):
        self.assertEqual(sum(summarize({}).values()), 0)

    def test_cli_invalid_plan_returns_error_without_summary(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/render_plan_comment.py")],
                                input=json.dumps({"resource_changes": [{"change": {"actions": ["unknown"]}}]}),
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("unsupported action", result.stderr)
