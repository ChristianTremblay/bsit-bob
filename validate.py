"""
Performs validation of the model/schema and data files in the 223P repository
"""
import argparse
import logging
import sys

import ontoenv
import pyshacl
from rdflib import SH, Graph, Namespace

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

S223 = Namespace("http://data.ashrae.org/standard223#")

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
    nargs="+",
    help="load an ontology graph",
)

# option to save the report graph
parser.add_argument(
    "-r",
    "--report",
    type=str,
    help="save report turtle file",
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

# option to save the "compiled" graph
parser.add_argument(
    "--compiled",
    type=str,
    help="compiled graph",
)

# logging options
parser.add_argument(
    "-d",
    "--debug",
    action="store_true",
    help="debug log level",
)
parser.add_argument(
    "-i",
    "--info",
    action="store_true",
    help="info log level",
)
# parse the command line arguments
args = parser.parse_args()

# logging options
if args.debug:
    logger.setLevel(logging.DEBUG)
    logger.debug("debug")
elif args.info:
    logger.setLevel(logging.INFO)
    logger.info("info")

# load the data graph(s)
data_graph = Graph()
for fname in args.ttl:
    if fname == "-":
        data_graph.parse(sys.stdin, format="turtle")
    else:
        logger.debug("loading %r", fname)
        data_graph.parse(fname, format="turtle")
logger.info("data_graph: %d triples", len(data_graph))

# copy the model to calculate "compiled" graph
if args.compiled:
    model = Graph()
    pyshacl.rdfutil.clone.clone_graph(data_graph, model)
    og = Graph()
    pyshacl.rdfutil.clone.clone_graph(data_graph, og)

# load in all dependent data validation and model definition shapes
shacl_graph = Graph()
pyshacl.rdfutil.clone.clone_graph(data_graph, shacl_graph)

env = ontoenv.OntoEnv()
env.import_dependencies(shacl_graph)
logger.info("shacl_graph: %d triples", len(shacl_graph) - len(data_graph))

# inferencing option
inference = "none"
if (args.rdfs and args.owlrl) or args.both:
    inference = "both"
elif args.rdfs and not args.owlrl:
    inference = "rdfs"
elif not args.rdfs and args.owlrl:
    inference = "owlrl"
logger.info("inference: %r", inference)


valid, report_graph, report_text = pyshacl.validate(
    data_graph=data_graph,
    shacl_graph=shacl_graph,
    ont_graph=shacl_graph,
    inference=inference,
    advanced=True,
    js=True,
    allow_warnings=False,
    inplace=True,
    iterate_rules=True,
)
logger.info("report_graph: %d triples", len(report_graph))

# save the report for analysis
if args.report:
    report_graph.serialize(args.report, format="turtle")

# save the compiled graph
if args.compiled:
    data_graph = (data_graph - model) + og
    data_graph.serialize(args.compiled, format="turtle")

# find the prefix definitions so the select can find them
namespace_map = {}
for prefix, uriref in report_graph.namespaces():
    namespace_map[prefix] = Namespace(uriref)

# find the validation results
qs = """
    SELECT ?resultSeverity ?sourceShape ?resultMessage ?focusNode ?value
    WHERE {
        ?report rdf:type sh:ValidationReport .
        ?report sh:result ?result .
        ?result sh:focusNode ?focusNode .
        ?result sh:resultMessage ?resultMessage .
        ?result sh:resultSeverity ?resultSeverity .
        ?result sh:sourceShape ?sourceShape .
        OPTIONAL { ?result sh:value ?value } .
        }
    """

# pretty colors
color_map = {SH.Violation: 33, SH.Info: 34, SH.Warning: 35, S223.g36: 36}

# run the query, sort the results
results = sorted(report_graph.query(qs, initNs=namespace_map))

prev = None
for resultSeverity, sourceShape, resultMessage, focusNode, value in results:
    if sourceShape != prev:
        color = color_map[resultSeverity]
        print(f"\x1b[{color}m{resultMessage}\x1b[0m")
        prev = sourceShape
    print(f"    {focusNode}{' ' + value if value else ''}")

# tell the shell
if not valid:
    sys.exit(1)
