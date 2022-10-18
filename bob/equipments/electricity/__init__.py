from bob.core import P223, S223, Equipment, Property

_namespace = S223


class _MotorStarter(Equipment):
    """
    This is required here so actuatesProperty gets its namespace from S223
    """

    _class_iri = S223.Equipment
    actuatesProperty: Property


class _VFD(Equipment):
    """
    This is required here so actuatesProperty gets its namespace from S223
    """

    _class_iri = S223.Equipment
    actuatesProperty: Property
