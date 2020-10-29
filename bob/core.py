"""
Bob the SI-WG Builder
"""

import sys
import inspect
from collections import defaultdict

from typing import Dict, Any, List, TextIO, Tuple, Type, TypeVar, Union, cast

from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD  # type: ignore

# options
MANDITORY_LABEL = True

# globals
g = Graph()
document = ""
_next_node = 1

# namespaces
ex = Namespace("urn:ex/")
g.namespace_manager.bind("ex", URIRef("urn:ex/"))

c223 = Namespace("http://data.ashrae.org/standard223/1.0/model/core#")
g.namespace_manager.bind(
    "c223", URIRef("http://data.ashrae.org/standard223/1.0/model/core#")
)

qudt = Namespace("http://qudt.org/schema/qudt/")
g.namespace_manager.bind("qudt", URIRef("http://qudt.org/schema/qudt/"))

quantitykind = Namespace("http://qudt.org/vocab/quantitykind/")
g.namespace_manager.bind("quantitykind", URIRef("http://qudt.org/vocab/quantitykind/"))

s4syst = Namespace("https://saref.etsi.org/")
g.namespace_manager.bind("s4syst", URIRef("https://saref.etsi.org/"))

# brick = Namespace("https://brickschema.org/schema/1.1.0/Brick#")
# g.namespace_manager.bind("brick", URIRef("https://brickschema.org/schema/1.1.0/Brick#"))

# connection type (air, etc) to connection classes
connection_classes: Dict[str, Any] = {}


T = TypeVar("T")

# cleanup annotation references, i.e. "System" to _nodes[attr] = System
NodeMap = Dict[str, Union[type, str]]
_annotation_forwards: Dict[str, List[Tuple[NodeMap, str]]] = defaultdict(list)


def register_connection_type(connection_class: Type[T]) -> Type[T]:
    connection_type: str = connection_class.connection_type  # type: ignore[attr-defined]
    connection_classes[connection_type] = connection_class
    return connection_class


class NodeMetaclass(type):
    def __new__(
        cls: Any,
        clsname: str,
        superclasses: Tuple[type, ...],
        attributedict: Dict[str, Any],
    ) -> "NodeMetaclass":
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
                _nodes[attr] = attr_type
                _annotation_forwards[attr].append((_nodes, attr))
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

            else:
                continue

            _inits[attr] = value

        # add these special attributes to the class before building it
        attributedict["_nodes"] = _nodes
        attributedict["_datatypes"] = _datatypes
        attributedict["_inits"] = _inits

        # make sure it has a type
        if "node_type" not in attributedict:
            attributedict["node_type"] = ex[clsname]

        metaclass = cast(
            NodeMetaclass,
            super(NodeMetaclass, cls).__new__(
                cls, clsname, superclasses, attributedict
            ),
        )

        return metaclass


class Node(metaclass=NodeMetaclass):
    """
    A node in the graph that optionally has a label.  Instances of this
    would be something like blank nodes.
    """

    # assigned by NodeMetaclass
    _nodes: NodeMap
    _datatypes: Dict[str, Literal]
    _inits: Dict[str, Any]

    node: URIRef
    node_type: URIRef
    label: str

    def __init__(self, *, label: str = "", **kwargs: Any) -> None:
        global _next_node

        self.node = ex[f"{_next_node:05d}"]
        _next_node += 1

        self.label = label
        if label:
            g.add((self.node, RDFS.label, Literal(label)))

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
        if attr.startswith("_") or ((attr not in self._nodes) and (attr not in self._datatypes)):
            super().__setattr__(attr, value)
            return

        # make sure the value isn't None, no "deleting" content
        if (value is None):
            raise ValueError(f"{attr}")

        # make sure the current value is None, no "reassigning" content
        current_value = super().__getattribute__(attr)
        if (current_value is not None):
            raise RuntimeError(f"attribute {attr} already has a value")

        # if this is a node, double check the type
        if attr in self._nodes:
            if isinstance(self._nodes[attr], str):
                raise NotImplementedError("get the class for {self._nodes[attr]}")
            node_class = cast(type, self._nodes[attr])

            # pass the value to the class to build one
            if not isinstance(value, node_class):
                value = node_class(value)

            # break the reference to the current child node
            # g.remove((self.node, ex[attr], None))

            # add the link
            if isinstance(value, (URIRef, Literal)):
                g.add((self.node, ex[attr], value))
            elif isinstance(value, Node):
                g.add((self.node, ex[attr], value.node))

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

            # remove the current value
            # g.remove((self.node, ex[attr], None))

            # add the literal
            g.add((self.node, ex[attr], value))

        # carry on
        super().__setattr__(attr, value)

    def __repr__(self) -> str:
        label = (" " + self.label) if self.label else ""
        return f"<{self.__class__.__name__}{label} at {self.node}>"

    def __iand__(self, value: "Property") -> None:
        """Add a property to a node."""
        if not isinstance(value, Property):
            value = Property(value)

        # link the two together
        g.add((self.node, ex.hasProperty, value.node))
        g.add((value.node, ex.isPropertyOf, self.node))


