"""
Bob the SI-WG Builder
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
import logging

from typing import (
    Dict,
    Optional,
    Set,
    Any,
    TextIO,
    Tuple,
)

from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD

# substance identifier (s223.Air, etc) to Connection subclass
substance_classes: Dict[URIRef, Any] = {}

# logging
log_level = os.getenv("BOB_LOG", "WARNING")
numeric_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: %s" % log_level)
logging.basicConfig(level=numeric_level)

# include/exclude predicates
include_predicates: Set[str] = set(os.getenv("BOB_INCLUDE", "").split())
exclude_predicates: Set[str] = set(os.getenv("BOB_EXCLUDE", "").split())

# include/exclude defaults
if (not include_predicates) and (not exclude_predicates):
    include_predicates.add("*")

# include/exlude combination error checking
if "*" in exclude_predicates:
    if len(exclude_predicates) != 1:
        raise RuntimeError("no")
    if not include_predicates:
        raise RuntimeError("no")
if "*" in include_predicates:
    if len(include_predicates) != 1:
        raise RuntimeError("no")
if include_predicates.intersection(exclude_predicates):
    raise RuntimeError("include/exclude overlap")
logging.debug(f"include_predicates {include_predicates}")
logging.debug(f"exclude_predicates {exclude_predicates}")

# options
MANDITORY_LABEL = True

# cleanup annotation references, i.e. "System" to _nodes[attr] = System
_annotation_reference: Dict[str, type] = {}
# globals
data_graph = None
schema_graph = None


def annotation_reference(cls: type) -> type:
    """
    Class decorator that maps the class name to the class because annotations
    are just strings.
    """
    global _annotation_reference

    cls_name = cls.__name__
    if cls_name in _annotation_reference:
        raise RuntimeError(
            f"{cls_name} already references {_annotation_reference[cls_name]}"
        )

    _annotation_reference[cls_name] = cls
    return cls


def resolve_reference(cls_name: str) -> Optional[type]:
    """Return the class that this name resolves to, or None."""
    return _annotation_reference.get(cls_name, None)


# pre-load annotation references
annotation_reference(URIRef)
annotation_reference(BNode)
annotation_reference(Literal)
annotation_reference(str)


class DataGraph(Graph):
    def add(self, triple: Tuple[Any, Any, Any]) -> None:
        """
        Add a triple to the data graph, checking the predicate to see if it should
        be included or excluded.
        """
        subj, pred, obj = triple

        (
            namespace,
            namespace_uriref,
            suffix,
        ) = data_graph.namespace_manager.compute_qname(pred)
        for test_name in (namespace + ":" + suffix, namespace + ":*", "*"):
            if test_name in include_predicates:
                break
            if test_name in exclude_predicates:
                return

        # passes the tests
        super().add(triple)


class SchemaGraph(Graph):
    def add(self, triple: Tuple[Any, Any, Any]) -> None:
        """
        Add a triple to the schema graph for statements about things in the
        model being build (like subtypes of a Device) but not about things
        in the s223 namespace.
        """
        subj, pred, obj = triple

        # exclude the schema content in the s223 namespace by default
        if subj.startswith(s223):
            return

        # passes the tests
        super().add(triple)


data_graph = DataGraph()
schema_graph = SchemaGraph()


def bind_namespace(prefix: str, uri: str) -> Namespace:
    """
    Create a Namespace and bind a prefix to it in both the default data graph
    and the default schema graph.
    """
    global data_graph, schema_graph

    namespace = Namespace(uri)
    data_graph.namespace_manager.bind(prefix, URIRef(uri))
    schema_graph.namespace_manager.bind(prefix, URIRef(uri))
    return namespace


# the namespace for a node is defined in the node as the _namespace attribute
# or in the __namespace__ special global for the module of the class, or the
# parent module, or it is inherited from a superclass that is defined in the
# same module
s223 = bind_namespace("s223", "http://data.ashrae.org/standard223#")

# everything in this module belongs in the standard
__namespace__ = s223

# common namespaces
qudt = bind_namespace("qudt", "http://qudt.org/schema/qudt/")
quantitykind = bind_namespace("quantitykind", "http://qudt.org/vocab/quantitykind/")
brick = bind_namespace("brick", "https://brickschema.org/schema/1.1.0/Brick#")

# the model_namespace is used to create "blank" node identifiers, a serial
# number to make it easier to debug a constructed file
model_namespace = None


def bind_model_namespace(prefix: str, uri: str) -> Namespace:
    """
    Create a Namespace for blank node identifiers and bind a prefix to the
    prefix in the graph.
    """
    global model_namespace
    model_namespace = bind_namespace(prefix, uri)
    return model_namespace


def register_substance(substance_uri: URIRef, cls: Any) -> None:
    """
    Register a substance so that the connection operators can line up the
    correct types.
    """
    substance_classes[substance_uri] = cls


def dump(
    graph: Graph = data_graph, file: TextIO = sys.stdout, format: str = "turtle"
) -> None:
    content = graph.serialize(format=format)
    if not isinstance(content, str):
        content = content.decode("utf-8")
    file.write(content)


def turtle(graph: Graph = data_graph, format: str = "turtle") -> None:
    content = graph.serialize(format=format)
    if not isinstance(content, str):
        content = content.decode("utf-8")
    return content


def clear(graph: Graph = data_graph) -> None:
    """Remove all the triples from the graph."""
    graph.remove((None, None, None))
