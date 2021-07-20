VALID_VERSIONS = 'major', 'minor' and 'patch'
VALID_TYPES = 'feature', 'bugfix', 'doc', 'removal', 'health', 'refactor', 'improve', 'automation' and 'misc'

create-changelog: ## Updates the changelog, available variables: <m> (required) - The messages to add on changelog separated by semi-colon and <t> (required) - The type of the changelog
	$(eval $(call check-var,m))
	$(eval $(call check-var,t))
ifneq ($(t), feature)
ifneq ($(t), bugfix)
ifneq ($(t), doc)
ifneq ($(t), removal)
ifneq ($(t), health)
ifneq ($(t), refactor)
ifneq ($(t), improve)
ifneq ($(t), misc)
ifneq ($(t), automation)
	$(error Invalid t='$(t)'. Availables <t> are: $(VALID_TYPES))
endif
endif
endif
endif
endif
endif
endif
endif
endif
	@export IFS=';'; \
		for i in $$(echo "${m}" | sed -r -e 's/; */;/g'); do \
			file_name=$$(uuidgen | cut -c 1-8); \
			echo $$i > changelog.d/$$(echo $${file_name}).$(t); \
		done

update-version: ## Updates the version, available variables: <v> (required) - The version type
	$(eval $(call check-var,v))
ifneq ($(v), major)
ifneq ($(v), minor)
ifneq ($(v), patch)
	$(error Invalid v='$(v)'. Availables <v> are: $(VALID_VERSIONS))
endif
endif
endif
	@git checkout master && git pull
	@poetry run bumpversion $(v) --dry-run --no-commit --list | grep new_version= | sed -e 's/new_version=//' | xargs -n 1 poetry run towncrier --yes --version
	@git commit -am 'Update CHANGELOG'
	@poetry run bumpversion $(v)
	@echo "\nChangelog and version updated successfully"

release-draft: ## Shows changelog preview
	@poetry run towncrier --draft

update-version-major: ## Updates to minor version
	@make update-version v=major

update-version-minor: ## Updates to major version
	@make update-version v=minor

update-version-patch: ## Updates to patch version
	@make update-version v=patch

push-version: ## Pushs the versioning changes to server
	@git push && git push --tags
