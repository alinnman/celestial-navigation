#!/bin/bash

# Simple build script. Bootstrapping the pure python libraries
# and then building using buildozer (p4a)

source .venv-buildozer/bin/activate

pip install folium
rm -r folium
mkdir folium
cp -r .venv-buildozer/lib/python3.11/site-packages/folium/* folium

pip install branca
rm -r branca
mkdir branca
cp -r .venv-buildozer/lib/python3.11/site-packages/branca/* branca

buildozer -v android debug

rm -r folium
rm -r branca






