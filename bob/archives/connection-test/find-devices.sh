#!/bin/bash

#
#   Find all of the devices and their label.
#

python3 ../sparql-query.py Topology.ttl $@ << EOF
select ?x ?y where {
    ?x rdf:type s223:Device .
    ?x rdfs:label ?y .
    }
EOF
