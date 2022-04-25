"""
Bob the SI-WG Builder
"""

from __future__ import annotations

import inspect
import io
import logging
import os
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Set, TextIO, Tuple, TypeVar, Union, cast

from rdflib import RDF, RDFS, XSD, BNode, Graph, Literal, Namespace, URIRef

from .multimethods import multimethod, new_class

T = TypeVar("T")
NodeMap = Dict[str, Union[type, str]]
_next_node = Counter()

# environment
try:
    _dotenv_import_error = False
    _env_file = os.path.join(os.getcwd(), ".env")
    if os.path.isfile(_env_file):
        from dotenv import load_dotenv as _load_dotenv

        _load_dotenv(_env_file)
except ImportError:
    _dotenv_import_error = True

# logging
log_level = os.getenv("BOB_LOG", "WARNING")
numeric_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: %s" % log_level)
logging.basicConfig(level=numeric_level)

if _dotenv_import_error:
    logging.warning("install python-dotenv to use your .env file")

# include/exclude predicates
include_predicates: Set[str] = set(os.getenv("BOB_INCLUDE", "").split())
exclude_predicates: Set[str] = set(os.getenv("BOB_EXCLUDE", "").split())

# include/exclude defaults
if (not include_predicates) and (not exclude_predicates):
    include_predicates.add("*")

# include/exclude combination error checking
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
INCLUDE_INVERSE = bool(
    os.getenv("INCLUDE_INVERSE", None) == "True"
)  # include inverse relations

# globals
data_graph = None
schema_graph = None

# cleanup annotation references, i.e. "System" to _nodes[attr] = System
_annotation_reference: Dict[str, type] = {}


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
annotation_reference(bool)
annotation_reference(int)
annotation_reference(float)
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
# or in the _namespace special global for the module of the class, or the
# parent module, or it is inherited from a superclass that is defined in the
# same module
s223 = bind_namespace("s223", "http://data.ashrae.org/standard223#")

# This namespace is added so in the development of Bob, when new cases occurs
# we can clearly establish that a new class is not yet part of the standard
p223 = bind_namespace("p223", "http://data.ashrae.org/proposal_to_standard223#")


# everything in this module belongs in the standard
_namespace = s223

