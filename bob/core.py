"""
Bob the SI-WG Builder
"""

from __future__ import annotations

import sys
import inspect
from collections import defaultdict

from typing import Dict, Any, TextIO, Tuple, Type, TypeVar, Union, cast

from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD  # type: ignore

# options
MANDITORY_LABEL = True
EXPLICIT_CORE_TYPES = True

# globals
g = Graph()
_next_node = 1

# cleanup annotation references, i.e. "System" to _nodes[attr] = System
NodeMap = Dict[str, Union[type, str]]
_annotation_forwards: Dict[str, type] = {}

# these are string annotations
_annotation_forwards["URIRef"] = URIRef
_annotation_forwards["BNode"] = BNode
_annotation_forwards["Literal"] = Literal


def bind_namespace(prefix: str, uri: str) -> Namespace:
    """
    Create a Namespace and bind a prefix to it in the graph.
    """
    namespace = Namespace(uri)
    g.namespace_manager.bind(prefix, URIRef(uri))
    return namespace


# common namespaces
c223 = bind_namespace("c223", "http://data.ashrae.org/standard223/1.0/model/core#")
qudt = bind_namespace("qudt", "http://qudt.org/schema/qudt/")
quantitykind = bind_namespace("quantitykind", "http://qudt.org/vocab/quantitykind/")
brick = bind_namespace("brick", "https://brickschema.org/schema/1.1.0/Brick#")

# the namespace for a node is defined in the node as the _namespace attribute,
# or in its module as the __namespace__ special global, and if it's not one
# of those two, it inherits the namespace from its superclass
__namespace__ = c223

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


# connection type (air, etc) to connection classes
connection_classes: Dict[str, Any] = {}


T = TypeVar("T")


def register_connection_type(connection_class: Type[T]) -> Type[T]:
    """
    Register a connection type so that the connection operators can line up the
    correct types.
    """
    connection_type: str = connection_class.connection_type  # type: ignore[attr-defined]
    connection_classes[connection_type] = connection_class
    return connection_class


