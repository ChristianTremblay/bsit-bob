#!/usr/bin/python3

"""
SPARQL Query

Load in a collection of Turtle files, optionally run an inference engine,
and prompt for SPARQL queries.
"""

import argparse
import sys
from rdflib import Graph, Namespace, RDF, RDFS, OWL
import owlrl

import pyparsing


# build a parser for the command line arguments
parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
)

# sample additional option to load/store from/to the expanded graph
parser.add_argument(
    "ttl", type=str, nargs="+", help="turtle files to load",
)

# add an option to run RDFS semantics
parser.add_argument(
    "--rdfs", action="store_true", help="run RDFS semantics",
)

# add an option to run OWLRL semantics
parser.add_argument(
    "--owlrl", action="store_true", help="run OWLRL semantics",
)

# add an option to run both RDFS and OWLRL semantics
parser.add_argument(
    "--both", action="store_true", help="run both RDFS and OWLRL semantics",
)

# add an option to run both RDFS and OWLRL semantics
parser.add_argument(
    "--clean", action="store_true", help="clean out useless statements",
)

# sample additional option to store the expanded graph
parser.add_argument(
    "--expanded", type=str, help="load/store the expanded graph",
)

# information about the loaded/interpreted graph
parser.add_argument(
    "--info", "-i", action="store_true", help="print prefixes in interactive mode",
)

# parse the command line arguments
args = parser.parse_args()

# make a graph
g = Graph()

# load the files
for fname in args.ttl:
    g.parse(fname, format="turtle")

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

# save the exloded graph for debugging
if args.expanded:
    with open(args.expanded, "wb") as f:
        g.serialize(f, format="turtle")

# make a reverse namespace
namespace_map = {}
for prefix, uriref in g.namespaces():
    namespace_map[prefix] = Namespace(uriref)

# print out the prefixes
if args.info and sys.stdin.isatty():
    print(f"triples: {len(g)}")
    print("prefixes:")
    for prefix, uriref in namespace_map.items():
        print(f"    {prefix}: {uriref}")
    print("")

# loop for queries
query = ""
while True:
    if sys.stdin.isatty():
        if not query:
            print(">>> ", end="", flush=True)
        else:
            print("... ", end="", flush=True)

    line = sys.stdin.readline()
    if not line:
        break
    query += " " + line[:-1]

    if not query.endswith("}"):
        continue

    try:
        query_results = g.query(query)

        for result in query_results:
            print(", ".join(result))

    except pyparsing.ParseException as parsing_error:
        args_query, args_offset, args_error = parsing_error.args
        print(" " * (args_offset + 4) + "^ " + args_error)

    query = ""