# common namespaces
qudt = bind_namespace("qudt", "http://qudt.org/schema/qudt/")
quantitykind = bind_namespace("quantitykind", "http://qudt.org/vocab/quantitykind/")
quantityValue = bind_namespace(
    "quantityValue", "http://qudt.org/schema/qudt/QuantityValue"
)
unit = bind_namespace("unit", "http://qudt.org/vocab/unit/")
brick = bind_namespace("brick", "https://brickschema.org/schema/1.1.0/Brick#")
owl = bind_namespace("owl", "http://www.w3.org/2002/07/owl#")
rdf = bind_namespace("owl", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
enum = bind_namespace(
    "enum", "http://data.ashrae.org/standard223/1.0/vocab/enumeration#"
)
bacnet = bind_namespace("bacnet", "http://data.ashrae.org/bacnet/2020#")
ref = bind_namespace("ref", "https://brickschema.org/schema/Brick/ref#")
tsdb = bind_namespace("tsdb", "https://brickschema.org/schema/Brick/ref/tsdb#")

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


def dump(
    graph: Graph = data_graph,
    file: TextIO = sys.stdout,
    filename: str = None,
    format: str = "turtle",
    header: str = None,
) -> str:
    if not header:
        content = graph.serialize(format=format)
    else:
        content = header + graph.serialize(format=format)
    if not isinstance(content, str):
        content = content.decode("UTF-8")

    content = clean_and_sort_turtle_file(content)
    if filename:
        with open(filename, "w", encoding="UTF-8") as ttl_file:
            ttl_file.write(content)
    file.write(content)


def clean_and_sort_turtle_file(content: str) -> str:
    """
    This will assure the TTL file header contains no
    duplicates, header is well formatted and
    all triples are sorted. We also remove blank lines
    to save some space.

    This is the equivalent of the sort_turtle_file script
    in the repo.

    """
    lines = io.StringIO(content).readlines()
    new_lines = ""
    chunks = []
    while lines:
        blank_line_index = 0
        try:
            blank_line_index = lines.index("\n")
        except ValueError:
            pass  # sort already done
        chunks.append(lines[0 : blank_line_index + 1])
        lines = lines[blank_line_index + 1 :]

    # print out the "# baseURI:" and "# imports:"
    new_lines += "".join(chunks[0][:-1])
    del chunks[0]

    # sort
    chunks.sort()

    # extract @prefix lines
    prefix_chunks = []
    prefix_indx = []
    for i, chunk in enumerate(chunks):
        if chunk[0].startswith("@prefix"):
            prefix_chunks.extend(chunk)
            prefix_indx.append(i)

    # remove the lines we found
    for i in reversed(prefix_indx):
        del chunks[i]

    # remove the blank lines
    prefix_chunks = [chunk for chunk in prefix_chunks if chunk != "\n"]

    # sort them and remove the duplicates
    prefix_chunks.sort()
    prefix_chunks = list(dict.fromkeys(prefix_chunks))
    new_lines += "".join(prefix_chunks)

    # print the rest
    for chunk in chunks:
        new_lines += "".join(chunk[:-1])

    return new_lines


def get_datagraph(graph: Graph = data_graph) -> Graph:
    content = graph
    return content


def clear(graph: Graph = data_graph) -> None:
    """Remove all the triples from the graph, reset the blank node counter."""
    global _next_node

    # remove all the triples
    graph.remove((None, None, None))

    # reset the "blank" node counter
    _next_node = Counter()


# === NODES
class NodeMetaclass(type):
    def __new__(
        cls: Any,
        clsname: str,
        superclasses: Tuple[type, ...],
        attributedict: Dict[str, Any],
    ) -> NodeMetaclass:
        logging.debug(f"NodeMetaclass.__new__ {clsname}")

        # start with empty maps
        _nodes: NodeMap = {}
        _datatypes: Dict[str, Literal] = {}
        _inits: Dict[str, Any] = {}

        attr_names: Set[str] = set()
        _attr_uriref: Dict[str, URIRef] = {}

        _data_graph: Graph
        _schema_graph: Graph

        # include the maps this class is inheriting
        for supercls in reversed(superclasses):
            logging.debug(f"    - supercls: {supercls!r}")
            if hasattr(supercls, "_data_graph"):
                _data_graph = supercls._data_graph  # type: ignore[attr-defined]
            if hasattr(supercls, "_schema_graph"):
                _schema_graph = supercls._schema_graph  # type: ignore[attr-defined]

            if hasattr(supercls, "_nodes"):
                _nodes.update(supercls._nodes)  # type: ignore[attr-defined]
            if hasattr(supercls, "_datatypes"):
                _datatypes.update(supercls._datatypes)  # type: ignore[attr-defined]
            if hasattr(supercls, "_inits"):
                _inits.update(supercls._inits)  # type: ignore[attr-defined]
            if hasattr(supercls, "_attr_uriref"):
                _attr_uriref.update(supercls._attr_uriref)  # type: ignore[attr-defined]
        logging.debug("    - from super classes:")
        logging.debug(f"    -     _nodes: {_nodes!r}")
        logging.debug(f"    -     _datatypes: {_datatypes!r}")
        logging.debug(f"    -     _inits: {_inits!r}")

        # update uri references defined in this new class
        _attr_uriref.update(attributedict.get("_attr_uriref", {}))  # type: ignore[attr-defined]
        logging.debug(f"    -     _attr_uriref: {_attr_uriref!r}")

        # pick up the attributes defined by annotations
        annotations = attributedict.get("__annotations__", {})
        global _annotation_reference
        for attr, attr_type in annotations.items():
            logging.debug(f"    - annotate {attr!r}: {attr_type!r}")

            if attr.startswith("_"):
                continue
            if attr in (
                "node",
                "node_type",
                "label",
                "comment",
            ):
                continue

            if isinstance(attr_type, URIRef):
                if attr_type.startswith(XSD):
                    _datatypes[attr] = attr_type
                else:
                    raise ValueError(f"datatype URI expected for {attr}: {attr_type}")
            elif inspect.isclass(attr_type):
                _nodes[attr] = attr_type
                attr_names.add(attr)
            elif isinstance(attr_type, str):
                if attr_type in _annotation_reference:
                    attr_type = _annotation_reference[attr_type]
                else:
                    _annotation_reference[attr_type] = None  # type: ignore[assignment]
                _nodes[attr] = attr_type
                attr_names.add(attr)
            else:
                raise ValueError(f"unknown annotation for {attr}: {attr_type}")
        logging.debug(f"    - _nodes: {_nodes!r}")
        logging.debug(f"    - _datatypes: {_datatypes!r}")

        # look for initializers like hasUnit = QUDT.DEG_F
        for attr, value in attributedict.items():
            if attr.startswith("_"):
                continue
            logging.debug(f"    - initialize {attr!r} = {value!r}")

            if attr in _nodes:
                if value is None:
                    continue
                if not isinstance(value, cast(type, _nodes[attr])):
                    raise TypeError(f"initializing {attr}: {_nodes[attr]} expected")

            elif attr in _datatypes:
                if isinstance(value, Literal):
                    if value.datatype != _datatypes[attr]:
                        raise TypeError(
                            f"initializing {attr}: literal {_datatypes[attr]} expected"
                        )
                elif isinstance(value, str):
                    value = Literal(value, datatype=_datatypes[attr])
                else:
                    value = Literal(value)
                    if value.datatype != _datatypes[attr]:
                        raise TypeError(
                            f"initializing {attr}: literal {_datatypes[attr]} expected"
                        )

            elif inspect.isclass(value) and issubclass(value, Node):
                _nodes[attr] = value
                attr_names.add(attr)

            else:
                continue

            _inits[attr] = value
        logging.debug(f"    - _inits: {_inits!r}")

        # add these special attributes to the class before building it
        attributedict["_nodes"] = _nodes
        attributedict["_datatypes"] = _datatypes
        attributedict["_inits"] = _inits
        attributedict["_attr_uriref"] = _attr_uriref

        # build the class
        metaclass = cast(
            NodeMetaclass,
            super(NodeMetaclass, cls).__new__(
                cls, clsname, superclasses, attributedict
            ),
        )

        # find the namespace in the class definition
        _namespace = None
        if "_namespace" in attributedict:
            _namespace = attributedict["_namespace"]
            logging.debug(f"    - class namespace: {_namespace}")
        else:
            # check the module
            cls_module = inspect.getmodule(metaclass)
            assert cls_module
            logging.debug(f"    - cls_module: {cls_module} {cls_module.__name__}")

            _namespace = getattr(cls_module, "_namespace", None)
            if _namespace:
                logging.debug(f"    - module {cls_module} namespace: {_namespace}")
            else:
                # check the parent module
                parent_module = sys.modules[
                    ".".join(cls_module.__name__.split(".")[:-1]) or "__main__"
                ]
                logging.debug(f"    - parent_module: {parent_module}")
                _namespace = getattr(parent_module, "_namespace", None)
                if _namespace:
                    logging.debug(
                        f"    - parent module {parent_module} namespace: {_namespace}"
                    )
                else:
                    # check the superclasses that are in the same module
                    for supercls in superclasses:
                        supercls_module = inspect.getmodule(supercls)
                        logging.debug(
                            f"    - supercls {supercls} module: {supercls_module}"
                        )
                        if supercls_module is not cls_module:
                            continue

                        _namespace = getattr(supercls, "_namespace", None)
                        if _namespace:
                            logging.debug(
                                f"    - supercls {supercls} namespace: {_namespace}"
                            )
                            break

        if _namespace is None:
            raise AttributeError(f"namespace not found: {clsname}")
        metaclass._namespace = _namespace  # type: ignore[attr-defined]

        # set the URIRef for the attrs defined in this class based on the
        # namespace that was just discovered _after_ the class is created
        for attr in attr_names:
            if attr in _attr_uriref:
                logging.debug(
                    f"    - attribute uri {attr!r} = already {_attr_uriref[attr]!r}"
                )
            else:
                logging.debug(f"    - attribute uri {attr!r} = {_namespace[attr]!r}")
                _attr_uriref[attr] = _namespace[attr]
        metaclass._attr_uriref = _attr_uriref  # type: ignore[attr-defined]

        # make sure it has a type
        if "node_type" not in attributedict:
            metaclass.node_type = _namespace[clsname]  # type: ignore[attr-defined]

        # this is a class, and a subclass of the super classes
        if metaclass.node_type is not None:
            _schema_graph.add((metaclass.node_type, RDF.type, RDFS.Class))
            for supercls in superclasses:
                if issubclass(supercls, Node):
                    node_type = getattr(supercls, "node_type", None)
                    if node_type is not None:
                        _schema_graph.add(
                            (metaclass.node_type, RDFS.subClassOf, supercls.node_type)
                        )

        # test to see if these special types resolve yet
        special_types_resolved = all(
            _annotation_reference.get(cname, None)
            for cname in (
                "Property",
                "ConnectionPoint",
                "SystemConnectionPoint",
                "ZoneConnectionPoint",
            )
        )

        # attributes are properties
        for attr in attr_names:
            _schema_graph.add((_attr_uriref[attr], RDF.type, RDF.Property))

            # special types get automatic sub-properties
            if special_types_resolved and (attr in _nodes):
                attr_type = _nodes[attr]
                if isinstance(attr_type, str):
                    raise RuntimeError(
                        f"unable to resolve {attr_type!r} in the definition of {attr!r}"
                    )
                if issubclass(attr_type, Property):
                    _schema_graph.add(
                        (_attr_uriref[attr], RDFS.subPropertyOf, s223.hasProperty)
                    )
                if issubclass(attr_type, ConnectionPoint):
                    _schema_graph.add(
                        (
                            _attr_uriref[attr],
                            RDFS.subPropertyOf,
                            s223.hasConnectionPoint,
                        )
                    )
                if issubclass(attr_type, SystemConnectionPoint):
                    _schema_graph.add(
                        (
                            _attr_uriref[attr],
                            RDFS.subPropertyOf,
                            s223.hasSystemConnectionPoint,
                        )
                    )
                if issubclass(attr_type, ZoneConnectionPoint):
                    _schema_graph.add(
                        (
                            _attr_uriref[attr],
                            RDFS.subPropertyOf,
                            s223.hasZoneConnectionPoint,
                        )
                    )
        # save the reference
        _annotation_reference[metaclass.__name__] = metaclass

        # let the multimethods know this is a new class, the typemap might have
        # to be reconstructed
        new_class(metaclass)

        return metaclass


class Node(metaclass=NodeMetaclass):
    """
    A node in the graph that optionally has a label.  Instances of this
    would be something like blank nodes.
    """

    _namespace: Namespace
    _data_graph: Graph = data_graph
    _schema_graph: Graph = schema_graph

    # assigned by NodeMetaclass
    _nodes: NodeMap
    _datatypes: Dict[str, Literal]
    _inits: Dict[str, Any]

    # attributes that can be changed
    _volatile: Tuple[str, ...] = ()

    node: URIRef
    node_type: Optional[URIRef] = None
    label: str
    comment: str

    def __init__(
        self,
        *,
        node_iri: URIRef = None,
        label: str = "",
        comment: str = None,
        **kwargs: Any,
    ) -> None:
        logging.debug(f"Node.__init__ label={label!r} {kwargs}")
        global _next_node, model_namespace

        if node_iri is not None:
            if not isinstance(node_iri, URIRef):
                raise TypeError(f"URIRef expected: {node_iri}")
            self.node = node_iri
        elif model_namespace:
            _next_node[model_namespace] += 1
            self.node = model_namespace[f"{_next_node[model_namespace]:05d}"]
        else:
            self.node = BNode()

        self.label = label or getattr(self, "label", "")
        if self.label:
            self._data_graph.add((self.node, RDFS.label, Literal(self.label)))

        self.comment = comment or getattr(self, "comment", "")
        if self.comment:
            self._data_graph.add((self.node, RDFS.comment, Literal(self.comment)))

        if hasattr(self, "node_type"):
            if self.node_type is not None:
                self._data_graph.add((self.node, RDF.type, self.node_type))

        for supercls in self.__class__.__mro__:
            if issubclass(supercls, Node):
                node_type = getattr(supercls, "node_type", None)
                if node_type is not None:
                    self._data_graph.add((self.node, RDF.type, node_type))

        logging.debug(f"    - _nodes: {self._nodes}")
        for attr, attr_type in self._nodes.items():
            super().__setattr__(attr, None)
            if attr in kwargs:

                setattr(self, attr, kwargs.pop(attr))

        logging.debug(f"    - _inits: {self._inits}")
        for attr, value in self._inits.items():
            if attr in kwargs:
                setattr(self, attr, kwargs.pop(attr))
            elif inspect.isclass(value):
                setattr(self, attr, value(label=self.label + "." + attr))
            else:
                setattr(self, attr, value)

        logging.debug(f"    - other: {kwargs}")
        for attr, value in kwargs.items():
            if attr in self._datatypes:
                setattr(self, attr, value)
            else:
                raise TypeError(f"unexpected keyword argument: {attr}")

    def __setattr__(self, attr: str, value: Any) -> None:
        """
        .
        """
        # continue with normal process for attributes that aren't special to us
        if attr.startswith("_") or (
            (attr not in self._nodes) and (attr not in self._datatypes)
        ):
            super().__setattr__(attr, value)
            return

        # make sure the value isn't None, no "deleting" content
        if value is None:
            raise ValueError(f"{attr} is None")

        # make sure the current value is None, no "reassigning" content
        current_value = super().__getattribute__(attr)
        if current_value is not None:
            volatile_attrs = super().__getattribute__("_volatile")
            if attr not in volatile_attrs:
                raise RuntimeError(f"attribute {attr} already has a value")

        # if this is a node, double check the type
        if attr in self._nodes:
            if isinstance(self._nodes[attr], str):
                node_class = _annotation_reference.get(self._nodes[attr], None)  # type: ignore[arg-type]
                if not node_class:
                    raise NotImplementedError(
                        f"class {self._nodes[attr]!r} for attribute {attr!r} not found"
                    )
                self._nodes[attr] = node_class
            else:
                node_class = cast(type, self._nodes[attr])

            # pass the value to the class to build one
            if not isinstance(value, node_class):
                ### if the node class doesn't allow passing an arg it SHOULD fail
                # This solves a bug when creating devices
                # where the number of argument of value is wrong
                # TypeError: __init__() takes 1 positional argument but 2 were given
                try:
                    logging.debug(f"    - construct {node_class} from: {value!r}")
                    value = node_class(value)
                except TypeError:
                    value = node_class(node_iri=value)

            # add the link(s)
            if isinstance(value, (URIRef, Literal)):
                if attr == "hasValue":
                    self._data_graph.set((self.node, self._attr_uriref[attr], value))  # type: ignore[attr-defined]
                else:
                    self._data_graph.add((self.node, self._attr_uriref[attr], value))  # type: ignore[attr-defined]
            if isinstance(value, Node):
                self._data_graph.add((self.node, self._attr_uriref[attr], value.node))  # type: ignore[attr-defined]

            # if the value is a property, link it to the node
            if isinstance(value, Property) and issubclass(node_class, Property):
                self.add_property(value)

            # if the value is an external reference, link it to the node
            if isinstance(value, ExternalReference):
                self.add_external_reference(value)

        # if this needs some datatype decoration, turn it into a literal
        if attr in self._datatypes:
            if isinstance(value, Literal):
                if value.datatype != self._datatypes[attr]:
                    raise TypeError(f"{attr}: literal {self._datatypes[attr]} expected")
            elif isinstance(value, str):
                value = Literal(value, datatype=self._datatypes[attr])
            else:
                value = Literal(value)
                if value.datatype != self._datatypes[attr]:
                    raise TypeError(f"{attr}: literal {self._datatypes[attr]} expected")

            # add the literal
            self._data_graph.add((self.node, self._attr_uriref[attr], value))  # type: ignore[attr-defined]

        # carry on
        super().__setattr__(attr, value)

    def __rshift__(self, other: Any) -> Any:
        """Build a connection from this thing to another thing."""
        connect_mm(self, other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """Build a connection to this thing from another thing."""
        connect_mm(other, self)
        return self

    def __repr__(self) -> str:
        label = getattr(self, "label", "")
        if label:
            label = " " + label
        return f"<{self.__class__.__name__}{label} at {self.node}>"

    def add_property(self, prop: Property) -> Property:
        """Add a property to a node, returns the added property."""
        assert isinstance(prop, Property)

        # link the two together
        self._data_graph.add((self.node, s223.hasProperty, prop.node))
        if INCLUDE_INVERSE:
            self._data_graph.add((prop.node, s223.isPropertyOf, self.node))

        return prop


class ExternalReference(Node):
    """
    This will be subclassed by different specific datasources, this simplest
    form uses hasRef as a literal, most likely a string.
    """

    node_type: URIRef = s223.ExternalReference
    # isExternalReferenceOf: Property
    hasRef: Literal

    def __init__(
        self,
        arg: Any = None,
        *,
        lang: Optional[str] = None,
        datatype: Optional[URIRef] = None,
        **kwargs: Any,
    ):
        logging.debug(
            f"ExternalReference.__init__ {arg!r} lang={lang!r} datetype={datatype!r} {kwargs}"
        )
        if arg is not None:
            if "hasRef" in kwargs:
                raise RuntimeError("initialization conflict")

            if isinstance(arg, Literal):
                pass
            elif datatype is not None:
                arg = Literal(arg, datatype=datatype)
            elif lang is not None:
                arg = Literal(arg, lang=lang)

            kwargs["hasRef"] = arg

        super().__init__(**kwargs)


class Property(Node):
    """
    An attribute, quality, or characteristic of a feature of interest.  This is
    an abstract base class.
    """

    # node_type: URIRef = None
    hasValue: Literal
    ofMedium: Medium
    ofSubstance: Substance
    hasExternalReference: ExternalReference

    # override this for a specialize subclass
    _external_reference_class: type = ExternalReference

    # override this for other volatile attributes
    _volatile = ("hasValue",)

    def __init__(self, value: Any = None, **kwargs: Any):
        logging.debug(f"Property.__init__ {value!r} {kwargs}")

        init_value = None
        if value is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = value

        external_reference = None
        if "hasExternalReference" in kwargs:
            if init_value:
                raise RuntimeError(
                    "initialization conflict, can't have a value and an external datasource"
                )
            external_reference = kwargs.pop("hasExternalReference")

        super().__init__(**kwargs)

        # if there is an initial value, link to it
        if init_value is not None:
            if not isinstance(init_value, Literal):
                init_value = Literal(init_value)
            self.hasValue = init_value

        # same for ExternalReference, allow initializing with a list of them
        if external_reference is not None:
            if isinstance(external_reference, list):
                for ref in external_reference:
                    self.add_external_reference(ref)
            else:
                self.add_external_reference(external_reference)

    def add_external_reference(self, external_reference: ExternalReference) -> None:
        """Add an additional external reference to a property."""
        if not isinstance(external_reference, self._external_reference_class):
            external_reference = self._external_reference_class(
                external_reference,
                label=f"{self.label}.ExternalReference",
            )

        # link the two together
        self._data_graph.add(
            (self.node, s223.hasExternalReference, external_reference.node)
        )
        if INCLUDE_INVERSE:
            external_reference.isExternalReferenceOf = self

    def __matmul__(self, external_reference: ExternalReference) -> Node:
        """
        This property is at some external reference.
        """
        self.add_external_reference(external_reference)
        return self


@annotation_reference
class PropertyReference:
    def __new__(cls, property):
        if not isinstance(property, Property):
            raise TypeError(f"property expected: {property}")
        return property


class Container(Node):
    """
    This class implements the Container Abstract Base Class.
    """

    node_type: URIRef = None
    _contents: Dict[str, Node]

    def __init__(self, *args, **kwargs) -> None:
        logging.debug(f"Container.__init__ {args} {kwargs}")
        if self.__class__ is Connectable:
            raise RuntimeError("Container is an abstract base class")

        super().__init__(*args, **kwargs)
        self._contents = {}

    def __getitem__(self, label: str) -> Node:
        logging.debug(f"Container.__getitem__ {label}")
        return self._contents[label]

    # def __len__(self):
    #     Do not define this function or `a < b < c` will break.

    def __gt__(self, other: Node) -> Node:
        """This node contains some other node."""
        logging.debug(f"Container.__gt__ {self} > {other}")

        if hasattr(other, "label"):
            if other.label in self._contents:
                raise ValueError(f"label already used: {self._contents[other.label]}")
            self._contents[other.label] = other

        contains_mm(self, other)
        return self

    def __lt__(self, other: Container) -> Node:
        """This node is contained in some other node."""
        logging.debug(f"Container.__lt__ {self} < {other}")

        if hasattr(self, "label"):
            if self.label in other._contents:
                raise ValueError(f"label already used: {other._contents[self.label]}")
            other._contents[self.label] = self

        contains_mm(other, self)
        return self


class EnumerationKind(Node):
    node_type: URIRef = s223.EnumerationKind
    _data_graph: Graph = schema_graph


class Medium(EnumerationKind):
    node_type: URIRef = s223.Medium
    _data_graph: Graph = schema_graph


Air = Medium(node_iri=s223["Medium-Air"])
Water = Medium(node_iri=s223["Medium-Water"])
Light = Medium(node_iri=s223["Medium-Light"])
Electricity = Medium(node_iri=s223["Medium-Electricity"])
NaturalGas = Medium(node_iri=s223["Medium-NaturalGas"])
CompressedAir = Medium(node_iri=s223["Medium-CompressedAir"])
# This one is weird...but to create an occupancy space, zone we
# need a medium.
# would Medium-People be better ?
People = Medium(node_iri=s223["Medium-People"])


class Direction(EnumerationKind):
    node_type: URIRef = s223.Direction
    _data_graph: Graph = schema_graph


Inlet = Direction(node_iri=s223["Direction-Inlet"])
Outlet = Direction(node_iri=s223["Direction-Outlet"])
Bidirectional = Direction(node_iri=s223["Direction-Bidirectional"])


class Substance(EnumerationKind):
    node_type: URIRef = s223.Substance
    _data_graph: Graph = schema_graph


class Domain(EnumerationKind):
    _data_graph: Graph = schema_graph


Electrical = Domain(node_iri=s223["Domain-Electrical"])
Fire = Domain(node_iri=s223["Domain-Fire"])
HVAC = Domain(node_iri=s223["Domain-HVAC"])
Lighting = Domain(node_iri=s223["Domain-Lighting"])
Networking = Domain(node_iri=s223["Domain-Networking"])
Security = Domain(node_iri=s223["Domain-Security"])
Physical = Domain(node_iri=s223["Domain-Physical"])
Refrigeration = Domain(node_iri=s223["Domain-Refrigeration"])
Plumbing = Domain(node_iri=s223["Domain-Plumbing"])
ConveyanceSystems = Domain(node_iri=s223["Domain-ConveyanceSystems"])
Occupancy = Domain(node_iri=p223["Domain-Occupancy"])


class Role(EnumerationKind):
    _data_graph: Graph = schema_graph


class Junction(Node):
    """
    Junction.
    """

    node_type: URIRef = s223.Junction
    hasMedium: Medium
    _lnx: Set[Segment]

    def __init__(self, **kwargs: Any) -> None:
        logging.debug(f"Junction.__init__ {kwargs}")
        super().__init__(**kwargs)

        # empty set of linked segments
        self._lnx = set()

    def link_to(self, other: Union[Junction, Segment, ConnectionPoint]) -> None:
        """
        Links from a junction to another junction or connection point creates a
        segment, links it to this and the other end, and then links this to
        the segment.
        """
        if isinstance(other, Segment):
            segment = other
        elif isinstance(other, (Junction, ConnectionPoint)):
            segment = Segment()
            segment.link_to(other)
        else:
            raise TypeError("Junction, Segment, or ConnectionPoint expected")

        # link the segment back
        segment.link_to(self)

    def connect_to(self, other: Union[Junction, ConnectionPoint]) -> None:
        """
        Links from a junction to a junction or connection point.  Similar
        to link_to().  This function is called by connect() to all the
        from- and to- connection points to also be junctions.
        """
        if not isinstance(other, (Junction, ConnectionPoint)):
            raise TypeError("Junction or ConnectionPoint expected")

        # create a segment and link it
        segment = Segment()
        segment.link_to(other)
        segment.link_to(self)


@multimethod
def connect_mm(from_junction: Junction, to_junction: Junction) -> None:
    """Junction >> Junction"""
    logging.info(f"connect from {from_junction} to {to_junction}")

    from_junction.link_to(to_junction)


@multimethod
def connect_mm(junction: Junction, segment: Segment) -> None:
    """Junction >> Segment"""
    logging.info(f"connect from {junction} to {segment}")

    junction.connect_to(segment)


@multimethod
def connect_mm(segment: Segment, junction: Junction) -> None:
    """Segment >> Junction"""
    logging.info(f"connect from {segment} to {junction}")

    junction.connect_to(segment)


@multimethod
def connect_mm(junction: Junction, connection_point: ConnectionPoint) -> None:
    """Junction >> ConnectionPoint"""
    logging.info(f"connect from {junction} to {connection_point}")

    junction.connect_to(connection_point)


@multimethod
def connect_mm(connection_point: ConnectionPoint, junction: Junction) -> None:
    """ConnectionPoint >> Junction"""
    logging.info(f"connect from {connection_point} to {junction}")

    junction.connect_to(connection_point)


class Segment(Node):
    """
    Segment.
    """

    node_type: URIRef = s223.Segment
    hasMedium: Medium
    _lnx: Set[Union[Junction, ConnectionPoint]]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # empty set of linked segment endpoints
        self._lnx = set()

    def link_to(self, other: Union[Junction, ConnectionPoint]) -> None:
        """
        Links from a segment to a junction or connection point.
        """
        if len(self._lnx) == 2:
            raise RuntimeError("segment already linked to two endpoints")
        if isinstance(other, Junction):
            # link the junction to the segment
            other._lnx.add(self)
            self._data_graph.add(
                (
                    other.node,
                    s223.lnx,
                    self.node,
                )
            )
        elif isinstance(other, ConnectionPoint):
            other.lnx = self
        else:
            raise TypeError("Junction or ConnectionPoint expected")

        # link the segment to the end point
        self._lnx.add(other)
        self._data_graph.add(
            (
                self.node,
                s223.lnx,
                other.node,
            )
        )


class System(Container, Node):
    """
    System
    """

    node_type: URIRef = s223.System
    hasPhysicalLocation: PhysicalSpace
    hasDomain: Domain

    _serves_zones: Dict[str, Zone]

    _system_connection_points: Dict[str, SystemConnectionPoint]

    def __init__(self, config: Dict[str, Any] = {}, *args, **kwargs: Any) -> None:
        logging.debug(f"System.__init__ {config} {args} {kwargs}")

        # if there are "params" in the configuation, use those as defaults for
        # kwargs and allow them to be overriden be additional kwargs
        # if config and "params" in config:
        #     kwargs = {**config["params"], **kwargs}

        super().__init__(*args, **kwargs)
        if config:
            for group_name, group_items in config.items():
                if group_name == "params":
                    continue

                things = []
                for (thing_name, thing_class), thing_kwargs in group_items.items():
                    if thing_name in self._contents:
                        raise ValueError(
                            f"label already used: {self._contents[thing_name]}"
                        )
                    thing = thing_class(label=thing_name, **thing_kwargs)

                    if isinstance(thing, (Device, System)):
                        self > thing
                    if isinstance(thing, Property):
                        thing @ self
                        self._contents[thing_name] = thing

                    things.append(thing)

                setattr(self, "_" + group_name, things)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        # merge the annotations
        merged_annotations = {}
        for cls in reversed(self.__class__.__mro__[:-1]):
            merged_annotations.update(cls.__annotations__)

        # instantiate and associate all of the system connection points
        self._system_connection_points = {}
        for var_name, var_annotation in merged_annotations.items():
            if var_name.startswith("_"):
                continue

            if isinstance(var_annotation, str):
                if var_annotation not in _annotation_reference:
                    logging.debug(
                        f"resolving {var_annotation!r} for attribute {var_name!r}, class not found"
                    )
                    continue
                var_annotation = _annotation_reference.get(var_annotation)

            if issubclass(var_annotation, ConnectionPoint):
                raise TypeError(
                    f"connection point {var_name}: must be a system connection point"
                )
            if not issubclass(var_annotation, SystemConnectionPoint):
                continue
            logging.debug(f"    var_annotation: {var_annotation}")

            # build an instance of this connection point
            var_element = var_annotation(self, label=self.label + "." + var_name)
            self._system_connection_points[var_name] = var_element
            logging.debug(f"    - connection point {var_name}: {var_element}")

            setattr(self, var_name, var_element)

        # zone references
        self._serves_zones = {}

    def serves_zone(self, other: Zone) -> None:
        connect_mm(self, other)


@multimethod
def contains_mm(system: System, device: Device) -> None:
    """System > Device"""
    logging.info(f"system {system} contains device {device}")

    system._data_graph.add((system.node, s223.contains, device.node))
    if INCLUDE_INVERSE:
        system._data_graph.add((device.node, s223.isContainedIn, system.node))


@multimethod
def contains_mm(system: System, subsystem: System) -> None:
    """System > System"""
    logging.info(f"system {system} contains subsystem {subsystem}")

    system._data_graph.add((system.node, s223.contains, subsystem.node))
    if INCLUDE_INVERSE:
        system._data_graph.add((subsystem.node, s223.isContainedIn, system.node))


@multimethod
def contains_mm(system: System, thing_list: List[Node]) -> None:
    """System > List[Union[Device,System]]"""
    logging.info(f"system {system} contains list of things {thing_list}")

    ###TODO: the signature should be thing_list: List[Union[Device,System]]

    for thing in thing_list:
        if not isinstance(thing, (Device, System)):
            raise TypeError(f"device or system expected: {thing}")
        contains_mm(system, thing)


class ConnectionMetaclass(NodeMetaclass):
    def __new__(
        cls: Any,
        clsname: str,
        superclasses: Tuple[type, ...],
        attributedict: Dict[str, Any],
    ) -> ConnectionMetaclass:
        logging.debug(f"ConnectionMetaclass.__new__ {clsname}")

        # build the class
        new_class = cast(
            ConnectionMetaclass,
            super().__new__(cls, clsname, superclasses, attributedict),
        )

        return new_class


class Connection(Node, metaclass=ConnectionMetaclass):
    """
    Generic connection object type, unrestricted.
    """

    node_type: URIRef = s223.Connection
    hasMedium: Medium

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class Connectable(Node):
    """
    A type of thing that can have connection points.
    """

    # node_type: URIRef = None
    _connection_points: Dict[str, ConnectionPoint]

    def __init__(self, **kwargs: Any) -> None:
        logging.debug(f"Connectable.__init__ {kwargs}")
        if self.__class__ is Connectable:
            raise RuntimeError("Connectable is an abstract base class")
        super().__init__(**kwargs)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        # merge the annotations
        merged_annotations = {}
        for cls in reversed(self.__class__.__mro__[:-1]):
            merged_annotations.update(cls.__annotations__)
        logging.debug(f"    - merged_annotations: {merged_annotations}")

        # instantiate and associate all of the connection points
        self._connection_points = {}
        for var_name, var_annotation in merged_annotations.items():
            if var_name.startswith("_"):
                continue

            if isinstance(var_annotation, str):
                if var_annotation not in _annotation_reference:
                    logging.debug(
                        f"resolving {var_annotation!r} for attribute {var_name!r}, class not found"
                    )
                    continue
                var_annotation = _annotation_reference.get(var_annotation)

            if not issubclass(var_annotation, ConnectionPoint):
                continue

            # build an instance of this connection point
            var_element = var_annotation(self, label=self.label + "." + var_name)
            self._connection_points[var_name] = var_element
            logging.debug(f"    - connection point {var_name}: {var_element}")

            setattr(self, var_name, var_element)


@multimethod
def connect_mm(from_thing: Connectable, to_thing: Connectable) -> None:
    """Connectable >> Connectable"""
    logging.info(f"connect from {from_thing} to {to_thing}")

    # build a dict of outlet connection points that are not already connected
    # organize them by medium
    from_out = defaultdict(set)
    for attr, connection_point in from_thing._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {from_thing} to {to_thing}")
    logging.debug(f"    - from_types: {from_types}")

    # build a dict of inlet connection points that are not already connected
    # organize them by medium
    to_in = defaultdict(set)
    for attr, connection_point in to_thing._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, InletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {from_thing} to {to_thing}")
    logging.debug(f"    - to_types: {to_types}")

    # find the common medium
    common_types = from_types.intersection(to_types)
    if not common_types:
        raise RuntimeError("no common connection types")
    if len(common_types) > 1:
        raise RuntimeError("too many common connection types")
    medium = common_types.pop()
    logging.debug(f"    - medium: {medium}")

    # get the two connection points
    from_connection_point = from_out[medium].pop()
    to_connection_point = to_in[medium].pop()

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


@multimethod
def connect_mm(from_thing: Connectable, to_things: List[Connectable]) -> None:
    """Connectable >> [Connectable]"""
    logging.info(f"connect from {from_thing} to {to_things}")

    # build a dict of outlet connection points that are not already connected
    # organize them by medium
    from_out = defaultdict(set)
    for attr, connection_point in from_thing._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {from_thing}")
    logging.debug(f"    - from_types: {from_types}")

    to_types_list: List[Set[Medium]] = []

    for to_thing in to_things:
        # build a dict of inlet connection points that are not already connected
        # organize them by medium
        to_in = defaultdict(set)
        for attr, connection_point in to_thing._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, InletConnectionPoint):
                continue

            medium = getattr(connection_point, "hasMedium", None)
            to_in[medium].add(connection_point)

        # filter them to a set where there is only one for that medium so it
        # would be unambiguous to use it
        to_types: Set[Medium]
        to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
        if not to_types:
            raise RuntimeError(f"no candidate destinations to {to_thing}")
        logging.debug(f"    - to_types: {to_types}")
        to_types_list.append(to_types)

    # find the common medium
    common_types = from_types.intersection(*to_types_list)
    if not common_types:
        raise RuntimeError("no common connection types")
    if len(common_types) > 1:
        raise RuntimeError("too many common connection types")
    medium = common_types.pop()
    logging.debug(f"    - medium: {medium}")

    # get from connection point
    from_connection_point = from_out[medium].pop()

    # create a connection
    connection = Connection(hasMedium=medium)

    # connect the from thing
    connect_mm(from_connection_point, connection)

    # connect the to things
    for to_thing in to_things:
        connect_mm(connection, to_thing)


class ConnectionPoint(Node):
    # node_type: URIRef = s223.ConnectionPoint
    node_type: URIRef = None
    hasMedium: Medium
    hasDirection: Direction

    lnx: Segment
    connectsThrough: Connection
    isConnectionPointOf: Connectable

    def __init__(self, thing: Connectable, **kwargs: Any) -> None:
        # abstract base class
        if self.__class__ is ConnectionPoint:
            raise RuntimeError("ConnectionPoint is an abstract base class")

        super().__init__(**kwargs)

        self._data_graph.add((thing.node, s223.hasConnectionPoint, self.node))
        self.isConnectionPointOf = thing

        # this is one of the connection points of the device
        thing._connection_points[str(self.node)] = self

    def link_to(self, other: Union[Junction, Segment]) -> None:
        """
        Links this connection point to a junction or a segment.
        """
        if self.lnx:
            raise RuntimeError("connection point already linked")

        if isinstance(other, Segment):
            segment = other
        elif isinstance(other, Junction):
            segment = Segment()
            segment.link_to(other)
        else:
            raise TypeError("Junction or Segment expected")

        # link the segment back
        segment.link_to(self)


@multimethod
def connect_mm(
    from_connection_point: ConnectionPoint, to_connection_point: ConnectionPoint
) -> None:
    """ConnectionPoint >> ConnectionPoint"""
    logging.info(f"connect from {from_connection_point} to {to_connection_point}")

    if isinstance(from_connection_point, InletConnectionPoint):
        raise TypeError(f"connection point direction: {from_connection_point}")
    if from_connection_point.connectsThrough:
        raise RuntimeError("outlet connection point already connected")

    if isinstance(to_connection_point, OutletConnectionPoint):
        raise TypeError("connection point direction: {to_connection_point}")
    if to_connection_point.connectsThrough:
        raise RuntimeError("inlet connection point already connected")

    from_medium = getattr(from_connection_point, "hasMedium", None)
    logging.debug("    - from_medium: %r", from_medium)
    to_medium = getattr(to_connection_point, "hasMedium", None)
    logging.debug("    - to_medium: %r", to_medium)

    if from_medium and to_medium and (from_medium != to_medium):
        raise RuntimeError(f"mismatched medium: {from_medium} != {to_medium}")

    # create a connection between the two
    connection = Connection()
    if from_medium:
        connection.hasMedium = from_medium

    # link the two things together
    from_connection_point._data_graph.add(
        (
            from_connection_point.isConnectionPointOf.node,
            s223.connectedTo,
            to_connection_point.isConnectionPointOf.node,
        )
    )
    from_connection_point._data_graph.add(
        (
            to_connection_point.isConnectionPointOf.node,
            s223.connectedFrom,
            from_connection_point.isConnectionPointOf.node,
        )
    )

    # set the relationships
    connect_mm(from_connection_point, connection)
    connect_mm(connection, to_connection_point)


@multimethod
def connect_mm(connection_point: ConnectionPoint, connection: Connection) -> None:
    """ConnectionPoint >> Connection"""
    logging.info(f"connect from {connection_point} to {connection}")

    if isinstance(connection_point, InletConnectionPoint):
        raise TypeError("connection point direction")
    if connection_point.connectsThrough:
        raise RuntimeError("connection point already connected")

    # check medium
    connection_medium = getattr(connection, "hasMedium", None)
    logging.debug(f"    - connection_medium: {connection_medium}")
    connection_point_medium = getattr(connection_point, "hasMedium", None)
    logging.debug(f"    - connection_point_medium: {connection_point_medium}")

    if (
        connection_medium
        and connection_point_medium
        and (connection_medium != connection_point_medium)
    ):
        raise RuntimeError(
            f"mismatched medium: {connection_medium} != {connection_point_medium}"
        )

    # property based link
    connection_point.connectsThrough = connection

    # link connection to the connection point and its device
    connection_point._data_graph.add(
        (connection.node, s223.connectsAt, connection_point.node)
    )
    connection_point._data_graph.add(
        (
            connection_point.isConnectionPointOf.node,
            s223.connectedThrough,
            connection.node,
        )
    )
    connection_point._data_graph.add(
        (
            connection.node,
            s223.connectsFrom,
            connection_point.isConnectionPointOf.node,
        )
    )


@multimethod
def connect_mm(connection: Connection, connection_point: ConnectionPoint) -> None:
    """Connection >> ConnectionPoint"""
    logging.info(f"connect from {connection} to {connection_point}")

    if isinstance(connection_point, OutletConnectionPoint):
        raise TypeError("connection point direction")
    if connection_point.connectsThrough:
        raise RuntimeError("connection point already connected")

    # check medium
    connection_medium = getattr(connection, "hasMedium", None)
    logging.debug(f"    - connection_medium: {connection_medium}")
    connection_point_medium = getattr(connection_point, "hasMedium", None)
    logging.debug(f"    - connection_point_medium: {connection_point_medium}")

    if (
        connection_medium
        and connection_point_medium
        and (connection_medium != connection_point_medium)
    ):
        raise RuntimeError(
            f"mismatched medium: {connection_medium} != {connection_point_medium}"
        )

    # property based link
    connection_point.connectsThrough = connection

    # link connection to the connection point and its device
    connection_point._data_graph.add(
        (
            connection_point.isConnectionPointOf.node,
            s223.connectedThrough,
            connection.node,
        )
    )
    connection._data_graph.add(
        (connection.node, s223.connectsAt, connection_point.node)
    )
    connection._data_graph.add(
        (connection.node, s223.connectsTo, connection_point.isConnectionPointOf.node)
    )


@multimethod
def connect_mm(device: Device, system_connection_point: SystemConnectionPoint) -> None:
    """Device >> SystemConnectionPoint"""
    logging.debug(f"connect from {device} to {system_connection_point}")

    to_connection_point = system_connection_point.mapsTo
    if not to_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {system_connection_point}"
        )

    connect_mm(device, to_connection_point)


