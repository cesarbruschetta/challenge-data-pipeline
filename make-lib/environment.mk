install-poetry: ## Installs poetry as user
	@pip install poetry --user

dependencies: ## Installs dev dependencies
	@poetry install --no-root

shell: ## Open an ipython on poetry
	@poetry run ipython

install-env-file: ## Create an .env file based on .env.example
	@if test -f .env; then cp .env .env.bkp && \
	echo "Warning: Backing up existing '.env' file"; fi
	@cp .env.example .env && \
	echo "'.env' file create successfully"

lock: ## Update Locks Pipfile.lock
	@poetry lock
