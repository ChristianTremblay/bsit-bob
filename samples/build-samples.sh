#!/bin/bash

for f in LPtest.py #sample*.py
do
    ttl=${f/[.]py/.ttl}
    echo $ttl
    python3 $f | python ../sort_turtle_file.py > $ttl
done