@multimethod
def connect_mm(device: Device, connection_point: ConnectionPoint) -> None:
    """Device >> ConnectionPoint"""
    logging.info(f"connect from {device} to {connection_point}")

    if connection_point.connectsThrough:
        raise RuntimeError("connection point already connected")
    to_medium = getattr(connection_point, "hasMedium", None)
    logging.debug(f"    - to_medium: {to_medium}")

    # build a dict of outlet connection points that are not already connected
    # that have the same medium
    from_out = set()
    for attr, cp in device._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(cp, OutletConnectionPoint):
            continue

        medium = getattr(cp, "hasMedium", None)
        if medium == to_medium:
            from_out.add(cp)
    logging.debug(f"    - from_out: {from_out}")

    if not from_out:
        raise RuntimeError(f"no candidate sources from {device} to {connection_point}")
    if len(from_out) > 1:
        raise RuntimeError("too many connection points")
    from_thing = from_out.pop()
    logging.debug(f"    - from_thing: {from_thing}")

    # link the two things together
    from_thing._data_graph.add(
        (
            from_thing.isConnectionPointOf.node,
            s223.connectedTo,
            connection_point.isConnectionPointOf.node,
        )
    )
    from_thing._data_graph.add(
        (
            connection_point.isConnectionPointOf.node,
            s223.connectedFrom,
            from_thing.isConnectionPointOf.node,
        )
    )

    # set the relationships
    connect_mm(from_thing, connection_point)


