#!/bin/bash

for f in *.py
do
    python3 $f > /dev/null
done
