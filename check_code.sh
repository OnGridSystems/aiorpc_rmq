#!/usr/bin/env bash
py_files=$(git ls-files -- '*.py' ':!:*/migrations/*.py')

if ! PIPENV_DONT_LOAD_ENV=1 pipenv run isort -m 3 -tc --check-only $py_files; \
then
  echo "'isort' returned non-zero code"
  PIPENV_DONT_LOAD_ENV=1 pipenv run isort -m 3 -tc --diff $py_files
  exit 1
fi

if ! PIPENV_DONT_LOAD_ENV=1 pipenv run black -l 79 -S --check -q $py_files; \
then
  echo "'black' returned non-zero code"
  PIPENV_DONT_LOAD_ENV=1 pipenv run black -l 79 -S --diff -q $py_files
  exit 1
fi

if ! PIPENV_DONT_LOAD_ENV=1 pipenv run flake8 $py_files; then
  echo "'flake8' returned non-zero code"
  exit 1
fi

# TODO: change to -nc after fixing C level
# TODO: change to -nb after fixing B level
complex_files=$(PIPENV_DONT_LOAD_ENV=1 pipenv run radon cc -nd $py_files)
if [ "$complex_files" != "" ]; then
  echo "Please check these files for redundant complexity:"
  echo "$complex_files"
  exit 1
fi
