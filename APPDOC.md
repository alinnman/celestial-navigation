<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Using the Celeste app

## Table of Contents

1. [About](#about)
1. [Entering Data](#entering_data)
    1. [DRP Position](#drp_position)
    1. [Star Fixes](#star-fixes)
        1. [Selection of star fix](#selection-of-star-fix)
        1. [Name of object](#name-of-object)
        1. [Altitude](#altitude-hs)
        1. [Artificial Horizon](#artificial-horizon)
        1. [Time](#time)
        1. [Index Error](#index-error)
        1. [Limb Correction](#limb-correction)
        1. [Observer Elevation](#observer-elevation)
        1. [Temperature](#temperature)
        1. [Temperature Gradient](#temperature-gradient)
        1. [Pressure](#pressure)
1. [Running a sight reduction](#running-a-sight-reduction)
1. [Presenting a map](#presenting-a-map)
1. [Installation and prerequisites](#installation-and-prerequisites)
1. [Tips for testing](#tips-for-testing)
1. [More information](#more_information)
1. [License](#license)

## About the screen, and how to switch window<a name="about"></a>

The app is configured as a full screen app. If your phone has
soft buttons (home, back, program list) you can access them
through swiping upwards from the bottom.

The map and help functions invoke the default web browser.

## Entering data<a name="entering_data"></a>

### DRP position<a name="drp_position"></a>

DRP (Dead-Reckoning Position) is a rough estimation of your current position.
<br>For a **2-star-fix** sight reduction it is used to select the correct
intersection point.
(A 2-star-fix will alway produce two intersections,
and these can be located far away from each other)
<br>For a **3-star-fix** sight reduction the DRP serves as a way to shorten the
execution time of finding an accurate result
(and in rare cases to eliminate false intersections).
This effect is however small, but you are advised to
use DRP values anyway. Normally you have at least a rough estimation of your
actual position.

At the top you see fields marked **DRP Latitude** and **DRP Longitude**.
Enter the latitude and longitude for your DRP in these fields.

### Star Fixes<a name="star_fixes"></a>

The input form contains input field for **three** observations (star fixes).

#### Selection of star fix<a name="star_fix_selection"></a>

You need to specify two or three star fixes. The check box **Use this sight**
can be used to eliminate one star fix if you only have two. You can even
use just one star fix but this will result in a failed sight reduction, but
the map view (see below) can be used to present the actual circle of equal
altitude and this can assist you in your work.

#### Name of object<a name="name"></a>

You have to select the **name** of the object.
Choose one of the planets (mercury, venus, mars, jupiter or saturn)
or a selected **navigational star**. You find a
[list&nbsp;of&nbsp;these&nbsp;stars&nbsp;here](https://github.com/alinnman/celestial-navigation/blob/main/README.md#navstars).

#### Altitude (Hs)<a name="altitude"></a>

The **altitude** is the angle between the object and the horizon,
as measured by a sextant (Hs).
It is specified in degrees, minutes and seconds in this format:
"DD:MM:SS". You may omit seconds and minutes,
and specifiy just "DD:MM" or "DD".

#### Artificial Horizon<a name="artificial_horizon"></a>

Check this box if you use an **artificial horizon**. The altitude value will
be divided by 2.

#### Time<a name="time"></a>

This is the **time** for the observation. It is specified in the ISO 8601
format. A valid date string is "2025-04-23 22:33:05+00:00".
The last part is a timezone specification. Use "+00:00" for GMT time.
Use "-HH:MM" for western timezones, and "+HH:MM" for eastern and specify
the difference vs GMT.

#### Index Error<a name="index_error"></a>

Specify the known **index error** of the sextant (in arcminutes).

#### Limb Correction<a name="limb_correction"></a>

Select between "UPPER", "CENTRAL" or "LOWER". Specifies the location/**limb**
of your measurement. Note: This setting has no effect on stars,
and very little effect on planets. It is mainly used for the Moon or the Sun.

#### Observer Elevation<a name="observer_elevation"></a>

Specify your **elevation above sea level** (in meters)
Note: You can use a non-zero observer height only if you are not using an
artificial horizon.

#### Temperature<a name="temperature"></a>

Specify the **temperature** (in degrees celsius). This setting affects the
effects of atmospheric refraction.

#### Temperature Gradient<a name="temperature_gradient"></a>

Specify how **temperature changes with increasing elevation**.
Default is "-0.01",
which means 1 degree celsius lower temperature for each 100 meters.
If you have temperature inversions you may increase this parameter to
a positive value ("0.1" for one degree temperature increase per 10 meters).

#### Pressure<a name="pressure"></a>

Specify **air pressure** (in kPa). Normal air pressure is "101".

## Running a sight reduction<a name="running_sight_reduction"></a>

Press the button <tt>"Perform sight reduction!"</tt>.
The calculated position will be
presented in the underlying field. If the sight reduction fails you will see
an error message. *The sight reduction does not depend on an active*
*internet or GPS connection.*

## Presenting a map<a name="presenting_map"></a>

Press the button <tt>"Show map!"</tt> to see a map representing the last
successful sight reduction. Even for failed sight reductions (and single sights)
you can display a map. This map can assist you in troubleshooting your
sextant readings.
*The map interface requires an active internet connection.*

## Installation and prerequisites<a name="installation"></a>

The application runs under Android 9 or higher. It is installed using
APK files which you can
[find&nbsp;here](https://drive.google.com/drive/folders/1QFcncVEuCQMnls8lyNElDtpTYruMgI0D?usp=sharing).

See [this article](https://www.wikihow.com/Install-APK-Files-on-Android)
for info on how to install APK files on Android.

## Tips for testing<a name="testing_tips"></a>

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
Note however that a mobile phone will never produce readings accurate enough for
precise navigation.

## More information<a name="more_information"></a>

This app is part of a software library for celestial navigation.
You can find
[more information here](https://github.com/alinnman/celestial-navigation)

## License<a name="license"></a>

<tt>© August Linnman, 2025, email: august@linnman.net</tt><br>
<tt>[MIT&nbsp;License](https://github.com/alinnman/celestial-navigation/blob/main/LICENSE)</tt>
