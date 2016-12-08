pep:
	pep8 aiovalidator example tests

test: pep
	py.test -q tests

cov cover coverage: pep
	py.test --cov=aiovalidator --cov-report=html --cov-report=term tests
	@echo "open file://`pwd`/htmlcov/index.html"

cov-ci: pep
	py.test -v --cov=aiovalidator --cov-report=term tests

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
	rm -rf docs/build
	rm -rf .tox

doc: clean
	cd docs && make html
#	google-chrome file://`pwd`/docs/build/html/index.html

