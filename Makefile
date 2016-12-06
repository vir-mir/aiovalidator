doc:
	cd docs && make html
	@echo "open file://`pwd`/docs/_build/html/index.html"

pep:
	pep8 aiorest_validator example tests

test: pep
	py.test -q tests

cov cover coverage: pep
	py.test --cov=aiorest_validator --cov-report=html --cov-report=term tests
	@echo "open file://`pwd`/htmlcov/index.html"

cov-ci: pep
	py.test -v --cov=aiorest_validator --cov-report=term tests

clean:
	find . -name __pycache__ |xargs rm -rf
	find . -type f -name '*.py[co]' -delete
	find . -type f -name '*~' -delete
	find . -type f -name '.*~' -delete
	find . -type f -name '@*' -delete
	find . -type f -name '#*#' -delete
	find . -type f -name '*.orig' -delete
	find . -type f -name '*.rej' -delete
	rm -f .coverage
	rm -rf coverage
	rm -rf docs/_build
	rm -rf .tox
