from bob.core import S223, Device, Property

_namespace = S223


class _MotorStarter(Device):
    """
    This is required here so actuatesProperty gets its namespace from S223
    """

    _class_iri = S223.MotorStarter
    actuatesProperty: Property


class _VFD(Device):
    """
    This is required here so actuatesProperty gets its namespace from S223
    """

    _class_iri = S223.VariableFrequencyDrive
    actuatesProperty: Property
