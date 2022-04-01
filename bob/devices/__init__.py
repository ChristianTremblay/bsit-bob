from re import S
from ..core import Device
from typing import Any


def contains_devices_list(config, **kwargs):
    if not config:
        return ([], kwargs)
    devices = []
    if "contains" in config:
        for device_label_and_class, device_data in config["contains"].items():
            _label, _cls = device_label_and_class
            try:
                if issubclass(_cls, Device):
                    _cls = _cls
            except:
                raise TypeError("Please provide class for device")
            devices.append(_cls(label=_label, **device_data))
    kwargs = {**config["params"], **kwargs}
    return (devices, kwargs)


def composite(cls):
    def finalize(self):
        """
        multimethod needs the class to be instanciated before
        being able to add relationships. Finalize wil lbe called
        after creation allowing composite devices (device containing
        sensors and/or devices) to be created with thoses relationships.

        It is popssible to override this method in the creation of a class
        electricity.distribution are using this possibility to add
        more complex conditions in the finalize.
        The decorator will not overwrite a finalize method that already
        exists in a class.
        """
        try:
            if self.sensors is not None:
                if isinstance(self.sensors, list):
                    for sensor in self.sensors:
                        self > sensor
                else:
                    self > self.sensors
        except AttributeError:
            print("OUPS")
        try:
            if self.devices is not None:
                for dev in self.devices:
                    self > dev
        except AttributeError:
            print("FLUTE")
        return self

    @property
    def sensor(self):
        """
        Some device have by definition only one sensor (like stats)
        It makes no sense to call for plural sensors so make sensor
        a valid choice
        """
        return self.sensors

    def __getitem__(self, name: str) -> Any:
        """
        Will allow the device['label'] syntax to be used
        """
        for each in self.sensors:
            if each.label == name:
                return each
        for each in self.devices:
            if each.label == name:
                return each
        raise KeyError(f"{name} not found")

    if not hasattr(cls, "finalize"):
        setattr(cls, "finalize", finalize)
    if not hasattr(cls, "__getitem__"):
        setattr(cls, "__getitem__", __getitem__)
    setattr(cls, "sensor", sensor)
    # cls = cls.finalize(cls)
    return cls
