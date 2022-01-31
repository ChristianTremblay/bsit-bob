"""
Bob the SI-WG Builder
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
import logging
import inspect

from typing import Dict, Optional, Set, Any, TextIO, Tuple, TypeVar, Union, cast

from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD

T = TypeVar("T")
NodeMap = Dict[str, Union[type, str]]
_next_node = 1

# substance identifier (s223.Air, etc) to Connection subclass
medium_classes: Dict[URIRef, Any] = {}

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


def register_medium(medium_uri: URIRef, cls: Any) -> None:
    """
    Register a substance so that the connection operators can line up the
    correct types.
    """
    medium_classes[medium_uri] = cls


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


def get_datagraph(graph: Graph = data_graph) -> None:
    content = graph
    return content


def clear(graph: Graph = data_graph) -> None:
    """Remove all the triples from the graph."""
    graph.remove((None, None, None))


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
                "hasQuantityKind",
                "unit",
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

            _namespace = getattr(cls_module, "__namespace__", None)
            if _namespace:
                logging.debug(f"    - module {cls_module} namespace: {_namespace}")
            else:
                # check the parent module
                parent_module = sys.modules[
                    ".".join(cls_module.__name__.split(".")[:-1]) or "__main__"
                ]
                logging.debug(f"    - parent_module: {parent_module}")
                _namespace = getattr(parent_module, "__namespace__", None)
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
                    #
                    # todo : Here it should not be added if observesProperty
                    # But we would lose isPropertyOf... not good
                    #
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

        # save the reference
        _annotation_reference[metaclass.__name__] = metaclass

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
            self.node = model_namespace[f"{_next_node:05d}"]
            _next_node += 1
        else:
            self.node = BNode()

        self.label = label or getattr(self, "label", "")
        if self.label:
            self._data_graph.add((self.node, RDFS.label, Literal(self.label)))

        self.comment = comment or getattr(self, "comment", "")
        if self.comment:
            self._data_graph.add((self.node, RDFS.comment, Literal(self.comment)))

        if isinstance(self, (Property, Value)):
            self.hasQuantityKind = getattr(self, "hasQuantityKind", "")
            if self.hasQuantityKind:
                self._data_graph.add(
                    (self.node, qudt.hasQuantityKind, self.hasQuantityKind)
                )
            self.unit = getattr(self, "unit", "")
            if self.unit:
                self._data_graph.add((self.node, qudt.unit, self.unit))

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
            raise ValueError(f"{attr}")

        # make sure the current value is None, no "reassigning" content
        current_value = super().__getattribute__(attr)
        if current_value is not None:
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
            elif not self._nodes[attr]:
                # This is weird case for isExternalReferenceOf.
                # Where even if it's typed as Property
                # it's not working...
                if attr == "isExternalReferenceOf":
                    node_class = Property
                    self._nodes[attr]

            else:
                node_class = cast(type, self._nodes[attr])
            # pass the value to the class to build one
            if not isinstance(value, node_class):
                # This solves a bug when creating devices
                # where the number of argument of value is wrong
                # TypeError: __init__() takes 1 positional argument but 2 were given
                try:
                    value = node_class(value)
                except TypeError:
                    value = node_class(node_iri=value)

            # add the link(s)
            if isinstance(value, (URIRef, Literal)):
                self._data_graph.add((self.node, self._attr_uriref[attr], value))  # type: ignore[attr-defined]
            if isinstance(value, Node):
                self._data_graph.add((self.node, self._attr_uriref[attr], value.node))  # type: ignore[attr-defined]

            # if the value is a property, link property to the node.  The
            # Value has a property called 'isValueOf' that is excluded.
            # ExternalReference have 'isExternalReferenceOf'
            # observesProperty have isObservedBy
            if isinstance(value, Property) and (
                not (isinstance(self, (Value, ExternalReference)))
            ):
                self.add_property(value)

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
        connect(self, other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """Build a connection to this thing from another thing."""
        connect(other, self)
        return self

    def __repr__(self) -> str:
        label = (" " + self.label) if self.label else ""
        return f"<{self.__class__.__name__}{label} at {self.node}>"

    def add_property(self, prop: Property) -> Property:
        """Add a property to a node, returns the added property."""
        assert isinstance(prop, Property)

        # link the two together
        self._data_graph.add((self.node, s223.hasProperty, prop.node))
        self._data_graph.add((prop.node, s223.isPropertyOf, self.node))

        return prop

    def __repr__(self):
        return f"{self.__dict__}"


class Value(Node):
    """
    Value node with the option to pass a value that gets turned into a
    Literal.  The 'lang' and 'datatype' values are forwarded to rdflib.
    """

    node_type: URIRef = s223.Value
    isValueOf: Property

    hasTimestamp: Literal
    hasSimpleValue: Literal
    hasQuantityKind: URIRef
    unit: URIRef

    def __init__(
        self,
        arg: Any = None,
        *,
        lang: Optional[str] = None,
        datatype: Optional[URIRef] = None,
        **kwargs: Any,
    ):
        logging.debug(
            f"Value.__init__ {arg!r} lang={lang!r} datetype={datatype!r} {kwargs}"
        )
        if arg is not None:
            if "hasSimpleValue" in kwargs:
                raise RuntimeError("initialization conflict")

            if isinstance(arg, Literal):
                pass
            elif datatype is not None:
                arg = Literal(arg, datatype=datatype)
            elif lang is not None:
                arg = Literal(arg, lang=lang)

            kwargs["hasSimpleValue"] = arg
        if "unit" in kwargs:
            self.unit = kwargs.pop("unit")
        if "hasQuantityKind" in kwargs:
            self.hasQuantityKind = kwargs.pop("hasQuantityKind")

        super().__init__(**kwargs)


class ExternalReference(Node):
    """
    ExternalReference node
    This is work in progress but we can start with something
    generic. This will be subclassed by different specific datasources
    For now I'm creating hasRef...
    """

    node_type: URIRef = s223.ExternalReference
    isExternalReferenceOf: Property
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

    node_type: URIRef = None
    hasValue: Value
    hasExternalReference: ExternalReference
    isObservedBy: Device  # a Sensor in fact, but it's not defined yet

    # override this for a specialize subclass
    _value_class: type = Value
    _ExternalReference_class: type = ExternalReference
    # _observes_class: type = Sensor

    def __init__(self, arg: Any = None, **kwargs: Any):
        logging.debug(f"Property.__init__ {arg!r} {kwargs}")
        init_value = None
        external_reference = None
        observes_reference = None
        if arg is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = arg

        if "hasExternalReference" in kwargs:
            if kwargs["hasExternalReference"]:
                if init_value:
                    raise RuntimeError(
                        "initialization conflict, can't have a value and an external datasource"
                    )
            external_reference = kwargs.pop("hasExternalReference")

        if "observesProperty" in kwargs:
            observes_reference = kwargs.pop("observesProperty")

        # unit and hasQuantityKind are not in the s223 namespace
        # but in the qudt namespace...
        if "unit" in kwargs:
            self.unit = kwargs.pop("unit")
        if "hasQuantityKind" in kwargs:
            self.hasQuantityKind = kwargs.pop("hasQuantityKind")

        super().__init__(**kwargs)

        # if there is an initial value, add/create and link to it
        if init_value is not None:
            if not isinstance(init_value, Value):
                init_value = self._value_class(init_value)

            # link the two together
            self.hasValue = init_value
            init_value.isValueOf = self
        # same for ExternalReference
        if external_reference is not None:
            if not isinstance(external_reference, ExternalReference):
                external_reference = self._ExternalReference_class(external_reference)

            # link the two together
            self.hasExternalReference = external_reference
            external_reference.isExternalReferenceOf = self

        # same for observesProperty
        # if observes_reference is not None:
        # if not isinstance(observes_reference, Device):
        #    observes_reference = self._ExternalReference_class(observes_reference)
        # sensor is not defined yet here... cross finger class type is good

        # link the two together
        #    self.observesProperty = observes_reference
        #    observes_reference.isObservedBy = self

    def add_value(self, value: Value) -> Value:
        """Add an additional value to a property, returns the value added."""
        assert isinstance(value, (Value, ExternalReference))
        if isinstance(value, Value):
            # link the two together
            self._data_graph.add((self.node, s223.hasValue, value.node))
            value.isValueOf = self

        if isinstance(value, ExternalReference):
            # link the two together
            self._data_graph.add((self.node, s223.hasExternalReference, value.node))
            value.isExternalReferenceOf = self

        return value


class Domain(Node):
    _data_graph: Graph = schema_graph


class Role(Node):
    _data_graph: Graph = schema_graph


class Medium(Node):
    node_type: URIRef = enum.EnumerationValue
    _data_graph: Graph = schema_graph


class Direction(Node):
    _data_graph: Graph = schema_graph


Inlet = Direction(node_iri=s223.Inlet)
Outlet = Direction(node_iri=s223.Outlet)
Bidirectional = Direction(node_iri=s223.Bidirectional)


class Junction(Node):
    """
    Junction.
    """

    node_type: URIRef = s223.Junction
    hasSubstance: Medium
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

    def __rshift__(self, other: Any) -> Any:
        """
        Build a connection (actaully a segment) from this thing to another thing.
        """
        self.connect_to(other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """
        Build a connection (actually a segment) to this thing from another thing.
        """
        self.connect_to(other)
        return self


class Segment(Node):
    """
    Segment.
    """

    node_type: URIRef = s223.Segment
    hasSubstance: Medium
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


class System(Node):
    """
    System
    """

    node_type: URIRef = s223.System
    hasDomain: Domain

    _system_connection_points: Dict[str, SystemConnectionPoint]

    def __init__(self, **kwargs: Any) -> None:
        logging.debug(f"System.__init__ {kwargs}")
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

    def __gt__(self, other: Node) -> Node:
        """self > other

        Build a subsystem heirarchy, the other system is a subsystem of
        this system.
        """
        logging.debug(f"__gt__ {self} {other}")

        if isinstance(other, (Device, System)):
            self._data_graph.add((self.node, s223.contains, other.node))
            self._data_graph.add((other.node, s223.isContainedIn, self.node))
        else:
            raise TypeError("system or device expected")

        return self

    def __lt__(self, other: Node) -> Node:
        """self < other

        Build a subsystem heirarchy, this is a subsystem of some other
        system.
        """
        logging.debug(f"__lt__ {self} {other}")

        if isinstance(other, System):
            self._data_graph.add((self.node, s223.isContainedIn, other.node))
            self._data_graph.add((other.node, s223.contains, self.node))
        else:
            raise TypeError("system expected")

        return other


class ConnectionMetaclass(NodeMetaclass):
    def __new__(
        cls: Any,
        clsname: str,
        superclasses: Tuple[type, ...],
        attributedict: Dict[str, Any],
    ) -> SubstanceMetaclass:
        logging.debug(f"ConnectionMetaclass.__new__ {clsname}")
        global medium_classes

        # build the class
        new_class = cast(
            ConnectionMetaclass,
            super().__new__(cls, clsname, superclasses, attributedict),
        )

        # if the class has a 'substance' initialized then register this
        # class for the substance
        medium = new_class._inits.get("hasSubstance", None)
        logging.debug(f"    - connection substance: {medium!r}")

        # make sure it's not already defined someplace else
        if medium in medium_classes:
            raise RuntimeError(
                f"medium {medium} already defined: {medium_classes[medium]}"
            )
        medium_classes[medium] = new_class

        return new_class


class Connection(Node, metaclass=ConnectionMetaclass):
    """
    Generic connection object type, unrestricted.
    """

    node_type: URIRef = s223.Connection
    hasSubstance: Medium

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def connect_to(self, connection_point: ConnectionPoint) -> None:
        """
        Connects from this connection to a connection point.
        """
        if not isinstance(connection_point, ConnectionPoint):
            raise TypeError("ConnectionPoint expected")
        if isinstance(connection_point, OutletConnectionPoint):
            raise TypeError("connection point direction")
        if connection_point.connectsThrough:
            raise RuntimeError("connection point already connected")

        # property based link
        connection_point.connectsThrough = self

        # link connection to the connection point and its device
        self._data_graph.add((self.node, s223.connectsAt, connection_point.node))
        self._data_graph.add(
            (
                connection_point.isConnectionPointOf.node,
                s223.connectedThrough,
                self.node,
            )
        )
        self._data_graph.add(
            (self.node, s223.connectsTo, connection_point.isConnectionPointOf.node)
        )

    def connect_from(self, connection_point: ConnectionPoint) -> None:
        """
        Connects from a connection point to this connection.
        """
        if not isinstance(connection_point, ConnectionPoint):
            raise TypeError("ConnectionPoint expected")
        if isinstance(connection_point, InletConnectionPoint):
            raise TypeError("connection point direction")
        if connection_point.connectsThrough:
            raise RuntimeError("connection point already connected")

        # property based link
        connection_point.connectsThrough = self

        # link connection to the connection point and its device
        self._data_graph.add((self.node, s223.connectsAt, connection_point.node))
        self._data_graph.add(
            (
                connection_point.isConnectionPointOf.node,
                s223.connectedThrough,
                self.node,
            )
        )
        self._data_graph.add(
            (self.node, s223.connectsFrom, connection_point.isConnectionPointOf.node)
        )


class Connectable(Node):
    """
    A type of thing that can have connection points.
    """

    node_type: URIRef = None
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


class ConnectionPoint(Node):
    node_type: URIRef = s223.ConnectionPoint
    hasSubstance: Medium
    hasDirection: Direction

    lnx: Segment
    connectsThrough: Connection
    isConnectionPointOf: Connectable

    def __init__(self, thing: Connectable, **kwargs: Any) -> None:
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

    def connect_to(self, other: Union[Connection, ConnectionPoint]) -> None:
        """
        Connects to a connection or a connection point.
        """
        if self.connectsThrough:
            raise RuntimeError("connection point already connected")

        if isinstance(other, Connection):
            connection = other
        elif isinstance(other, ConnectionPoint):
            connection = Connection()
            if self.hasSubstance:
                connection.hasSubstance = self.hasSubstance
            connection.connect_to(other)
        else:
            raise TypeError("connection or connection point expected")

        # link connection back from this connection point
        connection.connect_from(self)

    def connect_from(self, other: Union[Connection, ConnectionPoint]) -> None:
        """
        Connects from a connection or a connection point.
        """
        if self.connectsThrough:
            raise RuntimeError("connection point already connected")

        if isinstance(other, Connection):
            connection = other
        elif isinstance(other, ConnectionPoint):
            connection = Connection()
            if self.hasSubstance:
                connection.hasSubstance = self.hasSubstance
            connection.connect_from(other)
        else:
            raise TypeError("connection or connection point expected")

        # link connection to this connection point
        connection.connect_to(self)


class InletConnectionPoint(ConnectionPoint):
    hasDirection = Inlet


class OutletConnectionPoint(ConnectionPoint):
    hasDirection = Outlet


class SystemConnectionPoint(Node):
    """
    System Connection Point
    """

    node_type: URIRef = s223.SystemConnectionPoint
    hasSubstance: Medium
    hasDirection: Direction

    connectsThrough: Connection
    isSystemConnectionPointOf: System
    mapsTo: Node  # Union[Junction, ConnectionPoint]

    def __init__(self, system: System, **kwargs: Any) -> None:
        logging.debug(f"SystemConnectionPoint.__init__ {system} {kwargs}")
        super().__init__(**kwargs)

        self._data_graph.add((system.node, s223.hasSystemConnectionPoint, self.node))
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


class InletSystemConnectionPoint(SystemConnectionPoint):
    hasDirection = Inlet


class OutletSystemConnectionPoint(SystemConnectionPoint):
    hasDirection = Outlet


class Zone(Node):
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

    def __gt__(self, other: DomainSpace) -> Node:
        """self > other

        Build a containment heirarchy, the other domain space is contained in
        this zone.
        """
        logging.debug(f"__gt__ {self} {other}")

        if not isinstance(other, DomainSpace):
            raise TypeError("space expected")

        self._data_graph.add((self.node, s223.contains, other.node))
        self._data_graph.add((other.node, s223.isContainedIn, self.node))

        return self


class ZoneConnectionPoint(Node):
    """
    Zone Connection Point
    """

    node_type: URIRef = s223.ZoneConnectionPoint
    hasSubstance: Medium
    hasDirection: Direction

    isZoneConnectionPointOf: Zone
    mapsTo: Node

    def __init__(self, zone: Zone, **kwargs: Any) -> None:
        logging.debug(f"ZoneConnectionPoint.__init__ {zone} {kwargs}")
        super().__init__(**kwargs)

        self._data_graph.add((zone.node, s223.hasZoneConnectionPoint, self.node))
        self.isZoneConnectionPointOf = zone

        # this is one of the connection points of the zone
        zone._zone_connection_points[str(self.node)] = self

    def maps_to(self, other: Union[Junction, ConnectionPoint]) -> None:
        """
        Maps this connection point to a space connection point.
        """
        logging.debug(f"ZoneConnectionPoint.maps_to {other}")
        if self.mapsTo:
            raise RuntimeError("zone connection point already mapped")

        if not isinstance(other, (Junction, ConnectionPoint)):
            raise TypeError("ConnectionPoint expected")

        self.mapsTo = other


class InletZoneConnectionPoint(ZoneConnectionPoint):
    hasDirection = Inlet


class OutletZoneConnectionPoint(ZoneConnectionPoint):
    hasDirection = Outlet


class PhysicalSpace(Node):
    """
    A part of the physical world whose 3D spatial extent is bounded.
    """

    node_type: URIRef = s223.PhysicalSpace

    def __gt__(self, other: Union[DomainSpace, PhysicalSpace]) -> Node:
        """self > other

        Build a containment heirarchy, this contains some other space.
        """
        logging.debug(f"__gt__ {self} {other}")

        if isinstance(other, PhysicalSpace):
            self._data_graph.add((self.node, s223.contains, other.node))
            self._data_graph.add((other.node, s223.isContainedIn, self.node))
        elif isinstance(other, DomainSpace):
            self._data_graph.add((self.node, s223.encloses, other.node))
        else:
            raise TypeError("domain space or physical space expected")

        return self

    def __lt__(self, other: PhysicalSpace) -> Node:
        """self < other

        Build a containment heirarchy, this is contained in some other
        physical space.
        """
        logging.debug(f"__lt__ {self} {other}")

        if not isinstance(other, PhysicalSpace):
            raise TypeError("physical space expected")

        self._data_graph.add((other.node, s223.contains, self.node))
        self._data_graph.add((self.node, s223.isContainedIn, other.node))

        return other


Electrical = Domain(node_iri=s223.Electrical)
Fire = Domain(node_iri=s223.Fire)
HVAC = Domain(node_iri=s223.HVAC)
Lighting = Domain(node_iri=s223.Lighting)
Occupancy = Domain(node_iri=s223.Occupancy)
Security = Domain(node_iri=s223.Security)
Networking = Domain(node_iri=s223.Networking)
Physical = Domain(node_iri=s223.Physical)


def connect(from_thing: Any, to_thing: Any, segmented: bool = False) -> None:
    """
    Find an unambiguous way to connect to things together.
    """
    logging.info(f"connect from {from_thing} to {to_thing}")

    from_out = defaultdict(set)
    if isinstance(from_thing, ConnectionPoint):
        medium = getattr(from_thing, "hasSubstance", None)
        from_out[medium].add(from_thing)

    elif isinstance(from_thing, Connection):
        pass

    elif isinstance(from_thing, Connectable):
        for attr, connection_point in from_thing._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, OutletConnectionPoint):
                continue

            medium = getattr(connection_point, "hasSubstance", None)
            medium = getattr(medium, "node", medium)
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

        medium = getattr(connection_point, "hasSubstance", None)
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

            medium = getattr(connection_point, "hasSubstance", None)
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

            medium = getattr(connection_point, "hasSubstance", None)
            from_out[medium].add(connection_point)

    else:
        raise NotImplementedError(f"connecting from {from_thing}")
    logging.debug(f"    - from_out: {from_out}")

    from_types: Set[URIRef]
    if isinstance(from_thing, Connection):
        from_types = set([from_thing.hasSubstance])
    else:
        from_types = set(medium for medium in from_out if len(from_out[medium]) == 1)
        if not from_types:
            from_types = set(
                medium for medium in from_out if len(from_out[medium.node]) == 1
            )
        if not from_types:
            raise RuntimeError(f"no candidate sources from {from_thing} to {to_thing}")
    logging.debug(f"    - from_types: {from_types}")

    to_in = defaultdict(set)
    if isinstance(to_thing, ConnectionPoint):
        medium = getattr(to_thing, "hasSubstance", None)
        medium = getattr(medium, "node", medium)
        # ISSUE...having a hard time with electrical things
        to_in[medium].add(to_thing)

    elif isinstance(to_thing, Connection):
        pass

    elif isinstance(to_thing, Connectable):
        for attr, connection_point in to_thing._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, InletConnectionPoint):
                continue

            medium = getattr(connection_point, "hasSubstance", None)
            # Here when trying to connect a connectionpoint to a device
            # medium turned to be
            # {'node': rdflib.term.URIRef('http://data.ashrae.org/standard223/1.0/vocab/enumeration#Water-ChilledWater'), 'label': '', 'comment': ''}
            # and the intersection fails to recognize the substance
            medium = getattr(medium, "node", medium)
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

        medium = getattr(connection_point, "hasSubstance", None)
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

            medium = getattr(connection_point, "hasSubstance", None)
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

            medium = getattr(connection_point, "hasSubstance", None)
            to_in[medium].add(connection_point)

    else:
        raise NotImplementedError(f"connecting to {to_thing}")
    logging.debug(f"    - to_in: {to_in}")

    to_types: Set[URIRef]
    if isinstance(to_thing, Connection):
        to_types = set([to_thing.hasSubstance])
    else:
        to_types = set(medium for medium in to_in if len(to_in[medium]) == 1)
        if not to_types:
            raise RuntimeError(
                f"no candidate destinations from \n{from_thing}\n\n to\n {to_thing}"
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

        from_thing.connect_to(to_connection_point)

    elif isinstance(to_thing, Connection):
        from_connection_point = from_out[medium].pop()

        to_thing.connect_from(from_connection_point)

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
            from_connection_point.connect_to(to_connection_point)


class Device(Connectable):
    """
    A Device is normally a physical entity that one might buy from a vendor - a tangible object designed to accomplish a specific task.
    """

    node_type: URIRef = s223.Device
    # hasContextualRoleShape: Any
    # hasPropertyShape: Any
    hasRole: Role
    hasLocation: PhysicalSpace

    def __gt__(self, other: Union[Device, System]) -> Union[Device, System]:
        """self > other

        Build containment heirarchy.
        """
        if not isinstance(other, (Device, System)):
            raise TypeError("device or system expected")

        self._data_graph.add((self.node, s223.contains, other.node))
        self._data_graph.add((other.node, s223.isContainedIn, self.node))

        return self

    def __lt__(self, other: Union[Device, System]) -> Union[Device, System]:
        """self < other

        Build containment heirarchy, this is a device within a system.
        """
        if not isinstance(other, (Device, System)):
            raise TypeError("device or system expected")

        self._data_graph.add((self.node, s223.isContainedIn, other.node))
        self._data_graph.add((other.node, s223.contains, self.node))

        return other


class DomainSpace(Connectable):
    """
    A part of the physical world or a virtual world whose 3D spatial extent is
    bounded actually or theoretically, and provides for certain functions
    within the zone it is contained in.
    """

    node_type: URIRef = s223.DomainSpace
    hasDomain: Domain

    def __lt__(self, other: Union[Zone, PhysicalSpace]) -> Node:
        """self < other

        Build a containment heirarchy, this is contained in a zone or enclosed
        in a physical space.
        """
        logging.debug(f"__lt__ {self} {other}")

        if isinstance(other, Zone):
            self._data_graph.add((other.node, s223.contains, self.node))
            self._data_graph.add((self.node, s223.isContainedIn, other.node))
        elif isinstance(other, PhysicalSpace):
            self._data_graph.add((other.node, s223.encloses, self.node))
        else:
            raise TypeError("zone or physical space expected")

        return self
