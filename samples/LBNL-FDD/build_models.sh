#!/bin/bash

for f in *model.py device_props.py
do
    ttl=${f/[.]py/.ttl}
    echo $ttl
    #python3 "$f" | python ../sort_turtle_file.py > "$ttl"
    python3 "$f" > "$ttl"
done