@multimethod
def connect_mm(device: Device, connection: Connection) -> None:
    """Device >> Connection"""
    logging.info(f"connect from {device} to {connection}")
    connection_medium = getattr(connection, "hasMedium", None)
    logging.debug(f"    - to_medium: {connection_medium}")

    # build a dict of outlet connection points that are not already connected
    # that have the same medium
    from_out = set()
    for attr, connection_point in device._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        if medium == connection_medium:
            from_out.add(connection_point)

    if not from_out:
        raise RuntimeError(f"no candidate sources from {device} to {connection}")
    if len(from_out) > 1:
        raise RuntimeError("too many connection points")
    from_thing = from_out.pop()

    # set the relationships
    connect_mm(from_thing, connection)


@multimethod
def connect_mm(connection: Connection, device: Device) -> None:
    """Connection >> Device"""
    logging.info(f"connect from {connection} to {device}")
    connection_medium = getattr(connection, "hasMedium", None)
    logging.debug(f"    - to_medium: {connection_medium}")

    # build a dict of outlet connection points that are not already connected
    # that have the same medium
    to_in = set()
    for attr, connection_point in device._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        if medium == connection_medium:
            to_in.add(connection_point)
    logging.debug("    - to_in: %r", to_in)

    if not to_in:
        raise RuntimeError(f"no candidate destinations from {connection} to {device}")
    if len(to_in) > 1:
        raise RuntimeError("too many connection points")
    to_thing = to_in.pop()
    logging.debug("    - to_thing: %r", to_thing)

    # set the relationships
    connect_mm(connection, to_thing)


