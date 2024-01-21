#!/bin/bash

# the script needs to be run from its directory
pushd `dirname $0`

# merge all of the TTL files into one and remove the owl:imports
python3 merge-graphs.py --no-imports \
    ../../223standard/models/*.ttl \
    ../../223standard/vocab/*.ttl \
    ../../223standard/validation/*.ttl \
    ../../223standard/inference/*.shapes.ttl \
    ../../223standard/imports/qudt/VOCAB_QUDT-QUANTITY-KINDS-ALL-v2.1.ttl \
    ../../223standard/imports/qudt/VOCAB_QUDT-UNITS-ALL-v2.1.ttl \
    223standard.ttl

# build the image passing in the file name
docker build \
    --tag validate:latest \
    --file validate.dockerfile \
    .

popd