class NodeMetaclass(type):
    def __new__(
        cls: Any,
        clsname: str,
        superclasses: Tuple[type, ...],
        attributedict: Dict[str, Any],
    ) -> NodeMetaclass:
        # do this for every subclass of Node

        # start with empty maps
        _nodes: NodeMap = {}
        _datatypes: Dict[str, Literal] = {}
        _inits: Dict[str, Any] = {}

        # include the maps this class is inheriting
        for supercls in reversed(superclasses):
            if hasattr(supercls, "_nodes"):
                _nodes.update(supercls._nodes)  # type: ignore[attr-defined]
            if hasattr(supercls, "_datatypes"):
                _datatypes.update(supercls._datatypes)  # type: ignore[attr-defined]
            if hasattr(supercls, "_inits"):
                _inits.update(supercls._inits)  # type: ignore[attr-defined]

        # pick up the attributes defined by annotations
        annotations = attributedict.get("__annotations__", {})
        for attr, attr_type in annotations.items():
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
            elif isinstance(attr_type, str):
                if attr_type in _annotation_forwards:
                    attr_type = _annotation_forwards[attr_type]
                else:
                    _annotation_forwards[attr_type] = None  # type: ignore[assignment]
                _nodes[attr] = attr_type
            else:
                raise ValueError(f"unknown annotation for {attr}: {attr_type}")

        # look for initializers like hasUnit = QUDT.DEG_F
        for attr, value in attributedict.items():
            if attr.startswith("_"):
                continue

            if attr in _nodes:
                if isinstance(value, cast(type, _nodes[attr])):
                    _inits[attr] = value
                else:
                    raise TypeError(f"initializing {attr}: {_inits[attr]} expected")

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

        # add these special attributes to the class before building it
        attributedict["_nodes"] = _nodes
        attributedict["_datatypes"] = _datatypes
        attributedict["_inits"] = _inits

        # build the class
        metaclass = cast(
            NodeMetaclass,
            super(NodeMetaclass, cls).__new__(
                cls, clsname, superclasses, attributedict
            ),
        )

        # find the namespace in the class definition
        if "_namespace" in attributedict:
            _namespace = attributedict["_namespace"]
        else:
            # check the module
            cls_module = inspect.getmodule(metaclass)
            _namespace = getattr(cls_module, "__namespace__", None)
            if not _namespace:
                # check the superclasses
                for supercls in superclasses:
                    _namespace = getattr(supercls, "_namespace", None)
                    if _namespace:
                        break
                else:
                    raise AttributeError(f"namespace not found: {clsname}")

            metaclass._namespace = _namespace  # type: ignore[attr-defined]

        # make sure it has a type
        if "node_type" not in attributedict:
            metaclass.node_type = _namespace[clsname]  # type: ignore[attr-defined]

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

    def __init__(self, *, label: str = "", **kwargs: Any) -> None:
        global _next_node, model_namespace

        if model_namespace:
            self.node = model_namespace[f"{_next_node:05d}"]
            _next_node += 1
        else:
            self.node = BNode()

        self.label = label or getattr(self, "label", "")
        if self.label:
            g.add((self.node, RDFS.label, Literal(self.label)))

        if hasattr(self, "node_type"):
            g.add((self.node, RDF.type, self.node_type))

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
        """
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

            # break the reference to the current child node
            # g.remove((self.node, self._namespace[attr], None))

            # add the link(s)
            if isinstance(value, (URIRef, Literal)):
                g.add((self.node, self._namespace[attr], value))
            if isinstance(value, Node):
                g.add((self.node, self._namespace[attr], value.node))

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
            g.add((self.node, self._namespace[attr], value))

        # carry on
        super().__setattr__(attr, value)

    def __repr__(self) -> str:
        label = (" " + self.label) if self.label else ""
        return f"<{self.__class__.__name__}{label} at {self.node}>"

    def add_property(self, prop: Property) -> None:
        """Add a property to a node."""
        assert isinstance(prop, Property)

        # link the two together
        g.add((self.node, c223.hasProperty, prop.node))
        g.add((prop.node, c223.isPropertyOf, self.node))


class ConnectionType:
    connection_type: str = ""  # unrestricted by default


@register_connection_type
class Connection(Node, ConnectionType):
    """
    Generic connection object type, unrestricted.
    """

    node_type: URIRef = c223.Connection

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if EXPLICIT_CORE_TYPES:
            if self.connection_type:
                connection_type = self.connection_type + "Connection"
                g.add((self.node, RDF.type, self._namespace[connection_type],))

    def __rshift__(self, other: Union[ConnectionPoint, Connectable]) -> Union[ConnectionPoint, Connectable]:
        """self >> other"""

        # look for unconnected connection points for this connection type
        unbound_connection_points = set()

        if isinstance(other, ConnectionPoint):
            if other.connectsThrough:
                raise RuntimeError(f"already connected: {other!r}")

            # check the connection direction
            #@ if isinstance(other, Outlet):
            #@     raise TypeError("connection point direction")

            other_connection_type = getattr(other, "connection_type", "")
            if other_connection_type != self.connection_type:
                raise TypeError("connection type")

            # this is a candidate
            unbound_connection_points.add(other)

        elif isinstance(other, Connectable):
            for (
                connection_point_name,
                connection_point,
            ) in other._connection_points.items():
                # check the connection direction
                if isinstance(connection_point, Outlet):
                    continue
                # the connection point must not be already connected
                if connection_point.connectsThrough:
                    continue

                # the connection type needs to match
                connection_point_type = getattr(connection_point, "connection_type", "")
                if connection_point_type != self.connection_type:
                    continue

                # this is a candidate
                unbound_connection_points.add(connection_point)

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

        if not unbound_connection_points:
            raise RuntimeError(f"no unbound connection points: {other!r}")
        if len(unbound_connection_points) > 1:
            raise RuntimeError(f"multiple unbound connection points: {other!r}")

        connection_point = unbound_connection_points.pop()

        # link connection to connection point and back
        g.add((self.node, c223.connectsAt, connection_point.node))
        connection_point.connectsThrough = self

        # link the connection to the device of the connection point
        g.add(
            (
                connection_point.isConnectionPointOf.node,
                c223.connectedThrough,
                self.node,
            )
        )
        g.add((self.node, c223.connectsTo, connection_point.isConnectionPointOf.node))

        # for chaining
        return other

    def __lshift__(self, other: Union[ConnectionPoint, Connectable]) -> Union[ConnectionPoint, Connectable]:
        """self << other"""

        # look for <system> unconnected connection points for this connection type
        unbound_connection_points = set()

        if isinstance(other, ConnectionPoint):
            if other.connectsThrough:
                raise RuntimeError(f"already connected: {other!r}")

            # check the connection direction
            #@ if isinstance(other, Inlet):
            #@     raise TypeError("connection point direction")

            other_connection_type = getattr(other, "connection_type", "")
            if other_connection_type != self.connection_type:
                raise TypeError("connection type")

            # this is a candidate
            unbound_connection_points.add(other)

        elif isinstance(other, Connectable):
            for (
                connection_point_name,
                connection_point,
            ) in other._connection_points.items():
                # check the connection direction
                if isinstance(connection_point, Inlet):
                    continue

                connection_point_type = getattr(connection_point, "connection_type", "")

                # the connection type needs to match
                if connection_point_type != self.connection_type:
                    continue
                # the connection point must not be already connected
                if connection_point.connectsThrough:
                    continue

                # this is a candidate
                unbound_connection_points.add(connection_point)

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

        if not unbound_connection_points:
            raise RuntimeError(f"no unbound connection points: {other!r}")
        if len(unbound_connection_points) > 1:
            raise RuntimeError(f"multiple unbound connection points: {other!r}")

        connection_point = unbound_connection_points.pop()

        # link connection to connection point and back
        g.add((self.node, c223.connectsAt, connection_point.node))
        connection_point.connectsThrough = self

        # link the connection to the "owner" of the connection point
        g.add(
            (
                connection_point.isConnectionPointOf.node,
                c223.connectedThrough,
                self.node,
            )
        )
        g.add(
            (self.node, c223.connectsFrom, connection_point.isConnectionPointOf.node,)
        )

        # for chaining
        return other


    def __repr__(self) -> str:
        xid = id(self)
        if xid < 0:
            xid += 1 << 32
        sname = self.__module__ + "." + self.__class__.__name__
        return f"<{sname} instance at 0x{xid:08x}>"


class ConnectionPoint(Node):
    node_type: URIRef = c223.ConnectionPoint

    connectsThrough: Connection
    isConnectionPointOf: Connectable

    def __init__(self, connectable: Connectable, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if EXPLICIT_CORE_TYPES:
            if isinstance(self, ConnectionType) and self.connection_type:
                connection_point_type = self.connection_type + "ConnectionPoint"
                g.add((self.node, RDF.type, self._namespace[connection_point_type],))

        g.add((connectable.node, c223.hasConnectionPoint, self.node))
        self.isConnectionPointOf = connectable

    def __rshift__(self, other: Any) -> Union[Connection, ConnectionPoint]:
        """self >> other

        Build a connection from the connection point to a connection or
        another connection point.
        """

        #@ pass through connection points?
        #@ if self.connectsThrough:
        #@     raise RuntimeError(f"already connected: {self!r}")
        #@ if isinstance(self, Inlet):
        #@     raise RuntimeError("connection point direction")

        self_connection_type: str
        other_connection_type: str

        if isinstance(other, Connection):
            self_connection_type = getattr(self, "connection_type", "")
            if self_connection_type != other.connection_type:
                raise TypeError("connection point type")

            # link connection to connection point and back
            #@ self.connectsThrough = other
            g.add((other.node, c223.connectsAt, self.node))

            # link the connection points "owner" to the connection
            g.add((self.isConnectionPointOf.node, c223.connectedThrough, other.node,))
            g.add((other.node, c223.connectsFrom, self.isConnectionPointOf.node,))

            # for chaining
            return other

        elif isinstance(other, ConnectionPoint):
            if isinstance(other, Outlet):
                raise RuntimeError("connection point direction")

            self_connection_type = getattr(self, "connection_type", "")
            other_connection_type = getattr(other, "connection_type", "")
            if self_connection_type != other_connection_type:
                raise TypeError(
                    "connection point type: "
                    f"{self_connection_type!r} != {other_connection_type!r}"
                )

            if other.connectsThrough:
                raise RuntimeError(f"already connected: {other!r}")

            new_connection = connection_classes[self_connection_type]()

            # link it up
            new_connection << self
            new_connection >> other

            # for chaining
            return other

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

    def __lshift__(self, other: Any) -> Union[Connection, ConnectionPoint]:
        """self << other

        Build a connection to this connection point from a connection or
        another connection point.
        """

        #@ pass through connection points?
        #@ if self.connectsThrough:
        #@     raise RuntimeError(f"already connected: {self!r}")
        #@ if isinstance(self, Outlet):
        #@     raise RuntimeError("connection point direction")

        if isinstance(other, Connection):
            self_connection_type = getattr(self, "connection_type", "")
            if self_connection_type != other.connection_type:
                raise TypeError("connection point type")

            # link connection to connection point and back
            #@ self.connectsThrough = other
            g.add((other.node, c223.connectsAt, self.node))

            # link the connection points "owner" to the connection
            g.add((self.isConnectionPointOf.node, c223.connectedThrough, other.node,))
            g.add((other.node, c223.connectsTo, self.isConnectionPointOf.node,))

            # for chaining
            return other

        elif isinstance(other, ConnectionPoint):
            if isinstance(other, Inlet):
                raise RuntimeError("connection point direction")

            self_connection_type = getattr(self, "connection_type", "")
            other_connection_type = getattr(other, "connection_type", "")
            if self_connection_type != other_connection_type:
                raise TypeError(
                    "connection point type: "
                    f"{self_connection_type!r} != {other_connection_type!r}"
                )

            if other.connectsThrough:
                raise RuntimeError(f"already connected: {other!r}")

            new_connection = connection_classes[self_connection_type]()

            # link it up
            new_connection << other
            new_connection >> self

            # for chaining
            return other

        else:
            raise TypeError(f"{self!r} connection to {other!r}")


class Inlet(ConnectionPoint):
    pass


class Outlet(ConnectionPoint):
    pass


class Connectable(Node):
    """
    A type of thing that can has connection points.
    """

    node_type: URIRef = c223.Device
    _connection_points: Dict[str, ConnectionPoint]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        # <self> a Device
        if EXPLICIT_CORE_TYPES:
            g.add((self.node, RDF.type, c223.Connectable))

        # <self> a something
        g.add((self.node, RDF.type, self._namespace[self.__class__.__name__]))

        # instantiate and associate all of the connection points
        self._connection_points = {}
        for var_name, var_annotation in self.__annotations__.items():
            if var_name.startswith("_"):
                continue

            if isinstance(var_annotation, str):
                if var_annotation not in _annotation_forwards:
                    raise NotImplementedError(
                        f"resolving {var_annotation!r} for attribute {attr!r}, class not found"
                    )

                var_annotation = _annotation_forwards.get(var_annotation)
            if not issubclass(var_annotation, ConnectionPoint):
                # print(f"    not a subclass of ConnectionPoint")
                continue

            # build an instance of this connection point
            var_element = var_annotation(self, label=self.label + "." + var_name)
            self._connection_points[var_name] = var_element

            setattr(self, var_name, var_element)

    def add_connection_point(self, connection_point: ConnectionPoint) -> None:
        """Add a connection point."""
        assert isinstance(prop, ConnectionPoint)

        # link the two together
        connection_point.isConnectionPointOf = self
        g.add((self.node, c223.hasConnectionPoint, connection_point.node))

        # this connection point doesn't have a usual name, but this key
        # will be unique (so it will not step on any other points) and
        # it is not exposed as a label in the graph
        self._connection_points[connection_point.node] = connection_point

    @staticmethod
    def join_things(from_thing: Connectable, to_thing: Connectable) -> None:
        """Find an unambiguous way to connect <from> to <to>"""

        # print(f"{from_thing} join to {to_thing}")
        # print(f"    connection points: {from_thing._connection_points}")

        from_out = defaultdict(list)
        for attr, connection_point in from_thing._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, Outlet):
                continue

            connection_type = getattr(connection_point, "connection_type", "")
            from_out[connection_type].append(connection_point)

        # print(f"    from out {from_out}")

        from_types = set(
            connection_type
            for connection_type in from_out
            if len(from_out[connection_type]) == 1
        )
        if not from_types:
            raise RuntimeError(f"no candidate sources: {from_thing!r}")

        to_in = defaultdict(list)
        for attr, connection_point in to_thing._connection_points.items():
            if connection_point.connectsThrough:
                continue
            if not isinstance(connection_point, Inlet):
                continue

            connection_type = getattr(connection_point, "connection_type", "")
            to_in[connection_type].append(connection_point)

        # print(f"    to in {to_in}")

        to_types = set(
            connection_type
            for connection_type in to_in
            if len(to_in[connection_type]) == 1
        )
        if not to_types:
            raise RuntimeError(f"no candidate destinations: {to_thing!r}")

        # find the connection type that has one unconnected <from> and
        # one unconnected <to>
        common_types = from_types.intersection(to_types)
        if not common_types:
            raise RuntimeError("no common connection points")
        if len(common_types) > 1:
            raise RuntimeError("too many common types")

        connection_type = common_types.pop()
        from_connection_point = from_out[connection_type][0]
        to_connection_point = to_in[connection_type][0]

        # build the connection
        from_connection_point >> to_connection_point

    def __rshift__(self, other: Connectable) -> Connectable:
        """self >> other

        Build a connection from this thing to another connectable thing.
        """

        if isinstance(other, Connectable):
            self.join_things(self, other)
        elif isinstance(other, Connection):
            other << self
        else:
            raise TypeError(repr(other))

        return other

    def __lshift__(self, other: Connectable) -> Connectable:
        """self << other

        Build a connection to this thing from another connectable thing.
        """

        if isinstance(other, Connectable):
            self.join_things(other, self)
        elif isinstance(other, Connection):
            other >> self
        else:
            raise TypeError(repr(other))

        return other


class System(Connectable):
    """
    """

    _connection_points: Dict[str, Any]

    def __init__(self, **kwargs: Any) -> None:
        """
        """
        super().__init__(**kwargs)

        # <self> a System
        if EXPLICIT_CORE_TYPES:
            g.add((self.node, RDF.type, c223.System))

    def __gt__(self, other: Node) -> Node:
        """self > other

        Build a subsystem heirarchy, the other system is a subsystem of
        this system.
        """
        if isinstance(other, System):
            g.add((self.node, c223.hasSubsystem, other.node))
            g.add((other.node, c223.isSubsystemOf, self.node))
        elif isinstance(other, Device):
            g.add((self.node, c223.hasDevice, other.node))
            g.add((other.node, c223.isDeviceOf, self.node))
        else:
            raise TypeError("system or device expected")

        return self

    def __lt__(self, other: Node) -> Node:
        """self < other

        Build a subsystem heirarchy, this is a subsystem of some other
        system.
        """
        if isinstance(other, System):
            g.add((self.node, c223.isSubsystemOf, other.node))
            g.add((other.node, c223.hasSubsystem, self.node))
        else:
            raise TypeError("system expected")

        return other


class Device(Connectable):
    """
    Devices are connectable.
    """

    node_type: URIRef = c223.Device

    def __init__(self, **kwargs: Any) -> None:
        """
        """
        super().__init__(**kwargs)

        # <self> a System
        if EXPLICIT_CORE_TYPES:
            g.add((self.node, RDF.type, c223.Device))

    def __gt__(self, other: Node) -> Node:
        """self > other

        Build a subsystem heirarchy, the other is a device or a part.
        """
        if isinstance(other, Device):
            g.add((self.node, c223.hasDevice, other.node))
            g.add((other.node, c223.isDeviceOf, self.node))
        elif isinstance(other, Part):
            g.add((self.node, c223.hasPart, other.node))
            g.add((other.node, c223.isPartOf, self.node))
        else:
            raise TypeError("device or part expected")

        return self

    def __lt__(self, other: Node) -> Node:
        """self < other

        Build a subsystem heirarchy, this is a subsystem of some other
        system.
        """
        if isinstance(other, (System, Device)):
            g.add((self.node, c223.isDeviceOf, other.node))
            g.add((other.node, c223.hasDevice, self.node))
        else:
            raise TypeError("system or device expected")

        return other


class Part(Node):
    """
    """

    node_type: URIRef = c223.Part

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # <self> a Part
        if EXPLICIT_CORE_TYPES:
            g.add((self.node, RDF.type, c223.Part))

    def __gt__(self, other: Node) -> Node:
        """self > other

        Build a part heirarchy, the other system is a direct part of
        this system.
        """
        if not isinstance(other, (Device, Part)):
            raise ValueError("device or part expected")

        g.add((self.node, c223.hasPart, other.node))
        g.add((other.node, c223.isPartOf, self.node))
        return self

    def __lt__(self, other: Node) -> Node:
        """self < other

        Build a part heirarchy, this part is a direct part of the other part.
        """
        if not isinstance(other, (Device, Part)):
            raise ValueError("device or part expected")

        g.add((self.node, c223.isPartOf, other.node))
        g.add((other.node, c223.hasPart, self.node))
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
        if EXPLICIT_CORE_TYPES:
            g.add((self.node, RDF.type, c223.Value))


class Property(Node):
    """
    """

    node_type: URIRef = c223.Property
    hasValue: Value

    # override this for a specialize subclass
    _value_class: type = Value

    def __init__(self, arg: Any = None, **kwargs: Any):
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
        if EXPLICIT_CORE_TYPES:
            g.add((self.node, RDF.type, c223.Property))

        # if there is an initial value, add/create and link to it
        if init_value is not None:
            if not isinstance(init_value, Value):
                init_value = self._value_class(init_value)

            # link the two together
            self.hasValue = init_value
            init_value.isValueOf = self

    def add_value(self, value: Value) -> None:
        """Add an additional value to a property."""
        assert isinstance(value, Value)

        # link the two together
        g.add((self.node, c223.hasValue, value.node))
        value.isValueOf = self


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
    """
    """

    node_type: URIRef = c223.QuantifiableProperty
    hasQuantityKind: URIRef
    hasUnits: URIRef

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # <self> a QuantifiableProperty
        if EXPLICIT_CORE_TYPES:
            g.add((self.node, RDF.type, c223.QuantifiableProperty))


class QuantifiableActuatableProperty(QuantifiableProperty, ActuatableProperty):
    """
    Such as a numerical setpoint.
    """

    node_type: URIRef = c223.QuantifiableActuatableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # <self> a QuantifiableActuatableProperty
        if EXPLICIT_CORE_TYPES:
            g.add((self.node, RDF.type, c223.QuantifiableActuatableProperty))


class QuantifiableObservableProperty(QuantifiableProperty, ObservableProperty):
    """
    Such as a temperature reading.
    """

    node_type: URIRef = c223.QuantifiableObservableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # <self> a QuantifiableObservableProperty
        if EXPLICIT_CORE_TYPES:
            g.add((self.node, RDF.type, c223.QuantifiableObservableProperty))


def dump(file: TextIO = sys.stdout, format: str = "turtle") -> None:
    file.write(g.serialize(format=format).decode())


def clear() -> None:
    """Remove all the triples from the graph."""
    g.remove((None, None, None))
