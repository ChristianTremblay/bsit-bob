#!/bin/bash

# give this script the name of the data and schema file pairs like
# in samples and it will save the report and compiled TTL files

python3 validate.py $1.data.ttl $1.schema.ttl \
    ../223standard/models/*.ttl \
    ../223standard/vocab/*.ttl \
    ../223standard/validation/*.ttl \
    ../223standard/inference/model-rules.shapes.ttl \
    ../223standard/imports/qudt/VOCAB_QUDT-QUANTITY-KINDS-ALL-v2.1.ttl \
    ../223standard/imports/qudt/VOCAB_QUDT-UNITS-ALL-v2.1.ttl \
    --info \
    --report $1.report.ttl \
    --compiled $1.compiled.ttl
