<!---
    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
-->

# Using the Celeste app

## Entering data

### DRP position

DRP (Dead-Reckoning Position) is a rough estimation of your current position.
<br>For a **2-star-fix** sight reduction it is used to select the correct
intersection point.
(A 2-star-fix will alway produce two intersections,
and these can be located far away from each other)
<br>For a **3-star-fix** sight reduction the DRP serves as a way to shorten the
execution time of finding an accurate result.
This effect is however small, but you are advised to
use DRP values anyway. Normally you have at least a rough estimation of your
actual position.

At the top you see fields marked **DRP Latitude** and **DRP Longitude**.
Enter the latitude and longitude for your DRP in these fields.

### Star fixes

The input form contains input field for **three** observations (star fixes).

#### Selection of star fix

You need to specify two or three star fixes. The check box **Use this sight**
can be used to eliminate one star fix if you only have two. You can even
use just one star fix but this will result in a failed sight reduction, but
the map view (see below) can be used to present the actual circle of equal
altitude and this can assist you in your work.

#### Name of object

You have to select the **name** of the object.
Choose one of the planets (mercury, venus, mars, jupiter or saturn)
or a selected **navigational star**. You find a
[list&nbsp;of&nbsp;these&nbsp;stars&nbsp;here](https://github.com/alinnman/celestial-navigation/blob/main/README.md#navstars).

#### Altitude

The **altitude** is the angle between the object and the horizon,
as measured by a sextant.
It is specified in degrees, minutes and seconds in this format:
"DD:MM:SS". You may omit seconds and minutes,
and specifiy just "DD:MM" or "DD".

#### Artificial Horizon

Check this box if you use an **artificial horizon**. The altitude value will
be divided by 2.

#### Time

This is the **time** for the observation. It is specified in the ISO 8601
format. A valid date string is "2025-04-23 22:33:05+00:00".
The last part is a timezone specification. Use "+00:00" for GMT time.
Use "-HH:MM" for western timezones, and "+HH:MM" for eastern and specify
the difference vs GMT.

#### Index Error (optional)

Specify the known **index error** of the sextant (in arcminutes).

#### Limb Correction (optional)

Select between "UPPER", "CENTRAL" or "LOWER". Specifies the location/**limb**
of your measurement. Note: This setting has no effect on stars,
and very little effect on planets. It is mainly used for the Moon or the Sun.

#### Observer Height (optional)

Specify your **elevation above sea level** (in meters)
Note: You can use a non-zero observer height only if you are not using an
artificial horizon.

#### Temperature (optional)

Specify the **temperature** (in degrees celsius). This setting affects the
effects of atmospheric refraction.

#### Temperature Gradient (optional)

Specify how **temperature changes with increasing elevation**.
Default is "-0.01",
which means 1 degree celsius lower temperature for each 100 meters.
If you have temperature inversions you may increase this parameter to
a positive value ("0.1" for one degree temperature increase per 10 meters).

#### Pressure (optional)

Specify **air pressure** (in kPa). Normal air pressure is "101".

## Running a sight reduction

Press the button <tt>"Perform sight reduction!"</tt>.
The calculated position will be
presented in the underlying field. If the sight reduction fails you will see
an error message. *The sight reduction does not depend on an active*
*internet connection.*

## Presenting a map

Press the button <tt>"Show map!"</tt> to see a map representing the last
successful sight reduction. Even for failed sight reduction (and single sights)
you will see a map. This map can assist you in troubleshooting your
sextant readings.
*The map interface requires an active internet connection.*

## Installation and prerequisites

The application runs under Android 13 or higher. It is installed using
APK files which you can
[find&nbsp;here](https://drive.google.com/drive/folders/1QFcncVEuCQMnls8lyNElDtpTYruMgI0D?usp=sharing).

See [this article](https://www.wikihow.com/Install-APK-Files-on-Android)
for info on how to install APK files on Android.

## More information

This app is part of a software library for celestial navigation.
You can find
[more information here](https://github.com/alinnman/celestial-navigation)

## License

<tt>© August Linnman, 2025, email: august@linnman.net</tt><br>
<tt>[MIT&nbsp;License](https://github.com/alinnman/celestial-navigation/blob/main/LICENSE)</tt>
