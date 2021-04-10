#!/bin/bash

for f in *.py
do
    python $f > /dev/null
done
