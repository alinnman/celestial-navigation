<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Using the Celeste app

## Table of Contents

1. [Read this first](#read_this_first)
    1. [Warranty and liability](#legal)
    1. [What is this app?](#what_is_it)
    1. [Screen Visibility and Navigation](#visibility)
    1. [Astrometric Data](#astrometry)
    1. [Feedback](#feedback)
        1. [Sound Feedback](#sound)
        1. [Messages](#messages)
    1. [Units of measurement](#units)
1. [Entering Data](#entering_data)
    1. [DRP Position](#drp_position)
    1. [Sight Quality](#drp_quality)
    1. [Sights](#star_fixes)
        1. [Selection of sight](#star_fix_selection)
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
1. [Plotting (NMEA 0183 interface)](#plotting)
    1. [Using standard Wi-Fi](#standard-wifi)
    1. [Using a Mobile Hotspot](#hotspot)
    1. [Specific app configuration](#app-configurations)
1. [Working with configurations](#configs)
1. [Installation and prerequisites](#installation-and-prerequisites)
1. [Tips for Testing (without a sextant?)](#testing_tips)
1. [Troubleshooting](#troubleshooting)
    1. [Entering Parameters](#entering-of-parameters)
    1. [Display Problems](#display-problems)
1. [More Information](#more_information)
1. [Licenses](#license)

## Read this first<a name="read_this_first"></a>

### Warranty and liability <a name="legal"></a>

The code is open source, and comes with **no warranty or liability**.
Read more in the
[license&nbsp;description](https://github.com/alinnman/celestial-navigation/blob/main/LICENSE).

### What is this app? <a name="what_is_it"></a>

This app is a tool for
[**celestial navigation**](https://en.wikipedia.org/wiki/Celestial_navigation),
i.e. finding your location with just a sextant and an accurate watch.
This works even if you lose internet connection and/or lose a
correct GPS signal. It can be used if you are entering a zone
of [jammed GPS]((https://en.wikipedia.org/wiki/GNSS_spoofing))
(which is more and more common today as part
of signals warfare) or simply as a backup for GPS.

The app takes care of **sight reduction**, i.e. converting
your sextant and clock readings into your position. This can
also be done with analog methods (printed papers, plotting tools)
and you are advised to at least
[get&nbsp;acquainted](https://youtube.com/playlist?list=PLWcAZhCRTMByW_XEQ0y0OlGmxO3jp0LyE&si=Vzb2agqKltBIXQlA)
with classical methods for celestial navigation.

The sight reduction can be viewed in three different ways:

1. The coordinate is presented in the app window.
1. [You can present a **map**](#presenting-a-map)
in the browser of your Android unit.
1. You can connect an [external device](#plotting)
(plotter, GPS unit or similar) and see the
coordinate on a map display.
This is useful for marine operations and/or when using outdoor handheld devices.

Testing this app can be done with a good **sextant** (which requires
careful preparation and adjustments). You can also test it with
"sextant simulators", see [below](#testing_tips).
You must also have access to a precise watch/clock (**chronometer**).

### Screen visibility and Navigation<a name="visibility"></a>

The app is configured as a full screen app. If your phone has
soft buttons (home, back, program list) they may become **hidden**
but you can access them through swiping upwards from the bottom.

The map and help functions invoke the default web browser.
Go back to the Celeste app with the back button.

### Astrometric Data<a name="astrometry"></a>

The app is pre-packaged with astrometric data from 2024 to 2029.
Entering dates outside this range will result in an error.
If you want to do sight reductions for historical or future
(before 2024 or beyond 2029) observations you can use the
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
You can press the checkbox <tt><b>"Don't show this message again"</b></tt>
to get rid of a particular message.
*Note: In order to re-instate all messages you can perform a sight reduction*
*with zero (0) active sights. Disable all three sights and click*
*"Perform Sight Reduction"*.

### Units of measurement <a name="units"></a>

The app uses the metric system for all input and presented data,
with the exception for distance which is measured in **nautical miles** (nm).
A nautical mile = 1.852 km = 1.151 miles.

## Entering data<a name="entering_data"></a>

### DRP position<a name="drp_position"></a>

DRP (Dead-Reckoning Position) is a rough estimation of your current position.
<br>For a **2-star** sight reduction it is used to select the correct
intersection point.
A successful 2-star sight reduction will produce two intersections,
and these can be located far away from each other. The DRP selects the
closest intersection.
<br>For a **3-star** sight reduction the DRP serves as a way to shorten the
execution time of finding an accurate result.
Normally you should have at least a rough estimation of your
actual position. Sometimes a grossly incorrect DRP (1000s km off)
may result in a failed sight reduction,
due to a conflicting false intersection (which can be located very far away).

At the top you see fields marked **Latitude** and **Longitude**.
Enter the latitude and longitude for your DRP in these fields.

The format used is "DD:MM:SS", "DD:MM" or "DD" (degrees, arcminutes, arcseconds)
Decimal values can be used. Use negative degrees for southern latitudes
or western longitudes.
("59", "-35", "-120:34" and "23:34.2" are valid inputs)

Note: The values of these fields are automatically updated if you execute
a successful sight reduction. The newly computed coordinate will be your
new DRP.

### Sight Quality<a name="drp_quality"></a>

Your sextant work and the selected DRP might not be very accurate.
If you suspect non-accurate input you may **increase** this threshold value.
The normal default is "100" (nm), and this will put on these restrictions:

* The intersections be must located at most 100 nm from each other in order
  to be included in the calculation.
* For a three sights: The DRP should be within 100 nm from each intersection.

If you are a beginner, or insecure about your readings you may increase
this threshold to a higher value, "1000" (nm) or more.

### Sights<a name="star_fixes"></a>

The input form contains input field for **three** observations (sights).

#### Selection of sight<a name="star_fix_selection"></a>

You need to specify two or three sights. The check box **Use this sight**
can be used to eliminate one sight if you only have two. You can even
use just one sight but this will result in a failed sight reduction, but
the map view (see below) can be used to present the actual circle of equal
altitude and this can assist you in your work.

#### Name of Object<a name="name"></a>

You have to select the **name** of the object.
Choose the Sun, one of the planets (venus, mars, jupiter or saturn)
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

Time is specified as "HH24:MM:SS" (Hours in 24-hour format. PM/AM not used.)

##### Timezone <a name="timezone"></a>

The last part is a timezone specification. Use "+00:00" or "Z" for GMT time.
Use "-HH:MM" for western timezones, and "+HH:MM" for eastern and specify
the difference vs GMT.

#### Index Error<a name="index_error"></a>

Specify the known **index error** of the sextant (in arcminutes).

#### Limb Correction<a name="limb_correction"></a>

Select between "UPPER", "CENTRAL" or "LOWER". Specifies the location/**limb**
of your sextant measurement, i.e. if you are measuring towards the center or
the lower or upper edge of the Moon or the Sun.
Note: This setting has no effect on stars,
and very little effect on planets. It is mainly used for the Moon or the Sun.

#### Observer Elevation<a name="observer_elevation"></a>

Specify your **elevation above the sea surface** (in meters),
or more specifically: the elevation of your **eye**.
Note: You can use a non-zero observer elevation only if you are **not** using an
artificial horizon.
*This setting takes care of the effect of the dip of the horizon*.

#### Temperature<a name="temperature"></a>

Specify the **temperature** (in degrees celsius).
*This setting affects the effects of atmospheric refraction*.

#### Temperature Gradient<a name="temperature_gradient"></a>

Specify how **temperature changes with increasing elevation**.
Default is "-0.01" (normal atmospheric conditions),
which means 1 degree celsius lower temperature for each 100 meters.
If you have temperature inversions you may increase this parameter to
a positive value ("0.1" for one degree temperature increase per 10 meters).
*This setting affects the effects of atmospheric refraction*.

#### Pressure<a name="pressure"></a>

Specify **air pressure** (in kPa). Normal air pressure is "101" (kPa).
*This setting affects the effects of atmospheric refraction*.

## Running a sight reduction<a name="running_sight_reduction"></a>

Press the button <tt><b>"Perform sight reduction!"</b></tt>.
The calculated position will be
presented in the field above the button. If you are using 3 stars you will
also see an estimation of the accuracy (in nautical miles) based on the
proximity of the three central intersections.
If the sight reduction fails you will see an error message
(and hear an error sound).
*The sight reduction does not depend on an active*
*internet or GPS connection.*

## Presenting a map<a name="presenting_map"></a>

Press the button <tt><b>"Show map!"</b></tt> to see a map representing the last
successful sight reduction. Even for failed sight reductions (and single sights)
you can display a map. This map can assist you in troubleshooting your
sextant readings.

The map interface requires a **browser** and
an **active internet connection** to present
full map displays with full detail.
Without an internet connection you will see
a much coarser map on a continental scale.
Use [plotting](#plotting) for active navigation and map display
without internet connection if you have a plotting device available.

<a name="browser-list"></a>

Different browsers behave differently. This is a list of test
results for some browsers, when tested on a Samsung Galaxy S23 unit.
(Other devices may show different results!)
We show support for online (internet active) and offline
(no internet). The background tile will not work properly when
offline (the base map), but older tiles may be cached.
We also see if it is possible to touch the minute grid
around the intersection point, since this can be a help for hybrid work
with paper charts.

| Browser | Works Online | Works Offline | Supports touch of minute gridlines |
| :------ | :----------- | :------------ | :--------------------------|
| MS Edge | YES          | YES           | YES                        |
| Samsung Internet | YES | YES           | YES                        |
| Chrome  | YES          | <span style="color: red;">NO</span>   | YES  |
| Firefox | YES          | YES           | <span style="color: red;">NO<span> |
| Opera   | <span style="color: red;">NO</span> | <span style="color: red;">NO</span> | <span style="color: red;">NO</span>  |
| DuckDuckGo | <span style="color: red;">NO</span> | <span style="color: red;">NO</span>  | <span style="color: red;">NO</span> |

*Note: For a map with a single sight the circle may not touch your*
*location precisely, if your DRP is inaccurate.*
*This is a result of the need for adjustments to the oblateness of the Earth.*

## Plotting (NMEA-0183 interface) <a name="plotting"></a>

### Using standard Wi-Fi connection <a name="standard-wifi"></a>

If you have access to a marine chart plotter or similar device you
can easily use the Celeste app as an information source for the
coordinate resolved by sight reduction. Connect the plotting device with
Celeste using the following connection parameters.

* Connection type : NMEA 0183
* IP adress : Use the adress you see in the bottom field of the app.  
* Port : 10110
* Protocol : TCP
* Direction : Input

If the presented ip address is "No network connection" then you need
to connect your phone/tablet to the Wi-Fi where your plotting device
is connected.

NOTE: This allows for use (detailed mapping) in scenarios where you lack
internet connection!

NOTE: The NMEA server is active for 20 seconds after you have performed
a successful sight reduction. You are advised to check for the position
update on your plotter, and maybe make an additional marker to save the
position.

### Using a Mobile Hotspot <a name="hotspot"></a>

Connecting through Wi-Fi as described above requires
a separate Wi-Fi **router**.
You may also try using a connection based on a Mobile Hotspot. Unfortunately
the exact way of doing this varies between vendors and device models,
making it difficult to provide exact instructions here.
If you use the Celeste device as a Mobile Hotspot server you need to
find the "router address" of it and attempt connect to it from your plotter
devices. Another option is using a second phone as a Mobile Hotspot server.

### Specific configurations for plot server <a name="app-configurations"></a>

You are recommended to
[turn off the battery saving functions](https://youtu.be/zCqOzQjQ97Q?si=loZCNxzxlBNL9CQP)
in android for Celeste if you use the plotter server functionality.
Otherwise the plotter device will lose connection after a while
if you hide the app.

## Working with configurations<a name="configs"></a>

Whenever you execute a succesful sight reduction the active configuration
(settings of all fields) will be saved on the **clipboard** (in JSON format).
You can use this to save your work easily, using a document solution of
your own choice. Just paste the contents into a suitable document
in another app, and save.

When you press the button <tt><b>"Paste Config"</b></tt> you can transfer
back a saved configuration from another app through the clipboard.
If the clipboard does not contain a valid configuration
you will hear an error sound, and the paste operation will be aborted.

## Workflow Tips<a name="workflow"></a>

The app is simple and contains no support for managing your
**configurations/parameters**. But through using the clipboard support
(see [above](#configs)) you can easily build your own support using
suitable tools
([Google Docs](https://en.wikipedia.org/wiki/Google_Docs) may be a solution).

Regarding **maps**: To save maps you are advised to use the print functionality
of your web browser, and use the "print to PDF" option if available.

If you use an **external plotter** you can use it to build
routes, document waypoints etc.

## Installation and Prerequisites<a name="installation"></a>

The application runs under Android versions 13-16.
A 64-bit ARM processor is required.
It is installed using APK files which you can
[find&nbsp;here](https://drive.google.com/drive/folders/1QFcncVEuCQMnls8lyNElDtpTYruMgI0D?usp=sharing).
There is also an ongoing test program on Google Play.
Concact the [author](mailto:august@linnman.net) if
you want to participate. This test program will lead to a release of the
app on Google Play.

See [this article](https://www.wikihow.com/Install-APK-Files-on-Android)
for info on how to install APK files on Android.

You will need a **Web Browser** for the mapping function.
See the [list&nbsp;here](#browser-list) for a list of browsers
and potential issues. But you will likely have to check and test
browsers yourself and choose the best one for your device and
configuration.

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

You can test the app with or without a sextant. We go through some options,
going from simple to more complex.

For simple sextant-free testing: Download the app
[GPS&nbsp;Anti&nbsp;Spoof](https://play.google.com/store/apps/details?id=com.clockwk.GPSAntiSpoof&pcampaignid=web_share)
or
[GPS&nbsp;Anti&nbsp;Spoof&nbsp;Pro](https://play.google.com/store/apps/details?id=com.clockwk.GPSAntiSpoofPro)
and use it to collect altitude values.
Make sure you use true sextant readings (Hs),
take careful notes on limb positions used,
and take notes on observed times.
Insert the readings into the Celeste app, and you can check your position.
Using three sights you should reach 1-2 nautical miles accuracy.

You can also use online star atlases such as
[Stellarium](https://en.wikipedia.org/wiki/Stellarium_(software))
but this is a little more time-consuming.

*For really ambitious sextant-free testing you can use official navigation*
*software such as NOVAS published by*
*[the Astronomical Tools department of the US Navy](https://aa.usno.navy.mil/software/novas_info)*

Another option is testing with a sextant app using the camera, such as
[CamSextant](https://play.google.com/store/apps/details?id=com.embarcadero.CamSextant&pcampaignid=web_share).
Note however that a mobile phone sextant app will never produce readings
accurate enough for precise navigation.

You may of course also borrow sights from other navigators, and you
can easily find groups on Facebook and other social media where
sextant/chronometer readings are shared. Another source is using
courses and training material.

And finally you can of
course test your own skills with a **real sextant**.

Do you have problems getting a correct sight reduction?
In such case just use two sights, by unselecting
<tt><b>"Use this sight"</b></tt> for one of the sights.
You can also use just one sight through unselecting the check
box for two sights. This will result in an error, but you
can watch the map output anyway afterwards.
Watch the map carefully to pinpoint any incorrect input.
Note: the map function is available also after a
failed sight reduction.

## Troubleshooting<a name="troubleshooting"></a>

### Entering of parameters<a name="entering_parameters"></a>

Entering parameters requires accuracy. Here is a list of common errors

* You forget to specify the correct **limb correction**. <br>
  This will typically result in a circle being about 15 nautical miles off and a
  bad sight reduction.
* Your time zone is off. <br>
  This will typically lead to failed sight reductions. <br>
  --> Carefully check the [timezone](#timezone)
* Various typos. <br>
  Names of celestial objects,
  timestamps and angles must be specfied correctly. <br>
  You will often get an error message in the coordinate output field. <br>
  --> Check the error message and correct your input.

### Display problems<a name="display_problems"></a>

If you use very large fonts, or wide spacing you may encounter problems in the
layout of the input form. From android system settings
[reduce the system font size](https://support.google.com/accessibility/android/answer/11183305?hl=en)
if these problems affect your work.

## More Information<a name="more_information"></a>

This app is part of an open-source software library for celestial navigation.
You can find
[more information here](https://github.com/alinnman/celestial-navigation).

## Licenses<a name="license"></a>

<tt>© August Linnman, 2025, email: august@linnman.net</tt><br>
<tt>[Celeste Software: MIT&nbsp;License](https://github.com/alinnman/celestial-navigation/blob/main/LICENSE)</tt><br>
<tt>[Licenses for used software libraries and services](https://github.com/alinnman/celestial-navigation/blob/main/OTHER-LICENSES.md)</tt><br>
<tt>[Splash Image](https://commons.wikimedia.org/wiki/File:180423-N-DL434-149_(27894845758).jpg?uselang=en#Licensing)</tt>
