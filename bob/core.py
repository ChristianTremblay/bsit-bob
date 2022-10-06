"""
Bob the SI-WG Builder
"""

from __future__ import annotations

import copy
import inspect
import io
import itertools
import logging
import os
import re
import sys
from collections import Counter, defaultdict
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    TextIO,
    Tuple,
    TypeVar,
    Union,
    cast,
    get_origin,
)

from rdflib import RDF, RDFS, XSD, BNode, Graph, Literal, Namespace, URIRef

from .multimethods import all_subclasses, multimethod, new_class

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
log_filename = os.getenv("BOB_LOGFILENAME", None)
numeric_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: %s" % log_level)
logging.basicConfig(filename=log_filename, level=numeric_level)

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

# include inverse relations
INCLUDE_INVERSE = os.getenv("INCLUDE_INVERSE", "False") == "True"

# connection requires hasMedium
CONNECTION_HAS_MEDIUM = os.getenv("CONNECTION_HAS_MEDIUM", "True") == "True"

# globals
data_graph = None
schema_graph = None


class DataGraph(Graph):
    def add(self, triple: Tuple[Any, Any, Any]) -> None:
        """
        Add a triple to the data graph, checking the predicate to see if it should
        be included or excluded.
        """
        # logging.debug(f"DataGraph.add {triple}")
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
        in the S223 namespace.
        """
        # logging.debug(f"SchemaGraph.add {triple}")
        subj, pred, obj = triple

        # exclude the schema content in the S223 namespace by default
        if subj.startswith(S223):
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
S223 = bind_namespace("s223", "http://data.ashrae.org/standard223#")

# This namespace is added so in the development of Bob, when new cases occurs
# we can clearly establish that a new class is not yet part of the standard
P223 = bind_namespace("p223", "http://data.ashrae.org/proposal-to-standard223#")

# This namespace is added so si-builder (aka Bob), can provide its own schema
# of classes which are assemblage of S223 classes
BOB = bind_namespace("bob", "http://data.ashrae.org/standard223/si-builder#")

# This namespace is used when the module does not have a namespace provided
# which makes short examples easier to create
EX = bind_namespace("ex", os.getenv("BOB_EX", "http://example/"))

# This namespace is used for all related logics in Guideline 36
G36 = bind_namespace("g36", "http://data.ashrae.org/standard223/1.0/extension/g36#")

# everything in this module belongs in the standard
_namespace = S223

# common namespaces
QUDT = bind_namespace("qudt", "http://qudt.org/schema/qudt/")
QUANTITYKIND = bind_namespace("quantitykind", "http://qudt.org/vocab/quantitykind/")
QUANTITYVALUE = bind_namespace(
    "quantityValue", "http://QUDT.org/schema/qudt/quantityValue"
)
UNIT = bind_namespace("unit", "http://qudt.org/vocab/unit/")
enum = bind_namespace(
    "enum", "http://data.ashrae.org/standard223/1.0/vocab/enumeration#"
)
BRICK = bind_namespace("brick", "https://brickschema.org/schema/Brick#")

REF = bind_namespace("ref", "https://brickschema.org/schema/Brick/ref#")

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
    all triples are sorted.
    """
    logging.debug("clean_and_sort_turtle_file ...")

    header_chunks = []  # lines that start like '# baseURI: ...'
    prefix_chunks = []  # lines that start like '@prefix ...'

    # pattern for triple quoted literals
    tql = re.compile("\"\"\"[^\"]*\"\"\"|'''[^']*'''")

    tql_archive = []

    def tql_save(match) -> str:
        logging.debug("    - match: %r", match)
        mstart, mend = match.span()
        tql_archive.append(match.string[mstart:mend])
        return "\0"

    def tql_restore(match) -> str:
        return tql_archive.pop(0)

    # save the triple quoted strings
    content = tql.sub(tql_save, content)

    chunk = ""  # lines that belong together
    chunks = []  # groups of lines sorted later
    for line in io.StringIO(content).readlines():
        logging.debug("    - %r", line)

        # filter out comments and prefixes
        if line.startswith("# "):
            logging.debug("    - header")
            header_chunks.append(line)
            if chunk:
                chunks.append(chunk)
                chunk = ""
            continue
        if line.startswith("@prefix"):
            logging.debug("    - prefix")
            prefix_chunks.append(line)
            if chunk:
                chunks.append(chunk)
                chunk = ""
            continue

        chunk += line
        if line == "\n":
            logging.debug("    - end of chunk")
            chunks.append(chunk)
            chunk = ""

    # trailing chunk
    if chunk:
        logging.debug("    - trailing chunk")
        chunks.append(chunk)
        chunk = ""

    new_content = ""

    # dump the header chunks
    if header_chunks:
        new_content += "".join(header_chunks) + "\n"

    # sort prefix chunks and remove the duplicates
    if prefix_chunks:
        prefix_chunks.sort()
        prefix_chunks = list(dict.fromkeys(prefix_chunks))
        new_content += "".join(prefix_chunks) + "\n"

    # restore the triple quoted strings
    chunks = [re.sub("\0", tql_restore, chunk) for chunk in chunks]

    # sort them
    chunks.sort()
    new_content += "".join(chunks)

    return new_content


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
        _attr_uriref: Dict[str, URIRef] = {}

        # add these special attributes to the class before building it
        attributedict["_resolved"] = False
        attributedict["_nodes"] = _nodes
        attributedict["_datatypes"] = attributedict.get("_datatypes", _datatypes)
        attributedict["_attr_uriref"] = attributedict.get("_attr_uriref", _attr_uriref)

        # build the class
        metaclass = cast(
            NodeMetaclass,
            super(NodeMetaclass, cls).__new__(
                cls, clsname, superclasses, attributedict
            ),
        )

        # let the multimethods know this is a new class, the typemap might have
        # to be reconstructed
        new_class(metaclass)

        return metaclass


