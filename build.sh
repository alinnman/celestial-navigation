#!/bin/bash

#
#    © August Linnman, 2025, email: august@linnman.net
#    MIT License (see LICENSE file)
#



# Simple build script. Bootstrapping the pure python libraries
# and then building using buildozer (p4a)

source .venv-buildozer/bin/activate

# Cython seems to be needed so we install it
pip install cython

# Also make sure buildozer is installed
pip install buildozer==1.5.0
#pip install git+https://github.com/misl6/buildozer.git@feat/aab-support

# Convert the documentation file to HTML
pandoc -s -o APPDOC.html APPDOC.md -c APPDOC.css 

# Now build the android app
if [ "$1" == "release" ]; then
    buildozer -v android release
else
    buildozer -v android debug
fi

pip uninstall cython -y













