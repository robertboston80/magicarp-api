#!/usr/bin/env bash

python setup.py sdist upload -r testpypi
python setup.py bdist_wheel upload -r testpypi
