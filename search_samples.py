"""
Run a SPARL query on all of the samples.
"""

import os
import sys
import glob
from pathlib import Path

from rdflib import Graph, Namespace

if sys.argv[1] == "-":
    sparql_query = sys.stdin.read()
else:
    with open(sys.argv[1]) as f:
        sparql_query = f.read()

for fname in glob.glob(os.path.join(os.getcwd(), "samples", "ttl", "*.ttl")):
    model_name = Path(fname).stem

    print(f"----- {model_name} -----")

    # load the graph
    g = Graph()
    g.load(fname, format="turtle")

    # extract the namespace definitions
    namespace_map = {}
    for prefix, uriref in g.namespaces():
        namespace_map[prefix] = Namespace(uriref)

    # run the query
    for result in g.query(sparql_query, initNs=namespace_map):
        print("    ".join(str(item) for item in result))
