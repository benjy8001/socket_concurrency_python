DOCKER  	= docker
TAG_NAME	= app
EXEC        = $(DOCKER_COMPOSE) exec $(TAG_NAME)

##
## Project
## -------
##

build: ## Build container
	$(DOCKER) build . -t $(TAG_NAME)_image

start: ## Start the project
	$(DOCKER) run -p 5555:5555 --rm -d --name $(TAG_NAME) $(TAG_NAME)_image

connect: ## Connect to the container of the project
	$(DOCKER) exec -ti $(TAG_NAME) bash

stop: ## Stop the project
	$(DOCKER) stop $(TAG_NAME)

no-docker:
	$(eval DOCKER_COMPOSE := \#)
	$(eval EXEC := )

.PHONY: build start stop no-docker

.DEFAULT_GOAL := help
help:
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
.PHONY: help