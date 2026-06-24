from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALID_ENVS = {"dev", "stage", "prod"}


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing required path: {path.relative_to(ROOT)}")


def validate_env(env: str) -> None:
    if env not in VALID_ENVS:
        raise SystemExit(f"Unsupported environment '{env}'. Choose one of: {', '.join(sorted(VALID_ENVS))}")

    required_paths = [
        ROOT / "terraform" / "envs" / env / "main.tf",
        ROOT / "terraform" / "envs" / env / "variables.tf",
        ROOT / "terraform" / "envs" / env / "terraform.tfvars.example",
        ROOT / "kubernetes" / "overlays" / env / "kustomization.yaml",
        ROOT / "argocd" / "applications" / f"{env}.yaml",
    ]
    for path in required_paths:
        require(path)

    overlay = (ROOT / "kubernetes" / "overlays" / env / "kustomization.yaml").read_text(encoding="utf-8")
    if "../../base" not in overlay:
        raise SystemExit(f"kubernetes/overlays/{env}/kustomization.yaml must reference ../../base")

    application = (ROOT / "argocd" / "applications" / f"{env}.yaml").read_text(encoding="utf-8")
    expected_overlay = f"kubernetes/overlays/{env}"
    if expected_overlay not in application:
        raise SystemExit(f"argocd/applications/{env}.yaml must target {expected_overlay}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate local GitOps wiring without cloud credentials.")
    parser.add_argument("--env", choices=sorted(VALID_ENVS), default="dev")
    args = parser.parse_args()
    validate_env(args.env)
    print(f"GitOps layout validation passed for {args.env}")


if __name__ == "__main__":
    main()
