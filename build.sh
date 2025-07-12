#!/bin/bash

#
#    © August Linnman, 2025, email: august@linnman.net
#    MIT License (see LICENSE file)
#



# Simple build script. Bootstrapping the pure python libraries
# and then building using buildozer (p4a)

source .venv-buildozer/bin/activate

# This is a list of the pure python libraries we want to include
declare -a python_libs=("folium" "branca" "jinja2" "markupsafe" "xyzservices")

for i in "${python_libs[@]}"
do
    pip install $i
    rm -r $i
    mkdir $i
    cp -r .venv-buildozer/lib/python3.11/site-packages/$i/* $i
done

for i in "${python_libs[@]}"
do
    pip uninstall $i -y
done

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

#buildozer -v android release

for i in "${python_libs[@]}"
do
    rm -r $i
done

pip uninstall cython -y













