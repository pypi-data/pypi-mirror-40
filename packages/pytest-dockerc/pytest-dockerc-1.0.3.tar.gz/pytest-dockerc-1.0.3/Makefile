ROOTDIR=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

check:
	black $(shell git ls-files "*.py")
	flake8 --max-line-length=88 .

test:
	PYTHONPATH=$(ROOTDIR) PYTEST_PLUGINS=pytest_dockerc.plugin pytest

all: check test
