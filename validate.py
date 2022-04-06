# -*- coding: utf-8 -*-

import glob
import logging
import os
import sys

from pyshacl.validate import Validator
from rdflib import OWL, RDF, RDFS, SH, Graph, Namespace

logging.basicConfig(level=logging.WARNING)

#
#   Set the environment variable to the directory where the 223standard
#   has been cloned
#
S223_DIRECTORY = os.getenv("S223_DIRECTORY")
if not S223_DIRECTORY:
    raise RuntimeError("S223_DIRECTORY unset")

data_graph = Graph()
data_graph.parse(sys.argv[1], format="turtle")

shacl_graph = Graph()
for fname in glob.glob(os.path.join(S223_DIRECTORY, "models", "*.ttl")):
    logging.debug(fname)
    shacl_graph.load(fname, format="turtle")

for fname in glob.glob(os.path.join(S223_DIRECTORY, "validation", "*.ttl")):
    logging.debug(fname)
    shacl_graph.load(fname, format="turtle")

for fname in glob.glob(os.path.join(S223_DIRECTORY, "vocab", "*.ttl")):
    logging.debug(fname)
    shacl_graph.load(fname, format="turtle")

# create a validator and run it
v = Validator(
    data_graph,
    shacl_graph=shacl_graph,
    ont_graph=Graph(),
    options={"inference": "rdfs", "iterate_rules": True, "advanced": True},
)
conforms, report_graph, report_text = v.run()

if 0:
    print("----- report_graph -----")
    print(report_graph.serialize(format="turtle"))

if 0:
    print("----- report_text -----")
    print(report_text)

# find the definitions
namespace_map = {}
for prefix, uriref in report_graph.namespaces():
    namespace_map[prefix] = Namespace(uriref)
logging.debug(namespace_map)

# find the validation results
qs = """
    SELECT ?focusNode ?resultMessage ?resultSeverity
    WHERE {
        ?report rdf:type sh:ValidationReport .
        ?report sh:result ?result .
        ?result sh:focusNode ?focusNode .
        ?result sh:resultMessage ?resultMessage .
        ?result sh:resultSeverity ?resultSeverity .
        }
    """

# pretty colors
color_map = {SH.Violation: 33, SH.Info: 34}

# query
results = sorted(report_graph.query(qs, initNs=namespace_map))
prev = None
for focusNode, resultMessage, resultSeverity in results:
    if focusNode != prev:
        print(focusNode)
        prev = focusNode
    color = color_map[resultSeverity]
    print(f"\x1b[{color}m    {resultMessage}\x1b[0m")

if 0:
    # uncomment this section to show what was added as a result of running
    # the inferencing
    expanded_graph = v.target_graph
    if data_graph is expanded_graph:
        print("----- data_graph is expanded_graph -----")
    else:
        xor_graph = data_graph ^ expanded_graph

        # remove simple things
        xor_graph.remove((None, OWL.sameAs, None))
        xor_graph.remove((None, RDF.type, RDFS.Resource))
        xor_graph.remove((RDF.type, None, None))
        xor_graph.remove((RDFS.domain, None, None))
        xor_graph.remove((RDFS.range, None, None))
        xor_graph.remove((RDFS.subPropertyOf, None, None))
        for s_, p_, o_ in xor_graph.triples((None, RDFS.subPropertyOf, None)):
            if s_ == o_:
                xor_graph.remove((s_, p_, o_))

        print("----- data_graph ^ expanded_graph -----")
        print(xor_graph.serialize(format="turtle"))
