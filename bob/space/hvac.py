from rdflib import URIRef
from ..core import DomainSpace, HVAC, s223, Zone

__namespace__ = s223


class HVACSpace(DomainSpace):
    hasDomain = HVAC


class HVACZone(Zone):
    hasDomain = HVAC
