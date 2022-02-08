from rdflib import URIRef
from ..core import DomainSpace, Physical, bind_namespace, s223, PhysicalSpace


bot = bind_namespace("bot", "https://w3id.org/bot#")

__namespace__ = s223


class Site(PhysicalSpace):
    node_type: URIRef = s223.PhysicalSpace
    hasDomain = Physical
    # align to bot.Site
    # hasBuilding: bot.Building


class Building(PhysicalSpace):
    node_type: URIRef = s223.PhysicalSpace
    hasDomain = Physical
    # alignement to bot.Building
    # Brick Alignment example here
    # https://raw.githubusercontent.com/w3c-lbd-cg/bot/master/BRICKAlignment.ttl


class Roof(PhysicalSpace):
    node_type: URIRef = s223.PhysicalSpace
    hasDomain = Physical


class Floor(PhysicalSpace):
    node_type: URIRef = s223.PhysicalSpace
    hasDomain = Physical


class Basement(PhysicalSpace):
    node_type: URIRef = s223.PhysicalSpace
    hasDomain = Physical


class Hall(PhysicalSpace):
    node_type: URIRef = s223.PhysicalSpace
    hasDomain = Physical


class Office(PhysicalSpace):
    node_type: URIRef = s223.PhysicalSpace
    hasDomain = Physical


class Room(PhysicalSpace):
    node_type: URIRef = s223.PhysicalSpace
    hasDomain = Physical


class MechanicalRoom(PhysicalSpace):
    node_type: URIRef = s223.PhysicalSpace
    hasDomain = Physical
