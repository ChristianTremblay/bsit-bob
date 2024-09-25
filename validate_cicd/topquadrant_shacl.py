import os
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple

import ontoenv
import rdflib
from dotenv import load_dotenv
from rdflib import OWL, SH

load_dotenv()

MAX_ITERATIONS = 20
S223_FOLDER = Path(os.getenv("S223_FOLDER"))
# SHACL_FOLDER = Path(os.getenv('SHACL_FOLDER'))


def validate(data_graph: rdflib.Graph) -> Tuple[rdflib.Graph, bool, rdflib.Graph]:
    """
    Returns a tuple of (report_graph, valid, data_graph) where report_graph is the SHACL report graph,
    valid is a boolean indicating whether the data_graph is valid, and data_graph is the data graph
    with inferred triples added.
    """
    # import dependencies on other ontologies
    env = ontoenv.OntoEnv(initialize=True)
    env.import_dependencies(data_graph)

    # remove imports
    data_graph.remove((None, OWL.imports, None))

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        # Define the target path within the temporary directory
        target_file_path = temp_dir_path / "data.ttl"

        data_graph.serialize(target_file_path, format="ttl")

        # Run inference in a loop until the size of the data_graph doesn't change or we have run at least two iterations
        previous_size = 0
        current_size = len(data_graph)
        iteration_count = 0

        while iteration_count < MAX_ITERATIONS or previous_size != current_size:
            print(
                f"Running inference iteration {iteration_count} (previous size: {previous_size}, current size: {current_size})"
            )
            iteration_count += 1
            # get the shacl-1.4.2/bin/shaclinfer.sh script from the same directory
            # as this file
            script = (
                Path(__file__).resolve().parent.parent
                / "topbraid-validate"
                / "shacl-1.4.2"
                / "bin"
                / "shaclinfer.sh"
            )
            try:
                print(f"Running {script} -datafile {target_file_path}")
                output = subprocess.check_output(
                    ["/bin/bash", script, "-datafile", target_file_path],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )
            except subprocess.CalledProcessError as e:
                output = e.output  # Capture the output of the failed subprocess
            # Write logs to a file in the temporary directory (or the desired location)
            inferred_file_path = temp_dir_path / "inferred.ttl"
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

        # get the shacl-1.4.2/bin/shaclvalidate.sh script from the same directory
        # as this file
        script = (
            Path(__file__).resolve().parent.parent
            / "topbraid-validate"
            / "shacl-1.4.2"
            / "bin"
            / "shaclvalidate.sh"
        )
        try:
            print(f"Running {script} -datafile {target_file_path}")
            output = subprocess.check_output(
                ["/bin/bash", script, "-datafile", target_file_path],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
        except subprocess.CalledProcessError as e:
            output = e.output  # Capture the output of the failed subprocess

        # Write logs to a file in the temporary directory (or the desired location)
        report_file_path = temp_dir_path / "report.ttl"
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


# simple CLI for using this outside of pytest
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate a graph against the data and model shapes"
    )
    parser.add_argument("graph", type=str, help="graph file to validate")
    args = parser.parse_args()

    g = rdflib.Graph().parse(args.graph, format="turtle")
    report, valid, _ = validate(g)
    print(report.serialize(format="turtle"))
    print(f"Valid?: {valid}")
