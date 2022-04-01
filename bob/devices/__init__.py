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
    def compose(self, sensors=None, devices=None):
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
            if sensors is not None:
                if isinstance(sensors, list):
                    for sensor in sensors:
                        self > sensor
                else:
                    self > sensors
        except AttributeError:
            pass
        try:
            if devices is not None:
                if isinstance(sensors, list):
                    for dev in devices:
                        self > dev
                else:
                    self > devices
        except AttributeError:
            pass
        return self

    if not hasattr(cls, "compose"):
        setattr(cls, "compose", compose)
    return cls
