.PHONY: dev test lint docker-prod help

PORT ?= 8080
IMAGE ?= us-central1-docker.pkg.dev/noble-office-299208/mercy-of-toren/gnbio:prod

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

dev:  ## Run the dev server on $(PORT) (default 8080)
	python app.py --port $(PORT)

test:  ## Run the test suite
	pytest -v

lint:  ## Run ruff check + format check
	ruff check .
	ruff format --check .

docker-prod:  ## Build the production Docker image
	docker build -f assets/build/Dockerfile.prod -t $(IMAGE) .
