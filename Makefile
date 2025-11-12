.PHONY: help deploy-dev deploy-prod build push

CHART_PATH := ./helm/outreach-expenses
IMAGE_NAME := ghcr.io/vladkanatov/outreach-expenses
TAG ?= $(shell git rev-parse --short HEAD)

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker image
	docker build -t $(IMAGE_NAME):$(TAG) .

push: build ## Push Docker image to registry
	docker push $(IMAGE_NAME):$(TAG)

deploy-dev: ## Deploy to dev environment
	helm upgrade --install outreach-expenses $(CHART_PATH) \
		-f ./helm/values-dev.yaml \
		--set image.tag=$(TAG) \
		--namespace outreach-expenses-dev \
		--create-namespace \
		--wait

deploy-prod: ## Deploy to production
	helm upgrade --install outreach-expenses $(CHART_PATH) \
		-f ./helm/values-production.yaml \
		--set image.tag=$(TAG) \
		--namespace outreach-expenses-production \
		--create-namespace \
		--wait

template: ## Show rendered Helm templates
	helm template outreach-expenses $(CHART_PATH) -f ./helm/values-dev.yaml

logs: ## Show bot logs (production)
	kubectl logs -f deployment/outreach-expenses -n outreach-expenses-production

status: ## Check deployment status
	kubectl get all -n outreach-expenses-production

clean-dev: ## Delete dev deployment
	helm uninstall outreach-expenses -n outreach-expenses-dev || true
	kubectl delete namespace outreach-expenses-dev || true

clean-prod: ## Delete production deployment
	helm uninstall outreach-expenses -n outreach-expenses-production || true
	kubectl delete namespace outreach-expenses-production || true
