

all:
	python placer.py

g:
	python gui.py


t: tests
tests:
	pytest . --doctest-module --ignore=venv/ --ignore=gui.py
