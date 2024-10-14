from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.connections import (
    AirInletConnectionPoint,
    AirInletZoneConnectionPoint,
    ChilledWaterConnection,
)
from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.core import (
    S223,
    Domain,
    DomainSpace,
    PhysicalSpace,
    Zone,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)
from bob.equipment.hvac.coil import ChilledWaterCoil
from bob.equipment.hvac.fan import Fan
from bob.scratch.header import sample_header
from bob.space.hvac import HVACSpace

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class HVACZone(Zone):
    hasDomain: Domain = Domain.HVAC
    supplyAir: AirInletZoneConnectionPoint


# there is a chilled water connection, we don't know where the chilled
# is coming from
c = ChilledWaterConnection()

# there is a chilled water coil (itself a system) that is a subsystem
# of a larger context
coil1 = ChilledWaterCoil(label="CW-Coil-1")

# the coil gets its chilled water from the connection
c >> coil1.chilledWaterInlet

# there is a fan, and the air output of the fan goes into the coil
f = Fan(label="F", electricalInlet=ElectricalInletConnectionPoint)
f >> coil1.airInlet

# there is a zone and a space
zone = HVACZone(label="Zone-1")
room = PhysicalSpace(label="Room 191")
space = HVACSpace(label="Space")

# the room contains the space
room > space

# the zone contains the space, and the air input into the zone is
# mapped to the space connection point
zone > space
zone.supplyAir.maps_to(space.ductAirInlet)

for s, p, o in data_graph:
    if p == S223.cnx:
        if (o, p, s) not in data_graph:
            print(f"missing {o} -> {s}")

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
