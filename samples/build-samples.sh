#!/bin/bash

for f in sample*.py
do
    ttl=${f/[.]py/.ttl}
    echo $ttl
    python $f | python ../sort_turtle_file.py > $ttl
done
