from rdflib import URIRef
from typing import Dict
from ...core import ConnectionPoint, s223, p223, Device, Property

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...signal import AnalogIn, AnalogOut
from ...sensor import define_sensors
from ...devices import contains_devices_list
from ...properties.electricity import Amps, ElectricPowerkW, PowerFactor
from ...properties.force import HP
from ...properties.ratio import RPM, Percent

__namespace__ = p223

"""
vfd_template = {
    "params": {
        "label": "MyVFD", 
        "comment": "A VFD for a Big Fan",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
        "amps": 10,
        "hp": 10,
    },
    "sensors": {},
    "contains": {},
}
"""


class VFD(Device):
    node_type: URIRef = s223.VariableFrequencyDrive
    # electricalInlet: Must be provided in config
    # electricalOutlet: Must be provided in config
    amps: Amps
    hp: HP
    kW: ElectricPowerkW
    speed_reference: Percent
    # motor_temp: ?
    # run_status: Status
    # alarm

    def __init__(self, config: Dict = None, **kwargs):
        optional_properties = ["amps", "kW", "hp", "speed_reference"]
        _properties = {}
        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        sensors = define_sensors(config)
        devices, device_kwargs = contains_devices_list(config, **kwargs)
        _electricalInlet = (
            device_kwargs.pop("electricalInlet")
            if "electricalInlet" in device_kwargs
            else None
        )
        _electricalOutlet = (
            device_kwargs.pop("electricalOutlet")
            if "electricalOutlet" in device_kwargs
            else None
        )
        for each in optional_properties:
            _properties[each] = (
                device_kwargs.pop(each) if each in device_kwargs else None
            )

        super().__init__(**device_kwargs)
        self.electricalInlet = (
            _electricalInlet(self, label=f"{self.label}.electricalInlet")
            if _electricalInlet
            else None
        )
        self.electricalOutlet = (
            _electricalOutlet(self, label=f"{self.label}.electricalOutlet")
            if _electricalOutlet
            else None
        )
        for k, v in _properties.items():
            setattr(self, k, self.__annotations__[k](v))

        for sensor in sensors:
            self > sensor
        for dev in devices:
            self > dev


# class VFD(Device):
#    electricalInlet: ElectricalInletConnectionPoint
#    electricalOutlet: ElectricalOutletConnectionPoint
#
#
#    def __init__(self, properties: dict = default_props, **kwargs) -> None:
#    	super().__init__(**kwargs)
#    	self.properties = self.define_properties(properties)
#
#    	for prop_name, prop in self.properties.items():
#    		self.add_property(prop)
# propose moving these up to device or connectable
#    def add_property(self, prop: Property) -> Property:
#        """Add a property to a node, returns the added property."""
#        assert isinstance(prop, Property)

#        # link the two together
#        self._data_graph.add((self.node, s223.hasProperty, prop.node))

#        return prop

#    def define_properties(self, properties):
#        if not properties:
#            return {}
#        props = {}
#        for prop_name, _cls in properties.items():
#
#            try:
#                if issubclass(_cls, Property):
#                    _cls = _cls
#            except:
#                raise TypeError("Please provide class for property")
#
#            props[prop_name] = _cls(label = self.label+'.'+prop_name)

#        return props
