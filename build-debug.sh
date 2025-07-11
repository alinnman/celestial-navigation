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

# Cython seems to needed so we install it
pip install cython

# Convert the documentation file to HTML
pandoc -s -o APPDOC.html APPDOC.md -c APPDOC.css 
#--metadata title="Celeste App Documentation"

# Now build the android app
buildozer -v android debug

for i in "${python_libs[@]}"
do
    rm -r $i
done

pip uninstall cython -y













