import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Tuple

import ontoenv
import rdflib
from dotenv import load_dotenv
from rdflib import OWL, SH

from ttl_tools.validation2html import print_report

load_dotenv()

MAX_ITERATIONS = 20
S223_DIRECTORY = (
    Path(os.getenv("S223_DIRECTORY")) if os.getenv("S223_DIRECTORY") else None
)
SHACL_HOME = Path(os.getenv("SHACL_HOME")) if os.getenv("SHACL_HOME") else None
WINDOWS = True if sys.platform == "win32" else False


def infer(
    data_graph: rdflib.Graph = None,
    dir_path: Path | str = None,
    target_file_path: Path | str = None,
    returns_graph=False,
) -> rdflib.Graph | None:
    "Returns inferred triples from input graph"
    # Run inference in a loop until the size of the data_graph doesn't change or we have run at least two iterations
    previous_size = 0
    current_size = len(data_graph)
    iteration_count = 0
    original_size = len(data_graph)

    while int(previous_size) != int(current_size):
        if iteration_count > MAX_ITERATIONS:
            break
        print(
            f"Running inference iteration {iteration_count} (previous size: {previous_size}, current size: {current_size})"
        )
        iteration_count += 1
        # get the shacl-1.4.2/bin/shaclinfer.sh script from the same directory
        # as this file
        _script_name = "shaclinfer.bat" if WINDOWS else "shaclinfer.sh"
        script_folder = (
            (
                Path(__file__).resolve().parent.parent
                / "topbraid-validate"
                / "shacl-1.4.2"
            )
            if not SHACL_HOME
            else SHACL_HOME
        )
        script = script_folder / "bin" / _script_name
        print(script)
        try:
            print(f"Running {script} -datafile {target_file_path}")
            if WINDOWS:
                output = subprocess.check_output(
                    [script, "-datafile", target_file_path],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )
            else:
                output = subprocess.check_output(
                    ["/bin/bash", script, "-datafile", target_file_path],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )
        except subprocess.CalledProcessError as e:
            output = e.output  # Capture the output of the failed subprocess
        # Write logs to a file in the temporary directory (or the desired location)
        inferred_file_path = dir_path / "inferred.ttl"
        with open(inferred_file_path, "w") as f:
            for l in output.splitlines():
                if "::" not in l:
                    f.write(f"{l}\n")
        inferred_triples = rdflib.Graph()
        inferred_triples.parse(inferred_file_path, format="turtle")
        print(f"Got {len(inferred_triples)} inferred triples")

        # add inferred triples to the data graph, then serialize it
        data_graph += inferred_triples
        data_graph.serialize(target_file_path, format="ttl")

        # Update the sizes for the next iteration
        previous_size = current_size
        current_size = len(data_graph)
    print(
        f"Inference done ({iteration_count} iterations), added {len(data_graph)-original_size} triples to graph (from {original_size} to {len(data_graph)} triples)"
    )
    if returns_graph:
        return data_graph


def infer_and_validate(
    data_graph: rdflib.Graph,
) -> Tuple[rdflib.Graph, bool, rdflib.Graph]:
    """
    Returns a tuple of (report_graph, valid, data_graph) where report_graph is the SHACL report graph,
    valid is a boolean indicating whether the data_graph is valid, and data_graph is the data graph
    with inferred triples added.
    """
    # import dependencies on other ontologies
    env = ontoenv.OntoEnv(initialize=True, strict=False)
    env.import_dependencies(data_graph)

    # remove imports
    data_graph.remove((None, OWL.imports, None))

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        # Define the target path within the temporary directory
        target_file_path = temp_dir_path / "data.ttl"
        data_graph.serialize(target_file_path, format="ttl")

        inferred_data_graph = infer(
            data_graph=data_graph,
            dir_path=temp_dir_path,
            target_file_path=target_file_path,
            returns_graph=True,
        )
        report_g, validates, data_graph = validate(
            data_graph=inferred_data_graph,
            dir_path=temp_dir_path,
            target_file_path=target_file_path,
        )
    return report_g, validates, inferred_data_graph


def validate(
    data_graph: rdflib.Graph, dir_path: Path = None, target_file_path: Path = None
) -> Tuple[rdflib.Graph, bool, rdflib.Graph]:
    # get the shacl-1.4.2/bin/shaclvalidate.sh script from the same directory
    # as this file
    _script_name = "shaclvalidate.bat" if WINDOWS else "shaclvalidate.sh"
    script_folder = (
        (Path(__file__).resolve().parent.parent / "topbraid-validate" / "shacl-1.4.2")
        if not SHACL_HOME
        else SHACL_HOME
    )
    script = script_folder / "bin" / _script_name
    try:
        print(f"Running {script} -datafile {target_file_path}")
        if WINDOWS:
            output = subprocess.check_output(
                [script, "-datafile", target_file_path],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
        else:
            output = subprocess.check_output(
                ["/bin/bash", script, "-datafile", target_file_path],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
    except subprocess.CalledProcessError as e:
        output = e.output  # Capture the output of the failed subprocess

    # Write logs to a file in the temporary directory (or the desired location)
    report_file_path = dir_path / "report.ttl"
    with open(report_file_path, "w") as f:
        for l in output.splitlines():
            if "::" not in l:  # filter out log output
                f.write(f"{l}\n")

    report_g = rdflib.Graph()
    report_g.parse(report_file_path, format="turtle")

    # check if there are any sh:resultSeverity sh:Violation predicate/object pairs
    has_violation = len(
        list(report_g.subjects(predicate=SH.resultSeverity, object=SH.Violation))
    )
    conforms = len(
        list(report_g.subjects(predicate=SH.conforms, object=rdflib.Literal(True)))
    )
    validates = not has_violation or conforms

    return report_g, validates, data_graph


def main():
    parser = argparse.ArgumentParser(
        description="Validate a graph against the data and model shapes"
    )
    parser.add_argument("graph", type=str, help="Graph file to validate")
    parser.add_argument(
        "--action",
        type=str,
        choices=["infer", "validate", "both"],
        default="both",
        help="Action to perform: 'infer' to run inference only, 'validate' to run validation only, 'both' to run both inference and validation",
    )
    parser.add_argument("dir", type=str, help="Directory path")
    args = parser.parse_args()

    g = rdflib.Graph().parse(args.graph, format="turtle")
    g.remove((None, OWL.imports, None))
    dir_path = Path(args.dir)
    target_file_name = dir_path / "data.ttl"
    g.serialize(target_file_name, format="ttl")

    if args.action in {"infer", "both"}:
        infer(g, dir_path, target_file_name)

    if args.action in {"validate", "both"}:
        report, valid, _ = validate(g, dir_path, target_file_name)
        print_report(report.serialize(format="turtle"))
        print(f"Valid?: {valid}")


# simple CLI for using this outside of pytest
if __name__ == "__main__":
    main()
