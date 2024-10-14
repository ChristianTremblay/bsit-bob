#!/bin/bash

for f in g36-*.py
do
    echo "$f"
    python3 "$f"
done
