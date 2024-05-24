.PHONY: test
test:
	poetry run pytest test/*
.PHONY: check
check:
	poetry run pre-commit run --all-files
.PHONY: build
build:
	poetry build --verbose
