from bob.core import bind_model_namespace, dump, turtle, get_datagraph, enum
from bob.sensor.pressure import DifferentialStaticPressureSensor
from bob.space.hvac import HVACSpace
from bob.space.physical import PhysicalSpace, Building, Room, MechanicalRoom
import pytest

__namespace__ = bind_model_namespace("ex", "urn:ex/")


# Room static pressure sensors


def test_create_differential_static_air_pressure_sensor():
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
    tpd01.hasLocation = mechroom
    return tpd01


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    asps = test_create_differential_static_air_pressure_sensor()
    result = turtle()
    with open("test_sensor-002_results.ttl", "w") as file:
        file.write(result)
    print("Check file : test_sensor-002_results.ttl")
    print(result)
    graph = get_datagraph()
