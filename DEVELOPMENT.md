<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Some notes on development

## A virtual environment (venv)

This code was developed with
[VSCode](https://en.wikipedia.org/wiki/Visual_Studio_Code) on a Linux (Ubuntu)
machine.

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
    pip install offline_folium
    python -m offline_folium
    pip install kivy

After having created this you can use VSCode to define
this as your python environment using Ctrl-Shift-P
and selecting this as your Python interpreter.

## The .gitignore file

The file [.gitignore](.gitignore) contains several exclusion
patterns in order to not check in these files into git:

* The .venv (see above)
* Python cache files
* Jupyter temp files
* Test scripts (anything with a name beginning with <tt>testing</tt>)
* HTML and JSON files (these are produced as map output by Folium)

You may of course edit the git ignore file to adjust to your needs.

## Test scripts

The files in the [test](test) folder contain unit tests which can
be run in VSCode testing module.

## App development

The file [starfix_app.py](starfix_app.py) contains a very simple
app built on the Kivy framework. It can be used as a starter point
for developing Android or iOS apps.