@multimethod
def connect_mm(connection: Connection, devices: List[Device]) -> None:
    """Connection >> [Device]"""
    logging.info(f"connect from {connection} to {devices}")
    connection_medium = getattr(connection, "hasMedium", None)
    logging.debug("    - connection_medium: %r", connection_medium)

    for device in devices:
        # build a dict of inlet connection points that are not already connected
        # that have the same medium
        to_in = set()
        for attr, connection_point in device._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if isinstance(connection_point, OutletConnectionPoint):
                continue

            medium = getattr(connection_point, "hasMedium", None)
            if medium == connection_medium:
                to_in.add(connection_point)
        logging.debug("    - to_in: %r", to_in)

        if not to_in:
            raise RuntimeError(
                f"no candidate destinations from {connection} to {device}"
            )
        if len(to_in) > 1:
            raise RuntimeError("too many connection points")
        to_thing = to_in.pop()
        logging.debug("    - to_thing: %r", to_thing)

        # set the relationships
        connect_mm(connection, to_thing)


@multimethod
def connect_mm(connection_point: ConnectionPoint, device: Device) -> None:
    """ConnectionPoint >> Device"""
    logging.info(f"connect from {connection_point} to {device}")
    connection_point_medium = getattr(connection_point, "hasMedium", None)
    logging.debug("    - connection_point_medium: %r", connection_point_medium)

    # build a dict of outlet connection points that are not already connected
    # that have the same medium
    to_in = set()
    for attr, cp in device._connection_points.items():
        if cp.connectsThrough:
            continue
        if isinstance(cp, OutletConnectionPoint):
            continue

        medium = getattr(cp, "hasMedium", None)
        if medium == connection_point_medium:
            to_in.add(cp)
    logging.debug("    - to_in: %r", to_in)

    if not to_in:
        raise RuntimeError(
            f"no candidate destinations from {connection_point} to {device}"
        )
    if len(to_in) > 1:
        raise RuntimeError("too many connection points")
    to_thing = to_in.pop()
    logging.debug("    - to_thing: %r", to_thing)

    # set the relationships
    connect_mm(connection_point, to_thing)


@multimethod
def connect_mm(connection: Connection, system: System) -> None:
    """Connection >> System"""
    logging.info(f"connect from {connection} to {system}")

    connection_medium = getattr(connection, "hasMedium", None)
    logging.debug(f"    - connection_medium: {connection_medium}")

    # build a dict of mapped inlet connection points that are not
    # already connected, organized by medium
    to_in = set()
    for attr, system_connection_point in system._system_connection_points.items():
        if isinstance(system_connection_point, OutletSystemConnectionPoint):
            continue
        connection_point = system_connection_point.mapsTo
        if not connection_point:
            continue
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        if medium and connection_medium and (medium != connection_medium):
            continue
        to_in.add(connection_point)

    if not to_in:
        raise RuntimeError(f"no candidate destinations from {connection} to {system}")
    if len(to_in) > 1:
        raise RuntimeError("too many connection points")
    to_thing = to_in.pop()
    logging.debug("    - to_thing: %r", to_thing)

    # set the relationships
    connect_mm(connection, to_thing)


@multimethod
def connect_mm(system: System, connection: Connection) -> None:
    """System >> Connection"""
    logging.info(f"connect from {system} to {connection}")

    connection_medium = getattr(connection, "hasMedium", None)
    logging.debug("    - connection_medium: %r", connection_medium)

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    from_out = set()
    for attr, system_connection_point in system._system_connection_points.items():
        if isinstance(system_connection_point, InletSystemConnectionPoint):
            continue
        connection_point = system_connection_point.mapsTo
        if not connection_point:
            continue
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, InletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        if medium and connection_medium and (medium != connection_medium):
            continue
        from_out.add(connection_point)

    if not from_out:
        raise RuntimeError(f"no candidate destinations from {system} to {connection}")
    if len(from_out) > 1:
        raise RuntimeError("too many connection points")
    from_thing = from_out.pop()
    logging.debug("    - from_thing: %r", from_thing)

    # set the relationships
    connect_mm(from_thing, connection)


