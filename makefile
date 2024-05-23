.PHONY: test
test:
	pytest test/
.PHONY: check
check:
	pre-commit run --all-files
.PHONY: build
build:
	poetry build --verbose