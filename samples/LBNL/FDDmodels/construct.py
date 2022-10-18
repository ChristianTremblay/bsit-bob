#!/usr/bin/python3

"""
SPARQL Query

Load in a collection of Turtle files, optionally run an inference engine,
and prompt for a SPARQL query or read one from stdin.
"""


import argparse
import glob
import logging
import os
import sys

import owlrl
from pyshacl.validate import Validator
from rdflib import OWL, RDF, RDFS, SH, Graph, Namespace

logging.basicConfig(level=logging.WARNING)

# environment
try:
    _dotenv_import_error = False
    _env_file = os.path.join(os.getcwd(), ".env")
    if os.path.isfile(_env_file):
        from dotenv import load_dotenv as _load_dotenv

        _load_dotenv(_env_file)
except ImportError:
    logging.warning("install python-dotenv to use your .env file")

# build a parser for the command line arguments
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

# turtle files to load
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
    help="clean out useless statements",
)

# sample additional option to store the expanded graph
parser.add_argument(
    "--expanded",
    type=str,
    help="load/store the expanded graph",
)

# information about the loaded/interpreted graph
parser.add_argument(
    "--info",
    "-i",
    action="store_true",
    help="print prefixes in interactive mode",
)

# parse the command line arguments
args = parser.parse_args()

S223_DIRECTORY = os.getenv("S223_DIRECTORY")
if not S223_DIRECTORY:
    raise RuntimeError("S223_DIRECTORY unset")

# make a graph
g = Graph()
shacl_graph = Graph()
# load the files
for fname in args.ttl:
    g.parse(fname, format="turtle")

# for fname in glob.glob(os.path.join(S223_DIRECTORY, "inference", "*.ttl")):
#     logging.debug(fname)
#     shacl_graph.load(fname, format="turtle")

shacl_graph.load("Equipment_props_rules.ttl", format="turtle")
shacl_graph.print()

# expand the graph
if args.rdfs or args.owlrl or args.both:
    if (args.rdfs and args.owlrl) or args.both:
        inferencer = owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics)
    elif args.rdfs and not args.owlrl:
        inferencer = owlrl.DeductiveClosure(owlrl.RDFS_Semantics)
    elif not args.rdfs and args.owlrl:
        inferencer = owlrl.DeductiveClosure(owlrl.OWLRL_Semantics)
    inferencer.expand(g)

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

# print out the prefixes
if args.info and sys.stdin.isatty():
    print(f"triples: {len(g)}")
    print("prefixes:")
    for prefix, uriref in g.namespaces():
        print(f"    {prefix}: {uriref}")
    print("")

# loop for interactive queries
# if sys.stdin.isatty():
#     query = ""
#     while True:
#         if not query:
#             print(">>> ", end="", flush=True)
#         else:
#             print("... ", end="", flush=True)

#         line = sys.stdin.readline()
#         if not line:
#             break
#         query += " " + line[:-1]
# else:
#     query = " ".join(sys.stdin.read().split())

# query = " ".join(query.split())
query = """
    SELECT ?o 
    WHERE {
        ?s a sh:SPARQLRule ;
            sh:construct ?o .
    }
    """

sparql_rules = shacl_graph.query(query)

for rule in sparql_rules:
    print(rule)
    results = g.query(rule)

    try:
        for triple in results:
            g.add(triple)
    except Exception as e:
        print(e)


# save the exloded graph for debugging
if args.expanded:
    with open(args.expanded, "wb") as f:
        g.serialize(f, format="turtle")

sys.exit(0)