class Node(metaclass=NodeMetaclass):
    """
    A node in the graph that optionally has a label and a comment.  Instances
    of this would be something like blank nodes.
    """

    _namespace: Namespace
    _data_graph: Graph = data_graph
    _schema_graph: Graph = schema_graph

    # resolved annotations into nodes and datatypes
    _resolved: bool
    _nodes: NodeMap
    _datatypes: Dict[str, Literal] = {"label": Literal, "comment": Literal}
    _attr_uriref: Dict[str, URIRef] = {"label": RDFS.label, "comment": RDFS.comment}

    # attributes that can be changed
    _volatile: Tuple[str, ...] = ()

    _node_iri: URIRef
    _class_iri: Optional[URIRef] = None

    def __init__(
        self,
        *,
        _node_iri: URIRef = None,
        **kwargs: Any,
    ) -> None:
        logging.debug(f"Node.__init__ {kwargs}")
        global _next_node, model_namespace

        if not self._resolved:
            self._resolve_annotations()
        logging.debug(f"    - continue Node.__init__")

        if _node_iri is not None:
            if not isinstance(_node_iri, URIRef):
                raise TypeError(f"URIRef expected: {_node_iri}")
            super().__setattr__("_node_iri", _node_iri)
        elif model_namespace:
            _next_node[model_namespace] += 1
            super().__setattr__(
                "_node_iri", model_namespace[f"{_next_node[model_namespace]:05d}"]
            )
        else:
            super().__setattr__("_node_iri", BNode())

        if hasattr(self, "_class_iri"):
            if self._class_iri is not None:
                self._data_graph.add((self._node_iri, RDF.type, self._class_iri))
                logging.debug(f"    - has _class_iri: {self._class_iri}")

        # pull out the kwargs that are nodes and datatypes
        inits = {}
        for k, v in kwargs.items():
            if k in self._nodes or k in self._datatypes:
                inits[k] = v
        logging.debug(f"    - inits: {inits!r}")

        # pull out the init values in classes that aren't already found
        for supercls in self.__class__.__mro__:
            if issubclass(supercls, Node):
                _class_iri = vars(supercls).get("_class_iri")
                if _class_iri is not None:
                    self._data_graph.add((self._node_iri, RDF.type, _class_iri))
                    logging.debug(f"    - supercls {supercls} _class_iri: {_class_iri}")

            for k, v in supercls.__dict__.items():
                if k.startswith("_") or (k in inits):
                    continue
                if (k in self._datatypes) or (k in self._nodes):
                    inits[k] = v
                if inspect.isclass(v) and issubclass(v, Node):
                    logging.debug(f"    - ding {k!r} = {v!r}")

        # set the values
        for attr, attr_value in inits.items():
            logging.debug(f"    - init {attr}: {attr_value!r}")
            if attr_value is None:
                super().__setattr__(attr, None)
            else:
                setattr(self, attr, attr_value)

        # clear the nodes with no values
        for attr in self._nodes:
            if attr not in inits:
                super().__setattr__(attr, None)

        # unknown args
        unknown_kwargs = [attr for attr in kwargs if attr not in inits]
        if unknown_kwargs:
            raise RuntimeError(
                f"unexpected keyword arguments: {', '.join(unknown_kwargs)}"
            )

    @classmethod
    def _resolve_annotations(cls) -> None:
        """
        .
        """
        logging.debug(f"Node._resolve_annotations {cls}")
        if cls is Node:
            logging.debug(f"    - nothing to resolve here")
            cls._resolved = True
            return

        # include the maps this class is inheriting
        for supercls in reversed(cls.__mro__[1:]):
            logging.debug(f"    - supercls: {supercls}")
            if supercls is cls:
                break

            if not hasattr(supercls, "_resolved"):
                continue
            if not supercls._resolved:
                supercls._resolve_annotations()

            if hasattr(supercls, "_nodes"):
                cls._nodes.update(supercls._nodes)  # type: ignore[attr-defined]
            if hasattr(supercls, "_datatypes"):
                cls._datatypes.update(supercls._datatypes)  # type: ignore[attr-defined]
            if hasattr(supercls, "_attr_uriref"):
                cls._attr_uriref.update(supercls._attr_uriref)  # type: ignore[attr-defined]
        logging.debug("    - from super classes:")
        logging.debug(f"    -     _nodes: {cls._nodes!r}")
        logging.debug(f"    -     _datatypes: {cls._datatypes!r}")
        logging.debug(f"    -     _attr_uriref: {cls._attr_uriref!r}")

        # find the namespace in the class definition
        _namespace = vars(cls).get("_namespace")
        if _namespace:
            logging.debug(f"    - class namespace: {_namespace}")
        else:
            # check the module
            cls_module = inspect.getmodule(cls)
            logging.debug(f"    - cls_module: {cls_module} {cls_module.__name__}")

            _namespace = vars(cls_module).get("_namespace")
            if _namespace:
                logging.debug(f"    - module {cls_module} namespace: {_namespace}")
            else:
                # check the parent module
                parent_module = sys.modules[
                    ".".join(cls_module.__name__.split(".")[:-1]) or "__main__"
                ]
                logging.debug(f"    - parent_module: {parent_module}")
                _namespace = vars(parent_module).get("_namespace")
                if _namespace:
                    logging.debug(
                        f"    - parent module {parent_module} namespace: {_namespace}"
                    )
                else:
                    # check the superclasses that are in the same module
                    for supercls in cls.__mro__:
                        supercls_module = inspect.getmodule(supercls)
                        logging.debug(
                            f"    - supercls {supercls} module: {supercls_module}"
                        )
                        if supercls_module is not cls_module:
                            continue

                        _namespace = vars(supercls).get("_namespace")
                        if _namespace:
                            logging.debug(
                                f"    - supercls {supercls} namespace: {_namespace}"
                            )
                            break

        # use the "example" namespace if nothing else available
        if _namespace is None:
            _namespace = EX

        # save a reference to the namespace in the class
        cls._namespace = _namespace  # type: ignore[attr-defined]

        attr_annotations = vars(cls).get("__annotations__", {})
        for attr, attr_annotation in attr_annotations.items():
            if attr.startswith("_") or attr == "node_type":
                continue
            logging.debug(f"    - attr: {attr!r}")
            logging.debug(f"        - attr_annotation: {attr_annotation!r}")

            if isinstance(attr_annotation, str) and not isinstance(
                attr_annotation, URIRef
            ):
                # eval the string in the context of the globals in its module
                try:
                    cls_module = inspect.getmodule(cls)
                    logging.debug(f"        - {cls_module=}")
                    attr_type = eval(attr_annotation, vars(cls_module))
                except NameError:
                    raise RuntimeError(
                        f"class {cls}, attribute {attr}: unable to resolve {attr_annotation}"
                    )
            else:
                attr_type = attr_annotation
            logging.debug(f"        - attr_type: {attr_type!r}")

            attr_origin = get_origin(attr_type)
            logging.debug(f"        - attr_origin: {attr_origin!r}")

            attr_uriref = cls._attr_uriref.get(attr, _namespace[attr])
            logging.debug(f"        - attr_uriref: {attr_uriref!r}")

            if isinstance(attr_type, URIRef):
                if not attr_type.startswith(XSD):
                    raise ValueError(f"datatype URI expected for {attr}: {attr_type}")

                cls._datatypes[attr] = attr_type
                cls._attr_uriref[attr] = attr_uriref
                cls._schema_graph.add((attr_uriref, RDF.type, RDF.Property))

            elif attr_origin in (Any, Dict, Set, Union):
                logging.debug(f"    - inspection not supported")

            elif inspect.isclass(attr_type):
                cls._nodes[attr] = attr_type
                cls._attr_uriref[attr] = attr_uriref
                cls._schema_graph.add((attr_uriref, RDF.type, RDF.Property))

                if issubclass(
                    attr_type, (Property, PropertyReference, LocationReference)
                ):
                    cls._schema_graph.add(
                        (attr_uriref, RDFS.subPropertyOf, S223.hasProperty)
                    )
                elif issubclass(attr_type, ConnectionPoint):
                    cls._schema_graph.add(
                        (
                            attr_uriref,
                            RDFS.subPropertyOf,
                            S223.hasConnectionPoint,
                        )
                    )
                elif issubclass(attr_type, SystemConnectionPoint):
                    cls._schema_graph.add(
                        (
                            attr_uriref,
                            RDFS.subPropertyOf,
                            S223.hasSystemConnectionPoint,
                        )
                    )
                elif issubclass(attr_type, ZoneConnectionPoint):
                    cls._schema_graph.add(
                        (
                            attr_uriref,
                            RDFS.subPropertyOf,
                            S223.hasZoneConnectionPoint,
                        )
                    )

            elif isinstance(attr_type, EnumerationKind):
                cls._nodes[attr] = attr_type
                cls._attr_uriref[attr] = attr_uriref
                cls._schema_graph.add((attr_uriref, RDF.type, RDF.Property))

            else:
                raise ValueError(f"unknown annotation for {attr}: {attr_type}")

        for attr, attr_value in vars(cls).items():
            if attr.startswith("_"):
                continue
            if attr in attr_annotations:
                continue
            if inspect.isclass(attr_value) and issubclass(attr_value, Node):
                logging.debug(
                    f"    - future init {attr!r} to instance of {attr_value!r}"
                )
                attr_uriref = cls._attr_uriref.get(attr, _namespace[attr])

                cls._nodes[attr] = attr_value
                cls._attr_uriref[attr] = attr_uriref

        # give the class an IRI if it doesn't have one
        if "_class_iri" not in vars(cls):
            cls._class_iri = _namespace[cls.__name__]  # type: ignore[attr-defined]
            logging.debug(f"    - class given IRI: {cls._class_iri!r}")

        # this is a class, and a subclass of the super classes
        if cls._class_iri is not None:
            cls._schema_graph.add((cls._class_iri, RDF.type, RDFS.Class))

            # some documentation is nice
            if cls.__doc__:
                cls._schema_graph.add(
                    (cls._class_iri, RDFS.comment, Literal(cls.__doc__))
                )
            cls._schema_graph.add(
                (
                    cls._class_iri,
                    RDFS.label,
                    Literal(cls.__module__ + "." + cls.__name__),
                )
            )

            for supercls in cls.__mro__[1:]:
                if issubclass(supercls, Node):
                    _class_iri = vars(supercls).get("_class_iri")
                    if _class_iri is not None:
                        cls._schema_graph.add(
                            (cls._class_iri, RDFS.subClassOf, supercls._class_iri)
                        )

        cls._resolved = True
        logging.debug(f"    - resolved {cls}")

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
        logging.debug("__setattr__ %r %r", attr, value)

        # make sure the value isn't None, no "deleting" content
        if value is None:
            raise ValueError(f"{attr} is None")

        # make sure the current value is None, no "reassigning" content
        current_value = vars(self).get(attr)
        if current_value is not None:
            if attr not in getattr(self, "_volatile", {}):
                raise RuntimeError(
                    f"attribute {attr} already has a value: {current_value}"
                )

        # if this is a node, double check the type
        if attr in self._nodes:
            attr_type = self._nodes[attr]
            logging.debug("    - attr_type: %r", attr_type)

            # if the type reference is still a string, find the real type
            if isinstance(attr_type, str):
                raise RuntimeError(f"{attr_type!r} still a string for {attr!r}")

            # attr_type allows any instance of an enumeration kind
            if attr_type is EnumerationKind:
                if not isinstance(value, EnumerationKind):
                    raise TypeError(
                        f"value {value} for attribute {attr} not a {attr_type}"
                    )

            # attr_type requires a some sub-kind
            elif isinstance(attr_type, EnumerationKind):
                if (not isinstance(value, EnumerationKind)) or (
                    value not in attr_type._children
                ):
                    raise TypeError(
                        f"value {value} for attribute {attr} not a {attr_type}"
                    )

            # special case assigning type means creating an instance
            elif value is attr_type:
                logging.debug(f"    - construct new {attr_type}")
                value = attr_type()

            # pass the value to the class to build one
            elif not isinstance(value, attr_type):
                try:
                    logging.debug(f"    - construct {attr_type} from: {value!r}")
                    value = attr_type(value)
                except TypeError:
                    logging.debug(f"    - why is this trapped?")
                    value = attr_type(_node_iri=value)
                logging.debug("    - new value: %r", value)

            # add the link(s)
            ### can two different attributes have the same URIRef for calling
            ### rather than set()?
            if isinstance(value, (URIRef, Literal)):
                ### this is weird, why is hasValue special?
                if attr == "hasValue":
                    self._data_graph.set((self._node_iri, self._attr_uriref[attr], value))  # type: ignore[attr-defined]
                else:
                    self._data_graph.add((self._node_iri, self._attr_uriref[attr], value))  # type: ignore[attr-defined]
            if isinstance(value, Node):
                logging.debug(
                    "    - add (self, %r, %r)", self._attr_uriref[attr], value._node_iri
                )
                self._data_graph.add((self._node_iri, self._attr_uriref[attr], value._node_iri))  # type: ignore[attr-defined]

            # if the value is a property, link it to the node
            if isinstance(value, Property) and issubclass(attr_type, Property):
                self.add_property(value)

            # if the value is an external reference, link it to the node
            if isinstance(value, ExternalReference):
                self.add_external_reference(value)

        # if this needs some datatype decoration, turn it into a literal
        if attr in self._datatypes:
            attr_datatype = self._datatypes[attr]
            if attr_datatype is Literal:
                if not isinstance(value, Literal):
                    value = Literal(value)
            elif isinstance(value, Literal):
                if value.datatype != attr_datatype:
                    raise TypeError(f"{attr}: literal {attr_datatype} expected")
            elif isinstance(value, (str, int, float)):
                value = Literal(value, datatype=attr_datatype)
            else:
                value = Literal(value)
                if value.datatype != attr_datatype:
                    raise TypeError(f"{attr}: literal {attr_datatype} expected")

            # add the literal
            self._data_graph.add((self._node_iri, self._attr_uriref[attr], value))  # type: ignore[attr-defined]

        # carry on
        logging.debug("    - carry on")
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
        return f"<{self.__class__.__name__}{label} at {self._node_iri}>"

    def add_property(self, prop: Property) -> Property:
        """Add a property to a node, returns the added property."""
        assert isinstance(prop, Property)

        # link the two together
        self._data_graph.add((self._node_iri, S223.hasProperty, prop._node_iri))
        if INCLUDE_INVERSE:
            self._data_graph.add((prop._node_iri, S223.isPropertyOf, self._node_iri))

        return prop


