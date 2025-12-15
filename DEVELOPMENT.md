<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Some notes on development

## Choice of operating system

Almost all development has sofar been been made on Linux (Ubuntu 24.04 LTS).
You may try using MS Windows too, but be prepared for bugs.

## A virtual environment (venv)

This code was developed with
[VSCode](https://en.wikipedia.org/wiki/Visual_Studio_Code)
on a Linux (Ubuntu 24.04 LTS) machine.

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
    pip install kivy

After having created this you can use VSCode to define
this as your python environment using Ctrl-Shift-P
and selecting this as your Python interpreter.

NOTE: In order to support app development and distribution using
the buildozer tool (see below) I have also prepared an alternative
virtual environment (.venv-buildozer).

    python -m venv .venv-buildozer
    source .venv/bin/activate

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

The file [main.py](main.py) contains a mobile
app (Celeste) built on the Kivy framework. It can be used as a starter point
for developing Android or iOS apps.

A script solution based on [buildozer](https://github.com/kivy/buildozer)
is available and it produces a working/running app (APK or AAB file).

In order to use this you need to follow the installation instructions carefully.
Be careful to keep your work in the virtual environment. See above.

Building the app is done using these commands:

    source .venv-buildozer/bin/activate
    ./build.sh release

This executes the buildozer script and some other preparation steps.
The virtual environment .venv-buildozer needs to be prepared beforehand.

Note however that you probably need to fine-tune and adjust your enviroment
carefully before being able to run the app build script successfully.
For deployment vs later Android SDK levels you may need to carefully check
the [python-for-android](https://github.com/kivy/python-for-android)
setup, which may require forking and working with
detailed configuration.

Also note that the current buildozer setup sofar has only been tested in
a Python 3.11 environment.

## App testing

See [this item](https://github.com/alinnman/celestial-navigation/discussions/29)
for a description of app testing and the test program for Google Play.

## Test the NMEA-0183 interface

### Install plotter software

A good and cheap (free) plotter application for the PC is OpenCPN.
For more information [see here](https://opencpn.org/).
Install the application on your PC and a selection of usable charts.

### Setup a test workbench with OpenCPN

Now configure a debug session between the phone and the PC.
Start the Celeste App on your phone.

* Make sure you have the ADB utility installed on your PC
(bundled with Android Studio).
* Download the [SCRCPY utility](https://scrcpy.org/) on your PC.
* Configure the phone to use debugging over wi-fi (Developer settings).
* Check the ip-adress of your phone in the Celeste app window.
* Run the command <tt>adb pair \<ip\>:\<port\> --stay-alive</tt> on your PC.
* Check the passcode on your phone and enter it on your PC.
* The ADB connection is now live.
* Now run the command "srcpy" on your PC. A terminal window for the phone
  will now appear on the PC screen.

### Other hardware

You can now test various sight reductions and see how the position marker moves
in the OpenCpn plotter. In some cases the marker will not move until you do a
small zoom in or out of the plotter window.

You may of course also test a setup with another marine plotter
(Garmin, RayMarine etc).
If you find errors or problems then don't hesitate to get in touch
with this project
(Pull Request or interaction with this
[issue](https://github.com/alinnman/celestial-navigation/issues/37)).

### Test scripts for plotter interface

The mobile app has support for sending position data to a chart
plotter using the [NMEA-0183](https://en.wikipedia.org/wiki/NMEA_0183)
interface. In order to test this you may use these test scripts:

* [plotclient_test.py](plotclient_test.py)

    This emulates a chart plotter.

* [plotserver.py](plotserver.py)

    This emulates the position updates performed by the app.

## Generation of machine-readable nautical almanac

The machine-readable nautical almanac is generated by
[this package](https://github.com/alinnman/SkyAlmanac-Py3).

You start generation with this command and input:

    $python skyalmanac.py 

      What do you want to create?:

        1   Nautical Almanac      (for a day/month/year) <== SELECT THIS
        2   Sun tables only       (for a day/month/year)
        3   Event Time tables     (for a day/month/year)
        4   Lunar Distance tables (for a day/month/year)
        5   Lunar Distance charts (for a day/month)
        6   "Increments and Corrections" tables (static data)

       Enter as numeric digits (or 'x' for a brief sample):

        - starting date as 'DDMMYYYY'
        - or just 'YYYY' (for a whole year) 
        - or 'YYYY-YYYY' (for first and last year) <== SELECT THIS
        - or just 'MM' (01 - 12) for the current or a future month
        - or '-MM' for a previous month (e.g. '-02' is last February)
        - or 'x' for 6 days from today
        - nothing for the current day

      What table style is required?:

        t   Traditional
        m   Modern <== SELECT THIS 

After generation (can take a while, expect at least 20 minutes per year
generated) you get a selection of
.CSV files. You now need to create a manifest file
<tt>range.properties</tt>:

    [Limits]
    From=2024
    To=2030

Make sure the "From" and "To" values correspond to the range you
specified in the script execution.

When ready copy the .CSV files and the manifest file to the
<tt>sample_data</tt> folder.
