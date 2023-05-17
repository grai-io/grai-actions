.PHONY: help
.DEFAULT_GOAL := help

# Get the name of all of the directories in the current directory
LOCAL_DIRS := $(shell find . -maxdepth 1 -type d -not -path '*/\.*' -not -path '.' | xargs -I{} basename {})
build_md:  ## Run migrations
	@ rm README.md
	@ cp base_readme.md README.md
	@ echo "\n# Integrations\n" >> README.md
	@for dir in $(LOCAL_DIRS); do \
		if [[ -f $$dir/README.md ]]; then \
			echo "#$$(cat $$dir/README.md)" >> README.md; \
			echo "  " >> README.md; \
		fi; \
	  done



#---------------------------------------------

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
