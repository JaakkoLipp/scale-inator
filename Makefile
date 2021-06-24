.PHONY: all build clean install uninstall lint

all: help

help:
	@echo Valid options are: help, install, uninstall or lint

clean:
	$(RM) -rd build
	$(RM) -rd dist
	$(RM) -rd scale_inator.egg-info
	$(RM) -rd scale_inator/__pycache__

install:
	python setup.py install --user

uninstall:
	pip uninstall scale_inator

lint:
	flake8 scale_inator --exit-zero
