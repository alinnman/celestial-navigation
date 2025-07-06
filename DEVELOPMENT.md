<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Some notes on development

## Choice of operating system

All development has sofar been been made on Linux (Ubuntu 22.04 LTS).
You may try using windows too, but be prepared for bugs.

## A virtual environment (venv)

This code was developed with
[VSCode](https://en.wikipedia.org/wiki/Visual_Studio_Code)
on a Linux (Ubuntu 22.04 LTS) machine.

The Python environment has been installed in a
[virtual environment](https://docs.python.org/3.11/library/venv.html)
to allow for control of all dependencies and libraries.
This is placed in the <tt>.venv</tt> subfolder.

In order to create this environment you should execute these commands:

    python -m venv .venv
    source .venv/bin/activate
    pip install pandas
    pip install jupyter
    pip install folium
    pip install offline-folium
    python -m offline_folium
    pip install kivy

After having created this you can use VSCode to define
this as your python environment using Ctrl-Shift-P
and selecting this as your Python interpreter.

NOTE: In order to support app development and distribution using
the buildozer tool (see below) I have also prepared an alternative
virtual environment (.venv-buildozer).

    python -m venv .venv-buildozer
    source .venv/bin/activate
    pip install git+https://github.com/misl6/buildozer.git@feat/aab-support

## The .gitignore file

The file [.gitignore](.gitignore) contains several exclusion
patterns in order to not check in these files into git:

* .venv and .venv-buildozer (see above)
* Python cache files
* Jupyter temp files
* Test scripts (anything with a name beginning with <tt>testing</tt>)
* HTML and JSON files (these are produced as map output by Folium)

You may of course edit the git ignore file to adjust to your needs.

## Test scripts

The files in the [test](test) folder contain unit tests which can
be run in VSCode testing module.

## App development and deployment<a name="apps"></a>

The file [main.py](main.py) contains a very simple
app (Celeste) built on the Kivy framework. It can be used as a starter point
for developing Android or iOS apps.

A script solution based on [buildozer](https://github.com/kivy/buildozer)
is available and it produces a working/running app (APK file) for Android 15.
Currently I use a fork of
[this tool](https://gist.github.com/Guhan-SenSam/35c5ed7da254a7c0141e6a8b6101eb33)
which is documented here. This can also produce AAB files
(for releases on Google Play)

In order to use this you need to follow the installation instructions carefully.
Be careful to keep your work in the virtual environment. See above.

Building the app is done using these commands:

    source .venv-buildozer/bin/activate
    ./build-debug.sh

This executes a script preparing a debug APK file.

Note however that you probably need to fine-tune and adjust your enviroment
carefully before being able to run the app build script successfully.

## App testing

Check
[this&nbsp;folder](https://drive.google.com/drive/folders/1QFcncVEuCQMnls8lyNElDtpTYruMgI0D?usp=drive_link)
for a list of compiled APK files. These apps should run nicely
but still have limited functionality (mapping support may be missing).
At the moment I have not yet finalized publishing on Google Play.
