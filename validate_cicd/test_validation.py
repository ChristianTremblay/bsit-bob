"""
Performs validation of the model/schema and data files in the 223P repository
"""

import glob
import logging
import os
import sys
from pathlib import Path

import ontoenv
import rdflib
from dotenv import load_dotenv

from .topquadrant_shacl import validate

load_dotenv()
S223_FOLDER = Path(os.getenv("S223_FOLDER"))
# SHACL_FOLDER = Path(os.getenv('SHACL_FOLDER'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def copy_graph(g: rdflib.Graph) -> rdflib.Graph:
    c = rdflib.Graph()
    for t in g.triples((None, None, None)):
        c.add(t)
    return c


def test_schema_validation():
    """
    Validates the schema definition against the specified shapes
    """
    # load in schema validation shapes
    shape_graph = rdflib.Graph()
    for shape_file in glob.glob(str(S223_FOLDER / "validation" / "*.ttl")):
        shape_graph.parse(shape_file, format="turtle")
    for shape_file in glob.glob(str(S223_FOLDER / "inference" / "*.ttl")):
        shape_graph.parse(shape_file, format="turtle")
    for shape_file in glob.glob(str(S223_FOLDER / "models" / "*.ttl")):
        shape_graph.parse(shape_file, format="turtle")
    for shape_file in glob.glob(str(S223_FOLDER / "vocab" / "*.ttl")):
        shape_graph.parse(shape_file, format="turtle")
    for shape_file in glob.glob(str(S223_FOLDER / "imports" / "**" / "*.ttl")):
        shape_graph.parse(shape_file, format="turtle")

    # import dependencies on other ontologies
    env = ontoenv.OntoEnv()
    env.import_dependencies(shape_graph)

    logger.info("Validating schema definition")
    # validate with topquadrant shacl
    report, valid, _ = validate(shape_graph)

    # valid, _, res_text = pyshacl.validate(data_graph=shape_graph, advanced=True, allow_warnings=True)
    assert (
        valid
    ), f"Schema files not passing SHACL validation:\n{report.serialize(format='ttl')}"


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
    report, valid, inferred = validate(data_graph)
    # make 'compiled' directory
    (data_file.parent / "compiled").mkdir(exist_ok=True)
    # save inferred graph under same name into data/compiled/
    inferred.serialize(data_file.parent / "compiled" / data_file.name, format="turtle")
    assert valid, report.serialize(format="ttl")
