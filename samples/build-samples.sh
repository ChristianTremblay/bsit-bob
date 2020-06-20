#!/bin/bash

for f in *.py
do
    ttl=${f/[.]py/.ttl}
    echo $ttl
    python $f > $ttl
done