class ExternalReferenceValue:
    def __new__(cls, value):
        logging.debug(f"ExternalReferenceValue.__new__ {cls!r} {value!r}")
        if isinstance(value, Literal):
            pass
        elif isinstance(value, URIRef):
            pass
        elif isinstance(value, Node):
            value = value._node_iri
        else:
            value = Literal(value)

        return value


class ExternalReference(Node):
    """
    This will be subclassed by different specific datasources, this simplest
    form uses hasRef as a literal, most likely a string.  Note that this is
    currently from the Brick "ref" schema.
    """

    _class_iri: URIRef = REF.ExternalReference
    hasRef: ExternalReferenceValue

    def __init__(
        self,
        arg: Any = None,  # Union[str, Literal, URIRef, Node]
        **kwargs: Any,
    ):
        logging.debug(f"ExternalReference.__init__ {arg!r} {kwargs}")
        if arg is not None:
            if "hasRef" in kwargs:
                raise RuntimeError("initialization conflict")
            kwargs["hasRef"] = arg

        super().__init__(**kwargs)


class Property(Node):
    """
    An attribute, quality, or characteristic of a feature of interest.  This is
    an abstract base class.
    """

    _attr_uriref = {"hasExternalReference": REF.hasExternalReference}

    ofMedium: Medium
    ofSubstance: Substance
    hasValue: Literal
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
            )
            if hasattr(self, "label"):
                external_reference.label = self.label + ".ExternalReference"

        # link the two together
        self._data_graph.add(
            (self._node_iri, REF.hasExternalReference, external_reference._node_iri)
        )
        if INCLUDE_INVERSE:
            external_reference.isExternalReferenceOf = self

    def __matmul__(self, external_reference: ExternalReference) -> Node:
        """
        This property is at some external reference.
        """
        self.add_external_reference(external_reference)
        return self