@multimethod
def connect_mm(
    connection_point: ConnectionPoint, system_connection_point: SystemConnectionPoint
) -> None:
    """ConnectionPoint >> SystemConnectionPoint"""
    logging.info(f"connect from {connection_point} to {system_connection_point}")

    if isinstance(connection_point, InletConnectionPoint):
        raise TypeError("connection point direction")
    if connection_point.connectsThrough:
        raise RuntimeError("connection point already connected")

    to_connection_point = system_connection_point.mapsTo
    if not to_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {system_connection_point}"
        )
    if to_connection_point.connectsThrough:
        raise RuntimeError("system connection point already connected")

    # continue the process
    connect_mm(connection_point, to_connection_point)


@multimethod
def connect_mm(device: Device, system: System) -> None:
    """Device >> System"""
    logging.info(f"connect from {device} to {system}")

    # build a dict of outlet connection points that are not already connected
    # that have the same medium
    from_out = defaultdict(set)
    for attr, connection_point in device._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {device} to {system}")
    logging.debug(f"    - from_types: {from_types}")

    # build a dict of mapped inlet connection points that are not
    # already connected, organized by medium
    to_in = defaultdict(set)
    for attr, system_connection_point in system._system_connection_points.items():
        if not isinstance(system_connection_point, InletSystemConnectionPoint):
            continue
        connection_point = system_connection_point.mapsTo
        if not connection_point:
            continue
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, InletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {device} to {system}")
    logging.debug(f"    - to_types: {to_types}")

    # find the common medium
    common_types = from_types.intersection(to_types)
    if not common_types:
        raise RuntimeError("no common connection types")
    if len(common_types) > 1:
        raise RuntimeError("too many common connection types")
    medium = common_types.pop()
    logging.debug(f"    - medium: {medium}")

    # get the two connection points
    from_connection_point = from_out[medium].pop()
    to_connection_point = to_in[medium].pop()

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


@multimethod
def connect_mm(system: System, device: Device) -> None:
    """System >> Device"""
    logging.info(f"connect from {system} to {device}")

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    from_out = defaultdict(set)
    for attr, system_connection_point in system._system_connection_points.items():
        logging.debug(
            f"    - attr, system_connection_point: {attr} {system_connection_point}"
        )
        if not isinstance(system_connection_point, OutletSystemConnectionPoint):
            logging.debug("        - not a system outlet")
            continue
        connection_point = system_connection_point.mapsTo
        if not connection_point:
            logging.debug("        - not mapped")
            continue
        if connection_point.connectsThrough:
            logging.debug("        - already connected")
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            logging.debug("        - not an outlet")
            continue

        medium = getattr(connection_point, "hasMedium", None)
        from_out[medium].add(connection_point)
    logging.debug("    - from_out: %r", from_out)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {system} to {device}")
    logging.debug("    - from_types: %r", from_types)

    # build a dict of outlet connection points that are not already connected
    # that have the same medium
    to_in = defaultdict(set)
    for attr, connection_point in device._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, InletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {system} to {device}")
    logging.debug(f"    - from_types: {from_types}")

    # find the common medium
    common_types = from_types.intersection(to_types)
    if not common_types:
        raise RuntimeError("no common connection types")
    if len(common_types) > 1:
        raise RuntimeError("too many common connection types")
    medium = common_types.pop()
    logging.debug(f"    - medium: {medium}")

    # get the two connection points
    from_connection_point = from_out[medium].pop()
    to_connection_point = to_in[medium].pop()

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


class InletConnectionPoint(ConnectionPoint):
    hasDirection: Direction = Inlet


class OutletConnectionPoint(ConnectionPoint):
    hasDirection: Direction = Outlet


class BidirectionalConnectionPoint(ConnectionPoint):
    hasDirection: Direction = Bidirectional


class SystemConnectionPoint(Node):
    """
    System Connection Point
    """

    node_type: URIRef = s223.SystemConnectionPoint
    hasMedium: Medium
    hasDirection: Direction

    connectsThrough: Connection
    isSystemConnectionPointOf: System
    mapsTo: Node  # Union[Junction, ConnectionPoint]

    def __init__(self, system: System, **kwargs: Any) -> None:
        logging.debug(f"SystemConnectionPoint.__init__ {system} {kwargs}")
        # abstract base class
        if self.__class__ is ConnectionPoint:
            raise RuntimeError("SystemConnectionPoint is an abstract base class")

        super().__init__(**kwargs)

        self._data_graph.add((system.node, s223.hasSystemConnectionPoint, self.node))
        if INCLUDE_INVERSE:
            self.isSystemConnectionPointOf = system

        # this is one of the connection points of the system
        system._system_connection_points[str(self.node)] = self

    def maps_to(self, other: Union[Junction, ConnectionPoint]) -> None:
        """
        Maps this connection point to a space connection point.
        """
        logging.debug(f"SystemConnectionPoint.maps_to {other}")
        if self.mapsTo:
            raise RuntimeError("zone connection point already mapped")

        if not isinstance(other, (Junction, ConnectionPoint)):
            raise TypeError("ConnectionPoint expected")

        self.mapsTo = other


@multimethod
def connect_mm(from_system: System, to_system: System) -> None:
    """System >> System"""
    logging.info(f"connect from {from_system} to {to_system}")

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    from_out = defaultdict(set)
    for attr, system_connection_point in from_system._system_connection_points.items():
        if isinstance(system_connection_point, InletSystemConnectionPoint):
            continue
        connection_point = system_connection_point.mapsTo
        if not connection_point:
            continue
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, InletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        from_out[medium].add(connection_point)
    logging.debug(f"    - from_out: {from_out}")

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {from_system} to {to_system}")
    logging.debug(f"    - from_types: {from_types}")

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    to_in = defaultdict(set)
    for attr, system_connection_point in to_system._system_connection_points.items():
        if isinstance(system_connection_point, OutletSystemConnectionPoint):
            continue
        connection_point = system_connection_point.mapsTo
        if not connection_point:
            continue
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        to_in[medium].add(connection_point)
    logging.debug(f"    - to_in: {to_in}")

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(
            f"no candidate destinations from {from_system} to {to_system}"
        )
    logging.debug(f"    - to_types: {to_types}")

    # find the common medium
    common_types = from_types.intersection(to_types)
    if not common_types:
        raise RuntimeError("no common connection types")
    if len(common_types) > 1:
        raise RuntimeError("too many common connection types")
    medium = common_types.pop()
    logging.debug(f"    - medium: {medium}")

    # get the two connection points
    from_connection_point = from_out[medium].pop()
    to_connection_point = to_in[medium].pop()

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


@multimethod
def connect_mm(
    system_connection_point: SystemConnectionPoint, connection: Connection
) -> None:
    """SystemConnectionPoint >> Connection"""
    logging.info(f"connect from {system_connection_point} to {connection}")

    from_connection_point = system_connection_point.mapsTo
    if not from_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {system_connection_point}"
        )

    # continue the process
    connect_mm(from_connection_point, connection)


@multimethod
def connect_mm(
    connection: Connection, system_connection_point: SystemConnectionPoint
) -> None:
    """Connection >> SystemConnectionPoint"""
    logging.info(f"connect from {connection} to {system_connection_point}")

    to_connection_point = system_connection_point.mapsTo
    if not to_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {system_connection_point}"
        )

    # continue the process
    connect_mm(connection, to_connection_point)


@multimethod
def connect_mm(
    system_connection_point: SystemConnectionPoint, connection_point: ConnectionPoint
) -> None:
    """SystemConnectionPoint >> ConnectionPoint"""
    logging.info(f"connect from {system_connection_point} to {connection_point}")

    from_connection_point = system_connection_point.mapsTo
    if not from_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {system_connection_point}"
        )

    # continue the process
    connect_mm(from_connection_point, connection_point)


@multimethod
def connect_mm(
    from_system_connection_point: SystemConnectionPoint,
    to_system_connection_point: SystemConnectionPoint,
) -> None:
    """SystemConnectionPoint >> SystemConnectionPoint"""
    logging.info(
        f"connect from {from_system_connection_point} to {to_system_connection_point}"
    )

    from_connection_point = from_system_connection_point.mapsTo
    if not from_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {from_system_connection_point}"
        )

    to_connection_point = to_system_connection_point.mapsTo
    if not to_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {to_system_connection_point}"
        )

    connect_mm(from_connection_point, to_connection_point)


class InletSystemConnectionPoint(SystemConnectionPoint):
    hasDirection: Direction = Inlet


class OutletSystemConnectionPoint(SystemConnectionPoint):
    hasDirection: Direction = Outlet


class BidirectionalSystemConnectionPoint(SystemConnectionPoint):
    hasDirection: Direction = Bidirectional


class Zone(Container, Node):
    """
    A collection of spaces.
    """

    node_type: URIRef = s223.Zone
    _zone_connection_points: Dict[str, ZoneConnectionPoint]
    hasDomain: Domain

    def __init__(self, **kwargs: Any) -> None:
        logging.debug(f"Zone.__init__ {kwargs}")
        super().__init__(**kwargs)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        # merge the annotations
        merged_annotations = {}
        for cls in reversed(self.__class__.__mro__[:-1]):
            merged_annotations.update(cls.__annotations__)
        logging.debug(f"    - merged_annotations: {merged_annotations}")

        # instantiate and associate all of the connection points
        self._zone_connection_points = {}
        for var_name, var_annotation in merged_annotations.items():
            if var_name.startswith("_"):
                continue

            if isinstance(var_annotation, str):
                if var_annotation not in _annotation_reference:
                    logging.debug(
                        f"resolving {var_annotation!r} for attribute {var_name!r}, class not found"
                    )
                    continue
                var_annotation = _annotation_reference.get(var_annotation)

            if not issubclass(var_annotation, ZoneConnectionPoint):
                continue

            # build an instance of this connection point
            var_element = var_annotation(self, label=self.label + "." + var_name)
            self._zone_connection_points[var_name] = var_element
            logging.debug(f"    - connection point {var_name}: {var_element}")

            setattr(self, var_name, var_element)


