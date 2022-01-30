from ..core import Device


def contains_devices_list(config, **kwargs):
    if not config:
        return ([], kwargs)
    devices = []
    for device_label_and_class, device_data in config["contains"].items():
        _label, _cls = device_label_and_class
        try:
            if issubclass(_cls, Device):
                _cls = _cls
        except:
            raise TypeError("Please provide class for device")

        devices.append(_cls(label=_label, **device_data))
    kwargs = {**config["device"], **kwargs}
    return (devices, kwargs)
