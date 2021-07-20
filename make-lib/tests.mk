all-tests: ## Runs all tests
	@poetry run coverage run -p -m pytest -xvv ${SOURCE_PATH} \
		--disable-warnings \
		--import-mode=importlib

tests: ## Runs unit tests
	@make tests-matching-cov && \
	make coverage

define run-tests-matching
poetry run pytest -xvv ${SOURCE_PATH} -k "$(k)" $(1) \
--ignore="$(i)" \
--disable-warnings \
--import-mode=importlib
endef

tests-matching: ## Runs tests matching a patter with the 'k' parameter
	$(call run-tests-matching)

tests-matching-cov: ## Runs tests matching a patter with the 'k' parameter with coverage
	$(call run-tests-matching,--cov=${SOURCE_PATH} --no-cov-on-fail --cov-report=)

coverage: ## Runs the coverage command
	@echo "Running coverage..." && \
	poetry run coverage report && \
	poetry run coverage xml

report-html: ## Runs the coverage report in HTML
	@echo "Running coverage report in HTML..." && \
	poetry run coverage html