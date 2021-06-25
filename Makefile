.PHONY: all build clean install uninstall lint

all: help

help:
	@echo Valid options are: help, install, uninstall or lint

clean:
	$(RM) -rd build
	$(RM) -rd dist
	$(RM) -rd .pytest_cache
	$(RM) -rd scale_inator.egg-info
	$(RM) -rd src/__pycache__
	$(RM) -rd src/scale_inator/__pycache__
	$(RM) -rd src/tests/__pycache__

install:
	python setup.py install --user

uninstall:
	pip uninstall scale_inator

lint:
	flake8 src --exit-zero

test:
	pytest