@multimethod
def connect_mm(from_system: System, to_zone: Zone) -> None:
    """System >> Zone"""
    logging.info(f"connect from {from_system} to {to_zone}")

    # stash this in the system
    from_system._serves_zones[to_zone.label] = to_zone

    from_system._data_graph.add((from_system.node, s223.servesZone, to_zone.node))
    if INCLUDE_INVERSE:
        from_system._data_graph.add((to_zone.node, s223.isServedBy, from_system.node))

    return

    #
    #   skipped for now...
    #

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    from_out = defaultdict(set)
    for attr, system_connection_point in from_system._system_connection_points.items():
        if isinstance(system_connection_point, InletSystemConnectionPoint):
            continue
        connection_point = system_connection_point.mapsTo
        if not connection_point:
            continue
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, InletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        from_out[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    from_types: Set[Medium]
    from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
    if not from_types:
        raise RuntimeError(f"no candidate sources from {from_system} to {to_zone}")
    logging.debug(f"    - from_types: {from_types}")

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    to_in = defaultdict(set)
    for attr, system_connection_point in to_zone._zone_connection_points.items():
        if isinstance(system_connection_point, OutletSystemConnectionPoint):
            continue
        connection_point = system_connection_point.mapsTo
        if not connection_point:
            continue
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, OutletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {from_system} to {to_zone}")
    logging.debug(f"    - to_types: {to_types}")

    # find the common medium
    common_types = from_types.intersection(to_types)
    if not common_types:
        raise RuntimeError("no common connection types")
    if len(common_types) > 1:
        raise RuntimeError("too many common connection types")
    medium = common_types.pop()
    logging.debug(f"    - medium: {medium}")

    # get the two connection points
    from_connection_point = from_out[medium].pop()
    to_connection_point = to_in[medium].pop()

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)

    from_system._data_graph.add((from_system.node, s223.servesZone, to_zone.node))
    if INCLUDE_INVERSE:
        from_system._data_graph.add((to_zone.node, s223.isServedBy, from_system.node))


@multimethod
def connect_mm(zone: Zone, connection: Connection) -> None:
    """Zone >> Connection"""
    logging.info(f"connect from {zone} to {connection}")

    connection_medium = getattr(connection, "hasMedium", None)
    logging.info(f"    - connection_medium: {connection_medium}")

    # build a dict of mapped outlet connection points that are not
    # already connected, organized by medium
    from_out = set()
    for attr, zone_connection_point in zone._zone_connection_points.items():
        if isinstance(zone_connection_point, InletSystemConnectionPoint):
            continue
        connection_point = zone_connection_point.mapsTo
        if not connection_point:
            continue
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, InletConnectionPoint):
            continue

        medium = getattr(connection_point, "hasMedium", None)
        if medium and connection_medium and (medium != connection_medium):
            continue
        from_out.add(connection_point)

    if len(from_out) > 1:
        raise RuntimeError("too many source connection points")

    # get the two connection points
    connection_point = from_out.pop()

    # continue the connection
    connect_mm(connection_point, connection)


@multimethod
def contains_mm(zone: Zone, domain_space: DomainSpace) -> None:
    """Zone > DomainSpace"""
    logging.info(f"zone {zone} contains domain space {domain_space}")

    zone._data_graph.add((zone.node, s223.contains, domain_space.node))
    if INCLUDE_INVERSE:
        zone._data_graph.add((domain_space.node, s223.isContainedIn, zone.node))


class ZoneConnectionPoint(Node):
    """
    Zone Connection Point
    """

    node_type: URIRef = s223.ZoneConnectionPoint
    hasMedium: Medium
    hasDirection: Direction

    isZoneConnectionPointOf: Zone
    mapsTo: Node

    def __init__(self, zone: Zone, **kwargs: Any) -> None:
        logging.debug(f"ZoneConnectionPoint.__init__ {zone} {kwargs}")
        # abstract base class
        if self.__class__ is ZoneConnectionPoint:
            raise RuntimeError("ZoneConnectionPoint is an abstract base class")

        super().__init__(**kwargs)

        self._data_graph.add((zone.node, s223.hasZoneConnectionPoint, self.node))
        if INCLUDE_INVERSE:
            self.isZoneConnectionPointOf = zone

        # this is one of the connection points of the zone
        zone._zone_connection_points[str(self.node)] = self

    def maps_to(self, other: Union[Junction, ConnectionPoint]) -> None:
        """
        Maps this connection point to a domain space connection point.
        """
        logging.debug(f"ZoneConnectionPoint.maps_to {other}")
        if self.mapsTo:
            raise RuntimeError("zone connection point already mapped")

        if not isinstance(other, (Junction, ConnectionPoint)):
            raise TypeError("ConnectionPoint expected")

        self.mapsTo = other


@multimethod
def connect_mm(
    zone_connection_point: ZoneConnectionPoint, connection: Connection
) -> None:
    """ZoneConnectionPoint >> Connection"""
    raise NotImplementedError("ZoneConnectionPoint >> Connection")


@multimethod
def connect_mm(
    connection: Connection, zone_connection_point: ZoneConnectionPoint
) -> None:
    """Connection >> ZoneConnectionPoint"""
    raise NotImplementedError("Connection >> ZoneConnectionPoint")


@multimethod
def connect_mm(
    from_zone_connection_point: ZoneConnectionPoint,
    to_zone_connection_point: ZoneConnectionPoint,
) -> None:
    """ZoneConnectionPoint >> ZoneConnectionPoint"""
    logging.info(
        f"connect from {from_zone_connection_point} to {to_zone_connection_point}"
    )

    from_connection_point = from_zone_connection_point.mapsTo
    if not from_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {from_zone_connection_point}"
        )

    to_connection_point = to_zone_connection_point.mapsTo
    if not to_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {to_zone_connection_point}"
        )

    connect_mm(from_connection_point, to_connection_point)


@multimethod
def connect_mm(
    system_connection_point: SystemConnectionPoint,
    zone_connection_point: ZoneConnectionPoint,
) -> None:
    """SystemConnectionPoint >> ZoneConnectionPoint"""
    logging.info(f"connect from {system_connection_point} to {zone_connection_point}")

    from_connection_point = system_connection_point.mapsTo
    if not from_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {system_connection_point}"
        )

    to_connection_point = zone_connection_point.mapsTo
    if not to_connection_point:
        raise RuntimeError(f"unmapped zone connection point {zone_connection_point}")

    connect_mm(from_connection_point, to_connection_point)


@multimethod
def connect_mm(
    zone_connection_point: ZoneConnectionPoint,
    system_connection_point: SystemConnectionPoint,
) -> None:
    """ZoneConnectionPoint >> SystemConnectionPoint"""
    logging.info(f"connect from {system_connection_point} to {zone_connection_point}")

    from_connection_point = zone_connection_point.mapsTo
    if not from_connection_point:
        raise RuntimeError(f"unmapped zone connection point {zone_connection_point}")

    to_connection_point = system_connection_point.mapsTo
    if not to_connection_point:
        raise RuntimeError(
            f"unmapped system connection point {system_connection_point}"
        )

    connect_mm(from_connection_point, to_connection_point)


class InletZoneConnectionPoint(ZoneConnectionPoint):
    hasDirection: URIRef = s223["Direction-Inlet"]


class OutletZoneConnectionPoint(ZoneConnectionPoint):
    hasDirection: URIRef = s223["Direction-Outlet"]


class BidirectionalZoneConnectionPoint(ZoneConnectionPoint):
    hasDirection: URIRef = s223["Direction-Bidirectional"]


class PhysicalSpace(Container, Node):
    """
    A part of the physical world whose 3D spatial extent is bounded.
    """

    node_type: URIRef = s223.PhysicalSpace


@multimethod
def contains_mm(parent_space: PhysicalSpace, child_space: PhysicalSpace) -> None:
    """PhysicalSpace > PhysicalSpace"""
    logging.info(f"physical space {parent_space} contains physical space {child_space}")

    parent_space._data_graph.add((parent_space.node, s223.contains, child_space.node))
    if INCLUDE_INVERSE:
        parent_space._data_graph.add(
            (child_space.node, s223.isContainedIn, parent_space.node)
        )


@multimethod
def contains_mm(physical_space: PhysicalSpace, domain_space: DomainSpace) -> None:
    """PhysicalSpace > DomainSpace"""
    logging.info(f"physical space {physical_space} encloses {domain_space}")

    physical_space._data_graph.add(
        (physical_space.node, s223.encloses, domain_space.node)
    )
    if INCLUDE_INVERSE:
        physical_space._data_graph.add(
            (domain_space.node, s223.isEnclosedIn, physical_space.node)
        )


@multimethod
def contains_mm(physical_space: PhysicalSpace, thing_list: List[Node]) -> None:
    """PhysicalSpace >> List[Union[PhysicalSpace,DomainSpace]]"""
    logging.info(f"physical space {physical_space} contains/encloses list {thing_list}")

    ###TODO: the signature should be thing_list: List[Union[PhysicalSpace,DomainSpace]]

    for thing in thing_list:
        if not isinstance(thing, (PhysicalSpace, DomainSpace)):
            raise TypeError(f"device or system expected: {thing}")
        contains_mm(physical_space, thing)


