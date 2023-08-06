.PHONY: all docs test

SRC:=$(shell find ml)

LIBRARY_DIR:=libml

all: test

docs:
	$(MAKE) html -C docs 

test:
	tox

dist: $(SRC)
	rm -rf dist
	python setup.py sdist

upload_to_pypi: dist
	twine upload dist/*

typecheck:
	mypy $(LIBRARY_DIR) --ignore-missing-imports

clean:
	rm -rf dist **.pyc
