from datetime import datetime
from bob import bind_model_namespace, Node, Property, Value, dump, clear

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class Test(Node):
    pass


class Snork(Node):
    test: Test
    temp: Property


# build from pieces
print("----- test 1 -----")
s = Snork()
t = Test()
s.test = t
dump()
clear()
print("")

# use kwargs
print("----- test 2 -----")
s = Snork(test=Test())
dump()
clear()
print("")

# set a property value
print("----- test 3 -----")
p = Property()
v = Value()
v.hasValue = 1
p.hasValue = v
dump()
clear()
print("")

# kwargs set a property value
print("----- test 4 -----")
p = Property(4)
dump()
clear()
print("")

# kwargs set a property value
print("----- test 5 -----")
p = Property(hasValue=5)
dump()
clear()
print("")

# build a value that is a datetime
print("----- test 6 -----")
v = Value(datetime(2021, 1, 1))
dump()
clear()
print("")

# build a value that has a datetime
print("----- test 6 -----")
v = Value(hasSimpleValue=22.5, hasTimestamp=datetime(2021, 1, 1))
dump()
clear()
print("")
