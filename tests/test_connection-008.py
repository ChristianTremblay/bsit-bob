from bob.core import bind_model_namespace, Device, enum, Junction, Air, dump, p223
from rdflib import URIRef

from bob.space.hvac import HVACSpace, HVACZone
from bob.space.physical import Building, Floor, MechanicalRoom, Office
from bob.devices.hvac.fan import Fan
from bob.connections.light import (
    Light,
    LightVisibleConnection,
    LightVisible,
    LightVisibleOutletConnectionPoint,
)
from bob.connections.electricity import ElectricalInletConnectionPoint
from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_Light_Subclass_of_Medium_Connection(bob_fixture):
    class WeirdLuminaire(Device):
        node_type: URIRef = p223.Light
        lightOutlet: LightVisibleOutletConnectionPoint
        electricalInlet: ElectricalInletConnectionPoint

    lightcnx = LightVisibleConnection(label="Sun")

    WeirdLuminaire(label="WL") >> lightcnx

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
