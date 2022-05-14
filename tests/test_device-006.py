from pathlib import Path

from header import ttl_test_header

from bob.connections.electricity import (
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
)
from bob.core import bind_model_namespace, dump
from bob.devices.hvac.vfd import VFD
from bob.properties import (
    HP,
    RPM,
    Amps,
    ElectricPowerkW,
    OnOffCommand,
    OnOffStatus,
    Percent,
    PercentCommand,
    Temperature,
)
from bob.properties.states import NormalAlarmStatus

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_vfd_from_template(bob_fixture):
    vfd_template = {
        "params": {"label": "MyVFD", "comment": "A VFD for a Big Fan"},
        "cp": {
            "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
            "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
        },
    }
    v = VFD(config=vfd_template)
    assert type(v["rpm"]) is RPM
    assert type(v["alarm_status"]) is NormalAlarmStatus
    assert v.label == "MyVFD"
    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
