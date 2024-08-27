# Installation

The code is installed using just a file copy of the python (.py)
files to a suitable directory.
No additional libraries are necessary.
Python 3.11 is required.
This [link](https://github.com/alinnman/celestial-navigation/archive/refs/heads/main.zip)
will download all code in a ZIP file.

The python scripts could be installed in
[PyDroid](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3)
to allow for use on an Android mobile phone
(with no need for internet access).
To aid in installation a good file browser is recommended
(for copying and decompressing of ZIP files) such as [Cx File Explorer](https://play.google.com/store/apps/details?id=com.cxinventor.file.explorer&pcampaignid=web_share)

The script [starfix.py](starfix.py) contains the core routines.

The script [calibration.py](calibration.py) contains a setup of a used sextant,
with a correction for errors.
You are advised to adjust this script for your used sextant.

You are also advised to make copies (and modifications) of the supplied samples
[starfixdata.chicago.py](starfixdata.chicago.py) or [starfixdata.sea.py]
(starfixdata.sea.py) to support your workflow and observations.

The Nautical Almanac must be used manually to get the GP (ground point) of your observations.
Currently the almanac of 2024 is bundled in the repository in a digital version.
But you may of course use a hard-copy of the nautical almanac and these can be ordered
[here](https://www.amazon.com/Nautical-Almanac-2024-Year/dp/1951116690/ref=sr_1_1?crid=1IAIAP3U59XSX&dib=eyJ2IjoiMSJ9.d3xFA2pQJx8dny0H5kmiZLliYeANWFYB9BZ8He317-pq7X_P5hjJ-aQ5Ir7tAsTHKBmmclCDUVqueJoljDZ8pMVLTCGbF98Xnd4rvuET9FSOXDx-5zcZQXjvqMduNM4eVj7NjN3sq_oBYGavC31cYfErZ1TXimJXSvkgVdloz9g-meALl0_BZklDiJFh33wnJs-aba7SBQyP94c-7bBPn4qIhPGFOMmTE3Y0DZp3CgM.ZlExL1J_IC-osoQXy2XKkMZ3A4CllQRdgOp5Cy7_II8&dib_tag=se&keywords=nautical+almanac&qid=1718006483&sprefix=nautical+almanac%2Caps%2C351&sr=8-1).
New digital versions (for 2025 and onwards)
can be prepared using some GitHub code repositories,
and I used [this one](https://github.com/aendie/SkyAlmanac-Py3).

The script sample [terrestrial.landfall.py](terrestrial.landfall.py)
can be used (and modified) if you would like to use your sextant as an aid in
terrestrial navigation.
