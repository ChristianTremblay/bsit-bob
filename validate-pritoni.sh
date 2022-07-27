#!/bin/bash

#
#   Run the validation tool on the Pritoni model in debug mode given
#   both the data and schema files.  Save the report graph and the "compiled"
#   graph.
#

python validate.py --debug \
	samples/ttl/sample_pritoni_model.data.ttl \
	samples/ttl/sample_pritoni_model.schema.ttl \
    --report samples/ttl/sample_pritoni_model.report.ttl \
	--compiled samples/ttl/sample_pritoni_model.compiled.ttl
