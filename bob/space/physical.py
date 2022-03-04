from rdflib import URIRef
from ..core import Physical, bind_namespace, s223, PhysicalSpace


"""
This is a hack, Real Estate Core has many namespaces, and some of the physical
spaces defined in this module are not in REC or BOT.
"""
__namespace__ = bind_namespace("rec", "https://w3id.org/rec/core/")


class Site(PhysicalSpace):
    pass


class Building(PhysicalSpace):
    pass


class Roof(PhysicalSpace):
    pass


class Floor(PhysicalSpace):
    pass


class Basement(PhysicalSpace):
    pass


class Hall(PhysicalSpace):
    pass


class Corridor(PhysicalSpace):
    pass


class Bathroom(PhysicalSpace):
    pass


class Office(PhysicalSpace):
    pass


class Room(PhysicalSpace):
    pass


class MechanicalRoom(PhysicalSpace):
    pass
