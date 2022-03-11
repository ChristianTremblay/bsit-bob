from rdflib import URIRef
from ...core import s223, p223, Device, Property

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...signal import AnalogIn, AnalogOut

__namespace__ = p223



class VFD(Device):
    electricalInlet: ElectricalInletConnectionPoint
    electricalOutlet: ElectricalOutletConnectionPoint
    default_props = {'actual_speed': AnalogIn, 'motor_temp': AnalogIn}

    def __init__(self, properties: dict = default_props, **kwargs) -> None:
    	super().__init__(**kwargs)
    	self.properties = self.define_properties(properties)
    	
    	for prop_name, prop in self.properties.items():
    		self.add_property(prop)
#propose moving these up to device or connectable
    def add_property(self, prop: Property) -> Property:
        """Add a property to a node, returns the added property."""
        assert isinstance(prop, Property)

        # link the two together
        self._data_graph.add((self.node, s223.hasProperty, prop.node))

        return prop

    def define_properties(self, properties):
        if not properties:
            return {}
        props = {}
        for prop_name, _cls in properties.items():
            
            try:
                if issubclass(_cls, Property):
                    _cls = _cls
            except:
                raise TypeError("Please provide class for property")

            props[prop_name] = _cls(label = self.label+'.'+prop_name)

        return props
