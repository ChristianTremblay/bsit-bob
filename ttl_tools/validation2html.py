import argparse
import html
from pathlib import Path
from typing import Union

import rdflib
from rdflib.namespace import SH
from rich import box
from rich.console import Console
from rich.table import Table

console = Console()


def print_report(
    ttl_graph: Union[Path, rdflib.Graph],
    show_info: bool = False,
    html_path: Path = None,
    title: str = "",
):
    stats = {"violation": 0, "error": 0, "warning": 0, "info": 0}
    if isinstance(ttl_graph, Path):
        report_g = rdflib.Graph().parse(ttl_graph, format="turtle")
    else:
        report_g = ttl_graph
    # find the prefix definitions so the select can find them
    namespace_map = {}
    for prefix, uriref in report_g.namespaces():
        namespace_map[prefix] = rdflib.Namespace(uriref)
    if "sh" not in namespace_map:
        namespace_map["sh"] = SH

    # find the validation results
    qs = """
        SELECT ?resultSeverity ?sourceShape ?resultMessage ?focusNode ?value
        WHERE {
            ?report rdf:type sh:ValidationReport ;
                sh:result ?result .
            ?result sh:focusNode ?focusNode ;
                sh:resultMessage ?resultMessage ;
                sh:resultSeverity ?resultSeverity ;
                sh:sourceShape ?sourceShape .
            OPTIONAL { ?result sh:value ?value } .
            }
        """

    # run the query, sort the results
    results = sorted(report_g.query(qs, initNs=namespace_map))

    table = Table(title=f"Validation Results for {title}", box=box.ROUNDED)

    # Define the columns
    table.add_column("Severity", no_wrap=False)
    table.add_column("Source Shape", no_wrap=False)
    table.add_column("Message", no_wrap=False)
    table.add_column("Focus Node", no_wrap=False)
    table.add_column("Value", no_wrap=False)

    prev = None
    color_map = {
        "http://www.w3.org/ns/shacl#Violation": "red",
        "http://www.w3.org/ns/shacl#Error": "red",
        "http://www.w3.org/ns/shacl#Warning": "yellow",
        "http://www.w3.org/ns/shacl#Info": "green",
    }
    severity_map = {
        "http://www.w3.org/ns/shacl#Violation": "VIOLATION",
        "http://www.w3.org/ns/shacl#Error": "ERROR",
        "http://www.w3.org/ns/shacl#Warning": "WARNING",
        "http://www.w3.org/ns/shacl#Info": "INFO",
    }
    shape_map = {
        "http://data.ashrae.org/standard223": "s223",
        "http://data.ashrae.org/standard223/si-builder": "bob",
        "http://data.ashrae.org/proposal-to-standard223": "p223",
    }

    html_content = """
    <html>
    <head>
        <title>Validation Results</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            .red {
                background-color: #ffcccc;
            }
            .yellow {
                background-color: #ffffcc;
            }
            .green {
                background-color: #ccffcc;
            }
        </style>
    </head>
    <body>
        <h1>Validation Results for {ttl_graph}</h1>
        <table>
            <tr>
                <th>Severity</th>
                <th>Source Shape</th>
                <th>Message</th>
                <th>Focus Node</th>
                <th>Value</th>
            </tr>
    """

    for resultSeverity, sourceShape, resultMessage, focusNode, value in results:
        color = color_map.get(str(resultSeverity), "white")
        severity = severity_map.get(str(resultSeverity), "UNKNOWN")
        stats[severity.lower()] += 1
        if not show_info and severity == "INFO":
            continue
        shape_prefix = shape_map.get(str(sourceShape.split("#")[0]), sourceShape)
        shape = f"{shape_prefix}:{sourceShape.split('#')[-1]}"
        focusNode = focusNode.replace(
            "/", " / "
        )  # so wrap works in the table... if not, it truncates
        value = (
            value.replace("/", " / ") if value else ""
        )  # so wrap works in the table... if not, it truncates

        table.add_row(
            severity,
            shape,
            resultMessage,
            focusNode,
            value if value else "",
            style=color,
        )
        table.add_row("", "", "", "", "")  # Add an empty row as a separator

        html_content += f"""
        <tr class="{color}">
            <td>{html.escape(severity)}</td>
            <td>{html.escape(shape)}</td>
            <td>{html.escape(resultMessage)}</td>
            <td>{html.escape(focusNode)}</td>
            <td>{html.escape(value if value else "")}</td>
        </tr>
        """

    html_content += """
        </table>
        <p>Violations: {violations}, Errors: {errors}, Warnings: {warnings}, Info: {info}</p>
    </body>
    </html>
    """.format(
        violations=stats["violation"],
        errors=stats["error"],
        warnings=stats["warning"],
        info=stats["info"],
    )

    # Write the HTML content to a file
    if html_path is not None:
        html_content = html_content.replace("{ttl_graph}", title)
        with open(html_path, "w") as f:
            f.write(html_content)

    console.print(table)
    console.print(
        f"Violation: {stats['violation']}, Errors: {stats['error']}, Warnings: {stats['warning']}, Info: {stats['info']}"
    )


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process and print RDF validation report."
    )
    parser.add_argument(
        "ttl_graph", type=str, help="Path to the TTL file or RDF graph."
    )
    parser.add_argument(
        "--show-info", action="store_true", help="Show info level messages."
    )
    parser.add_argument("--output-path", type=str, help="Path to save the HTML report.")

    args = parser.parse_args()

    ttl_graph_path = Path(args.ttl_graph)
    print_report(ttl_graph_path, show_info=args.show_info, html_path=args.output_path)
