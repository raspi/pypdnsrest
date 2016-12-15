#!/bin/bash -e

export VENV="$(dirname $(readlink -f "$0"))"
python3 -m venv $VENV

cd $VENV

find dist/ -type f -delete

$VENV/bin/python setup.py sdist

cd -