class PropertyReference:
    def __new__(cls, property):
        if not isinstance(property, Property):
            raise TypeError(f"property expected: {property}")
        return property


class LocationReference:
    def __new__(cls, location):
        if not isinstance(
            location, (Connectable, Connection, Segment, ConnectionPoint, PhysicalSpace)
        ):
            raise TypeError(f"location expected: {location}")
        return location


class Container(Node):
    """
    This class implements the Container Abstract Base Class.
    """

    _class_iri: URIRef = None
    _contents: Dict[str, Node]

    def __init__(self, *args, **kwargs) -> None:
        logging.debug(f"Container.__init__ {args} {kwargs}")
        if self.__class__ is Container:
            raise RuntimeError("Container is an abstract base class")

        super().__init__(*args, **kwargs)
        self._contents = {}

    def __getitem__(self, label: Union[str, Literal]) -> Node:
        logging.debug(f"Container.__getitem__ {label!r}")
        if isinstance(label, str):
            label = Literal(label)
        elif not isinstance(label, Literal):
            raise TypeError(f"Literal or string expected: {label!r}")
        return self._contents[label]

    def __setitem__(self, label: Union[str, Literal], value: Node) -> None:
        logging.debug(f"Container.__getitem__ {label!r} {value!r}")
        if isinstance(label, str):
            label = Literal(label)
        elif not isinstance(label, Literal):
            raise TypeError(f"Literal or string expected: {label!r}")
        self._contents[label] = value

    def __contains__(self, label: Union[str, Literal]) -> bool:
        logging.debug(f"Container.__contains__ {label!r}")
        if isinstance(label, str):
            label = Literal(label)
        elif not isinstance(label, Literal):
            raise TypeError(f"Literal or string expected: {label!r}")
        return label in self._contents

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


#
#   Enumerations
#


class EnumerationKind(Node):
    _class_iri: URIRef = _namespace["EnumerationKind"]
    _data_graph = schema_graph

    def __init__(self, name, *args, **kwargs) -> None:
        logging.debug("EnumerationKind.__init__ %r", name)

        if "_alt_namespace" in kwargs:
            _ns = kwargs.pop("_alt_namespace")
            kwargs["_node_iri"] = _ns["EnumerationKind" + "-" + name]
        elif "_node_iri" not in kwargs:
            kwargs["_node_iri"] = _namespace["EnumerationKind" + "-" + name]

        super().__init__(**kwargs)

        schema_graph.add((self._node_iri, RDF.type, RDFS.Class))
        schema_graph.add((self._node_iri, RDF.type, self._node_iri))

        schema_graph.add(
            (self._node_iri, RDFS.subClassOf, _namespace["EnumerationKind"])
        )

        logging.debug("     - len(schema_graph): %r", len(schema_graph))

        self._name = name
        self._parent = None
        self._children = set([self])

    def __call__(self, name, _alt_namespace=None) -> EnumerationKind:
        if _alt_namespace:
            new_child = EnumerationKind(
                name, _node_iri=_alt_namespace[self._name + "-" + name]
            )
        else:
            new_child = EnumerationKind(
                name, _node_iri=_namespace[self._name + "-" + name]
            )

        new_child._parent = self

        pnode = self
        while pnode:
            pnode._children.add(new_child)
            schema_graph.add((new_child._node_iri, RDFS.subClassOf, pnode._node_iri))
            pnode = pnode._parent

        return new_child


