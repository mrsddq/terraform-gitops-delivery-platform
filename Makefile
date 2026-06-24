.PHONY: validate fmt-check test sample-plan-comment

validate: test sample-plan-comment

fmt-check:
	terraform fmt -recursive -check terraform

test:
	python -m unittest discover -s tests

sample-plan-comment:
	python scripts/render_plan_comment.py --sample > /tmp/terraform-plan-comment.md
