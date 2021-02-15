"""
Bob the SI-WG Builder
"""

from __future__ import annotations

import os
import sys
import inspect
from collections import defaultdict
import logging

from typing import (
    Dict,
    Optional,
    Set,
    Any,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD  # type: ignore

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

# globals
data_graph = Graph()
schema_graph = Graph()
_next_node = 1


# cleanup annotation references, i.e. "System" to _nodes[attr] = System
NodeMap = Dict[str, Union[type, str]]
_annotation_forwards: Dict[str, type] = {}

# these are string annotations
_annotation_forwards["URIRef"] = URIRef
_annotation_forwards["BNode"] = BNode
_annotation_forwards["Literal"] = Literal

# I shouldn't need these!
_annotation_forwards["str"] = str


def bind_namespace(prefix: str, uri: str) -> Namespace:
    """
    Create a Namespace and bind a prefix to it in the graphs.
    """
    namespace = Namespace(uri)
    data_graph.namespace_manager.bind(prefix, URIRef(uri))
    schema_graph.namespace_manager.bind(prefix, URIRef(uri))
    return namespace


# common namespaces
c223 = bind_namespace("c223", "http://data.ashrae.org/standard223/1.0/model/core#")
d223 = bind_namespace("d223", "http://data.ashrae.org/standard223/1.0/model/device#")
qudt = bind_namespace("qudt", "http://qudt.org/schema/qudt/")
quantitykind = bind_namespace("quantitykind", "http://qudt.org/vocab/quantitykind/")
brick = bind_namespace("brick", "https://brickschema.org/schema/1.1.0/Brick#")

# the namespace for a node is defined in the node as the _namespace attribute
# or in the __namespace__ special global for the module of the class, or the
# parent module, or it is inherited from a superclass that is defined in the
# same module
__namespace__ = c223

# the model_namespace is used to create "blank" node identifiers, a serial
# number to make it easier to debug a constructed file
model_namespace = None


def data_graph_add(triple: Tuple[Any, Any, Any]) -> None:
    """
    Add a triple to the data graph, checking the predicate to see if it should
    be included or excluded.
    """
    global data_graph
    subj, pred, obj = triple

    namespace, namespace_uriref, suffix = data_graph.namespace_manager.compute_qname(
        pred
    )
    for test_name in (namespace + ":" + suffix, namespace + ":*", "*"):
        if test_name in include_predicates:
            break
        if test_name in exclude_predicates:
            return

    # passes the tests
    data_graph.add(triple)


def schema_graph_add(triple: Tuple[Any, Any, Any]) -> None:
    """
    Add a triple to the schema graph for statements about things in the
    model being build (like subtypes of a Device) but not about things
    in the c223 namespace.
    """
    global schema_graph
    subj, pred, obj = triple

    # exclude the schema content in the c223 namespace by default
    if subj.startswith(c223):
        return

    # passes the tests
    schema_graph.add(triple)


def bind_model_namespace(prefix: str, uri: str) -> Namespace:
    """
    Create a Namespace for blank node identifiers and bind a prefix to the
    prefix in the graph.
    """
    global model_namespace
    model_namespace = bind_namespace(prefix, uri)
    return model_namespace


# substance identifier (c223.Air, etc) to Connection subclass
substance_classes: Dict[URIRef, Any] = {}


T = TypeVar("T")


def register_substance(substance_uri: URIRef, cls: Any) -> None:
    """
    Register a substance so that the connection operators can line up the
    correct types.
    """
    substance_classes[substance_uri] = cls


class NodeMetaclass(type):
    def __new__(
        cls: Any,
        clsname: str,
        superclasses: Tuple[type, ...],
        attributedict: Dict[str, Any],
    ) -> NodeMetaclass:
        logging.debug(f"NodeMetaclass.__new__ {clsname}")
        # do this for every subclass of Node

        # start with empty maps
        _nodes: NodeMap = {}
        _datatypes: Dict[str, Literal] = {}
        _inits: Dict[str, Any] = {}

        attr_names: Set[str] = set()
        _attr_uriref: Dict[str, URIRef] = {}

        # include the maps this class is inheriting
        for supercls in reversed(superclasses):
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
        for attr, attr_type in annotations.items():
            logging.debug(f"    - attr, attr_type: {attr!r}, {attr_type!r}")

            if attr.startswith("_"):
                continue
            if attr in ("node", "node_type", "label"):
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
                if attr_type in _annotation_forwards:
                    attr_type = _annotation_forwards[attr_type]
                else:
                    _annotation_forwards[attr_type] = None  # type: ignore[assignment]
                _nodes[attr] = attr_type
                attr_names.add(attr)
            else:
                raise ValueError(f"unknown annotation for {attr}: {attr_type}")

        # look for initializers like hasUnit = QUDT.DEG_F
        for attr, value in attributedict.items():
            if attr.startswith("_"):
                continue

            if attr in _nodes:
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

            else:
                continue

            _inits[attr] = value
            attr_names.add(attr)

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
            _attr_uriref[attr] = _namespace[attr]
        metaclass._attr_uriref = _attr_uriref  # type: ignore[attr-defined]

        # make sure it has a type
        if "node_type" not in attributedict:
            metaclass.node_type = _namespace[clsname]  # type: ignore[attr-defined]

        # this is a class, and a subclass of the super classes
        schema_graph_add((metaclass.node_type, RDF.type, RDFS.Class))
        for supercls in superclasses:
            if issubclass(supercls, Node):
                schema_graph_add(
                    (metaclass.node_type, RDFS.subClassOf, supercls.node_type)
                )

        # attributes are properties
        for attr in attr_names:
            schema_graph_add((_attr_uriref[attr], RDF.type, RDF.Property))

            # check for automatic sub-properties
            if all(
                _annotation_forwards.get(cname, None)
                for cname in (
                    "Property",
                    "ConnectionPoint",
                    "SystemConnectionPoint",
                )
            ):
                if attr in _nodes:
                    attr_type = _nodes[attr]
                    if issubclass(attr_type, Property):
                        schema_graph_add(
                            (_attr_uriref[attr], RDFS.subPropertyOf, c223.hasProperty)
                        )
                    if issubclass(attr_type, (ConnectionPoint, SystemConnectionPoint)):
                        schema_graph_add(
                            (
                                _attr_uriref[attr],
                                RDFS.subPropertyOf,
                                c223.hasConnectionPoint,
                            )
                        )

        # save the reference
        _annotation_forwards[metaclass.__name__] = metaclass

        return metaclass


class Node(metaclass=NodeMetaclass):
    """
    A node in the graph that optionally has a label.  Instances of this
    would be something like blank nodes.
    """

    _namespace: Namespace

    # assigned by NodeMetaclass
    _nodes: NodeMap
    _datatypes: Dict[str, Literal]
    _inits: Dict[str, Any]

    node: URIRef
    node_type: URIRef
    label: str

    def __init__(
        self, *, node_iri: URIRef = None, label: str = "", **kwargs: Any
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
            data_graph_add((self.node, RDFS.label, Literal(self.label)))

        if hasattr(self, "node_type"):
            data_graph_add((self.node, RDF.type, self.node_type))

        for attr, attr_type in self._nodes.items():
            super().__setattr__(attr, None)
            if attr in kwargs:
                setattr(self, attr, kwargs.pop(attr))

        for attr, value in self._inits.items():
            if attr in kwargs:
                setattr(self, attr, kwargs.pop(attr))
            elif inspect.isclass(value):
                setattr(self, attr, value())
            else:
                setattr(self, attr, value)

        for attr, value in kwargs.items():
            if attr in self._datatypes:
                setattr(self, attr, value)
            else:
                raise TypeError(f"unexpected keyword argument: {attr}")

    def __setattr__(self, attr: str, value: Any) -> None:
        """"""
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
                node_class = _annotation_forwards.get(self._nodes[attr], None)  # type: ignore[arg-type]
                if not node_class:
                    raise NotImplementedError(
                        f"class {self._nodes[attr]!r} for attribute {attr!r} not found"
                    )
                self._nodes[attr] = node_class
            else:
                node_class = cast(type, self._nodes[attr])

            # pass the value to the class to build one
            if not isinstance(value, node_class):
                value = node_class(value)

            # add the link(s)
            if isinstance(value, (URIRef, Literal)):
                data_graph_add((self.node, self._attr_uriref[attr], value))  # type: ignore[attr-defined]
            if isinstance(value, Node):
                data_graph_add((self.node, self._attr_uriref[attr], value.node))  # type: ignore[attr-defined]

            # if the value is a property, link property to the node.  The
            # Value has a property called 'isValueOf' that is excluded.
            if isinstance(value, Property) and (not isinstance(self, Value)):
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
            data_graph_add((self.node, self._attr_uriref[attr], value))  # type: ignore[attr-defined]

        # carry on
        super().__setattr__(attr, value)

    def __repr__(self) -> str:
        label = (" " + self.label) if self.label else ""
        return f"<{self.__class__.__name__}{label} at {self.node}>"

    def add_property(self, prop: Property) -> Property:
        """Add a property to a node, returns the added property."""
        assert isinstance(prop, Property)

        # link the two together
        data_graph_add((self.node, c223.hasProperty, prop.node))
        data_graph_add((prop.node, c223.isPropertyOf, self.node))

        return prop


class SubstanceMetaclass(NodeMetaclass):
    def __new__(
        cls: _Any,
        clsname: str,
        superclasses: Tuple[type, ...],
        attributedict: Dict[str, _Any],
    ) -> SubstanceMetaclass:
        logging.debug(f"SubstanceMetaclass.__new__ {clsname}")

        # build the class
        new_class = cast(
            SubstanceMetaclass,
            super().__new__(cls, clsname, superclasses, attributedict),
        )
        logging.debug(f"    - new_class.node_type: {new_class.node_type}")

        return new_class


class Substance(Node, metaclass=SubstanceMetaclass):
    pass


class ConnectionMetaclass(NodeMetaclass):
    def __new__(
        cls: _Any,
        clsname: str,
        superclasses: Tuple[type, ...],
        attributedict: Dict[str, _Any],
    ) -> SubstanceMetaclass:
        logging.debug(f"ConnectionMetaclass.__new__ {clsname}")
        global substance_classes

        # build the class
        new_class = cast(
            ConnectionMetaclass,
            super().__new__(cls, clsname, superclasses, attributedict),
        )

        # if the class has a 'substance' initialized then register this
        # class for the substance
        substance = new_class._inits.get("substance", None)
        logging.debug(f"    - connection substance: {substance!r}")

        # make sure it's not already defined someplace else
        if substance in substance_classes:
            raise RuntimeError(
                f"substance {substance} already defined: {substance_classes[substance]}"
            )
        substance_classes[substance] = new_class

        return new_class


# @register_substance
class Connection(Node, metaclass=ConnectionMetaclass):
    """
    Generic connection object type, unrestricted.
    """

    node_type: URIRef = c223.Connection
    substance: URIRef

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # if self.substance:
        #     substance = self.substance + "Connection"
        #     data_graph_add(
        #         (
        #             self.node,
        #             RDF.type,
        #             self._namespace[substance],
        #         )
        #     )

    def __rshift__(
        self, other: Union[ConnectionPoint, SystemConnectionPoint, Device, System]
    ) -> Union[ConnectionPoint, SystemConnectionPoint, Device, System]:
        """self >> other"""

        # look for unconnected connection points for this connection type
        unbound_connection_points = set()

        if isinstance(other, (ConnectionPoint, SystemConnectionPoint)):
            if other.connectsThrough:
                raise RuntimeError(f"already connected: {other!r}")

            other_substance = getattr(other, "substance", None)
            if other_substance != self.substance:
                raise TypeError("connection type")

            # this is a candidate
            unbound_connection_points.add(other)

        elif isinstance(other, Device):
            for (
                connection_point_name,
                connection_point,
            ) in other._connection_points.items():
                # check the connection direction
                if isinstance(connection_point, OutletConnectionPoint):
                    continue
                # the connection point must not be already connected
                if connection_point.connectsThrough:
                    continue

                # the connection type needs to match
                connection_point_type = getattr(connection_point, "substance", None)
                if connection_point_type != self.substance:
                    continue

                # this is a candidate
                unbound_connection_points.add(connection_point)

        elif isinstance(other, System):
            for (
                connection_point_name,
                connection_point,
            ) in other._connection_points.items():
                # check the connection direction
                if isinstance(connection_point, SystemOutletConnectionPoint):
                    continue
                # the connection point must not be already connected
                if connection_point.connectsThrough:
                    continue

                # the connection type needs to match
                connection_point_type = getattr(connection_point, "substance", None)
                if connection_point_type != self.substance:
                    continue

                # this is a candidate
                unbound_connection_points.add(connection_point)

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

        if not unbound_connection_points:
            raise RuntimeError(f"no unbound connection points: {other!r}")
        if len(unbound_connection_points) > 1:
            raise RuntimeError(f"multiple unbound connection points: {other!r}")

        # peek at the connection point and maybe include mapped connection points
        connection_point = unbound_connection_points.pop()
        if isinstance(connection_point, SystemConnectionPoint):
            unbound_connection_points.update(connection_point._maps_to)
        else:
            unbound_connection_points.add(connection_point)
        logging.info(f"connection: {self} >> {unbound_connection_points}")

        # loop around and link them up
        for connection_point in unbound_connection_points:
            # link connection to connection point
            data_graph_add((self.node, c223.connectsAt, connection_point.node))
            connection_point.connectsThrough = self

            # link the connection to the device/system of the connection point
            data_graph_add(
                (
                    connection_point.isConnectionPointOf.node,
                    c223.connectedThrough,
                    self.node,
                )
            )
            data_graph_add(
                (self.node, c223.connectsTo, connection_point.isConnectionPointOf.node)
            )

        # for chaining
        return other

    def __lshift__(
        self, other: Union[ConnectionPoint, SystemConnectionPoint, Device, System]
    ) -> Union[ConnectionPoint, SystemConnectionPoint, Device, System]:
        """self << other"""

        # look for <system> unconnected connection points for this connection type
        unbound_connection_points = set()

        if isinstance(other, (ConnectionPoint, SystemConnectionPoint)):
            if other.connectsThrough:
                raise RuntimeError(f"already connected: {other!r}")

            other_substance = getattr(other, "substance", None)
            if other_substance != self.substance:
                raise TypeError("connection type")

            # this is a candidate
            unbound_connection_points.add(other)

        elif isinstance(other, Device):
            for (
                connection_point_name,
                connection_point,
            ) in other._connection_points.items():
                # check the connection direction
                if isinstance(connection_point, InletConnectionPoint):
                    continue
                # the connection point must not be already connected
                if connection_point.connectsThrough:
                    continue

                # the connection type needs to match
                connection_point_type = getattr(connection_point, "substance", None)
                if connection_point_type != self.substance:
                    continue

                # this is a candidate
                unbound_connection_points.add(connection_point)

        elif isinstance(other, System):
            for (
                connection_point_name,
                connection_point,
            ) in other._connection_points.items():
                # check the connection direction
                if isinstance(connection_point, SystemInletConnectionPoint):
                    continue
                # the connection point must not be already connected
                if connection_point.connectsThrough:
                    continue

                # the connection type needs to match
                connection_point_type = getattr(connection_point, "substance", None)
                if connection_point_type != self.substance:
                    continue

                # this is a candidate
                unbound_connection_points.add(connection_point)

        else:
            raise TypeError(f"{self!r} connection from {other!r}")

        if not unbound_connection_points:
            raise RuntimeError(f"no unbound connection points: {other!r}")
        if len(unbound_connection_points) > 1:
            raise RuntimeError(f"multiple unbound connection points: {other!r}")

        # peek at the connection point and maybe include mapped connection points
        connection_point = unbound_connection_points.pop()
        if isinstance(connection_point, SystemConnectionPoint):
            unbound_connection_points.update(connection_point._maps_to)
        else:
            unbound_connection_points.add(connection_point)
        logging.info(f"connection: {self} << {unbound_connection_points}")

        # loop around and link them up
        for connection_point in unbound_connection_points:
            # link connection to connection point and back
            data_graph_add((self.node, c223.connectsAt, connection_point.node))
            connection_point.connectsThrough = self

            # link the connection to the "owner" of the connection point
            data_graph_add(
                (
                    connection_point.isConnectionPointOf.node,
                    c223.connectedThrough,
                    self.node,
                )
            )
            data_graph_add(
                (
                    self.node,
                    c223.connectsFrom,
                    connection_point.isConnectionPointOf.node,
                )
            )

        # for chaining
        return other


class Direction(Node):
    pass


# these instances show up in the data graph
# Inlet = Direction(node_iri=c223.Inlet, label="inlet")
# Outlet = Direction(node_iri=c223.Outlet, label="outlet")
# Bidirectional = Direction(node_iri=c223.Bidirectional, label="bidirectional")


class ConnectionPoint(Node):
    node_type: URIRef = c223.ConnectionPoint
    substance: URIRef  # identifier of a subclass of Substance
    direction: URIRef  # one of c223.Inlet, c223.Outlet, c223.Bidirectional

    connectsThrough: Connection
    isConnectionPointOf: Device

    def __init__(self, device: Device, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # if isinstance(self, ConnectionType) and self.substance:
        #     connection_point_type = self.substance + "ConnectionPoint"
        #     data_graph_add(
        #         (
        #             self.node,
        #             RDF.type,
        #             self._namespace[connection_point_type],
        #         )
        #     )

        data_graph_add((device.node, c223.hasConnectionPoint, self.node))
        self.isConnectionPointOf = device

        # this is one of the connection points of the device
        device._connection_points[str(self.node)] = self

    def __rshift__(
        self, other: Any
    ) -> Union[Connection, ConnectionPoint, Device, System]:
        """self >> other

        Build a connection from the connection point to a connection or
        another connection point.
        """

        self_substance: str
        other_substance: str

        if isinstance(other, Connection):
            self_substance = getattr(self, "substance", None)
            other_substance = getattr(other, "substance", None)
            if self_substance != other_substance:
                raise TypeError("connection point type")

            logging.info(f"connection: {self} >> {other}")
            if self.connectsThrough:
                raise RuntimeError(
                    f"already connected: {self} connects through {self.connectsThrough}"
                )

            # link connection to connection point and back
            self.connectsThrough = other
            data_graph_add((other.node, c223.connectsAt, self.node))

            # link the connection points "owner" to the connection
            data_graph_add(
                (
                    self.isConnectionPointOf.node,
                    c223.connectedThrough,
                    other.node,
                )
            )
            data_graph_add(
                (
                    other.node,
                    c223.connectsFrom,
                    self.isConnectionPointOf.node,
                )
            )

            # for chaining
            return other

        elif isinstance(other, ConnectionPoint):
            # check the direction
            if isinstance(other, OutletConnectionPoint):
                raise TypeError(
                    f"connection point direction: {other} is an outlet connection point"
                )

            # check the connection type
            self_substance = getattr(self, "substance", None)
            other_substance = getattr(other, "substance", None)
            if self_substance != other_substance:
                raise TypeError(
                    "connection point type: "
                    f"{self_substance!r} != {other_substance!r}"
                )

            # make sure they aren't already connected
            if self.connectsThrough:
                raise RuntimeError(
                    f"already connected: {self} connects through {self.connectsThrough}"
                )
            if other.connectsThrough:
                raise RuntimeError(
                    f"already connected: {other} connects through {other.connectsThrough}"
                )

            # make a new connection
            new_connection = substance_classes[self_substance]()
            logging.info(f"connection: {self} >> {new_connection} >> {other}")

            # link it up
            new_connection << self
            new_connection >> other

            # for chaining
            return other

        elif isinstance(other, SystemConnectionPoint):
            # check the direction
            if isinstance(other, SystemOutletConnectionPoint):
                raise TypeError(
                    f"connection point direction: {other} is a system outlet connection point"
                )

            # check the connection type
            self_substance = getattr(self, "substance", None)
            other_substance = getattr(other, "substance", None)
            if self_substance != other_substance:
                raise TypeError(
                    "connection point type: "
                    f"{self_substance!r} != {other_substance!r}"
                )

            # make sure they aren't already connected
            if self.connectsThrough:
                raise RuntimeError(
                    f"already connected: {self} connects through {self.connectsThrough}"
                )
            # if other.connectsThrough:
            #     raise RuntimeError(
            #         f"already connected: {other} connects through {other.connectsThrough}"
            #     )

            # make a new connection
            new_connection = substance_classes[self_substance]()
            logging.info(f"connection: {self} >> {new_connection} >> {other}")

            # link it up
            new_connection << self
            new_connection >> other

            # for chaining
            return other

        elif isinstance(other, (Device, System)):
            raise NotImplementedError(f"{self!r} connection to {other!r}")

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

    def __lshift__(
        self, other: Any
    ) -> Union[Connection, ConnectionPoint, Device, System]:
        """self << other

        Build a connection to this connection point from a connection or
        another connection point.
        """

        self_substance: str
        other_substance: str

        if isinstance(other, Connection):
            self_substance = getattr(self, "substance", None)
            other_substance = getattr(other, "substance", None)
            if self_substance != other_substance:
                raise TypeError("connection point type")

            logging.info(f"connection: {other} >> {self}")
            if self.connectsThrough:
                raise RuntimeError(
                    f"already connected: {self} connects through {self.connectsThrough}"
                )

            # link connection to connection point and back
            self.connectsThrough = other
            data_graph_add((other.node, c223.connectsAt, self.node))

            # link the connection points "owner" to the connection
            data_graph_add(
                (
                    self.isConnectionPointOf.node,
                    c223.connectedThrough,
                    other.node,
                )
            )
            data_graph_add(
                (
                    other.node,
                    c223.connectsTo,
                    self.isConnectionPointOf.node,
                )
            )

            # for chaining
            return other

        elif isinstance(other, ConnectionPoint):
            # check the direction
            if isinstance(self, InletConnectionPoint):
                raise TypeError(
                    f"connection point direction: {other} is an inlet connection point"
                )

            # check the connection type
            self_substance = getattr(self, "substance", None)
            other_substance = getattr(other, "substance", None)
            if self_substance != other_substance:
                raise TypeError(
                    "connection point type: "
                    f"{self_substance!r} != {other_substance!r}"
                )

            # make sure they aren't already connected
            if self.connectsThrough:
                raise RuntimeError(
                    f"already connected: {self} connects through {self.connectsThrough}"
                )
            if other.connectsThrough:
                raise RuntimeError(
                    f"already connected: {other} connects through {other.connectsThrough}"
                )

            # make a new connection
            new_connection = substance_classes[self_substance]()
            logging.info(f"connection: {other} >> {new_connection} >> {self}")

            # link it up
            new_connection << other
            new_connection >> self

            # for chaining
            return other

        elif isinstance(other, SystemConnectionPoint):
            # check the direction
            if isinstance(other, SystemInletConnectionPoint):
                raise TypeError(
                    f"connection point direction: {other} is a system inlet connection point"
                )

            # check the connection type
            self_substance = getattr(self, "substance", None)
            other_substance = getattr(other, "substance", None)
            if self_substance != other_substance:
                raise TypeError(
                    "connection point type: "
                    f"{self_substance!r} != {other_substance!r}"
                )

            # make sure they aren't already connected
            if self.connectsThrough:
                raise RuntimeError(
                    f"already connected: {self} connects through {self.connectsThrough}"
                )
            # if other.connectsThrough:
            #     raise RuntimeError(
            #         f"already connected: {other} connects through {other.connectsThrough}"
            #     )

            # make a new connection
            new_connection = substance_classes[self_substance]()
            logging.info(f"connection: {other} >> {new_connection} >> {self}")

            # link it up
            new_connection << other
            new_connection >> self

            # for chaining
            return other

        elif isinstance(other, (Device, System)):
            raise NotImplementedError(f"{self!r} connection from {other!r}")

        else:
            raise TypeError(f"{self!r} connection from {other!r}")


class InletConnectionPoint(ConnectionPoint):
    direction: URIRef = c223.Inlet


class OutletConnectionPoint(ConnectionPoint):
    direction: URIRef = c223.Outlet


class Device(Node):
    """
    A type of thing that can has connection points.
    """

    node_type: URIRef = c223.Device
    _connection_points: Dict[str, ConnectionPoint]

    def __init__(self, **kwargs: Any) -> None:
        logging.debug(f"Device.__init__ {kwargs}")
        super().__init__(**kwargs)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        # <self> a Device
        data_graph_add((self.node, RDF.type, c223.Device))

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
                if var_annotation not in _annotation_forwards:
                    logging.debug(
                        f"resolving {var_annotation!r} for attribute {var_name!r}, class not found"
                    )
                    continue
                var_annotation = _annotation_forwards.get(var_annotation)

            if not issubclass(var_annotation, ConnectionPoint):
                continue

            # build an instance of this connection point
            var_element = var_annotation(self, label=self.label + "." + var_name)
            self._connection_points[var_name] = var_element
            logging.debug(f"    - connection point {var_name}: {var_element}")

            setattr(self, var_name, var_element)

    @staticmethod
    def join_devices(from_device: Device, to_device: Device) -> None:
        """Find an unambiguous way to connect <from_device> to <to_device>"""
        logging.info(f"join from {from_device} to {to_device}")

        from_out = defaultdict(set)
        for attr, connection_point in from_device._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, OutletConnectionPoint):
                continue

            substance = getattr(connection_point, "substance", None)
            from_out[substance].add(connection_point)

        from_types = set(
            substance for substance in from_out if len(from_out[substance]) == 1
        )
        if not from_types:
            raise RuntimeError(
                f"no candidate sources from {from_device} to {to_device}"
            )
        logging.debug(f"    - from_types: {from_types}")

        to_in = defaultdict(set)
        for attr, connection_point in to_device._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, InletConnectionPoint):
                continue

            substance = getattr(connection_point, "substance", None)
            to_in[substance].add(connection_point)

        to_types = set(substance for substance in to_in if len(to_in[substance]) == 1)
        if not to_types:
            raise RuntimeError(
                f"no candidate destinations from {from_device} to {to_device}"
            )
        logging.debug(f"    - to_types: {to_types}")

        # find the connection type that has one unconnected <from> and
        # one unconnected <to>
        common_types = from_types.intersection(to_types)
        if not common_types:
            raise RuntimeError("no common connection types")
        if len(common_types) > 1:
            raise RuntimeError("too many common connection types")

        substance = common_types.pop()
        from_connection_point = from_out[substance].pop()
        to_connection_point = to_in[substance].pop()

        # build the connection
        from_connection_point >> to_connection_point

    def __gt__(self, other: Part) -> Part:
        """self > other

        Build a part heirarchy.
        """
        if not isinstance(other, Part):
            raise TypeError("part expected")

        data_graph_add((self.node, c223.contains, other.node))
        data_graph_add((other.node, c223.isContainedIn, self.node))

        return self

    def __lt__(self, other: System) -> System:
        """self < other

        Build a heirarchy, this is a device within a system.
        """
        if not isinstance(other, System):
            raise TypeError("system expected")

        data_graph_add((self.node, c223.isContainedIn, other.node))
        data_graph_add((other.node, c223.contains, self.node))

        return other

    def __rshift__(self, other: Any) -> Any:
        """self >> other

        Build a connection from this device to another device, connection, or
        system.
        """

        if isinstance(other, Device):
            Device.join_devices(self, other)
        elif isinstance(other, Connection):
            other << self
        elif isinstance(other, System):
            from_out = defaultdict(set)
            for attr, connection_point in self._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(connection_point, OutletConnectionPoint):
                    continue

                substance = getattr(connection_point, "substance", None)
                from_out[substance].add(connection_point)

            from_types = set(
                substance for substance in from_out if len(from_out[substance]) == 1
            )
            if not from_types:
                raise RuntimeError(f"no candidate sources from {self} to {other}")

            to_in = defaultdict(set)
            for attr, connection_point in other._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(connection_point, SystemInletConnectionPoint):
                    continue

                substance = getattr(connection_point, "substance", None)
                to_in[substance].add(connection_point)

            to_types = set(
                substance for substance in to_in if len(to_in[substance]) == 1
            )
            if not to_types:
                raise RuntimeError(f"no candidate destinations from {self} to {other}")

            # find the connection type that has one unconnected <from> and
            # one unconnected <to>
            common_types = from_types.intersection(to_types)
            if not common_types:
                raise RuntimeError("no common connection types")
            if len(common_types) > 1:
                raise RuntimeError("too many common connection types")

            substance = common_types.pop()
            from_connection_point = from_out[substance].pop()
            to_connection_point = to_in[substance].pop()

            # make a new connection
            new_connection = substance_classes[substance]()
            logging.info(
                f"connection: {from_connection_point} >> {new_connection} >> {to_connection_point}"
            )

            # link it up
            new_connection << from_connection_point
            new_connection >> to_connection_point

        elif isinstance(other, (ConnectionPoint, SystemConnectionPoint)):
            other_substance = getattr(other, "substance", None)
            if other.connectsThrough:
                raise RuntimeError(f"already connected: {other}")

            from_out = set()
            for attr, connection_point in self._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(connection_point, OutletConnectionPoint):
                    continue

                substance = getattr(connection_point, "substance", None)
                if substance != other_substance:
                    continue

                from_out.add(connection_point)
            if not from_out:
                raise RuntimeError(f"no candidate sources from {self} to {other}")
            if len(from_out) > 1:
                raise RuntimeError(f"too many candidate sources from {self} to {other}")
            from_connection_point = from_out.pop()

            # make a new connection
            new_connection = substance_classes[other_substance]()
            logging.info(
                f"connection: {from_connection_point} >> {new_connection} >> {other}"
            )

            # link it up
            new_connection << from_connection_point
            new_connection >> other

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

        return other

    def __lshift__(self, other: Any) -> Any:
        """self << other

        Build a connection to this device from another device, connection, or
        system.
        """

        if isinstance(other, Device):
            Device.join_devices(other, self)
        elif isinstance(other, Connection):
            other >> self
        elif isinstance(other, System):
            from_out = defaultdict(set)
            for attr, connection_point in other._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(connection_point, SystemOutletConnectionPoint):
                    continue

                substance = getattr(connection_point, "substance", None)
                from_out[substance].add(connection_point)

            from_types = set(
                substance for substance in from_out if len(from_out[substance]) == 1
            )
            if not from_types:
                raise RuntimeError(f"no candidate sources from {other} to {self}")

            to_in = defaultdict(set)
            for attr, connection_point in self._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(connection_point, InletConnectionPoint):
                    continue

                substance = getattr(connection_point, "substance", None)
                to_in[substance].add(connection_point)

            to_types = set(
                substance for substance in to_in if len(to_in[substance]) == 1
            )
            if not to_types:
                raise RuntimeError(f"no candidate destinations from {other} to {self}")

            # find the connection type that has one unconnected <from> and
            # one unconnected <to>
            common_types = from_types.intersection(to_types)
            if not common_types:
                raise RuntimeError("no common connection types")
            if len(common_types) > 1:
                raise RuntimeError("too many common connection types")

            substance = common_types.pop()
            to_connection_point = to_in.pop()

            # make a new connection
            new_connection = substance_classes[substance]()
            logging.info(f"connection: {other} >> {new_connection} >> {self}")

            # link it up
            new_connection << other
            new_connection >> self

        elif isinstance(other, (ConnectionPoint, SystemConnectionPoint)):
            other_substance = getattr(other, "substance", None)
            if other.connectsThrough:
                raise RuntimeError(f"already connected: {other}")

            self_in = set()
            for attr, connection_point in self._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(connection_point, InletConnectionPoint):
                    continue

                substance = getattr(connection_point, "substance", None)
                if substance != other_substance:
                    continue

                self_in.add(connection_point)

            if not self_in:
                raise RuntimeError(f"no candidate sources from {other} to {self}")
            if len(self_in) > 1:
                raise RuntimeError(
                    f"too many candidate destinations from {other} to {self}"
                )
            to_connection_point = self_in.pop()

            # make a new connection
            new_connection = substance_classes[other_substance]()
            logging.info(
                f"connection: {other} >> {new_connection} >> {to_connection_point}"
            )

            # link it up
            new_connection << other
            new_connection >> to_connection_point

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

        return other


class SystemConnectionPoint(Node):
    """"""

    node_type: URIRef = c223.SystemConnectionPoint

    connectsThrough: Connection
    isConnectionPointOf: System
    _maps_to: Set[ConnectionPoint]

    def __init__(self, system: System, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # if isinstance(self, ConnectionType) and self.substance:
        #     connection_point_type = self.substance + "SystemConnectionPoint"
        #     data_graph_add(
        #         (
        #             self.node,
        #             RDF.type,
        #             self._namespace[connection_point_type],
        #         )
        #     )

        data_graph_add((system.node, c223.hasConnectionPoint, self.node))
        self.isConnectionPointOf = system

        # this is one of the connection points of the connectable
        system._connection_points[str(self.node)] = self

        # doesn't map to any connection points yet
        self._maps_to = set()

    def __gt__(self, other: ConnectionPoint) -> ConnectionPoint:
        """self > other

        Build reference from this system connection point to a connection point.
        """
        # for a system connection point, reference the other connection points
        if isinstance(other, SystemConnectionPoint):
            if not other._maps_to:
                raise RuntimeError(f"system connection point unmapped: {other}")
            for other_connection_point in other._maps_to:
                self > other_connection_point
            return

        if not isinstance(other, ConnectionPoint):
            raise TypeError("connection point expected")
        # if isinstance(self, SystemInletConnectionPoint) and not isinstance(other, InletConnectionPoint):
        #     raise TypeError(f"inlet connection point expected: {other}")
        # if isinstance(self, SystemOutletConnectionPoint) and not isinstance(other, OutletConnectionPoint):
        #     raise TypeError(f"outlet connection point expected: {other}")

        # make sure they aren't already connected
        if self.connectsThrough:
            raise RuntimeError(
                f"already connected: {self} connects through {self.connectsThrough}"
            )
        if other.connectsThrough:
            raise RuntimeError(
                f"already connected: {other} connects through {other.connectsThrough}"
            )

        data_graph_add((self.node, c223.mapsTo, other.node))
        self._maps_to.add(other)

        return self

    def __lt__(self, other: Node) -> Node:
        """self < other

        Build reference from a connection point to this system connection point.
        """
        # for a system connection point, reference the other connection points
        if isinstance(other, SystemConnectionPoint):
            if not other._maps_to:
                raise RuntimeError(f"system connection point unmapped: {other}")
            for other_connection_point in other._maps_to:
                self < other_connection_point
            return

        if not isinstance(other, ConnectionPoint):
            raise TypeError("connection point expected")
        # if isinstance(self, SystemInletConnectionPoint) and not isinstance(other, InletConnectionPoint):
        #     raise TypeError(f"inlet connection point expected: {other}")
        # if isinstance(self, SystemOutletConnectionPoint) and not isinstance(other, OutletConnectionPoint):
        #     raise TypeError(f"outlet connection point expected: {other}")

        # make sure they aren't already connected
        if self.connectsThrough:
            raise RuntimeError(
                f"already connected: {self} connects through {self.connectsThrough}"
            )
        if other.connectsThrough:
            raise RuntimeError(
                f"already connected: {other} connects through {other.connectsThrough}"
            )

        data_graph_add((self.node, c223.mapsTo, other.node))
        self._maps_to.add(other)

        return other

    def __rshift__(
        self, other: Any
    ) -> Union[Connection, ConnectionPoint, Device, SystemConnectionPoint, System]:
        """self >> other

        Build a connection from this system connection point to ...
        """

        self_substance: str
        other_substance: str

        if isinstance(other, Connection):
            self_substance = getattr(self, "substance", None)
            other_substance = getattr(other, "substance", None)
            if self_substance != other_substance:
                raise TypeError("connection point type")

            logging.info(f"connection: {self} >> {other}")
            if self.connectsThrough:
                raise RuntimeError(
                    f"already connected: {self} connects through {self.connectsThrough}"
                )

            # link it up, includes mapped connection points
            other << self

        elif isinstance(other, (ConnectionPoint, SystemConnectionPoint)):
            # check the direction
            if isinstance(other, (OutletConnectionPoint, SystemOutletConnectionPoint)):
                raise TypeError(
                    f"connection point direction: {other} is an outlet connection point"
                )

            # check the connection type
            self_substance = getattr(self, "substance", None)
            other_substance = getattr(other, "substance", None)
            if self_substance != other_substance:
                raise TypeError(
                    "connection point type: "
                    f"{self_substance!r} != {other_substance!r}"
                )

            # make sure they aren't already connected
            if self.connectsThrough:
                raise RuntimeError(
                    f"already connected: {self} connects through {self.connectsThrough}"
                )
            if other.connectsThrough:
                raise RuntimeError(
                    f"already connected: {other} connects through {other.connectsThrough}"
                )

            # make a new connection
            new_connection = substance_classes[self_substance]()
            logging.info(f"connection: {self} >> {new_connection} >> {other}")

            # link it up, includes mapped connection points
            new_connection << self
            new_connection >> other

        elif isinstance(other, (Device, System)):
            # check the connection type
            self_substance = getattr(self, "substance", None)

            to_in = set()
            for attr, connection_point in other._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(
                    connection_point, (InletConnectionPoint, SystemInletConnectionPoint)
                ):
                    continue

                substance = getattr(connection_point, "substance", None)
                if substance != self_substance:
                    continue

                to_in.add(connection_point)

            if not to_in:
                raise RuntimeError(f"no candidate destinations from {self} to {other}")
            if len(to_in) > 1:
                raise RuntimeError(
                    "too many candidate destinations from {self} to {other}"
                )
            to_connection_point = to_in.pop()

            # make a new connection
            new_connection = substance_classes[self_substance]()
            logging.info(
                f"connection: {self} >> {new_connection} >> {to_connection_point}"
            )

            # link it up
            new_connection << self
            new_connection >> other

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

        # for chaining
        return other

    def __lshift__(
        self, other: Any
    ) -> Union[Connection, ConnectionPoint, Device, SystemConnectionPoint, System]:
        """self << other

        Build a connection to this connection point from a connection or
        another connection point.
        """

        self_substance: str
        other_substance: str

        if isinstance(other, Connection):
            self_substance = getattr(self, "substance", None)
            other_substance = getattr(other, "substance", None)
            if self_substance != other_substance:
                raise TypeError("connection point type")

            logging.info(f"connection: {other} >> {self}")
            if self.connectsThrough:
                raise RuntimeError(
                    f"already connected: {self} connects through {self.connectsThrough}"
                )

            # link connection to connection point and back
            self.connectsThrough = other
            data_graph_add((other.node, c223.connectsAt, self.node))

            # link the connection points "owner" to the connection
            data_graph_add(
                (
                    self.isConnectionPointOf.node,
                    c223.connectedThrough,
                    other.node,
                )
            )
            data_graph_add(
                (
                    other.node,
                    c223.connectsTo,
                    self.isConnectionPointOf.node,
                )
            )

        elif isinstance(other, (ConnectionPoint, SystemConnectionPoint)):
            # check the direction
            if isinstance(other, (InletConnectionPoint, SystemInletConnectionPoint)):
                raise TypeError(
                    f"connection point direction: {other} is an inlet connection point"
                )

            # check the connection type
            self_substance = getattr(self, "substance", None)
            other_substance = getattr(other, "substance", None)
            if self_substance != other_substance:
                raise TypeError(
                    "connection point type: "
                    f"{self_substance!r} != {other_substance!r}"
                )

            # make sure they aren't already connected
            if self.connectsThrough:
                raise RuntimeError(
                    f"already connected: {self} connects through {self.connectsThrough}"
                )
            if other.connectsThrough:
                raise RuntimeError(
                    f"already connected: {other} connects through {other.connectsThrough}"
                )

            # make a new connection
            new_connection = substance_classes[self_substance]()
            logging.info(f"connection: {other} >> {new_connection} >> {self}")

            # link it up
            new_connection << other
            new_connection >> self

        elif isinstance(other, (Device, System)):
            # check the connection type
            self_substance = getattr(self, "substance", None)

            from_out = set()
            for attr, connection_point in other._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(
                    connection_point,
                    (OutletConnectionPoint, SystemOutletConnectionPoint),
                ):
                    continue

                substance = getattr(connection_point, "substance", None)
                if substance != self_substance:
                    continue

                from_out.add(connection_point)

            if not from_out:
                raise RuntimeError(f"no candidate sources from {other} to {self}")
            if len(from_out) > 1:
                raise RuntimeError("too many candidate sources from {other} to {self}")
            from_connection_point = from_out.pop()

            # make a new connection
            new_connection = substance_classes[self_substance]()
            logging.info(
                f"connection: {from_connection_point} >> {new_connection} >> {self}"
            )

            # link it up
            new_connection << from_connection_point
            new_connection >> self

        else:
            raise TypeError(f"{self!r} connection from {other!r}")

        # for chaining
        return other


class SystemInletConnectionPoint(SystemConnectionPoint):
    pass


class SystemOutletConnectionPoint(SystemConnectionPoint):
    pass


class System(Node):
    """"""

    _connection_points: Dict[str, SystemConnectionPoint]

    def __init__(self, **kwargs: Any) -> None:
        logging.debug(f"System.__init__ {kwargs}")
        super().__init__(**kwargs)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        # <self> a System
        data_graph_add((self.node, RDF.type, c223.System))

        # merge the annotations
        merged_annotations = {}
        for cls in reversed(self.__class__.__mro__[:-1]):
            merged_annotations.update(cls.__annotations__)

        # instantiate and associate all of the system connection points
        self._connection_points = {}
        for var_name, var_annotation in merged_annotations.items():
            if var_name.startswith("_"):
                continue

            if isinstance(var_annotation, str):
                if var_annotation not in _annotation_forwards:
                    logging.debug(
                        f"resolving {var_annotation!r} for attribute {var_name!r}, class not found"
                    )
                    continue
                var_annotation = _annotation_forwards.get(var_annotation)

            if issubclass(var_annotation, ConnectionPoint):
                raise TypeError(
                    f"connection point {var_name}: must be a system connection point"
                )
            if not issubclass(var_annotation, SystemConnectionPoint):
                continue

            # build an instance of this connection point
            var_element = var_annotation(self, label=self.label + "." + var_name)
            self._connection_points[var_name] = var_element
            logging.debug(f"    - connection point {var_name}: {var_element}")

            setattr(self, var_name, var_element)

    @staticmethod
    def join_system(from_system: System, to_system: System) -> None:
        """Find an unambiguous way to connect <from_system> to <to_system>"""
        logging.info(f"join from {from_system} to {to_system}")

        from_out = defaultdict(set)
        for attr, system_connection_point in from_system._connection_points.items():
            if system_connection_point.connectsThrough:
                continue
            if not isinstance(system_connection_point, SystemOutletConnectionPoint):
                continue

            substance = getattr(system_connection_point, "substance", None)
            from_out[substance].add(system_connection_point)

        from_types = set(
            substance for substance in from_out if len(from_out[substance]) == 1
        )
        if not from_types:
            raise RuntimeError(
                f"no candidate sources from {from_system} to {to_system}"
            )

        to_in = defaultdict(set)
        for attr, system_connection_point in to_system._connection_points.items():
            if system_connection_point.connectsThrough:
                continue
            if not isinstance(system_connection_point, SystemInletConnectionPoint):
                continue

            substance = getattr(system_connection_point, "substance", None)
            to_in[substance].add(system_connection_point)

        to_types = set(substance for substance in to_in if len(to_in[substance]) == 1)
        if not to_types:
            raise RuntimeError(
                f"no candidate destinations from {from_system} to {to_system}"
            )

        # find the connection type that has one unconnected <from> and
        # one unconnected <to>
        common_types = from_types.intersection(to_types)
        if not common_types:
            raise RuntimeError("no common connection types")
        if len(common_types) > 1:
            raise RuntimeError("too many common connection types")

        # get the connection type and the connection points
        substance = common_types.pop()
        from_system_connection_point = from_out[substance].pop()
        to_system_connection_point = to_in[substance].pop()

        # make a new connection
        new_connection = substance_classes[substance]()
        logging.info(
            f"connection: {from_system_connection_point} >> {new_connection} >> {to_system_connection_point}"
        )

        # link it up
        new_connection << from_system_connection_point
        new_connection >> to_system_connection_point

    def __gt__(self, other: Node) -> Node:
        """self > other

        Build a subsystem heirarchy, the other system is a subsystem of
        this system.
        """
        logging.debug(f"__gt__ {self} {other}")

        if isinstance(other, (Device, System)):
            data_graph_add((self.node, c223.contains, other.node))
            data_graph_add((other.node, c223.isContainedIn, self.node))
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
            data_graph_add((self.node, c223.isContainedIn, other.node))
            data_graph_add((other.node, c223.contains, self.node))
        else:
            raise TypeError("system expected")

        return other

    def __rshift__(self, other: Any) -> Any:
        """self >> other

        Build a connection from this system to ...
        """
        logging.debug(f"__rshift__ {self} {other}")

        if isinstance(other, System):
            self.join_system(self, other)
        elif isinstance(other, Device):
            from_out = defaultdict(set)
            for attr, connection_point in self._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(connection_point, SystemOutletConnectionPoint):
                    continue

                substance = getattr(connection_point, "substance", None)
                from_out[substance].add(connection_point)

            from_types = set(
                substance for substance in from_out if len(from_out[substance]) == 1
            )
            if not from_types:
                raise RuntimeError(f"no candidate sources from {self} to {other}")

            to_in = defaultdict(set)
            for attr, connection_point in other._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(connection_point, InletConnectionPoint):
                    continue

                substance = getattr(connection_point, "substance", None)
                to_in[substance].add(connection_point)

            to_types = set(
                substance for substance in to_in if len(to_in[substance]) == 1
            )
            if not to_types:
                raise RuntimeError(f"no candidate destinations from {self} to {other}")

            # find the connection type that has one unconnected <from> and
            # one unconnected <to>
            common_types = from_types.intersection(to_types)
            if not common_types:
                raise RuntimeError("no common connection types")
            if len(common_types) > 1:
                raise RuntimeError("too many common connection types")

            substance = common_types.pop()
            from_connection_point = from_out[substance].pop()
            to_connection_point = to_in[substance].pop()

            # make a new connection
            new_connection = substance_classes[substance]()
            logging.info(
                f"connection: {from_connection_point} >> {new_connection} >> {to_connection_point}"
            )

            # link it up
            new_connection << from_connection_point
            new_connection >> to_connection_point

        elif isinstance(other, Connection):
            other << self

        else:
            raise NotImplementedError(f"from {self} to {other}")

        return other

    def __lshift__(self, other: Any) -> Any:
        """self << other

        Build a connection to this system from ...
        """
        logging.debug(f"__lshift__ {self} {other}")

        if isinstance(other, System):
            self.join_system(other, self)
        elif isinstance(other, Device):
            from_out = defaultdict(set)
            for attr, connection_point in other._connection_points.items():
                # print(f"*** {attr!r}: {connection_point}")
                if connection_point.connectsThrough:
                    # print("***     - connected")
                    continue
                if not isinstance(connection_point, OutletConnectionPoint):
                    # print("***     - not an outlet")
                    continue

                substance = getattr(connection_point, "substance", None)
                from_out[substance].add(connection_point)

            # print(f"*** from_out: {from_out}")
            from_types = set(
                substance for substance in from_out if len(from_out[substance]) == 1
            )
            if not from_types:
                raise RuntimeError(f"no candidate sources from {other} to {self}")

            to_in = defaultdict(set)
            for attr, connection_point in self._connection_points.items():
                if connection_point.connectsThrough:
                    continue
                if not isinstance(connection_point, SystemInletConnectionPoint):
                    continue

                substance = getattr(connection_point, "substance", None)
                to_in[substance].add(connection_point)

            to_types = set(
                substance for substance in to_in if len(to_in[substance]) == 1
            )
            if not to_types:
                raise RuntimeError(f"no candidate destinations from {other} to {self}")

            # find the connection type that has one unconnected <from> and
            # one unconnected <to>
            common_types = from_types.intersection(to_types)
            if not common_types:
                raise RuntimeError("no common connection types")
            if len(common_types) > 1:
                raise RuntimeError("too many common connection types")

            substance = common_types.pop()
            from_connection_point = from_out[substance].pop()
            to_connection_point = to_in[substance].pop()

            # make a new connection
            new_connection = substance_classes[substance]()
            logging.info(
                f"connection: {from_connection_point} >> {new_connection} >> {to_connection_point}"
            )

            # link it up
            new_connection << from_connection_point
            new_connection >> to_connection_point

        elif isinstance(other, Connection):
            other >> self

        else:
            raise NotImplementedError(f"from {other} to {self}")

        return other


class Part(Node):
    """"""

    node_type: URIRef = c223.Part

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # <self> a Part
        data_graph_add((self.node, RDF.type, c223.Part))

    def __gt__(self, other: Node) -> Node:
        """self > other

        Build a part heirarchy, the other system is a direct part of
        this system.
        """
        if not isinstance(other, (Device, Part)):
            raise ValueError("device or part expected")

        data_graph_add((self.node, c223.contains, other.node))
        data_graph_add((other.node, c223.isContainedIn, self.node))
        return self

    def __lt__(self, other: Node) -> Node:
        """self < other

        Build a part heirarchy, this part is a direct part of the other part.
        """
        if not isinstance(other, (Device, Part)):
            raise ValueError("device or part expected")

        data_graph_add((self.node, c223.isContainedIn, other.node))
        data_graph_add((other.node, c223.contains, self.node))
        return other


class Value(Node):
    """
    Value node with the option to pass a value that gets turned into a
    Literal.  The 'lang' and 'datatype' values are forwarded to rdflib.
    """

    node_type: URIRef = c223.Value
    isValueOf: Property

    hasTimestamp: Literal
    hasSimpleValue: Literal
    hasUnits: URIRef

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

        super().__init__(**kwargs)

        # <self> a Value
        data_graph_add((self.node, RDF.type, c223.Value))


class Property(Node):
    """"""

    node_type: URIRef = c223.Property
    hasValue: Value

    # override this for a specialize subclass
    _value_class: type = Value

    def __init__(self, arg: Any = None, **kwargs: Any):
        logging.debug(f"Property.__init__ {arg!r} {kwargs}")
        init_value = None
        if arg is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = arg

        super().__init__(**kwargs)

        # <self> a Property
        data_graph_add((self.node, RDF.type, c223.Property))

        # if there is an initial value, add/create and link to it
        if init_value is not None:
            if not isinstance(init_value, Value):
                init_value = self._value_class(init_value)

            # link the two together
            self.hasValue = init_value
            init_value.isValueOf = self

    def add_value(self, value: Value) -> Value:
        """Add an additional value to a property, returns the value added."""
        assert isinstance(value, Value)

        # link the two together
        data_graph_add((self.node, c223.hasValue, value.node))
        value.isValueOf = self

        return value


class ActuatableProperty(Property):
    """
    Such as the setting of a switch.
    """

    node_type: URIRef = c223.ActuatableProperty


class ObservableProperty(Property):
    """
    Such as the state of an alarm detector.
    """

    node_type: URIRef = c223.ObservableProperty


class QuantifiableProperty(Property):
    """"""

    node_type: URIRef = c223.QuantifiableProperty
    hasQuantityKind: URIRef
    hasUnits: URIRef

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # <self> a QuantifiableProperty
        data_graph_add((self.node, RDF.type, c223.QuantifiableProperty))


class QuantifiableActuatableProperty(QuantifiableProperty, ActuatableProperty):
    """
    Such as a numerical setpoint.
    """

    node_type: URIRef = c223.QuantifiableActuatableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # <self> a QuantifiableActuatableProperty
        data_graph_add((self.node, RDF.type, c223.QuantifiableActuatableProperty))


class QuantifiableObservableProperty(QuantifiableProperty, ObservableProperty):
    """
    Such as a temperature reading.
    """

    node_type: URIRef = c223.QuantifiableObservableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # <self> a QuantifiableObservableProperty
        data_graph_add((self.node, RDF.type, c223.QuantifiableObservableProperty))


def dump(
    graph: Graph = data_graph, file: TextIO = sys.stdout, format: str = "turtle"
) -> None:
    file.write(graph.serialize(format=format).decode())


def clear(graph: Graph = data_graph) -> None:
    """Remove all the triples from the graph."""
    graph.remove((None, None, None))
