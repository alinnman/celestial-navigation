<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Using the Celeste app

## Table of Contents

1. [Read this first](#read_this_first)
    1. [What is this app?](#what_is_it)
    1. [Screen Visibility and Navigation](#visibility)
    1. [Astrometric Data](#astrometry)
    1. [Feedback](#feedback)
        1. [Sound Feedback](#sound)
        1. [Messages](#messages)
1. [Entering Data](#entering_data)
    1. [DRP Position](#drp_position)
    1. [Star Fixes](#star-fixes)
        1. [Selection of star fix](#selection-of-star-fix)
        1. [Name of Object](#name-of-object)
        1. [Altitude](#altitude-hs)
        1. [Artificial Horizon](#artificial-horizon)
        1. [Time parameters](#time-parameters)
            1. [Date](#date)
            1. [Time](#time)
            1. [Timezone](#timezone)
        1. [Index Error](#index-error)
        1. [Limb Correction](#limb-correction)
        1. [Observer Elevation](#observer-elevation)
        1. [Temperature](#temperature)
        1. [Temperature Gradient](#temperature-gradient)
        1. [Pressure](#pressure)
1. [Running a sight reduction](#running-a-sight-reduction)
1. [Presenting a Map](#presenting-a-map)
1. [Working with configurations](#configs)
1. [Installation and prerequisites](#installation-and-prerequisites)
1. [Tips for Testing (without a sextant?)](#testing_tips)
1. [More Information](#more_information)
1. [License](#license)

## Read this first<a name="read_this_first"></a>

### What is this app? <a name="what_is_it"></a>

This app is a tool for
[**celestial navigation**](https://en.wikipedia.org/wiki/Celestial_navigation),
i.e. finding your location with just a sextant and an accurate watch.
This works even if you lose internet connection and/or lose a
correct GPS signal. It can be used if you are entering a zone
of jammed GPS (which is more and more common today as part
of signals warfare) or simply as a backup for GPS.

The app takes care of **sight reduction**, i.e. converting
your sextant and clock readings into your position. This can
also be done with analog methods (printed papers, plotting tools)
and you are advised to at least
[get&nbsp;acquainted](https://youtube.com/playlist?list=PLWcAZhCRTMByW_XEQ0y0OlGmxO3jp0LyE&si=Vzb2agqKltBIXQlA)
with classical methods for celestial navigation.

Testing this app can be done with a good **sextant** (which requires
careful preparation and adjustments). You can also test it with
"sextant simulators", see [below](#testing_tips).
You must also have access to a precise watch (**chronometer**).

### Screen visibility and Navigation<a name="visibility"></a>

The app is configured as a full screen app. If your phone has
soft buttons (home, back, program list) they may become **hidden**
but you can access them through swiping upwards from the bottom.

The map and help functions invoke the default web browser.
Go back to the Celeste app with the back button.

### Astrometric Data<a name="astrometry"></a>

The app is pre-packaged with astrometric data from 2024 to 2028.
Entering dates outside this range will result in an error.
If you want to do sight reductions for historical or future (beyond 2028)
observations you can use the
[script&nbsp;solution](https://github.com/alinnman/celestial-navigation/blob/main/INSTALL.md).

### Feedback <a name="feedback"></a>

#### Sound Feedback <a name="sound"></a>

The app is simple and designed for use in a noisy environment
(typically a boat). Sound effects are used for feedback instead of subtle
visual effects. The sounds are loud and you are advised to
regulate the volume button accordingly.

#### Messages <a name="messages"></a>

When you run the app for the first time you will see messages appear,
explaining briefly the mechanisms and what to expect and do.
You can press the checkbox <tt>Don't show this message again</tt>
to get rid of a particular message.
*Note: In order to re-instate the messages you can perform a sight reduction*
*with zero (0) active sights*.

## Entering data<a name="entering_data"></a>

### DRP position<a name="drp_position"></a>

DRP (Dead-Reckoning Position) is a rough estimation of your current position.
<br>For a **2-star-fix** sight reduction it is used to select the correct
intersection point.
(A successful 2-star-fix sight reduction will produce two intersections,
and these can be located far away from each other)
<br>For a **3-star-fix** sight reduction the DRP serves as a way to shorten the
execution time of finding an accurate result
(and in rare cases to eliminate false intersections).
This effect is however small, but you are advised to
use DRP values anyway. Normally you have at least a rough estimation of your
actual position.

At the top you see fields marked **DRP Latitude** and **DRP Longitude**.
Enter the latitude and longitude for your DRP in these fields.

Note: The values of these fields are automatically updated if you execute
a successful sight reduction.

### Star Fixes<a name="star_fixes"></a>

The input form contains input field for **three** observations (star fixes).

#### Selection of star fix<a name="star_fix_selection"></a>

You need to specify two or three star fixes. The check box **Use this sight**
can be used to eliminate one star fix if you only have two. You can even
use just one star fix but this will result in a failed sight reduction, but
the map view (see below) can be used to present the actual circle of equal
altitude and this can assist you in your work.

#### Name of Object<a name="name"></a>

You have to select the **name** of the object.
Choose the Sun, one of the planets (mercury, venus, mars, jupiter or saturn)
or a selected **navigational star**. You find a
[list&nbsp;of&nbsp;these&nbsp;stars&nbsp;here](https://github.com/alinnman/celestial-navigation/blob/main/README.md#navstars).

The name of the entered celestial object isn't case-sensitive.

#### Altitude (Hs)<a name="altitude"></a>

The **altitude** is the angle between the object and the horizon,
as measured by a sextant (Hs).
It is specified in degrees, arcminutes and arcseconds in this format:
"DD:MM:SS". You may omit arcseconds and arcminutes,
and specifiy just "DD:MM" or "DD". Decimal values may be used,
e.g. "23:15.2" or "33:21:5.6".

#### Artificial Horizon<a name="artificial_horizon"></a>

Check this box if you use an **artificial horizon**. The altitude value will
be divided by 2. (*An artificial horizon is a simple mirror, often built using*
*a water or metal (mercury) surface.*
*It can be used whenever you don't have access*
*to a physical horizon*).

#### Time parameters<a name="timeparameters"></a>

These specify the **time** for the observation.
Time parameters are based on the
[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
format.

##### Date<a name="date"></a>

Date is specified as "YYYY-MM-DD"

##### Time<a name="time"></a>

Time is specified as "HH24:MM:SS"

##### Timezone <a name="timezone"></a>

The last part is a timezone specification. Use "+00:00" or "Z" for GMT time.
Use "-HH:MM" for western timezones, and "+HH:MM" for eastern and specify
the difference vs GMT.

#### Index Error<a name="index_error"></a>

Specify the known **index error** of the sextant (in arcminutes).

#### Limb Correction<a name="limb_correction"></a>

Select between "UPPER", "CENTRAL" or "LOWER". Specifies the location/**limb**
of your sextant measurement. Note: This setting has no effect on stars,
and very little effect on planets. It is mainly used for the Moon or the Sun.

#### Observer Elevation<a name="observer_elevation"></a>

Specify your **elevation above the horizon** (in meters)
Note: You can use a non-zero observer elevation only if you are not using an
artificial horizon.
*This setting takes care of the effect of the dip of the horizon*.

#### Temperature<a name="temperature"></a>

Specify the **temperature** (in degrees celsius). *This setting affects the
effects of atmospheric refraction*.

#### Temperature Gradient<a name="temperature_gradient"></a>

Specify how **temperature changes with increasing elevation**.
Default is "-0.01",
which means 1 degree celsius lower temperature for each 100 meters.
If you have temperature inversions you may increase this parameter to
a positive value ("0.1" for one degree temperature increase per 10 meters).
*This setting affects the effects of atmospheric refraction*.

#### Pressure<a name="pressure"></a>

Specify **air pressure** (in kPa). Normal air pressure is "101".
*This setting affects the effects of atmospheric refraction*.

## Running a sight reduction<a name="running_sight_reduction"></a>

Press the button <tt>"Perform sight reduction!"</tt>.
The calculated position will be
presented in the underlying field. If the sight reduction fails you will see
an error message (and hear an error sound).
*The sight reduction does not depend on an active*
*internet or GPS connection.*

## Presenting a map<a name="presenting_map"></a>

Press the button <tt>"Show map!"</tt> to see a map representing the last
successful sight reduction. Even for failed sight reductions (and single sights)
you can display a map. This map can assist you in troubleshooting your
sextant readings.

*Note: For a map with a single sight the circle may not touch your*
*location precisely, if your DRP is inaccurate.*
*This is a result of the need for adjustments to the oblateness of the Earth.*

*The map interface requires an active internet connection to present*
*full map displays. Without an internet connection you will only see*
*the circles of equal altitude, local coordinate grid, GP:s and intersections*

## Working with configurations<a name="configs"></a>

Whenever you execute a succesful sight reduction the active configuration
(settings of all fields) will be saved on the **clipboard** (in JSON format).
You can use this to save your work easily, using a document solution of
your own choice. Just paste the contents into a suitable document
in another app, and save.

When you press the button <tt>Paste Config</tt> you can transfer back a saved
configuration from another app through the clipboard.
If the clipboard does not contain a valid configuration
you will hear an error sound.

## Workflow Tips<a name="workflow"></a>

The app is simple and contains no support for managing your
**configurations/parameters**. But through using the clipboard support
(see [above](#configs)) you can easily build your own support using
suitable tools
([Google Docs](https://en.wikipedia.org/wiki/Google_Docs) may be a solution).

Regarding **maps**: To save maps you are advised to use the print functionality
of your web browser, and use the "print to PDF" option if available.

## Installation and Prerequisites<a name="installation"></a>

The application runs under Android 13 or higher.
A 64-bit ARM processor is required.
It is installed using APK files which you can
[find&nbsp;here](https://drive.google.com/drive/folders/1QFcncVEuCQMnls8lyNElDtpTYruMgI0D?usp=sharing).
There is also an ongoing test program on Google Play.
Concact the [author](mailto:august@linnman.net) if
you want to participate. This test program will lead to a release of the
app on Google Play.

See [this article](https://www.wikihow.com/Install-APK-Files-on-Android)
for info on how to install APK files on Android.

Celeste is built on the P4A platform
([Python for Android](https://github.com/kivy/python-for-android))
and this is a convenient way of distributing apps coded in Python.
The underlying code (and many used libraries) are written in Python
and this has motivated this implementation choice.

There are however some implications from this:

* The memory requirement is about 200 MB. Make sure your phone or tablet has
enough memory.

* On modern phones or tablets the execution speed is
good, but you may find the app a litte "sluggish" on older phones/tablets.

## Tips for Testing (without a sextant?)<a name="testing_tips"></a>

Download the app
[GPS&nbsp;Anti&nbsp;Spoof](https://play.google.com/store/apps/details?id=com.clockwk.GPSAntiSpoof&pcampaignid=web_share)
and use it to collect altitude values.
Make sure you use true sextant readings (Hs),
take careful notes on limb positions used,
and take notes on observed times.
Insert the readings into the Celeste app, and you can check your position.
Using three fixes you should reach 1-2 nautical miles accuracy.

You can also use online star atlases such as
[Stellarium](https://en.wikipedia.org/wiki/Stellarium_(software))
but this is a little more time-consuming.

Another option is testing with a sextant app, such as
[CamSextant](https://play.google.com/store/apps/details?id=com.embarcadero.CamSextant&pcampaignid=web_share).
Note however that a mobile phone sextant app will never produce readings
accurate enough for precise navigation.

Do you have problems getting a correct sight reduction?
In such case just use two fixes (sights), by unselecting
<tt>Use this sight</tt> for one of the sights.
You can also use just one sight through unselecting the check
box for two sights.
Watch the map carefully to pinpoint any incorrect input.
Also note that the map function is available also after a
failed sight reduction.

## More Information<a name="more_information"></a>

This app is part of an open-source software library for celestial navigation.
You can find
[more information here](https://github.com/alinnman/celestial-navigation).

## License<a name="license"></a>

<tt>© August Linnman, 2025, email: august@linnman.net</tt><br>
<tt>[MIT&nbsp;License](https://github.com/alinnman/celestial-navigation/blob/main/LICENSE)</tt>
