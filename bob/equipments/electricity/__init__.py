from bob.core import P223, S223, Device, Property

_namespace = S223


class _MotorStarter(Device):
    """
    This is required here so actuatesProperty gets its namespace from S223
    """

    _class_iri = S223.Device
    actuatesProperty: Property


class _VFD(Device):
    """
    This is required here so actuatesProperty gets its namespace from S223
    """

    _class_iri = S223.Device
    actuatesProperty: Property
