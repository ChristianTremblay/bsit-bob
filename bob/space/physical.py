from rdflib import URIRef

from ..core import PhysicalSpace, bind_namespace, s223

"""
This is a hack, Real Estate Core has many namespaces, and some of the physical
spaces defined in this module are not in REC or BOT.
"""
_namespace = bind_namespace("rec", "https://w3id.org/rec/core/")


class Site(PhysicalSpace):
    pass


class Building(PhysicalSpace):
    pass


class Roof(PhysicalSpace):
    pass


class Floor(PhysicalSpace):
    pass


class Basement(Floor):
    pass


class Room(PhysicalSpace):
    pass


class Hall(Room):
    pass


class Corridor(Room):
    pass


class Bathroom(Room):
    pass


class Office(Room):
    pass


class MechanicalRoom(Room):
    pass