class ConnectionType:
    connection_type: str = ""  # unrestricted by default


@register_connection_type
class Connection(Node, ConnectionType):
    """
    Generic connection object type, unrestricted.
    """

    node_type: URIRef = s4syst.Connection

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if self.connection_type:
            g.add((self.node, RDF.type, ex[self.connection_type + "Connection"]))

    def __rshift__(self, other: Any) -> None:
        """self >> other"""

        if isinstance(other, ConnectionPoint):
            if other.connectedThrough:
                raise RuntimeError(f"already connected: {other!r}")

            # check the connection direction
            if isinstance(other, Outlet):
                raise TypeError("connection point direction")

            other_connection_type = getattr(other, "connection_type", "")
            if other_connection_type != self.connection_type:
                raise TypeError("connection point type")

            # <self> connects system at <other>
            g.add((self.node, s4syst.connectsSystemAt, other.node))

            # <other> connected through <self>
            g.add((other.node, s4syst.connectedThrough, self.node))
            other.connectedThrough = self

        elif isinstance(other, System):
            # look for <system> unconnected connection points for this connection type
            unbound_connection_points = set()
            for (
                connection_point_name,
                connection_point,
            ) in other._connection_points.items():
                # check the connection direction
                if isinstance(connection_point, Outlet):
                    continue

                connection_point_type = getattr(connection_point, "connection_type", "")

                # the connection type needs to match
                if connection_point_type != self.connection_type:
                    continue
                # the connection point must not be already connected
                if connection_point.connectedThrough:
                    continue

                # this is a candidate
                unbound_connection_points.add(connection_point)

            if not unbound_connection_points:
                raise RuntimeError("no unbound connection points: {other!r}")

            connection_point = unbound_connection_points.pop()

            # <self> connects system at <connection_point>
            g.add((self.node, s4syst.connectsSystemAt, connection_point.node))

            # <connection_point> connected through <self>
            g.add((connection_point.node, s4syst.connectedThrough, self.node))
            connection_point.connectedThrough = self

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

    def __lshift__(self, other: Any) -> None:
        """self << other"""

        if isinstance(other, ConnectionPoint):
            if other.connectedThrough:
                raise RuntimeError(f"already connected: {other!r}")

            # check the connection direction
            if isinstance(other, Inlet):
                raise TypeError("connection point direction")

            other_connection_type = getattr(other, "connection_type", "")
            if other_connection_type != self.connection_type:
                raise TypeError("connection point type")

            # <self> connects system at <other>
            g.add((self.node, s4syst.connectsSystemAt, other.node))

            # <other> connected through <self>
            g.add((other.node, s4syst.connectedThrough, self.node))
            other.connectedThrough = self

        elif isinstance(other, System):
            # look for <system> unconnected connection points for this connection type
            unbound_connection_points = set()
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
                if connection_point.connectedThrough:
                    continue

                # this is a candidate
                unbound_connection_points.add(connection_point)

            if not unbound_connection_points:
                raise RuntimeError("no unbound connection points: {other!r}")

            connection_point = unbound_connection_points.pop()

            # <self> connects system at <connection_point>
            g.add((self.node, s4syst.connectsSystemAt, connection_point.node))

            # <connection_point> connected through <self>
            g.add((connection_point.node, s4syst.connectedThrough, self.node))
            connection_point.connectedThrough = self

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

    def __repr__(self) -> str:
        xid = id(self)
        if xid < 0:
            xid += 1 << 32
        sname = self.__module__ + "." + self.__class__.__name__
        return f"<{sname} instance at 0x{xid:08x}>"


