ifneq ($(VIRTUAL_ENV),$(CURDIR)/venv)
$(info No virtual env found. Run these commands to make one)
$(info $Q $Q [[ -d venv ]] || virtualenv venv; . venv/bin/activate)
$(info $Q)
$(error virtualenv)
endif

NAME := $(shell python setup.py --name)
VER := $(shell python setup.py --version)
PKG := dist/$(NAME)-$(VER)-py2-none-any.whl


.PHONY: venv init build install clean test test-upload
.DEFAULT_GOAL := build

init:
	pip install .[dev]

build: $(PKG)
	@true

$(PKG):
	python setup.py sdist bdist_wheel

install: $(PKG)
	pip install $(PKG)

clean:
	rm -rf build/ dist/ $(NAME).egg-info  */*.pyc
	pip uninstall -y $(NAME) || true

test:
	tox

test-upload:
	twine check dist/*
	twine upload --repository testpypi dist/*
