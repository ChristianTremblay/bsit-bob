from pathlib import Path

from header import ttl_test_header
from rdflib import URIRef

from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.connections.light import (
    Light,
    LightVisible,
    LightVisibleConnection,
    LightVisibleOutletConnectionPoint,
)
from bob.core import Air, Device, Junction, bind_model_namespace, dump, enum, p223
from bob.devices.hvac.fan import Fan
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.physical import Building, Floor, MechanicalRoom, Office

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_Light_Subclass_of_Medium_Connection(bob_fixture):
    class WeirdLuminaire(Device):
        node_type: URIRef = p223.Light
        lightOutlet: LightVisibleOutletConnectionPoint
        electricalInlet: ElectricalInletConnectionPoint

    lightcnx = LightVisibleConnection(label="Sun")

    WeirdLuminaire(label="WL") >> lightcnx

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
