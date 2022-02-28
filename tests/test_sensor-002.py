from pathlib import Path

from bob.core import bind_model_namespace, dump
from bob.sensor.pressure import DifferentialStaticPressureSensor
from bob.space.hvac import HVACSpace
from bob.space.physical import Building, Room, MechanicalRoom
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_sensor_002():
    # Create a clean room with a SAS in a Building
    # Sensors are all in the mechnical room
    clean_room_hvac = HVACSpace(label="CleanRoom HVAC Space")
    SAS_hvac = HVACSpace(label="SAS HVAC Space")
    building = Building(label="Clients's place")
    clean_room = Room(label="Clean Room #1")
    sas = Room(label="SAS leading to Clean Room #1")
    mechroom = MechanicalRoom(label="Mechanical room for Clean Room #1")

    building > clean_room > clean_room_hvac
    building > sas > SAS_hvac
    building > mechroom

    tpd01 = DifferentialStaticPressureSensor(
        label="TPD-01",
        comment="Static Pressure between Clean Room (+) and SAS (-)",
        hasExternalReference=["bacnet://570005/analog-input,10084/present-value"],
    )
    tpd01.hasMeasurementLocationHigh = clean_room_hvac
    tpd01.hasMeasurementLocationLow = SAS_hvac
    tpd01.hasPhysicalLocation = mechroom

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
