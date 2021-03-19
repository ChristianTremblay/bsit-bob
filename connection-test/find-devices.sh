#!/bin/bash

#
#   Find all of the devices and their label.
#

python ../sparql-query.py Topology.ttl $@ << EOF
select ?x ?y where {
    ?x rdf:type d223:Device .
    ?x rdfs:label ?y .
    }
EOF
