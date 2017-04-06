

g:
	python -m pydelaunator


t: tests
tests:
	pytest pydelaunator --doctest-module --ignore=venv/ --ignore=gui.py
mt:
	watch -n 0.5 -c -e -b make tests


# Pypi related recipes
upload:
	python setup.py sdist upload
install:
	python -m pip install -U pydelaunator
