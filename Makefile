# Copyright (C) 2017 Alpha Griffin
# @%@~LICENSE~@%@
#
# A most basic make file.


.PHONY: default

default: help
	@echo
	@echo "Please choose a make target and try again."

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  help           display this help screen"
	@echo ""
	@echo "  all            to make all common tasks: example"
	@echo "  clean          to clean all common tasks: example_clean"
	@echo ""
	@echo "  install        to install what has been built to the system (first try make all)"
	@echo ""
	@echo "  example        to build this example"
	@echo "  example_clean  to clean up after this example build"


all:	example

clean:	example_clean



example:
	@echo Congratulations...example build does nothing!

example_clean:
	@echo Congratulations...example build has nothing to clean up!



install:
	@echo Congratulations...faux project has nothing to install!




