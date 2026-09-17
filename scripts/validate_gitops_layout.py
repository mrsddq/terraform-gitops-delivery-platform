"""Validate GitOps routing and the production manual-sync boundary without a cluster."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALID_ENVS = {"dev", "stage", "prod"}
REPOSITORY = "https://github.com/mrsddq/terraform-gitops-delivery-platform.git"


def load_mapping(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def validate_env(env: str, root: Path = ROOT) -> None:
    if env not in VALID_ENVS:
        raise ValueError(f"Unsupported environment: {env}")
    for relative in (
        f"terraform/envs/{env}/main.tf",
        f"terraform/envs/{env}/variables.tf",
        f"terraform/envs/{env}/terraform.tfvars.example",
    ):
        if not (root / relative).is_file():
            raise ValueError(f"Missing required path: {relative}")
    overlay = load_mapping(root / "kubernetes/overlays" / env / "kustomization.yaml")
    if "../../base" not in overlay.get("resources", []):
        raise ValueError(f"{env}: overlay resources must reference ../../base")
    namespace = f"delivery-{env}"
    if overlay.get("namespace") != namespace:
        raise ValueError(f"{env}: overlay namespace must be {namespace}")
    application = load_mapping(root / "argocd/applications" / f"{env}.yaml")
    if application.get("apiVersion") != "argoproj.io/v1alpha1" or application.get("kind") != "Application":
        raise ValueError(f"{env}: expected an Argo CD Application")
    spec = application.get("spec", {})
    source = spec.get("source", {})
    expected = {
        "repoURL": REPOSITORY,
        "targetRevision": "main",
        "path": f"kubernetes/overlays/{env}",
    }
    for key, value in expected.items():
        if source.get(key) != value:
            raise ValueError(f"{env}: source.{key} must be {value}")
    destination = spec.get("destination", {})
    if destination.get("namespace") != namespace:
        raise ValueError(f"{env}: destination namespace must be {namespace}")
    if destination.get("server") != "https://kubernetes.default.svc":
        raise ValueError(f"{env}: destination must use the local cluster")
    if env == "prod" and "automated" in spec.get("syncPolicy", {}):
        raise ValueError("prod: automated sync is forbidden; use a reviewed manual sync")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", choices=["all", *sorted(VALID_ENVS)], default="all")
    args = parser.parse_args()
    environments = sorted(VALID_ENVS) if args.env == "all" else [args.env]
    try:
        for env in environments:
            validate_env(env)
            print(f"GitOps layout validation passed for {env}")
    except (ValueError, OSError, yaml.YAMLError, AttributeError, TypeError) as exc:
        parser.exit(2, f"GitOps validation failed: {exc}\n")


if __name__ == "__main__":
    main()