class ConnectionPoint(Node):
    node_type: URIRef = s4syst.ConnectionPoint

    connectedThrough: Connection
    connectionPointOf: "System"

    def __init__(self, system: "System", **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # <self> connection point of <system>
        g.add((self.node, s4syst.connectionPointOf, system.node))
        self.connectionPointOf = system

        # <system> connects at <self>
        g.add((system.node, s4syst.connectsAt, self.node))

    def __rshift__(self, other: Any) -> None:
        """self >> other

        Build a connection from the connection point to a connection or
        another connection point.
        """

        if self.connectedThrough:
            raise RuntimeError(f"already connected: {self!r}")
        if isinstance(self, Inlet):
            raise RuntimeError("connection point direction")

        self_connection_type: str
        other_connection_type: str

        if isinstance(other, Connection):
            self_connection_type = getattr(self, "connection_type", "")
            if self_connection_type != other.connection_type:
                raise TypeError("connection point type")

            # <self> connected through <other>
            g.add((self.node, s4syst.connectedThrough, other.node))
            self.connectedThrough = other

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

            if other.connectedThrough:
                raise RuntimeError(f"already connected: {other!r}")

            new_connection = connection_classes[self_connection_type]()
            for connection_point in (self, other):
                # <new_connection> connects system at <connection_point>
                g.add(
                    (
                        new_connection.node,
                        s4syst.connectsSystemAt,
                        connection_point.node,
                    )
                )

                # <connection_point> connected through <new_connection>
                g.add(
                    (
                        connection_point.node,
                        s4syst.connectedThrough,
                        new_connection.node,
                    )
                )
                connection_point.connectedThrough = new_connection

        else:
            raise TypeError(f"{self!r} connection to {other!r}")

    def __lshift__(self, other: Any) -> None:
        """self << other

        Build a connection to the connection point from a connection or
        another connection point.
        """

        if self.connectedThrough:
            raise RuntimeError(f"already connected: {self!r}")
        if isinstance(self, Outlet):
            raise RuntimeError("connection point direction")

        if isinstance(other, Connection):
            self_connection_type = getattr(self, "connection_type", "")
            if self_connection_type != other.connection_type:
                raise TypeError("connection point type")

            # <self> connected through <other>
            g.add((self.node, s4syst.connectedThrough, other.node))
            self.connectedThrough = other

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

            if other.connectedThrough:
                raise RuntimeError(f"already connected: {other!r}")

            new_connection = connection_classes[self_connection_type]()
            for connection_point in (self, other):
                # <new_connection> connects system at <connection_point>
                g.add(
                    (
                        new_connection.node,
                        s4syst.connectsSystemAt,
                        connection_point.node,
                    )
                )

                # <connection_point> connected through <new_connection>
                g.add(
                    (
                        connection_point.node,
                        s4syst.connectedThrough,
                        new_connection.node,
                    )
                )
                connection_point.connectedThrough = new_connection

        else:
            raise TypeError(f"{self!r} connection to {other!r}")


class Inlet(ConnectionPoint):
    pass


class Outlet(ConnectionPoint):
    pass


class System(Node):
    _connection_points: Dict[str, ConnectionPoint]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if MANDITORY_LABEL:
            if "label" not in kwargs:
                raise RuntimeError("no label")
            if not kwargs["label"]:
                raise RuntimeError("empty label")

        # <self> a System
        g.add((self.node, RDF.type, s4syst.System))

        # if there is a brick annotation, refer this instance to that class
        # if self.__annotations__.get("__brick__"):
        #     g.add((self.node, RDF.type, brick[self.__annotations__["__brick__"]]))

        # <self> a something
        g.add((self.node, RDF.type, ex[self.__class__.__name__]))

        self._connection_points = {}
        for var_name, var_annotation in self.__annotations__.items():
            if var_name.startswith("_"):
                continue
            if not issubclass(var_annotation, ConnectionPoint):
                continue

            # build an instance of this connection point
            var_element = var_annotation(self, label=self.label + "." + var_name)
            self._connection_points[var_name] = var_element

            setattr(self, var_name, var_element)

    @staticmethod
    def join_systems(from_system: "System", to_system: "System") -> None:
        """Find an unambiguous way to connect <from> to <to>"""
        from_out = defaultdict(list)
        for connection_point in from_system._connection_points.values():
            if connection_point.connectedThrough:
                continue
            if not isinstance(connection_point, Outlet):
                continue

            connection_type = getattr(connection_point, "connection_type", "")
            from_out[connection_type].append(connection_point)

        from_types = set(
            connection_type
            for connection_type in from_out
            if len(from_out[connection_type]) == 1
        )
        if not from_types:
            raise RuntimeError(f"no candidate sources: {from_system!r}")

        to_in = defaultdict(list)
        for connection_point in to_system._connection_points.values():
            if connection_point.connectedThrough:
                continue
            if not isinstance(connection_point, Inlet):
                continue
            connection_type = getattr(connection_point, "connection_type", "")
            to_in[connection_type].append(connection_point)
        to_types = set(
            connection_type
            for connection_type in to_in
            if len(to_in[connection_type]) == 1
        )
        if not to_types:
            raise RuntimeError(f"no candidate destinations: {to_system!r}")

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

        # add brick:feeds between the systems
        # g.add((from_system.node, brick.feeds, to_system.node))

    def __rshift__(self, other: Any) -> None:
        """self >> other

        Build a connection from this system to another system.
        """

        if isinstance(other, System):
            self.join_systems(self, other)
        elif isinstance(other, Connection):
            other << self
        else:
            raise TypeError(repr(other))

    def __lshift__(self, other: Any) -> None:
        """self << other

        Build a connection to this system from another system.
        """

        if isinstance(other, System):
            self.join_systems(other, self)
        elif isinstance(other, Connection):
            other >> self
        else:
            raise TypeError(repr(other))

    @staticmethod
    def system_heirarchy(system: "System", subsystem: "System") -> None:
        """Connect the two systems in a heirarchy."""
        g.add((system.node, s4syst.hasSubSystem, subsystem.node))
        # g.add((system.node, brick.hasPart, subsystem.node))
        g.add((subsystem.node, s4syst.subSystemOf, system.node))
        # g.add((subsystem.node, brick.isPartOf, system.node))

    def __gt__(self, other: "System") -> "System":
        """self > other

        Build a subsystem heirarchy, the other system is a subsystem of
        this system.
        """

        self.system_heirarchy(self, other)
        return self

    def __lt__(self, other: "System") -> "System":
        """self < other

        Build a subsystem heirarchy, this is a subsystem of some other
        system.
        """

        self.system_heirarchy(other, self)
        return other


class Value(Node):
    """
    """

    node_type: URIRef = ex.Value

    hasTimestamp: Literal
    hasSimpleValue: Literal
    hasUnits: URIRef

    def __init__(self, arg: Any = None, **kwargs: Any):
        if arg is not None:
            if "hasSimpleValue" in kwargs:
                raise RuntimeError("initialization conflict")
            kwargs["hasSimpleValue"] = arg

        super().__init__(**kwargs)


class Property(Node):
    """
    """

    node_type: URIRef = ex.Property
    hasValue: Value
    hasQuantityKind: URIRef

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

        # if there is an initial value, add/create and link to it
        if init_value is not None:
            self += init_value

    def __iadd__(self, value: Any) -> "Property":
        """Add a value to a property."""
        if not isinstance(value, Value):
            value = Value(value)

        # link the two together
        g.add((self.node, ex.hasValue, value.node))
        g.add((value.node, ex.isValueOf, self.node))

        return self

class QuantifiableProperty(Property):
    """
    """

    node_type: URIRef = ex.QuantifiableProperty
    hasQuantityKind: URIRef
    hasUnits: URIRef


class Device(System):
    """
    """

    node_type: URIRef = ex.Device

    def __gt__(self, other: Any) -> "Device":
        """self > other

        Build a subsystem heirarchy, the other system is a subsystem of
        this system.
        """
        if isinstance(other, Part):
            g.add((self.node, ex.hasDirectPart, other.node))
            g.add((other.node, s4syst.isDirectPartOf, self.node))
        else:
            self.system_heirarchy(self, other)

        return self


class Part(Node):
    """
    """

    node_type: URIRef = ex.Part

    def __gt__(self, other: Any) -> "Part":
        """self > other

        Build a part heirarchy, the other system is a direct part of
        this system.
        """
        if not isinstance(other, (Device, Part)):
            raise ValueError(f"device or part expected")

        g.add((self.node, ex.hasDirectPart, other.node))
        g.add((other.node, s4syst.isDirectPartOf, self.node))

        return self

    def __lt__(self, other: Any) -> Any:
        """self < other

        Build a part heirarchy, this part is a direct part of the other part.
        """
        if not isinstance(other, (Device, Part)):
            raise ValueError(f"device or part expected")

        g.add((other.node, ex.hasDirectPart, self.node))
        g.add((self.node, s4syst.isDirectPartOf, other.node))

        return other


def dump(file: TextIO = sys.stdout, format: str = "turtle") -> None:
    file.write(g.serialize(format="turtle").decode())


def clear() -> None:
    """Remove all the triples from the graph."""
    g.remove((None, None, None))
