# Installation and usage

## Quick Demo

A [quick demo](https://colab.research.google.com/github/alinnman/celestial-navigation/blob/main/starfix_colab_demo.ipynb)
of the code can be run at Google Colab. You can use it to run a standard
three-star fix. A Google account is necessary.

## Installation

The code is installed using just a file copy of the python (.py) and (optionally)
Jupyter notebook (.ipynb) files to a suitable directory.
No additional libraries are necessary.
Python 3.11 is required.
This [link](https://github.com/alinnman/celestial-navigation/archive/refs/heads/main.zip)
will download all code in a ZIP file.

The python scripts could be installed in
[PyDroid](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3)
to allow for use on an Android mobile phone
(with no need for internet access).
To aid in installation a good file browser is recommended
(for copying and decompressing of ZIP files) such as [Cx File Explorer](https://play.google.com/store/apps/details?id=com.cxinventor.file.explorer&pcampaignid=web_share).
You are recommended to unzip the file to a specific directory (not a root directory),
on Android you could create a directory in the "Documents" tree,
e.g. "Documents/work/coding".  

The script [starfix.py](starfix.py) contains the core routines.

The script [calibration.py](calibration.py) contains a setup of a used sextant,
with a correction for errors.
You are advised to adjust this script for your used sextant.

You are also advised to make copies (and modifications) of the supplied samples
[starfixdata.stat.1.py](starfixdata.stat.1.py)
or [starfixdata.sea.py](starfixdata.sea.py) to support your workflow and observations. 
There are also Jupyter notebooks availabe, see below. 

The Nautical Almanac must be used manually to get the GP (ground point) of
your observations. Currently the almanacs of [2024](NAtrad(A4)_2024.pdf)
and [2025](NAtrad(A4)_2024.pdf)
are bundled in the repository in a digital version.
But you may of course use a hard-copy of the nautical almanac and these can be ordered
[here](https://www.amazon.com/s?i=stripbooks&rh=p_27%3AU.K.+Hydrographic&s=relevancerank&text=U.K.+Hydrographic&ref=dp_byline_sr_book_1).
New digital versions (for 2026 and onwards)
can be prepared using some GitHub code repositories,
such as [this one](https://github.com/aendie/SkyAlmanac-Py3).

The script sample [terrestrial.py](terrestrial.py)
can be used (and modified) if you would like to use your sextant as an aid in
terrestrial navigation.

In addition to the supplied scripts you may also run the code in
[Jupyter Notebooks](https://en.wikipedia.org/wiki/Project_Jupyter#Jupyter_Notebook).
[Jupyter can be installed in Pydroid](https://www.codementor.io/@olalekanrahman/how-to-access-jupyter-notebook-on-pydroid-1ckw13mtgz), 
and this allows for a convenient way to keep your workflow in an easily
managed web interface. The notebook web interface can be launched from specific
launch scipts (launch.xxx.py). 