def obsolete_connect(from_thing: Any, to_thing: Any, segmented: bool = False) -> None:
    """
    Find an unambiguous way to connect to things together.
    """
    logging.info(f"connect from {from_thing} to {to_thing}")

    from_out = defaultdict(set)
    if isinstance(from_thing, (Connection, ConnectionPoint)):
        medium = getattr(from_thing, "hasMedium", None)
        # medium = getattr(medium, "node", medium)
        from_out[medium].add(from_thing)

    elif isinstance(from_thing, Connectable):
        for attr, connection_point in from_thing._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, OutletConnectionPoint):
                continue

            medium = getattr(connection_point, "hasMedium", None)
            # medium = getattr(medium, "node", medium)
            # ISSUE...having a hard time with electrical things
            from_out[medium].add(connection_point)

    elif isinstance(from_thing, (SystemConnectionPoint, ZoneConnectionPoint)):
        if not from_thing.mapsTo:
            if isinstance(from_thing, SystemConnectionPoint):
                raise RuntimeError(f"unmapped system connection point {to_thing}")
            if isinstance(from_thing, ZoneConnectionPoint):
                raise RuntimeError(f"unmapped zone connection point {to_thing}")
        connection_point = from_thing.mapsTo

        if isinstance(connection_point, ConnectionPoint):
            if connection_point.connectsThrough:
                raise RuntimeError(
                    f"connection point already connected: {connection_point}"
                )
            if getattr(connection_point, "hasDirection", None) == Inlet:
                raise TypeError(f"connection point direction: {connection_point}")
        elif isinstance(connection_point, Junction):
            pass

        medium = getattr(connection_point, "hasMedium", None)
        from_out[medium].add(connection_point)

    elif isinstance(from_thing, System):
        for attr, connection_point in from_thing._system_connection_points.items():
            if not connection_point.mapsTo:
                continue
            connection_point = connection_point.mapsTo

            if isinstance(connection_point, ConnectionPoint):
                if connection_point.connectsThrough:
                    continue
                if getattr(connection_point, "hasDirection", None) == Inlet:
                    continue
            elif isinstance(connection_point, Junction):
                pass

            medium = getattr(connection_point, "hasMedium", None)
            from_out[medium].add(connection_point)

    elif isinstance(from_thing, Zone):
        for attr, connection_point in from_thing._zone_connection_points.items():
            if not connection_point.mapsTo:
                continue
            connection_point = connection_point.mapsTo

            if isinstance(connection_point, ConnectionPoint):
                if connection_point.connectsThrough:
                    continue
                if getattr(connection_point, "hasDirection", None) == Inlet:
                    continue
            elif isinstance(connection_point, Junction):
                pass

            medium = getattr(connection_point, "hasMedium", None)
            from_out[medium].add(connection_point)

    else:
        raise NotImplementedError(f"connecting from {from_thing}")
    logging.debug(f"    - from_out: {from_out}")

    from_types: Set[Medium]
    if isinstance(from_thing, Connection):
        from_types = set([from_thing.hasMedium])
    else:
        from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
        if not from_types:
            raise RuntimeError(f"no candidate sources from {from_thing} to {to_thing}")
    logging.debug(f"    - from_types: {from_types}")

    to_in = defaultdict(set)
    if isinstance(to_thing, (Connection, ConnectionPoint)):
        medium = getattr(to_thing, "hasMedium", None)
        # medium = getattr(medium, "node", medium)
        # ISSUE...having a hard time with electrical things
        # maybe this was due to me, breaking Joel's toy
        to_in[medium].add(to_thing)

    elif isinstance(to_thing, Connectable):
        for attr, connection_point in to_thing._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, InletConnectionPoint):
                continue

            medium = getattr(connection_point, "hasMedium", None)
            # Here when trying to connect a connectionpoint to a device
            # medium turned to be
            # {'node': rdflib.term.URIRef('http://data.ashrae.org/standard223/1.0/vocab/enumeration#Water-ChilledWater'), 'label': '', 'comment': ''}
            # and the intersection fails to recognize the substance
            # medium = getattr(medium, "node", medium)
            to_in[medium].add(connection_point)

    elif isinstance(to_thing, (SystemConnectionPoint, ZoneConnectionPoint)):
        if not to_thing.mapsTo:
            if isinstance(to_thing, SystemConnectionPoint):
                raise RuntimeError(f"unmapped system connection point {to_thing}")
            if isinstance(to_thing, ZoneConnectionPoint):
                raise RuntimeError(f"unmapped zone connection point {to_thing}")
        connection_point = to_thing.mapsTo

        if isinstance(connection_point, ConnectionPoint):
            if connection_point.connectsThrough:
                raise RuntimeError(
                    f"connection point already connected: {connection_point}"
                )
            if getattr(connection_point, "hasDirection", None) == Outlet:
                raise TypeError(f"connection point direction: {connection_point}")
        elif isinstance(connection_point, Junction):
            pass

        medium = getattr(connection_point, "hasMedium", None)
        to_in[medium].add(connection_point)

    elif isinstance(to_thing, System):
        for attr, connection_point in to_thing._system_connection_points.items():
            if not connection_point.mapsTo:
                continue
            connection_point = connection_point.mapsTo

            if isinstance(connection_point, ConnectionPoint):
                if connection_point.connectsThrough:
                    continue
                if getattr(connection_point, "hasDirection", None) == Outlet:
                    continue
            elif isinstance(connection_point, Junction):
                pass

            medium = getattr(connection_point, "hasMedium", None)
            to_in[medium].add(connection_point)

    elif isinstance(to_thing, Zone):
        for attr, connection_point in to_thing._zone_connection_points.items():
            if not connection_point.mapsTo:
                continue
            connection_point = connection_point.mapsTo

            if isinstance(connection_point, ConnectionPoint):
                if connection_point.connectsThrough:
                    continue
                if getattr(connection_point, "hasDirection", None) == Outlet:
                    continue
            elif isinstance(connection_point, Junction):
                pass

            medium = getattr(connection_point, "hasMedium", None)
            to_in[medium].add(connection_point)

    else:
        raise NotImplementedError(f"connecting to {to_thing}")
    logging.debug(f"    - to_in: {to_in}")

    to_types: Set[Medium]
    if isinstance(to_thing, Connection):
        to_types = set([to_thing.hasMedium])
    else:
        to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
        if not to_types:
            raise RuntimeError(
                f"no candidate destinations from {from_thing} to {to_thing}"
            )
    logging.debug(f"    - to_types: {to_types}")

    # find the common medium
    common_types = from_types.intersection(to_types)
    if not common_types:
        raise RuntimeError("no common connection types")
    if len(common_types) > 1:
        raise RuntimeError("too many common connection types")
    medium = common_types.pop()
    logging.debug(f"    - medium: {medium}")

    if isinstance(from_thing, Connection):
        if isinstance(to_thing, Connection):
            raise RuntimeError("connection to connection")
        to_connection_point = to_in[medium].pop()

        # from_thing.connect_to(to_connection_point)
        connect_mm(from_thing, to_connection_point)

    elif isinstance(to_thing, Connection):
        from_connection_point = from_out[medium].pop()

        # to_thing.connect_from(from_connection_point)
        connect_mm(from_connection_point, to_thing)

    else:
        # get the medium and the two connection points
        from_connection_point = from_out[medium].pop()
        to_connection_point = to_in[medium].pop()

        # if either connection point is a junction, this is segmented
        if (
            segmented
            or isinstance(from_connection_point, Junction)
            or isinstance(to_connection_point, Junction)
        ):
            segment = Segment()
            segment.link_to(from_connection_point)
            segment.link_to(to_connection_point)
        else:
            # from_connection_point.connect_to(to_connection_point)
            connect_mm(from_connection_point, to_connection_point)


class Device(Container, Connectable):
    """
    A Device is normally a physical entity that one might buy from a vendor - a tangible object designed to accomplish a specific task.
    """

    node_type: URIRef = s223.Device
    # hasContextualRoleShape: Any
    # hasPropertyShape: Any
    hasRole: Role
    hasPhysicalLocation: PhysicalSpace

    def __init__(self, config: Dict[str, Any] = {}, *args, **kwargs: Any) -> None:
        logging.debug(f"Device.__init__ {config} {args} {kwargs}")

        # if there are "params" in the configuation, use those as defaults for
        # kwargs and allow them to be overriden be additional kwargs
        # if config and "params" in config:
        #     kwargs = {**config["params"], **kwargs}

        super().__init__(*args, **kwargs)

        if config:
            for group_name, group_items in config.items():
                if group_name == "params":
                    continue

                things = []
                for (thing_name, thing_class), thing_kwargs in group_items.items():
                    if thing_name in self._contents:
                        raise ValueError(
                            f"label already used: {self._contents[thing_name]}"
                        )
                    thing = thing_class(label=thing_name, **thing_kwargs)

                    if isinstance(thing, (Device, System)):
                        self > thing
                    if isinstance(thing, Property):
                        thing @ self
                        self._contents[thing_name] = thing

                    things.append(thing)

                setattr(self, "_" + group_name, things)


@multimethod
def contains_mm(system: System, device: Device) -> None:
    """System > Device"""
    logging.info(f"system {system} contains device {device}")

    system._data_graph.add((system.node, s223.contains, device.node))
    if INCLUDE_INVERSE:
        system._data_graph.add((device.node, s223.isContainedIn, system.node))


@multimethod
def contains_mm(parent_device: Device, child_device: Device) -> None:
    """Device > Device"""
    logging.info(f"device {parent_device} contains device {child_device}")

    parent_device._data_graph.add(
        (parent_device.node, s223.contains, child_device.node)
    )
    if INCLUDE_INVERSE:
        parent_device._data_graph.add(
            (child_device.node, s223.isContainedIn, parent_device.node)
        )


class DomainSpace(Connectable):
    """
    A part of the physical world or a virtual world whose 3D spatial extent is
    bounded actually or theoretically, and provides for certain functions
    within the zone it is contained in.
    """

    node_type: URIRef = s223.DomainSpace
    hasDomain: Domain
    hasMedium: Medium  ### required?  maybe implied by Domain?


@multimethod
def contains_mm(zone: Zone, domain_space: DomainSpace) -> None:
    """Zone > DomainSpace"""
    logging.info(f"zone {zone} contains domain space {domain_space}")

    zone._data_graph.add((zone.node, s223.contains, domain_space.node))
    if INCLUDE_INVERSE:
        zone._data_graph.add((domain_space.node, s223.isContainedIn, zone.node))


@multimethod
def contains_mm(zone: Zone, domain_spaces: List[DomainSpace]) -> None:
    """Zone > List[DomainSpace]"""
    logging.info(f"zone {zone} contains domain spaces {domain_spaces}")

    for domain_space in domain_spaces:
        contains_mm(zone, domain_space)


@multimethod
def connect_mm(domain_space: DomainSpace, connection_point: ConnectionPoint) -> None:
    """DomainSpace >> ConnectionPoint"""
    logging.info(f"connect from {domain_space} to {connection_point}")

    if connection_point.connectsThrough:
        raise RuntimeError("connection point already connected")
    to_medium = getattr(connection_point, "hasMedium", None)
    logging.debug(f"    - to_medium: {to_medium}")

    # build a dict of outlet connection points that are not already connected
    # that have the same medium
    from_out = set()
    for attr, cp in domain_space._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if isinstance(cp, InletConnectionPoint):
            continue

        medium = getattr(cp, "hasMedium", None)
        if medium == to_medium:
            from_out.add(cp)
    logging.debug(f"    - from_out: {from_out}")

    if not from_out:
        raise RuntimeError(
            f"no candidate sources from {domain_space} to {connection_point}"
        )
    if len(from_out) > 1:
        raise RuntimeError("too many connection points")
    from_thing = from_out.pop()
    logging.debug(f"    - from_thing: {from_thing}")

    connect_mm(from_thing, connection_point)
