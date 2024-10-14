#!/usr/bin/python3

"""
Merge Graphs

Load in a collection of Turtle files, optionally run an inference engine,
optionally remove OWL import statements, and save the results as a Turtle file.
"""

import argparse
import sys
from pathlib import Path

from rdflib import OWL, RDF, RDFS, Graph, Literal, URIRef

try:
    import owlrl
except ImportError:
    owlrl = None


def main():
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

    if owlrl:
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

    # add an option to remove OWL imports
    parser.add_argument(
        "--no-imports",
        action="store_true",
        help="remove OWL imports",
    )

    # add an option to clean out 'useless' statements
    parser.add_argument(
        "--clean",
        action="store_true",
        help="clean out useless statements",
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
    for fname in args.ttl[:-1]:
        g.parse(fname, format="turtle")

    # expand the graph
    if owlrl and (args.rdfs or args.owlrl or args.both):
        if (args.rdfs and args.owlrl) or args.both:
            inferencer = owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics)
        elif args.rdfs and not args.owlrl:
            inferencer = owlrl.DeductiveClosure(owlrl.RDFS_Semantics)
        elif not args.rdfs and args.owlrl:
            inferencer = owlrl.DeductiveClosure(owlrl.OWLRL_Semantics)
        inferencer.expand(g)

    # remove OWL imports
    if args.no_imports:
        for s, p, o in g.triples((None, OWL.imports, None)):
            g.remove((s, p, o))

    # clean out most of the useless triples
    if args.clean:
        for s, p, o in g.triples((None, RDF.type, RDFS.Resource)):
            g.remove((s, p, o))
        for s, p, o in g.triples((None, RDF.type, RDFS.Datatype)):
            g.remove((s, p, o))
        for s, p, o in g.triples((None, RDF.type, OWL.Thing)):
            g.remove((s, p, o))
        for s, p, o in g.triples((OWL.Nothing, None, None)):
            g.remove((s, p, o))
        for s, p, o in g.triples((OWL.Thing, None, None)):
            g.remove((s, p, o))
        for s, p, o in g.triples((None, OWL.sameAs, None)):
            if s == o:
                g.remove((s, p, o))

    _path = Path(args.ttl[-1])

    prefix = _path.stem.split(".")[0]
    header = f"# baseURI: http://example.org/{prefix}\n# imports: http://data.ashrae.org/standard223/1.0/model/all\n# prefix: {prefix}\n\n"
    s = URIRef(f"http://example.org/{prefix}")
    g.add((s, RDF.type, OWL.Ontology))
    g.add((s, OWL.imports, URIRef("http://data.ashrae.org/standard223/1.0/model/all")))
    g.add((s, OWL.versionInfo, Literal("Created with Bob The Builder")))

    # save the merged graph
    with open(args.ttl[-1], "wb") as f:
        f.write(header.encode("utf-8"))
        print(f"Saving merged graph to {args.ttl[-1]}")
        g.serialize(f, format="turtle")

    print("Done")


if __name__ == "__main__":
    main()
