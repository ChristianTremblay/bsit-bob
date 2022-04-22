#!/usr/bin/python3

"""
SPARQL Query

Load in a collection of Turtle files, optionally run an inference engine,
and prompt for a SPARQL query or read one from stdin.
"""

import argparse
import sys

import owlrl
import pyparsing
from rdflib import Graph, URIRef, RDF, RDFS, OWL

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

# print out the prefixes
if args.info and sys.stdin.isatty():
    print(f"triples: {len(g)}")
    print("prefixes:")
    for prefix, uriref in g.namespaces():
        print(f"    {prefix}: {uriref}")
    print("")

# loop for interactive queries
if sys.stdin.isatty():
    query = ""
    while True:
        if not query:
            print(">>> ", end="", flush=True)
        else:
            print("... ", end="", flush=True)

        line = sys.stdin.readline()
        if not line:
            break
        query += " " + line[:-1]
else:
    query = " ".join(sys.stdin.read().split())

query = " ".join(query.split())

try:
    query_results = g.query(query)

    for result in query_results:
        str_result = []
        for item in result:
            if isinstance(item, URIRef):
                str_result.append(item.n3(g.namespace_manager))
            elif item is None:
                str_result.append("")
            else:
                str_result.append(item)
        print(", ".join(str_result))

except pyparsing.ParseException as parsing_error:
    args_query, args_offset, args_error = parsing_error.args
    sys.stderr.write(query + "\n")
    sys.stderr.write(" " * args_offset + "^ " + args_error + "\n")
    sys.exit(1)

sys.exit(0)
