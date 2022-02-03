from pathlib import Path

from typing import Any

from bob.core import (
    System,
    Zone,
    Node,
    s223,
    Segment,
    Junction,
    bind_namespace,
    quantitykind,
    enum,
    turtle,
    get_datagraph,
    bind_model_namespace,
    dump,
)

from bob.devices.hvac.damper import ElectricalActuatedDamper
from bob.devices.hvac.coil import ChilledWaterCoil
from bob.devices.hvac.fan import Fan
from bob.systems.hvac.airhandlingunit import AirHandlingUnit
from bob.sensor.temperature import AirTemperatureSensor

from bob.connections.air import *

from bob.role import (
    Exhaust,
    Supply,
)
from bob.signal import (
    AnalogOut,
    AnalogIn,
)
from rdflib import Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD

# from header import g36_header

# model_name = Path(__file__).stem
model_name = "B59"
__namespace__ = ex = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_rooftop(node_iri=None):
    _config = {
        "params": {"node_iri": node_iri, "label": "RTU-1", "comment": "Supply Fan"},
        "sensors": {
            ("T-1", AirTemperatureSensor): {"comment": "Supply Air Temperature sensor"},
            ("T-2", AirTemperatureSensor): {"comment": "Return Air Temperature sensor"},
        },
        "contains": {
            ("SF-1", Fan): {"comment": "Supply Fan"},
            ("RF-1", Fan): {"comment": "Return Fan"},
            ("OAD-1", ElectricalActuatedDamper): {"comment": "Outside Air Damper"},
            ("RAD-1", ElectricalActuatedDamper): {"comment": "Return Air Damper"},
            ("CWC-1", ChilledWaterCoil): {"comment": "Chilled Water coil"},
        },
    }
    _mixedAir = AirConnection(
        label="MIXED-AIR", comment="Where return air and outside air mix"
    )
    _returnAir = AirConnection(label="RETURN-AIR", comment="Air returns from zone here")
    _rtu = AirHandlingUnit(config=_config)
    # Relationships between devices
    _rtu["OAD-1"] >> _mixedAir
    _rtu["RF-1"] >> _mixedAir
    _mixedAir >> _rtu["SF-1"]
    _rtu["SF-1"] >> _rtu["CWC-1"]

    # Mapping of the system
    _rtu.outsideAirInlet.mapsTo = _rtu["OAD-1"].airInlet
    _rtu.returnAirInlet.mapsTo = _rtu["RF-1"].airInlet
    _rtu.supplyAirOutlet.mapsTo = _rtu["CWC-1"].airOutlet

    return _rtu


# Should a plenum be a segment or is system correct??
class Plenum(System):
    AirInlet: AirInletSystemConnectionPoint  # would the outlet be a junction, or just connection points??
    AirOutlet: AirOutletSystemConnectionPoint
    hasSubstance = Air

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        j = Junction(label=self.label + ".inlet")
        # j.hasSubstance = Air
        j2 = Junction(label=self.label + ".outlet")
        # j2.hasSubstance = Air #If the junction has a substance, then it doesn't connect. Am I just doing this wrong??
        self.AirInlet.mapsTo = j
        self.AirOutlet.mapsTo = j2


# make an instance
# class HVACZone2(HVACZone):
#    node_type = None  # Does this just mean that this isn't something in 223p yet?
#    temperature_setpoint: AnalogOut###

#    def __init__(self, label: str) -> None:
#        super().__init__(label=label)
#        # I need a junction to be the system inlet and outlet if I want to connect to another junction.
#        j = Junction()
#        self.supplyAir.mapsTo = j#


# r = RooftopUnit(node_iri=ex.rtu, label="rtu")
# p = Plenum(label="plenum")
# z = HVACZone2(label="zone")
# can't seem to connect system connection points to junctions
# r.supplyAirOutlet >> p.AirInlet

# p.AirOutlet.link_to(z.supplyAir) #getting no common connection types, because supply Air isn't a junction
# p.AirOutlet >> (z.supplyAir)


# g36_header(model_name)
# dump()

if __name__ == "__main__":
    r = test_create_rooftop(node_iri=ex.rtu)
    result = turtle()
    with open("b-59_LP.ttl", "w") as file:
        file.write(result)
    print("Check file : b-59_LP.ttl")
    print(result)
    graph = get_datagraph()
