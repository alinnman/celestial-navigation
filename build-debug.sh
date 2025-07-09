#!/bin/bash

#
#    © August Linnman, 2025, email: august@linnman.net
#    MIT License (see LICENSE file)
#

# Simple build script. Bootstrapping the pure python libraries
# and then building using buildozer (p4a)

source .venv-buildozer/bin/activate

# The libraries folium, branca and jinja2 are injected as pure python
# libraries and will be deployed into the private.tar asset

pip install folium
rm -r folium
mkdir folium
cp -r .venv-buildozer/lib/python3.11/site-packages/folium/* folium

pip install branca
rm -r branca
mkdir branca
cp -r .venv-buildozer/lib/python3.11/site-packages/branca/* branca

pip install jinja2
rm -r jinja2
mkdir jinja2
cp -r .venv-buildozer/lib/python3.11/site-packages/jinja2/* jinja2

pip install markupsafe
rm -r markupsafe
mkdir markupsafe
cp -r .venv-buildozer/lib/python3.11/site-packages/markupsafe/* markupsafe

pip install xyzservices
rm -r xyzservices
mkdir xyzservices
cp -r .venv-buildozer/lib/python3.11/site-packages/xyzservices/* xyzservices

pip uninstall folium -y
pip uninstall branca -y
pip uninstall jinja2 -y
pip uninstall markupsafe -y
pip uninstall xyzservices -y

pip install cython

# Convert the documentation file to HTML
pandoc -o APPDOC.html APPDOC.md

buildozer -v android debug

rm -r folium
rm -r branca
rm -r jinja2
rm -r markupsafe
rm -r xyzservices











