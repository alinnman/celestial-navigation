#!/bin/bash

#
#    © August Linnman, 2025, email: august@linnman.net
#    MIT License (see LICENSE file)
#

# Simple build script. Bootstrapping the pure python libraries
# and then building using buildozer (p4a)

# This script has been successfully executed in an Ubuntu 24.04 LTS setup. 

export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

source .venv-buildozer/bin/activate

# Cython seems to be needed so we install it
pip install cython

# Also make sure buildozer is installed
pip install buildozer==1.5.0
#pip install git+https://github.com/misl6/buildozer.git@feat/aab-support

# Convert the documentation file to HTML
pandoc -s -o APPDOC.html APPDOC.md -c APPDOC.css 

echo "You NEED to setup the offline tiles directory with download_tiles.py "
echo "But to avoid lockouts this will not be done in the build script."
echo "You must do this at a convenient time. Once."

# Now build the android app
if [ "$1" == "release" ]; then
    buildozer -v android release
else
    buildozer -v android debug
fi

# pip uninstall cython -y













