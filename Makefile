.PHONY: validate fmt-check lint security-scan deploy destroy test sample-plan-comment

ENV ?= dev
CONFIRM_DEPLOY ?= false

validate: test sample-plan-comment

fmt-check:
	terraform fmt -recursive -check terraform

lint: validate fmt-check

security-scan:
	checkov -d terraform --quiet

deploy:
	@if [ "$(CONFIRM_DEPLOY)" != "true" ]; then echo "Set CONFIRM_DEPLOY=true to create billable AWS resources."; exit 2; fi
	terraform -chdir=terraform/envs/$(ENV) init
	terraform -chdir=terraform/envs/$(ENV) apply

destroy:
	@if [ "$(CONFIRM_DEPLOY)" != "true" ]; then echo "Set CONFIRM_DEPLOY=true to destroy AWS resources."; exit 2; fi
	terraform -chdir=terraform/envs/$(ENV) destroy

test:
	python -m unittest discover -s tests

sample-plan-comment:
	python scripts/render_plan_comment.py --sample > /tmp/terraform-plan-comment.md
