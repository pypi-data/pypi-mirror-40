.PHONY: build
build: init
	pipenv run flit build

.PHONY: test
test:
	pipenv run tox
	@# pipenv run tox --sdistonly

.PHONY: publish
publish:
	flit publish

.PHONY: init
init:
	if ! pipenv 1>/dev/null; then python3 -m pip install --user pipenv; fi
	if ! pipenv --where 1>/dev/null; then pipenv install; fi
