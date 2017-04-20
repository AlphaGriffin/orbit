# Copyright (C) 2017 Alpha Griffin
# @%@~LICENSE~@%@
#
# A simple make file for any Python project.


.PHONY: default

default: help
	@echo
	@echo "Please choose a make target and try again."

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  help           display this help screen"
	@echo ""
	@echo "  all            to make all common tasks: python"
	@echo "  clean          to clean all common tasks: python_clean"
	@echo ""
	@echo "  install        to install what has been built to the system (first try make all)"
	@echo ""
	@echo "  python         to build Python code"
	@echo "  python_clean   to clean up after Python build"


all:	python

clean:	python_clean



python:
	./setup.py build_py

python_clean:
	./setup.py clean
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ | xargs -r rm -r



install:
	./setup.py install



