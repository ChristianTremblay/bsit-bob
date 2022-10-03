#!/usr/bin/python3

"""
Browse

Load in a collection of Turtle files, optionally run an inference engine,
and prompt for a node.
"""

import argparse
import logging
import sys

import ontoenv
import owlrl
import pyshacl
from rdflib import OWL, RDF, RDFS, Graph, Namespace, URIRef

logger = logging.getLogger(__name__)

# build a parser for the command line arguments
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

# turtle files to load into the data graph
parser.add_argument(
    "ttl",
    type=str,
    nargs="+",
    help="turtle files to load",
)

# add an option to run RDFS semantics
parser.add_argument(
    "--rdfs",
    action="store_true",
    help="run RDFS semantics",
)

# add an option to run OWLRL semantics
parser.add_argument(
    "--owlrl",
    action="store_true",
    help="run OWLRL semantics",
)

# add an option to run both RDFS and OWLRL semantics
parser.add_argument(
    "--both",
    action="store_true",
    help="run both RDFS and OWLRL semantics",
)

# add an option to run both RDFS and OWLRL semantics
parser.add_argument(
    "--clean",
    action="store_true",
    help="""clean out "useless" triples""",
)

# export the graph for debugging
parser.add_argument(
    "-e",
    "--export",
    type=str,
    help="export the graph for debugging",
)

# logging options
parser.add_argument(
    "--debug",
    action="store_true",
    help="debug log level",
)
parser.add_argument(
    "--info",
    action="store_true",
    help="info log level",
)

# parse the command line arguments
args = parser.parse_args()

# logging options
if args.debug:
    logger.setLevel(logging.DEBUG)
elif args.info:
    logger.setLevel(logging.INFO)

# make a graph
g = Graph()

# load the data graph(s)
for fname in args.ttl:
    if fname == "-":
        g.parse(sys.stdin, format="turtle")
    else:
        g.parse(fname, format="turtle")
logger.info("g data: %d triples", len(g))

# suck in the ontology files
env = ontoenv.OntoEnv()
env.import_dependencies(g)
logger.info("g env: %d triples", len(g))

# expand the graph
if args.rdfs or args.owlrl or args.both:
    if (args.rdfs and args.owlrl) or args.both:
        inferencer = owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics)
    elif args.rdfs and not args.owlrl:
        inferencer = owlrl.DeductiveClosure(owlrl.RDFS_Semantics)
    elif not args.rdfs and args.owlrl:
        inferencer = owlrl.DeductiveClosure(owlrl.OWLRL_Semantics)
    inferencer.expand(g)
    logger.info("g inference: %d triples", len(g))

# clean out most of the useless triples
if args.clean:
    for (s, p, o) in g.triples((None, RDF.type, RDFS.Resource)):
        g.remove((s, p, o))
    for (s, p, o) in g.triples((None, RDF.type, RDFS.Datatype)):
        g.remove((s, p, o))
    for (s, p, o) in g.triples((None, RDF.type, OWL.Thing)):
        g.remove((s, p, o))
    for (s, p, o) in g.triples((OWL.Nothing, None, None)):
        g.remove((s, p, o))
    for (s, p, o) in g.triples((OWL.Thing, None, None)):
        g.remove((s, p, o))
    for (s, p, o) in g.triples((None, OWL.sameAs, None)):
        if s == o:
            g.remove((s, p, o))
    logger.info("g cleaned: %d triples", len(g))

# save the result for debugging
if args.export:
    g.serialize(args.export, format="turtle")

# keep an easy reference to prefixes
prefixes = {}
for prefix, uriref in g.namespaces():
    prefixes[prefix] = Namespace(uriref)

# loop for interactive queries
while True:
    print(">>> ", end="", flush=True)
    line = sys.stdin.readline()
    if not line:
        print()
        break

    if upstream := line[0] == "^":
        line = line[1:]

    # get a prefixed node name
    prefix, node_name = line[:-1].split(":")
    if prefix not in prefixes:
        print(f"{prefix}?")
        continue

    node_iri = prefixes[prefix][node_name]

    # build a mini graph of stuff that is found
    mini_graph = Graph()
    for k, v in prefixes.items():
        mini_graph.bind(k, v)

    if upstream:
        for stmt in g.triples((None, None, node_iri)):
            mini_graph.add(stmt)

    for stmt in g.triples((node_iri, None, None)):
        mini_graph.add(stmt)

        # expand the results to the next nodes
        if (stmt[1] != RDF.type) and isinstance(stmt[2], URIRef):
            for substmt in g.triples((stmt[2], None, None)):
                mini_graph.add(substmt)

    print(mini_graph.serialize(format="turtle"))
    continue
