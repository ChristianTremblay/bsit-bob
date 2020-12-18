from datetime import datetime
from bob import bind_model_namespace, Node, Property, Value, dump, clear

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class Test(Node):
    pass


class Snork(Node):
    test: Test
    temp: Property


print("----- node assignment -----")
s = Snork()
t = Test()
s.test = t
dump()
clear()
print("")

print("----- property assignment via kwargs-----")
s = Snork(test=Test())
dump()
clear()
print("")

print("----- setting a property value -----")
p = Property()
v = Value()
v.hasValue = 1
p.hasValue = v
dump()
clear()
print("")

print("----- auto build Value, init property value -----")
p = Property(4)
dump()
clear()
print("")

print("----- kwargs set property value -----")
p = Property(hasValue=5)
dump()
clear()
print("")

print("----- datetime value -----")
v = Value(datetime(2021, 1, 1))
dump()
clear()
print("")

print("----- value with a timestamp -----")
v = Value(hasSimpleValue=22.5, hasTimestamp=datetime(2021, 1, 1))
dump()
clear()
print("")
