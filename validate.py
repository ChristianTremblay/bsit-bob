# -*- coding: utf-8 -*-

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

# turtle files to load into the data graph
parser.add_argument(
    "ttl",
    type=str,
    nargs="+",
    help="turtle files to load",
)

# option to load an additional ontology graph that is merged with the data
# graph before validation rules are run
parser.add_argument(
    "--ontology",
    type=str,
    help="load an ontology graph",
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

# sample additional option to store the post-validate graph
parser.add_argument(
    "--inference",
    type=str,
    help="store the inference graph",
)

# load/run inference rules in s223 standard inference directory
parser.add_argument(
    "--s223-sparql-rule",
    action="store_true",
    help="runs SPARQL construct rules in inference directory",
)

# run file(s) of sparql rules
parser.add_argument(
    "--sparql-rule",
    type=str,
    nargs='+',
    help="runs SPARQL rules in file",
)

# sample additional option to store the post-validate graph
parser.add_argument(
    "--report",
    type=str,
    help="store the report graph",
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

# get standard directory
S223_DIRECTORY = os.getenv("S223_DIRECTORY")
if not S223_DIRECTORY:
    raise RuntimeError("S223_DIRECTORY unset")

# load the data graph(s)
data_graph = Graph()
for fname in args.ttl:
    if fname == "-":
        data_graph.parse(sys.stdin, format="turtle")
    else:
        data_graph.parse(fname, format="turtle")
        if args.info and sys.stdin.isatty():
            print(f"data triples: {len(data_graph)}")

# load the shapes graphs
shacl_graph = Graph()
for fname in glob.glob(os.path.join(S223_DIRECTORY, "models", "*.ttl")):
    logging.debug(fname)
    shacl_graph.load(fname, format="turtle")

for fname in glob.glob(os.path.join(S223_DIRECTORY, "validation", "*.ttl")):
    logging.debug(fname)
    shacl_graph.load(fname, format="turtle")

# load the vocabulary into the ontology graph
ontology_graph = Graph()
for fname in glob.glob(os.path.join(S223_DIRECTORY, "vocab", "*.ttl")):
    logging.debug(fname)
    ontology_graph.load(fname, format="turtle")

if args.ontology:
    ontology_graph.parse(fname, format="turtle")
    if args.info and sys.stdin.isatty():
        print(f"ontology triples: {len(ontology_graph)}")

if args.s223_sparql_rule:
    for fname in glob.glob(os.path.join(S223_DIRECTORY, "inference", "*.ttl")):
        logging.debug(fname)
        shacl_graph.load(fname, format="turtle")
if args.sparql_rule:
    for fname in args.sparql_rule:
        shacl_graph.parse(fname, format = 'turtle')
        print(shacl_graph.print())

# expand the graph
if args.rdfs or args.owlrl or args.both:
    if (args.rdfs and args.owlrl) or args.both:
        inferencer = owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics)
    elif args.rdfs and not args.owlrl:
        inferencer = owlrl.DeductiveClosure(owlrl.RDFS_Semantics)
    elif not args.rdfs and args.owlrl:
        inferencer = owlrl.DeductiveClosure(owlrl.OWLRL_Semantics)
    inferencer.expand(data_graph)
    if args.info and sys.stdin.isatty():
        print(f"data triples after inferencer: {len(data_graph)}")

# clean out most of the useless triples
if args.clean:
    for (s, p, o) in data_graph.triples((None, RDF.type, RDFS.Resource)):
        data_graph.remove((s, p, o))
    for (s, p, o) in data_graph.triples((None, RDF.type, RDFS.Datatype)):
        data_graph.remove((s, p, o))
    for (s, p, o) in data_graph.triples((None, RDF.type, OWL.Thing)):
        data_graph.remove((s, p, o))
    for (s, p, o) in data_graph.triples((OWL.Nothing, None, None)):
        data_graph.remove((s, p, o))
    for (s, p, o) in data_graph.triples((OWL.Thing, None, None)):
        data_graph.remove((s, p, o))
    for (s, p, o) in data_graph.triples((None, OWL.sameAs, None)):
        if s == o:
            data_graph.remove((s, p, o))
    if args.info and sys.stdin.isatty():
        print(f"data triples after cleaning: {len(data_graph)}")

# save the expanded graph for debugging
if args.expanded:
    with open(args.expanded, "wb") as f:
        data_graph.serialize(f, format="turtle")

# print out the prefixes
if args.info and sys.stdin.isatty():
    print("prefixes:")
    for prefix, uriref in data_graph.namespaces():
        print(f"    {prefix}: {uriref}")
    print("")

# create a validator and run it
v = Validator(
    data_graph,
    shacl_graph=shacl_graph,
    ont_graph=ontology_graph,
    options={"iterate_rules": True, "advanced": True},
)
conforms, report_graph, report_text = v.run()

# option to save the report graph
if args.report:
    with open(args.report, "wb") as f:
        report_graph.serialize(f, format="turtle")

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
color_map = {SH.Violation: 33, SH.Info: 34, SH.Warning: 35}

# query
results = sorted(report_graph.query(qs, initNs=namespace_map))
prev = None
for focusNode, resultMessage, resultSeverity in results:
    if focusNode != prev:
        print(focusNode)
        prev = focusNode
    color = color_map[resultSeverity]
    print(f"\x1b[{color}m    {resultMessage}\x1b[0m")

# option to save the inference graph
if args.inference:
    expanded_graph = v.target_graph
    if data_graph is expanded_graph:
        logging.info("data_graph is expanded_graph")
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

        with open(args.inference, "wb") as f:
            xor_graph.serialize(f, format="turtle")
