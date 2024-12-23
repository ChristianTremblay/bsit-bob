"""
Performs validation of the model/schema and data files in the 223P repository
"""

import glob
import logging
import os
import shutil
import sys
from pathlib import Path

import ontoenv
import pytest
import rdflib
from dotenv import load_dotenv
from rdflib import OWL

try:
    from ..ttl_tools.topquadrant_shacl import infer_and_validate
    from ..ttl_tools.validation2html import print_report
except ImportError:
    from ttl_tools.topquadrant_shacl import infer_and_validate
    from ttl_tools.validation2html import print_report

from bob import core  # to load .env if required
from bob.assemblage import configure_known_namespaces  # to bind prefixes
from bob.core import dump

load_dotenv()
S223_FOLDER = Path(os.getenv("S223_FOLDER"))
# SHACL_FOLDER = Path(os.getenv('SHACL_FOLDER'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
schema_report = None


def copy_graph(g: rdflib.Graph) -> rdflib.Graph:
    c = rdflib.Graph()
    for t in g.triples((None, None, None)):
        c.add(t)
    return c


def create_schema():
    """
    Creates the schema definition against the specified shapes
    """
    # load in schema validation shapes
    shape_graph = rdflib.Graph()
    print("Loading shapes from", S223_FOLDER / "validation")
    for shape_file in glob.glob(str(S223_FOLDER / "validation" / "*.ttl")):
        print("    Loading", shape_file)
        shape_graph.parse(shape_file, format="turtle")
    print("Loading shapes from", S223_FOLDER / "inference")
    for shape_file in glob.glob(str(S223_FOLDER / "inference" / "*.ttl")):
        print("    Loading", shape_file)
        shape_graph.parse(shape_file, format="turtle")
    print("Loading shapes from", S223_FOLDER / "models")
    for shape_file in glob.glob(str(S223_FOLDER / "models" / "*.ttl")):
        print("    Loading", shape_file)
        shape_graph.parse(shape_file, format="turtle")
    print("Loading shapes from", S223_FOLDER / "vocab")
    for shape_file in glob.glob(str(S223_FOLDER / "vocab" / "*.ttl")):
        print("    Loading", shape_file)
        shape_graph.parse(shape_file, format="turtle")
    print("Loading shapes from", S223_FOLDER / "imports")
    for shape_file in glob.glob(str(S223_FOLDER / "imports" / "**" / "*.ttl")):
        print("    Loading", shape_file)
        shape_graph.parse(shape_file, format="turtle")
    return shape_graph


@pytest.mark.skip  # the schema is provided by other. We don't need to test it here
def test_schema_validation():
    """
    Validates the schema definition against the specified shapes
    """
    # load in schema validation shapes
    shape_graph = create_schema()
    configure_known_namespaces(shape_graph)
    shape_graph.serialize("223p_schema.ttl", format="turtle")

    # import dependencies on other ontologies
    env = ontoenv.OntoEnv()
    env.import_dependencies(shape_graph)
    shape_graph.remove((None, OWL.imports, None))

    logger.info("Validating schema definition")
    # validate with topquadrant shacl
    report, valid, _ = infer_and_validate(shape_graph)
    global schema_report
    schema_report = report
    report.serialize(format="ttl")

    # valid, _, res_text = pyshacl.validate(data_graph=shape_graph, advanced=True, allow_warnings=True)
    assert (
        valid
    ), f"Schema files not passing SHACL validation. See 223p_schema.validation_report.html for details"


def test_data_validation(data_file):
    """
    Validates the graphs in the data/ folder against the data and model shapes

    WARNS but does not fail the test on a validation error for a shape with sh:Info severity
    """
    data_file = Path(data_file)

    env = ontoenv.OntoEnv()
    model = rdflib.Graph().parse(data_file, format="turtle")
    # check that model imports "http://data.ashrae.org/standard223/1.0/model/all"
    if (
        None,
        rdflib.URIRef("http://www.w3.org/2002/07/owl#imports"),
        rdflib.URIRef("http://data.ashrae.org/standard223/1.0/model/all"),
    ) not in model:
        assert False, f"Model file {data_file} does not import the s223 ontology"
    data_graph = copy_graph(model)

    # load in all dependent data validation and model definition shapes
    env.import_dependencies(model)
    data_graph += model

    # remove all owl:imports statements from model and data graph
    # we need to run pyshacl multiple times to get all the inferred values
    logger.info(
        "Validating data definition of %s (%d triples)", data_file, len(data_graph)
    )
    # run topquadrant shacl and get the report
    report, valid, inferred = infer_and_validate(data_graph)
    configure_known_namespaces(report)
    configure_known_namespaces(inferred)
    # make 'compiled' directory
    (data_file.parent / "validation").mkdir(exist_ok=True)
    # save inferred graph under same name into data/compiled/
    inferred.serialize(
        data_file.parent / "validation" / data_file.name, format="turtle"
    )
    report.serialize(
        data_file.parent / "validation" / f"{data_file.stem}.validation_report.ttl",
        format="turtle",
    )
    # global schema_report
    # if schema_report is not None:
    #    schema_report.serialize(
    #        data_file.parent / "compiled" / f"{data_file.stem}.schema_report.ttl",
    #        format="turtle",
    #    )
    global schema_report
    if schema_report is not None:
        schema_report.serialize(
            data_file.parent / "validation" / f"{data_file.stem}.schema_report.ttl",
            format="turtle",
        )

        html_path = data_file.parent / "validation" / "schema.validation_report.html"
        print_report(
            schema_report, show_info=True, html_path=html_path, title=data_file.stem
        )
        _sample_doc_folder = html_path.parent.parent.parent / "doc"
        if _sample_doc_folder.exists():
            _existing_file = _sample_doc_folder / "schema.validation_report.html"
            if _existing_file.exists():
                os.remove(_existing_file)
            shutil.move(html_path, _sample_doc_folder)

    html_path = (
        data_file.parent / "validation" / f"{data_file.stem}.validation_report.html"
    )
    print_report(report, show_info=True, html_path=html_path, title=data_file.stem)
    _sample_doc_folder = html_path.parent.parent.parent / "doc"
    if _sample_doc_folder.exists():
        _existing_file = _sample_doc_folder / f"{data_file.stem}.validation_report.html"
        if _existing_file.exists():
            os.remove(_existing_file)
        shutil.move(html_path, _sample_doc_folder)
    assert report.serialize(format="ttl")
    assert valid


def dump_graphs():
    """
    Dumps the schema and data graphs to ttl files
    """
    # load in all dependent data validation and model definition shapes
    env = ontoenv.OntoEnv()
    shape_graph = create_schema()
    env.import_dependencies(shape_graph)
    dump(
        shape_graph,
        filename="schema.ttl",
        header="# Schema definition for the 223P repository",
    )


if __name__ == "__main__":
    dump_graphs()
