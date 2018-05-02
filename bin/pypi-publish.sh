#!/usr/bin/env bash

rm -rf build/
rm -rf magicarp_api.egg-info/

python setup.py clean 
python setup.py sdist upload
python setup.py bdist_wheel upload
