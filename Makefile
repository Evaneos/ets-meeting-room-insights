.DEFAULT_GOAL: help

# See https://www.thapaliya.com/en/writings/well-documented-makefiles/
help: ## Display this help
	@awk 'BEGIN {FS = ":.* ##"; printf "\n\033[1mUsage:\033[0m\n  make \033[32m<target>\033[0m\n"} /^[a-zA-Z_-]+:.* ## / { printf "  \033[33m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

DOCKER_IMAGE_NAME = evaneos/ets-meeting-room-insights
DOCKER_IMAGE_TAG = dev

build: ## Build image and install dependencies
	docker build -t $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) -f ./Dockerfile .

start: ## Start export from Twilio (may take a few minutes)
	docker run $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) 2> export.csv
