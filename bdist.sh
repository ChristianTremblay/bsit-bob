#!/bin/bash

# remove everything in the current dist/ directory
[ -d dist ] && rm -Rf dist

# start with a clean build directory
[ -d build ] && rm -Rf build

# remove the egg info
[ -d bob.egg-info ] && rm -Rf bob.egg-info

# use the build package
python3 -m build --no-isolation

echo
echo	This is what was built...
echo
ls -1 dist/
echo
