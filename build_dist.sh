#!/bin/bash

# remove everything in the current dist/ directory
[ -d dist ] && rm -Rfv dist

# start with a clean build directory
[ -d build ] && rm -Rfv build

for version in 3.7 3.8 3.9 3.10; do
    if [ -a "`which python$version`" ]; then
        python$version setup.py bdist_egg
        python$version setup.py bdist_wheel
        rm -Rfv build/
    fi
done

echo
echo	This is what was built...
echo
ls -1 dist/
echo
