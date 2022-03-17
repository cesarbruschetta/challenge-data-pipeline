format: isort-save black-save ## Runs isort and black on save mode 

isort-save: ## Formats imports
	@poetry run isort ${SOURCE_PATH} && \
	echo 'Isort save success!\n'

black-save: ## Formats code
	@poetry run black ${SOURCE_PATH}  && \
	echo 'Black save success!\n'

check-code: format flake8 mypy ## Runs format, flake8 and

checks: blank-line check-code ## Runs security checks, format, flake8 and

blank-line:
	@echo

flake8: ## Runs some checks on code
	@poetry run flake8 ${SOURCE_PATH}  && \
	echo 'Flake8 check success!\n'

mypy: ## Checks python typing
	@poetry run mypy \
	    --strict ${SOURCE_PATH}  && \
	echo 'Mypy check success!\n'

checks-nosave: blank-line isort black flake8 ## Runs isort and black on check mode (don't automatic format the code), flake8 and

isort: ## Shows diff for correct formating imports
	@poetry run isort --recursive --diff --check-only ${SOURCE_PATH}  && \
	echo 'Isort check success!\n'

black: ## Shows diff for correct formating code
	@poetry run black --check --diff ${SOURCE_PATH}  && \
	echo 'Black check success!\n'
