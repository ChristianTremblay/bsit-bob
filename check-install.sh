#!/bin/bash

#
#   This script loops through the available Python versions and dumps out
#   the installed version of Bob, if there is one.  This is handy when there
#   are multiple installations floating around, maybe from different paths.
#

for version in 3.7 3.8 3.9 3.10;
do
if [ -a "`which python$version`" ]; then
python$version << EOF

import sys
python_version = "%d.%d.%d" % sys.version_info[:3]

try:
    import bob
    print("%s: %s @ %s" %(
        python_version,
        bob.__version__, bob.__file__,
        ))
except ImportError:
    print("%s: not installed" % (
        python_version,
        ))
EOF
fi
done
