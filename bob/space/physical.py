from rdflib import URIRef

from ..core import QUANTITYKIND, S223, UNIT, PhysicalSpace, bind_namespace
from ..properties.physical import Area, Length

"""
This is a hack, Real Estate Core has many namespaces, and some of the physical
spaces defined in this module are not in REC or BOT.
"""
_namespace = bind_namespace("rec", "https://w3id.org/rec/core/")


class Site(PhysicalSpace):
    Area: Area


class Building(PhysicalSpace):
    Area: Area


class Roof(PhysicalSpace):
    Area: Area


class Floor(PhysicalSpace):
    Area: Area


class Basement(Floor):
    Area: Area


class Room(PhysicalSpace):
    Area: Area


class Hall(Room):
    Area: Area


class Corridor(Room):
    Area: Area


class Bathroom(Room):
    Area: Area


class Office(Room):
    Area: Area


class MechanicalRoom(Room):
    Area: Area