class Junction(Node):
    """
    Junction.
    """

    _class_iri: URIRef = S223.Junction
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

    _class_iri: URIRef = S223.Segment
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
                    other._node_iri,
                    S223.lnx,
                    self._node_iri,
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
                self._node_iri,
                S223.lnx,
                other._node_iri,
            )
        )

class S223System(Container):
    _class_iri: URIRef = S223.System
    hasPhysicalLocation: PhysicalSpace
    hasDomain: Domain

    _serves_zones: Dict[str, Zone]

    def __init__(self, config: Dict[str, Any] = {}, *args, **kwargs: Any) -> None:
        logging.debug(f"System.__init__ {config} {args} {kwargs}")

        # if there are "params" in the configuation, use those as defaults for
        # kwargs and allow them to be overriden be additional kwargs
        # if config and "params" in config:
        #     kwargs = {**config["params"], **kwargs}

        super().__init__(*args, **kwargs)
            # zone references
        self._serves_zones = {}

    def serves_zone(self, other: Zone) -> None:
        connect_mm(self, other)

class System(S223System, Node):
    """
    System
    """

    _class_iri: URIRef = BOB.System

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
                    logging.debug(
                        f"    - thing_name, thing_class: {thing_name}, {thing_class}"
                    )
                    if thing_name in self:
                        raise ValueError(f"label already used: {self[thing_name]}")
                    thing = thing_class(label=thing_name, **thing_kwargs)

                    if isinstance(thing, (Device, System)):
                        self > thing
                    if isinstance(thing, Property):
                        thing @ self
                        self[thing_name] = thing
                        self.add_property(thing)

                    things.append(thing)

                setattr(self, "_" + group_name, things)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        # instantiate and associate all of the system connection points
        self._system_connection_points = {}
        for attr_name, attr_type in self._nodes.items():
            if inspect.isclass(attr_type) and issubclass(
                attr_type, SystemConnectionPoint
            ):
                # build an instance of this connection point
                attr_element = attr_type(self, label=self.label + "." + attr_name)
                self._system_connection_points[attr_name] = attr_element
                logging.debug(
                    f"    - system connection point {attr_name}: {attr_element}"
                )

                setattr(self, attr_name, attr_element)

@multimethod
def contains_mm(system: System, device: Device) -> None:
    """System > Device"""
    logging.info(f"system {system} contains device {device}")

    system._data_graph.add((system._node_iri, S223.contains, device._node_iri))
    if INCLUDE_INVERSE:
        system._data_graph.add((device._node_iri, S223.isContainedIn, system._node_iri))


