<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Installation and usage

## Quick Demo

A
[demo](https://colab.research.google.com/drive/1bZt35-P6aiPlKWktyXgU3he6Di_N-PpA)
of the code can be run in Google Colab. You can use it to run a standard
three-star fix. A Google account is necessary.

## Installation

### About operating systems

All development and testing has sofar been done on Linux (Ubuntu),
Android and Google Colab.
Nothing has (yet) been tested thourougly in MS Windows. You will likely be able
to develop and run scripts and the kivy app on Windows,
but the android cross-compiling kit
(buildozer) has sofar only been executed under Linux.

### A mobile app (Android)

A mobile app has been developed but it is still in alpha stage and not
yet published on Google Play.<br>
[Read more about the app and how to install it here](DEVELOPMENT.md#apps)

[See here](APPDOC.md) for instructions on how to use the app.

### Python scripts and notebooks

The code is installed using just a file copy of the python (.py)
and (optionally) Jupyter notebook (.ipynb) files to a suitable directory.
You may also need the machine-readable nautical almanacs residing in the
<tt>sample_data</tt> subfolder and some optional libraries.

Your Python setup:

* [Python 3.11](https://www.python.org/downloads/release/python-3110/)
or higher with core libraries.
* [Pandas](https://pandas.pydata.org/)
(*Optional*, needed for the
[machine-readable nautical almanac](README.md#mr)).
* [Jupyter](https://jupyter.org/) (*Optional*, needed for running notebooks.)
* [Folium](https://github.com/python-visualization/folium)
(*Optional*, needed for high-quality mapping)
* [Kivy](https://kivy.org/)
(*Optional*, for running the demo app.)

NOTE: The Offline Folium package seems to have bugs,
resulting in incorrect plotting.
I have disabled it for now.

No other additional libraries are necessary.
[This link](https://github.com/alinnman/celestial-navigation/archive/refs/heads/main.zip)
will download **all** source code and needed files in a ZIP file.
The optional libraries can be installed using the standard <tt>pip</tt> utility.

The python scripts could be installed in
[PyDroid](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3)
to allow for use on an Android mobile phone
(with no need for internet access).
To aid in installation a good file browser is recommended
(for copying and decompressing of ZIP files) such as Cx File Explorer as
[described&nbsp;here](https://play.google.com/store/apps/details?id=com.cxinventor.file.explorer&pcampaignid=web_share).
You are recommended to unzip the file to a specific directory
(not a root directory).
On Android you could create a directory in the "Documents" tree,
e.g. "Documents/work/coding".
Pydroid has access to <tt>pip</tt>
for installing needed external libraries.

The script [starfix.py](starfix.py) contains the core routines.

The script [calibration.py](calibration.py) contains a setup of a used sextant,
with a correction for errors.
You are advised to adjust this script for your used sextant.

You are also advised to make copies (and modifications) of the supplied samples
[starfixdata_stat_1.py](starfixdata_stat_1.py)
or [starfixdata_sea_1.py](starfixdata_sea_1.py)
to support your workflow and observations.
There are also Jupyter notebooks availabe, see below.

A Nautical Almanac must be used to get the GP (ground point) of
your observations. If your observations are made from 2024 to 2028
you have a machine-readable almanac [available here](./sample_data).
But you can also use a manual/printed almanac.
Currently PDF almanacs of [2024](nautical_almanacs/NAmod(A4)_2024.pdf),
[2025](nautical_almanacs/NAmod(A4)_2025.pdf),
[2026](nautical_almanacs/NAmod(A4)_2026.pdf),
[2027](nautical_almanacs/NAmod(A4)_2027.pdf)
and [2028](nautical_almanacs/NAmod(A4)_2028.pdf)
are bundled in the repository in a digital version.
But you may of course use a hard-copy of the nautical almanac and
these can be
[ordered&nbsp;here](https://www.amazon.com/s?i=stripbooks&rh=p_27%3AU.K.+Hydrographic&s=relevancerank&text=U.K.+Hydrographic&ref=dp_byline_sr_book_1).
New digital versions (PDF or machine-readable)
can be prepared using some GitHub code repositories,
such as [this one](https://github.com/alinnman/SkyAlmanac-Py3).

The script sample [terrestrial.py](terrestrial.py)
can be used (and modified) if you would like to use your sextant as an aid in
terrestrial navigation.

In addition to the supplied scripts you may also run the code in
[Jupyter&nbsp;Notebooks](https://en.wikipedia.org/wiki/Project_Jupyter#Jupyter_Notebook).
[Jupyter&nbsp;can&nbsp;be&nbsp;installed&nbsp;in&nbsp;Pydroid](https://www.codementor.io/@olalekanrahman/how-to-access-jupyter-notebook-on-pydroid-1ckw13mtgz),
and this allows for a convenient way to keep your workflow in an easily
managed web interface. The notebook web interface can be launched from specific
launch scripts (launch.xxx.py).

The Pydroid app should also
be tweaked slightly, in order to allow for running Jupyter notebooks. Using
the Settings (Android) app make sure you have these configurations made.

1. Set "Allow notifications".
1. Remove any battery saving settings.

Unless you do these adjustments you will likely get an error while running
notebooks causing the kernel to hang after about 1 minute.

## Development

[Some short notes on development here](DEVELOPMENT.md).
