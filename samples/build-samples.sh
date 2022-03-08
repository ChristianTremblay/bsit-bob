#!/bin/bash

for f in b-59_LP.py LPtest.py pritoni_ct.py pritoni2.py sample*.py
do
    ttl=${f/[.]py/.ttl}
    echo $ttl
    python3 $f | python ../sort_turtle_file.py > $ttl
done