@multimethod
def contains_mm(system: System, subsystem: System) -> None:
    """System > System"""
    logging.info(f"system {system} contains subsystem {subsystem}")

    system._data_graph.add((system._node_iri, S223.contains, subsystem._node_iri))
    if INCLUDE_INVERSE:
        system._data_graph.add(
            (subsystem._node_iri, S223.isContainedIn, system._node_iri)
        )


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

    _class_iri: URIRef = S223.Connection
    hasMedium: Medium

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class Connectable(Node):
    """
    A type of thing that can have connection points.
    """

    _class_iri: URIRef = None
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

        # instantiate and associate all of the connection points
        self._connection_points = {}
        for attr_name, attr_type in self._nodes.items():
            if inspect.isclass(attr_type) and issubclass(attr_type, ConnectionPoint):
                # build an instance of this connection point
                attr_element = attr_type(self, label=self.label + "." + attr_name)
                self._connection_points[attr_name] = attr_element
                logging.debug(f"    - connection point {attr_name}: {attr_element}")

                setattr(self, attr_name, attr_element)


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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {from_thing} to {to_thing}")
    logging.debug(f"    - to_types: {to_types}")

    # find compatible pairs
    pairs = []
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if (from_medium in to_medium._children) or (to_medium in from_medium._children):
            pairs.append((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs[0]
    from_connection_point = from_out[from_medium].pop()
    logging.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    logging.debug(f"    - to_connection_point: {to_connection_point}")

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
    if CONNECTION_HAS_MEDIUM:
        connection = Connection(hasMedium=medium, label="cnx")
    else:
        connection = Connection(label="cnx")

    # connect the from thing
    connect_mm(from_connection_point, connection)

    # connect the to things
    for to_thing in to_things:
        connect_mm(connection, to_thing)


class ConnectionPoint(Node):
    """
    Connection Point
    """

    _class_iri: URIRef = None
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

        self._data_graph.add((thing._node_iri, S223.hasConnectionPoint, self._node_iri))
        self.isConnectionPointOf = thing

        # this is one of the connection points of the device
        thing._connection_points[str(self._node_iri)] = self

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

    # check medium
    if not (from_medium := getattr(from_connection_point, "hasMedium", None)):
        raise AttributeError(f"{from_connection_point} hasMedium")
    logging.debug(f"    - from_medium: {from_medium}")

    if not (to_medium := getattr(to_connection_point, "hasMedium", None)):
        raise AttributeError(f"{to_connection_point} hasMedium")
    logging.debug(f"    - to_medium: {to_medium}")

    if (from_medium not in to_medium._children) and (
        to_medium not in from_medium._children
    ):
        raise RuntimeError(
            f"mismatched medium: {from_connection_point} >> {to_connection_point}"
        )

    # create a connection between the two
    if CONNECTION_HAS_MEDIUM:
        connection = Connection(hasMedium=from_medium, label="cnx")
    else:
        connection = Connection(label="cnx")

    # link the two things together
    from_connection_point._data_graph.add(
        (
            from_connection_point.isConnectionPointOf._node_iri,
            S223.connectedTo,
            to_connection_point.isConnectionPointOf._node_iri,
        )
    )
    from_connection_point._data_graph.add(
        (
            to_connection_point.isConnectionPointOf._node_iri,
            S223.connectedFrom,
            from_connection_point.isConnectionPointOf._node_iri,
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
    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        logging.debug(f"    - connection_medium: {connection_medium}")

        if not (
            connection_point_medium := getattr(connection_point, "hasMedium", None)
        ):
            raise AttributeError(f"{connection_point} hasMedium")
        logging.debug(f"    - connection_point_medium: {connection_point_medium}")

        if (connection_medium not in connection_point_medium._children) and (
            connection_point_medium not in connection_medium._children
        ):
            raise RuntimeError(f"mismatched medium: {connection_point} >> {connection}")

    # property based link
    connection_point.connectsThrough = connection

    # link connection to the connection point and its device
    connection_point._data_graph.add(
        (connection._node_iri, S223.connectsAt, connection_point._node_iri)
    )
    connection_point._data_graph.add(
        (
            connection_point.isConnectionPointOf._node_iri,
            S223.connectedThrough,
            connection._node_iri,
        )
    )
    connection_point._data_graph.add(
        (
            connection._node_iri,
            S223.connectsFrom,
            connection_point.isConnectionPointOf._node_iri,
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
    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        logging.debug(f"    - connection_medium: {connection_medium}")

        if not (
            connection_point_medium := getattr(connection_point, "hasMedium", None)
        ):
            raise AttributeError(f"{connection_point} hasMedium")
        logging.debug(f"    - connection_point_medium: {connection_point_medium}")

        if (connection_medium not in connection_point_medium._children) and (
            connection_point_medium not in connection_medium._children
        ):
            raise RuntimeError(f"mismatched medium: {connection} >> {connection_point}")

    # property based link
    connection_point.connectsThrough = connection

    # link connection to the connection point and its device
    connection_point._data_graph.add(
        (
            connection_point.isConnectionPointOf._node_iri,
            S223.connectedThrough,
            connection._node_iri,
        )
    )
    connection._data_graph.add(
        (connection._node_iri, S223.connectsAt, connection_point._node_iri)
    )
    connection._data_graph.add(
        (
            connection._node_iri,
            S223.connectsTo,
            connection_point.isConnectionPointOf._node_iri,
        )
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
    if not (to_medium := getattr(connection_point, "hasMedium", None)):
        raise AttributeError(f"{connection_point} hasMedium")
    logging.debug(f"    - to_medium: {to_medium}")

    # build a dict of outlet connection points of the device that are not
    # already connected that have a compatiable medium
    from_out = set()
    for attr, cp in device._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(cp, OutletConnectionPoint):
            continue

        if not (medium := getattr(cp, "hasMedium", None)):
            continue
        if (medium in to_medium._children) or (to_medium in medium._children):
            from_out.add(cp)
    logging.debug(f"    - from_out: {from_out}")

    if not from_out:
        raise RuntimeError(f"no candidate sources from {device} to {connection_point}")
    if len(from_out) > 1:
        raise RuntimeError("too many candidate connection points")
    from_thing = from_out.pop()
    logging.debug(f"    - from_thing: {from_thing}")

    # link the two things together
    from_thing._data_graph.add(
        (
            from_thing.isConnectionPointOf._node_iri,
            S223.connectedTo,
            connection_point.isConnectionPointOf._node_iri,
        )
    )
    from_thing._data_graph.add(
        (
            connection_point.isConnectionPointOf._node_iri,
            S223.connectedFrom,
            from_thing.isConnectionPointOf._node_iri,
        )
    )

    # set the relationships
    connect_mm(from_thing, connection_point)


@multimethod
def connect_mm(device: Device, connection: Connection) -> None:
    """Device >> Connection"""
    logging.info(f"connect from {device} to {connection}")

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        logging.debug(f"    - connection_medium: {connection_medium}")

    # build a dict of outlet connection points of the device that are not
    # already connected that have a compatable medium
    from_out = set()
    for attr, connection_point in device._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if not isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if CONNECTION_HAS_MEDIUM:
            if (medium in connection_medium._children) or (
                connection_medium in medium._children
            ):
                from_out.add(connection_point)
        else:
            from_out.add(connection_point)
    logging.debug(f"    - from_out: {from_out}")

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

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        logging.debug(f"    - connection_medium: {connection_medium}")

    # build a dict of inlet connection points that are not already connected
    # that have a compatable medium
    to_in = set()
    for attr, connection_point in device._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue

        if CONNECTION_HAS_MEDIUM:
            if (medium in connection_medium._children) or (
                connection_medium in medium._children
            ):
                to_in.add(connection_point)
        else:
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

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        logging.debug(f"    - connection_medium: {connection_medium}")

    for device in devices:
        # build a dict of inlet connection points that are not already connected
        # that have a compatible medium
        to_in = set()
        for attr, connection_point in device._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if isinstance(connection_point, OutletConnectionPoint):
                continue

            if not (medium := getattr(connection_point, "hasMedium", None)):
                continue

            if CONNECTION_HAS_MEDIUM:
                if (medium in connection_medium._children) or (
                    connection_medium in medium._children
                ):
                    to_in.add(connection_point)
            else:
                to_in.add(connection_point)
        logging.debug("    - to_in: %r", to_in)

        if not to_in:
            raise RuntimeError(
                f"no candidate destinations from {connection} to {device}"
            )
        if len(to_in) > 1:
            raise RuntimeError("too many destinations from {connection} to {device}")
        to_thing = to_in.pop()
        logging.debug("    - to_thing: %r", to_thing)

        # set the relationships
        connect_mm(connection, to_thing)


@multimethod
def connect_mm(connection_point: ConnectionPoint, device: Device) -> None:
    """ConnectionPoint >> Device"""
    logging.info(f"connect from {connection_point} to {device}")
    if not (connection_point_medium := getattr(connection_point, "hasMedium", None)):
        raise AttributeError(f"{connection_point} hasMedium")
    logging.debug("    - connection_point_medium: %r", connection_point_medium)

    # build a dict of inlet connection points that are not already connected
    # that have a compatable medium
    to_in = set()
    for attr, connection_point in device._connection_points.items():
        if connection_point.connectsThrough:
            continue
        if isinstance(connection_point, OutletConnectionPoint):
            continue

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if (medium in connection_point_medium._children) or (
            connection_point_medium in medium._children
        ):
            to_in.add(connection_point)
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

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        logging.debug(f"    - connection_medium: {connection_medium}")

    # build a dict of mapped inlet connection points that are not
    # already connected, filtered by medium
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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if CONNECTION_HAS_MEDIUM:
            if (medium in connection_medium._children) or (
                connection_medium in medium._children
            ):
                to_in.add(connection_point)
        else:
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

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        logging.debug(f"    - connection_medium: {connection_medium}")

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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if CONNECTION_HAS_MEDIUM:
            if (medium in connection_medium._children) or (
                connection_medium in medium._children
            ):
                from_out.add(connection_point)
        else:
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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {device} to {system}")
    logging.debug(f"    - to_types: {to_types}")

    # find compatible pairs
    pairs = []
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if (from_medium in to_medium._children) or (to_medium in from_medium._children):
            pairs.append((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs[0]
    from_connection_point = from_out[from_medium].pop()
    logging.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    logging.debug(f"    - to_connection_point: {to_connection_point}")

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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        to_in[medium].add(connection_point)

    # filter them to a set where there is only one for that medium so it
    # would be unambiguous to use it
    to_types: Set[Medium]
    to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
    if not to_types:
        raise RuntimeError(f"no candidate destinations from {system} to {device}")
    logging.debug(f"    - from_types: {from_types}")

    # find compatible pairs
    pairs = []
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if (from_medium in to_medium._children) or (to_medium in from_medium._children):
            pairs.append((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    # get the two connection points
    from_medium, to_medium = pairs[0]
    from_connection_point = from_out[from_medium].pop()
    logging.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    logging.debug(f"    - to_connection_point: {to_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)


class SystemConnectionPoint(Node):
    """
    System Connection Point
    """

    _class_iri: URIRef = None
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

        self._data_graph.add(
            (system._node_iri, BOB.hasSystemConnectionPoint, self._node_iri)
        )
        if INCLUDE_INVERSE:
            self.isSystemConnectionPointOf = system

        # this is one of the connection points of the system
        system._system_connection_points[str(self._node_iri)] = self

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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
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

    # find compatible pairs
    pairs = []
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if (from_medium in to_medium._children) or (to_medium in from_medium._children):
            pairs.append((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs[0]
    from_connection_point = from_out[from_medium].pop()
    logging.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    logging.debug(f"    - to_connection_point: {to_connection_point}")

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


class Zone(Container, Node):
    """
    A collection of spaces.
    """

    _class_iri: URIRef = S223.Zone
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

        # instantiate and associate all of the zone connection points
        self._zone_connection_points = {}
        for attr_name, attr_type in self._nodes.items():
            if inspect.isclass(attr_type) and issubclass(
                attr_type, ZoneConnectionPoint
            ):
                # build an instance of this connection point
                attr_element = attr_type(self, label=self.label + "." + attr_name)
                self._zone_connection_points[attr_name] = attr_element
                logging.debug(f"    - connection point {attr_name}: {attr_element}")

                setattr(self, attr_name, attr_element)


@multimethod
def connect_mm(from_system: System, to_zone: Zone) -> None:
    """System >> Zone"""
    logging.info(f"connect from {from_system} to {to_zone}")

    # stash this in the system
    from_system._serves_zones[to_zone.label] = to_zone

    from_system._data_graph.add(
        (from_system._node_iri, BRICK.feeds, to_zone._node_iri)
    )
    if INCLUDE_INVERSE:
        from_system._data_graph.add(
            (to_zone._node_iri, BRICK.isFedBy, from_system._node_iri)
        )

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

    # find compatible pairs
    pairs = []
    for from_medium, to_medium in itertools.product(from_types, to_types):
        if (from_medium in to_medium._children) or (to_medium in from_medium._children):
            pairs.append((from_medium, to_medium))
    if len(pairs) == 0:
        raise RuntimeError("no compatiable connection points")
    if len(pairs) > 1:
        raise RuntimeError("too many compatiable connection points")

    from_medium, to_medium = pairs[0]
    from_connection_point = from_out[from_medium].pop()
    logging.debug(f"    - from_connection_point: {from_connection_point}")
    to_connection_point = to_in[to_medium].pop()
    logging.debug(f"    - to_connection_point: {to_connection_point}")

    # continue creating the connection
    connect_mm(from_connection_point, to_connection_point)

    from_system._data_graph.add(
        (from_system._node_iri, S223.servesZone, to_zone._node_iri)
    )
    if INCLUDE_INVERSE:
        from_system._data_graph.add(
            (to_zone._node_iri, S223.isServedBy, from_system._node_iri)
        )


@multimethod
def connect_mm(zone: Zone, connection: Connection) -> None:
    """Zone >> Connection"""
    logging.info(f"connect from {zone} to {connection}")

    if CONNECTION_HAS_MEDIUM:
        if not (connection_medium := getattr(connection, "hasMedium", None)):
            raise AttributeError(f"{connection} hasMedium")
        logging.debug(f"    - connection_medium: {connection_medium}")

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

        if not (medium := getattr(connection_point, "hasMedium", None)):
            continue
        if CONNECTION_HAS_MEDIUM:
            if (medium in connection_medium._children) or (
                connection_medium in medium._children
            ):
                from_out.add(connection_point)
        else:
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

    zone._data_graph.add((zone._node_iri, S223.contains, domain_space._node_iri))
    if INCLUDE_INVERSE:
        zone._data_graph.add(
            (domain_space._node_iri, S223.isContainedIn, zone._node_iri)
        )


class ZoneConnectionPoint(Node):
    """
    Zone Connection Point
    """

    _class_iri: URIRef = BOB.ZoneConnectionPoint
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

        self._data_graph.add(
            (zone._node_iri, BOB.hasZoneConnectionPoint, self._node_iri)
        )
        if INCLUDE_INVERSE:
            self.isZoneConnectionPointOf = zone

        # this is one of the connection points of the zone
        zone._zone_connection_points[str(self._node_iri)] = self

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


class PhysicalSpace(Container, Node):
    """
    A part of the physical world whose 3D spatial extent is bounded.
    """

    _class_iri: URIRef = S223.PhysicalSpace


@multimethod
def contains_mm(parent_space: PhysicalSpace, child_space: PhysicalSpace) -> None:
    """PhysicalSpace > PhysicalSpace"""
    logging.info(f"physical space {parent_space} contains physical space {child_space}")

    parent_space._data_graph.add(
        (parent_space._node_iri, S223.contains, child_space._node_iri)
    )
    if INCLUDE_INVERSE:
        parent_space._data_graph.add(
            (child_space._node_iri, S223.isContainedIn, parent_space._node_iri)
        )


@multimethod
def contains_mm(physical_space: PhysicalSpace, domain_space: DomainSpace) -> None:
    """PhysicalSpace > DomainSpace"""
    logging.info(f"physical space {physical_space} encloses {domain_space}")

    physical_space._data_graph.add(
        (physical_space._node_iri, S223.encloses, domain_space._node_iri)
    )
    if INCLUDE_INVERSE:
        physical_space._data_graph.add(
            (domain_space._node_iri, S223.isEnclosedIn, physical_space._node_iri)
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

    _class_iri: URIRef = S223.Device
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

        # When passing kwargs to create an instance of a class, some datatype
        # are not yet visible in the chain of creation. This lead to
        # ex. TypeError: unexpected keyword argument: waterInlet
        # By removing properties and connection points from kwargs and explicitly
        # putting them in config, it should be better
        _config = dict(config.items())
        for attr_name, attr_value in kwargs.copy().items():
            if inspect.isclass(attr_value):
                # if issubclass(attr_value, Property):
                #    config["properties"] = (
                #        {**config["properties"], **{attr_name: kwargs.pop(attr_name)}}
                #        if "properties" in config.keys()
                #        else {attr_name: kwargs.pop(attr_name)}
                #    )
                if issubclass(attr_value, ConnectionPoint):
                    _config["cp"] = (
                        {**_config["cp"], **{attr_name: kwargs.pop(attr_name)}}
                        if "cp" in _config.keys()
                        else {attr_name: kwargs.pop(attr_name)}
                    )

        super().__init__(*args, **kwargs)

        if _config:
            for group_name, group_items in _config.items():
                if group_name == "params":
                    continue
                if group_name == "cp":
                    for (thing_name, thing_class) in group_items.items():
                        setattr(
                            self,
                            thing_name,
                            thing_class(self, label=f"{self.label}.{thing_name}"),
                        )
                    continue
                things = []
                for (thing_name, thing_class), thing_kwargs in group_items.items():
                    if thing_name in self:
                        raise ValueError(f"label already used: {self[thing_name]}")
                    thing = thing_class(label=thing_name, **thing_kwargs)

                    if isinstance(thing, (Device, System)):
                        self > thing
                    if isinstance(thing, Property):
                        self[thing_name] = thing
                        self.add_property(thing)

                    things.append(thing)

                setattr(self, "_" + group_name, things)


@multimethod
def contains_mm(system: System, device: Device) -> None:
    """System > Device"""
    logging.info(f"system {system} contains device {device}")

    system._data_graph.add((system._node_iri, S223.contains, device._node_iri))
    if INCLUDE_INVERSE:
        system._data_graph.add((device._node_iri, S223.isContainedIn, system._node_iri))


@multimethod
def contains_mm(parent_device: Device, child_device: Device) -> None:
    """Device > Device"""
    logging.info(f"device {parent_device} contains device {child_device}")

    parent_device._data_graph.add(
        (parent_device._node_iri, S223.contains, child_device._node_iri)
    )
    if INCLUDE_INVERSE:
        parent_device._data_graph.add(
            (child_device._node_iri, S223.isContainedIn, parent_device._node_iri)
        )


class DomainSpace(Connectable):
    """
    A part of the physical world or a virtual world whose 3D spatial extent is
    bounded actually or theoretically, and provides for certain functions
    within the zone it is contained in.
    """

    _class_iri: URIRef = S223.DomainSpace
    hasDomain: Domain
    hasMedium: Medium


@multimethod
def contains_mm(zone: Zone, domain_space: DomainSpace) -> None:
    """Zone > DomainSpace"""
    logging.info(f"zone {zone} contains domain space {domain_space}")

    zone._data_graph.add((zone._node_iri, S223.contains, domain_space._node_iri))
    if INCLUDE_INVERSE:
        zone._data_graph.add(
            (domain_space._node_iri, S223.isContainedIn, zone._node_iri)
        )


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
    raise NotImplementedError("DomainSpace >> ConnectionPoint")

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


def template_update(base: Dict = {}, config: Dict = None, bases: List = None):
    """
    This utility allows to preserve module templates from
    undesired modification during creation of devices.

    Usage :
    _config = template_update(template, user_provided_config_dict)

    """

    def merge_dict(existing, new):
        for k in new:
            if k in existing:
                if isinstance(existing[k], dict) and isinstance(new[k], dict):
                    merge_dict(existing[k], new[k])
                else:
                    existing[k] = new[k]
            else:
                existing[k] = new[k]

    if bases:
        d1, d2 = bases
        _d1 = copy.deepcopy(d1)
        _d2 = copy.deepcopy(d2)
        merge_dict(_d1, _d2)
        if config:
            merge_dict(_d1, config)
        return _d1

    else:
        _d = copy.deepcopy(base)
        if config:
            merge_dict(_d, config)
        return _d


#
#   Direction EnumerationKind Instances
#

Direction = EnumerationKind("Direction")
logging.debug("Direction: %r", Direction)

Inlet = Direction("Inlet")
Outlet = Direction("Outlet")
Bidirectional = Direction("Bidirectional")

#
#   Direction Specific Connection Points
#


class InletConnectionPoint(ConnectionPoint):
    hasDirection: Direction = Inlet


class OutletConnectionPoint(ConnectionPoint):
    hasDirection: Direction = Outlet


class BidirectionalConnectionPoint(ConnectionPoint):
    hasDirection: Direction = Bidirectional


#
#   Direction Specific System Connection Points
#


class InletSystemConnectionPoint(SystemConnectionPoint):
    _class_uri: URIRef = BOB.InletSystemConnectionPoint
    hasDirection: Direction = Inlet


class OutletSystemConnectionPoint(SystemConnectionPoint):
    _class_uri: URIRef = BOB.OutletSystemConnectionPoint
    hasDirection: Direction = Outlet


class BidirectionalSystemConnectionPoint(SystemConnectionPoint):
    _class_uri: URIRef = BOB.BidirectionalSystemConnectionPoint
    hasDirection: Direction = Bidirectional


#
#   Direction Specific Zone Connection Points
#


class InletZoneConnectionPoint(ZoneConnectionPoint):
    _class_uri: URIRef = BOB.InletZoneConnectionPoint
    hasDirection: Direction = Inlet


class OutletZoneConnectionPoint(ZoneConnectionPoint):
    _class_uri: URIRef = BOB.OutletZoneConnectionPoint
    hasDirection: Direction = Outlet


class BidirectionalZoneConnectionPoint(ZoneConnectionPoint):
    _class_uri: URIRef = BOB.BidirectionalZoneConnectionPoint
    hasDirection: Direction = Bidirectional


#
#   EnumerationKind Instances
#

# General EnumerationKind
Medium = EnumerationKind("Medium")
Substance = EnumerationKind("Substance")
Role = EnumerationKind("Role")
Domain = EnumerationKind("Domain")

# Top Hierarchy Media
Air = Medium("Air")
Water = Medium("Water")
Light = Medium("Light")
Electricity = Medium("Electricity")
NaturalGas = Medium("NaturalGas")
Glycol = Medium("Glycol")
Occupant = Medium("Occupant")
MechanicalCoupling = Medium("MechanicalCoupling", _alt_namespace=P223)
