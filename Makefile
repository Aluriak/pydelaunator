

g:
	python -m pydelaunator


t: tests
tests:
	pytest pydelaunator --doctest-module --ignore=venv/ --ignore=gui.py


# Pypi related recipes
upload:
	python setup.py sdist upload
install:
	python -m pip install -U pydelaunator
