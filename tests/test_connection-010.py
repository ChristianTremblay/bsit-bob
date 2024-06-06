from pathlib import Path

from header import ttl_test_header
from rdflib import URIRef

from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.connections.liquid import (
    Glycol15PercentInletConnectionPoint,
    Glycol15PercentOutletConnectionPoint,
)
from bob.core import (
    P223,
    Equipment,
    bind_model_namespace,
    dump,
    enum,
    data_graph,
    schema_graph,
)
from bob.equipment.network.switch import PoESwitch, EthernetSwitch
from bob.equipment.hvac.pump import Pump
from bob.equipment.hvac.valve import TwoWayValve

from bob.space.hvac import HVACSpace, HVACZone
from bob.space.physical import Building, Floor, MechanicalRoom, Office

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# Test if I can connect Water to Glycol15Percent
def test_GlycolAndWater(bob_fixture):
    glycol_equip = {
        "cp": {
            "waterInlet": Glycol15PercentInletConnectionPoint,
            "waterOutlet": Glycol15PercentOutletConnectionPoint,
        },
    }
    water_pump = Pump(label="WaterPump")
    glycol_equip = Equipment(label="Glycol Valve", config=glycol_equip)

    water_pump >> glycol_equip

    dump(
        data_graph,
        filename=f"tests/ttl/{model_name}.data.ttl",
        header=ttl_test_header(model_name),
    )

    dump(
        schema_graph,
        filename=f"tests/ttl/{model_name}.schema.ttl",
        header=ttl_test_header(model_name),
    )
