#!/bin/bash

for f in b59_spaces.py
do
    ttl=${f/[.]py/.ttl}
    echo $ttl
    #python3 "$f" | python ../sort_turtle_file.py > "$ttl"
    python3 "$f" > "$ttl"
done
