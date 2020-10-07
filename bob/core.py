"""
Bob the SI-WG Builder
"""

import sys
from collections import defaultdict

from typing import Dict, Any, Optional, TextIO, Type, TypeVar

from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS  # type: ignore

# options
MANDITORY_LABEL = True

# globals
g = Graph()
document = ""
_next_node = 1

# namespaces
ex = Namespace("urn:ex:")
g.namespace_manager.bind("ex", URIRef("urn:ex:"))

s4syst = Namespace("https://saref.etsi.org/")
g.namespace_manager.bind("s4syst", URIRef("https://saref.etsi.org/"))

# brick = Namespace("https://brickschema.org/schema/1.1.0/Brick#")
# g.namespace_manager.bind("brick", URIRef("https://brickschema.org/schema/1.1.0/Brick#"))

# connection type (air, etc) to connection classes
connection_classes: Dict[str, Any] = {}


T = TypeVar("T")


def register_connection_type(connection_class: Type[T]) -> Type[T]:
    connection_type: str = connection_class.connection_type  # type: ignore[attr-defined]
    connection_classes[connection_type] = connection_class
    return connection_class


class Node:
    """
    A node in the graph that optionally has a label.  Instances of this
    would be something like blank nodes.
    """

    node: URIRef
    label: str

    def __init__(self, *, label: str = "", **kwargs: Any) -> None:
        global _next_node

        self.node = ex[f"{_next_node:05d}"]
        _next_node += 1

        self.label = label
        if label:
            g.add((self.node, RDFS.label, Literal(label)))

    def __repr__(self) -> str:
        label = (" " + self.label) if self.label else ""
        return f"<{self.__class__.__name__}{label}>"


class ConnectionType:
    connection_type: str = ""  # unrestricted by default


@register_connection_type
class Connection(Node, ConnectionType):
    """
    Generic connection object type, unrestricted.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # <self> a Connection
        g.add((self.node, RDF.type, s4syst.Connection))

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
    connectedThrough: Optional[Connection]
    connectionPointOf: "System"

    def __init__(self, system: "System", **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # start out unconnected
        self.connectedThrough = None

        # <self> a ConnectionPoint
        g.add((self.node, RDF.type, s4syst.ConnectionPoint))

        # <self> a something
        g.add((self.node, RDF.type, ex[self.__class__.__name__]))

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

    def __repr__(self) -> str:
        label = (" " + self.label) if self.label else ""
        rslt = f"<{self.__class__.__name__}{label}"
        if self.connectedThrough:
            rslt += " connected through " + repr(self.connectedThrough)
        rslt += ">"

        return rslt


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

    def __gt__(self, other: Any) -> None:
        """self > other

        Build a subsystem heirarchy, the other system is a subsystem of
        this system.
        """

        self.system_heirarchy(self, other)

    def __lt__(self, other: Any) -> None:
        """self < other

        Build a subsystem heirarchy, this is a subsystem of some other
        system.
        """

        self.system_heirarchy(other, self)


def dump(file: TextIO = sys.stdout, format: str = "turtle") -> None:
    file.write(g.serialize(format="turtle").decode())
