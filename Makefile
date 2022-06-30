.PHONY: help
.DEFAULT_GOAL := help


prep_testing:  ## Install testing dependencies
	brew install act

on_pull:  ## Run tests for pull requests
	act -j on_pull

#---------------------------------------------

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
