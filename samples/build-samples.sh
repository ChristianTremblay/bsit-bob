#!/bin/bash

for f in sample[0-9][0-9][0-9].py
do
    ttl=${f/[.]py/.ttl}
    echo $ttl
    python $f | python sort_turtle_file.py > $ttl
done
