import argparse
import json
import os
import shutil
from pathlib import Path

import rdflib
from rdflib import BNode, Graph, Literal, URIRef

from bob.core import clear
from rdf2html.rdf2html import to_html

SEPARATOR = "; "


def load_query(query_file):
    with open(query_file, "r") as file:
        return file.read()


def execute_query(graph, query):
    return graph.query(query)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Load RDF graph and execute SPARQL query."
    )
    parser.add_argument("ttl_file", type=str, help="Path to the compiled.ttl file")
    parser.add_argument(
        "sparql", type=str, help="Path to the SPARQL query file or folder"
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move the output file to a different directory",
        default=True,
    )

    args = parser.parse_args()

    # Load the RDF graph
    ttl_file = Path(args.ttl_file).resolve()
    graph = rdflib.Graph()
    graph.parse(ttl_file, format="ttl")
    queries = Path(args.sparql).resolve()
    if queries.is_dir():
        for each_query in queries.iterdir():
            query(graph, Path(each_query), args.move)
    else:
        query(graph, queries, args.move)


def query(model: rdflib.Graph = None, sparql: Path = None, move=False):
    # Load the SPARQL query
    query = load_query(sparql)

    # Execute the query
    results = execute_query(model, query)

    # Write the results to the output file
    _folder = sparql.parent
    _name = sparql.name.split(".rq")[0]
    report_file = _folder / f"{_name}_results.html"
    with open(report_file.resolve(), "w") as output_file:
        output_file.write("<html><body>\n")
        output_file.write("<h1>SPARQL Query</h1>\n")
        output_file.write("<h2>{}</h2>\n".format(_name))
        output_file.write("<pre>{}</pre>\n".format(query))
        output_file.write("<h1>Results</h1>\n")

        headers = results.vars
        output_file.write("<table border='1'>\n")
        output_file.write("<tr>")
        if results.vars is not None:
            for header in headers:
                output_file.write(f"<th>{header}</th>")
            output_file.write("</tr>\n")

            for row in results:
                output_file.write("<tr>\n")
                for var in row:
                    if var is None:
                        output_file.write(f"<td>(n/a)</td>")
                    elif isinstance(var, rdflib.term.URIRef):
                        value = model.namespace_manager.normalizeUri(var)
                        output_file.write(f"<td>{str(value)}</td>")
                    elif SEPARATOR in var:
                        value = var.split(SEPARATOR)
                        for each in value:
                            if isinstance(var, rdflib.term.URIRef) or "http" in each:
                                value = model.namespace_manager.normalizeUri(each)
                                output_file.write(f"<td>{str(value)}</td>")
                            else:
                                value = str(each)
                                output_file.write(f"<td>{str(value)}</td>")
                    else:
                        value = str(
                            var
                        )  # Fallback to the full URI if it cannot be normalized
                        output_file.write(f"<td>{str(value)}</td>")
                output_file.write("</tr>\n")
            output_file.write("</table>\n")
        # output_file.write("<h1>Graph of result</h1>\n")
        # json_result = result_to_graph(results).serialize(format='json-ld')
        # pretty_json = json.dumps(json.loads(json_result), indent=4)
        # output_file.write(f"<pre>{pretty_json}</pre>\n")
        if results.graph is not None:
            output_file.write("<h1>Browse</h1>\n")
            iframe_html = to_html(
                results.graph,
                return_html=True,
                filter_menu=False,
                physic_options=False,
            )
            try:
                iframe_html_utf8 = iframe_html.encode("utf-8").decode("utf-8")
            except UnicodeEncodeError:
                iframe_html_utf8 = iframe_html.encode("cp1252").decode("utf-8")
            output_file.write(
                '<iframe srcdoc="{}" width="100%" height="1000px"></iframe>\n'.format(
                    iframe_html_utf8.replace('"', "&quot;")
                )
            )
        # output_file.write("<h1>Text of result</h1>\n")
        # output_file.write(f"{results.serialize(format='txt').decode('utf-8')}\n")
        output_file.write("</body></html>\n")

    if move:
        destination_dir = _folder.parent / "doc"
        _existing = destination_dir / f"{_name}_results.html"
        if _existing.exists():
            print("Replacing file: ", _existing)
            os.remove(_existing.resolve())
        shutil.move(report_file, destination_dir)


if __name__ == "__main__":
    main()
