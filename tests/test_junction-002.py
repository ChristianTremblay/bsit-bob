from bob.core import bind_model_namespace, dump
from bob.core import Junction

__namespace__ = bind_model_namespace("ex", "urn:ex/")

j1 = Junction()
j2 = Junction()
j1.link_to(j2)

dump()
