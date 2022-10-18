#!/bin/bash

#
#   Find all of the Equipments and their label.
#

python3 ../sparql-query.py Topology.ttl $@ << EOF
select ?x ?y where {
    ?x rdf:type s223:Equipment .
    ?x rdfs:label ?y .
    }
EOF
