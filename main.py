''' 
    Basic app for celestial navigation. 
    Based on Kivy, and runnable on Android.
    See APPDOC.md for more info.
    See buildozer.spec and build.sh for deployment information. 

    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
    
    Modified with font awareness support
'''
# pylint: disable=C0413
# pylint: disable=C0411
from multiprocessing import freeze_support
from queue import Queue, Empty
import threading
from types import NoneType
import importlib
import socket
import time
from starfix import LatLonGeodetic, SightCollection, Sight, \
    get_representation, IntersectError, get_folium_load_error, show_or_display_file, \
    is_windows, exit_handler, start_http_server, parse_angle_string
import os
import json
import kivy
kivy.require('2.0.0')
from kivy.core.audio import SoundLoader
# Sound has to be loaded now directly
# This seems to be due to a Kivy bug. Delaying sound loading leads to UI crashes.
click_sound = SoundLoader.load('./sounds/mouse-click.mp3')
error_sound = SoundLoader.load('./sounds/error.mp3')
kivy.config.Config.set('graphics', 'resizable', False)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from kivy.app import App, runTouchApp
from kivy.core.clipboard import Clipboard # Import the Clipboard module
from kivy.core.window import Window
from kivy.utils import platform

from functools import partial
from plotserver import NMEAServer

# pylint: disable=W0702
try:
    # Activate android libraries, needed for correct webbrowser functionality
    importlib.import_module("android")
# pylint: disable=W0702
except:
    pass

Window.softinput_mode = 'below_target'

# pylint: enable=C0413
# pylint: enable=C0411

def str2bool(v):
    ''' Simple conversion from bool to string '''
    return v.lower() in ("yes", "true", "t", "1")

Window.clearcolor = (0.4, 0.4, 0.4, 1.0)

DEBUG_FONT_HANDLING = False

# Font scale configuration class
class FontAwareConfig:
    """Configuration class that adapts to system font scaling"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FontAwareConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        #if self._initialized:
        #    return
        self.font_scale = self.detect_font_scale()
        self.config = self.load_adaptive_config()
        self._initialized = True

        # Show warning if font scale is very large
        if DEBUG_FONT_HANDLING:
            if self.font_scale > 1.3:
                Clock.schedule_once(self.show_font_scale_warning, 1.0)

    def detect_font_scale(self):
        """Detect system font scale"""
        if platform == 'android':
            try:
# pylint: disable=E0401
# pylint: disable=C0415
                from android import mActivity # type: ignore
# pylint: disable=W0611
                from jnius import autoclass # type: ignore
# pylint: enable=W0611
# pylint: enable=E0401
# pylint: enable=C0415

                context = mActivity
                resources = context.getResources()
                configuration = resources.getConfiguration()
                font_scale = configuration.fontScale
                print(f"Detected system font scale: {font_scale}")
                return font_scale
# pylint: disable=W0718
            except Exception as e:
# pylint: enable=W0718
                print(f"Could not detect font scale: {e}")
        return 1.0

    def load_adaptive_config(self):
        """Load configuration based on font scale"""
        base_config = {
            'base_element_height': 35,
            'base_spacing': 5,
            'base_padding': 5,
            'max_font_scale': 1.4,  # Prevent complete UI breakdown
            'font_size_reduction': 0.85  # Reduce font size for very large scales
        }

        # Calculate effective scale (capped to prevent UI breaking)
        effective_scale = min(self.font_scale, base_config['max_font_scale'])

        # Apply font size reduction for very large scales
        font_reduction = 1.0
        if self.font_scale > 1.25:
            font_reduction = base_config['font_size_reduction']

        adapted_config = {
            'element_height': int(base_config['base_element_height'] * effective_scale),
            'spacing': int(base_config['base_spacing'] * effective_scale),
            'padding': int(base_config['base_padding'] * effective_scale),
            'font_scale_factor': font_reduction,
            'use_scroll': self.font_scale > 1.15,  # Force scroll for large fonts
            'effective_scale': effective_scale
        }

        return adapted_config

    def get_element_height(self):
        """Get adaptive element height"""
        return dp(self.config['element_height'])

    def get_spacing(self):
        """Get adaptive spacing"""
        return dp(self.config['spacing'])

    def get_padding(self):
        """Get adaptive padding"""
        return dp(self.config['padding'])

    def get_font_size_factor(self):
        """Get font size reduction factor"""
        return self.config['font_scale_factor']

    def should_use_scroll(self):
        """Whether to force scrolling for this font scale"""
        return self.config['use_scroll']

    def show_font_scale_warning(self): #, dt):
        """Show warning for very large font scales"""
        if hasattr(StarFixApp, 'message_popup'):
            StarFixApp.message_popup(
                f"[b]Large Font Scale Detected[/b]\n\n"
                f"Your system font size is set to {self.font_scale:.1f}x normal size.\n"
                f"The app layout has been optimized for better readability.\n\n"
                f"If you experience any layout issues, consider reducing\n"
                f"your system font size in Android Settings.",
                "FONT_SCALE_WARNING"
            )

# Initialize global font config
font_config = FontAwareConfig()

# Set default color and sizes of the form with font awareness
USE_KV = True
if USE_KV:
    # Generate adaptive KV string based on font scale
    def generate_adaptive_kv():
        ''' Generated adaptive KV string '''
# pylint: disable=W0612
        element_height = font_config.get_element_height()
# pylint: enable=W0612
        spacing = font_config.get_spacing()
        padding = font_config.get_padding()
        font_factor = font_config.get_font_size_factor()

        return f"""
<FormSection@GridLayout>:
    cols: 2
    spacing: {spacing}
    padding: {padding}
    canvas.before:
        Color:
            rgba: 0.35, 0.35, 0.35, 1
        Rectangle:
            pos: self.pos
            size: self.size

<MyLabel>:
    size_hint_x: 0.4
    halign: 'right'
    valign: 'middle'
    padding: dp(1)
    text_size: self.width, None
    size_hint_x : 0.45
    font_size: sp(14 * {font_factor})

<MyTextInput>:
    size_hint_x: 0.8
    valign: 'middle'
    multiline: False
    font_size: sp(14 * {font_factor})

<LimbDropDown>:
    size_hint_x: 0.8
    font_size: sp(14 * {font_factor})

<MyCheckbox@CheckBox>:
    size_hint_x: 0.8

<SightInputSection@GridLayout>:
    cols: 2
    size_hint_y: None
    size_hint_x: 0.8
    spacing: {spacing}
    padding: {padding}
    canvas.before:
        Color:
            rgba: 0.25, 0.25, 0.25, 1
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: '[b]Use this sight:[/b]'
        markup: True
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None    
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyCheckbox:
        id: use_checkbox
        size_hint_x: 0.8
    Label:
        text: '[b]Name :[/b]'
        markup: True        
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyTextInput:
        id: object_name
        size_hint_x: 0.8
        multiline: False               
    Label:
        text: '[b]Altitude (Hs) :[/b]'
        markup: True         
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyTextInput:
        id: altitude
        size_hint_x: 0.8
        multiline: False
    Label:
        text: '[b]Artificial Horizon :[/b]'
        markup: True        
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyCheckbox:
        id: artificial_horizon
        size_hint_x: 0.8               
    Label:
        text: '[b]Date :[/b]'
        markup: True         
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyTextInput:
        id: set_time_date
        size_hint_x: 0.8
        multiline: False
    Label:
        text: '[b]Time :[/b]'
        markup: True         
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyTextInput:
        id: set_time
        size_hint_x: 0.8
        multiline: False                   
    Label:
        text: '[b]Timezone :[/b]'
        markup: True         
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyTextInput:
        id: set_time_tz
        size_hint_x: 0.8
        multiline: False                    
    Label:
        text: 'Index Error (am) :'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyTextInput:
        id: index_error
        size_hint_x: 0.8
        multiline: False         
    Label:
        text: 'Limb correction :'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    LimbDropDown:
        id: limb_correction
        size_hint_x: 0.8                
    Label:
        text: 'Elevation (m) :'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyTextInput:
        id: observer_height
        size_hint_x: 0.8
        multiline: False         
    Label:
        text: 'Temperature (°C):'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyTextInput:
        id: temperature
        size_hint_x: 0.8
        multiline: False        
    Label:
        text: 'Gradient (°C/m):'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyTextInput:
        id: temperature_gradient
        size_hint_x: 0.8
        multiline: False         
    Label:
        text: 'Pressure (kPa):'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        size_hint_x : 0.45
        font_size: sp(14 * {font_factor})
    MyTextInput:
        id: pressure
        size_hint_x: 0.8
        multiline: False         
"""

    Builder.load_string(generate_adaptive_kv())

FILE_NAME = None
NUM_DICT = None

# [Keep all the existing functions unchanged: get_starfixes, get_local_ip, etc.]
# SIGHT REDUCTION.

def get_starfixes(drp_pos: LatLonGeodetic) -> SightCollection:
    ''' Returns a list of used star fixes (SightCollection) '''
    assert isinstance(NUM_DICT, dict)

    Sight.set_estimated_position(drp_pos)
    retval = []
    assert isinstance(NUM_DICT, dict)

    def str2float_or_default (val : str, default : float | int) -> float | int:
        if len(val) == 0:
            retval = default
        else:
            retval = float(val)
        return retval

    for i in range(3):
        if str2bool(NUM_DICT["Use"+str(i+1)]):
            time_string = NUM_DICT["Date"+str(i+1)]+" "+\
                          NUM_DICT["Time"+str(i+1)]+\
                          NUM_DICT["TimeZone"+str(i+1)]
            assert isinstance (time_string, str)
            time_string = time_string.strip().upper()
            retval.append(
                Sight(object_name=NUM_DICT["ObjectName"+str(i+1)],
                      measured_alt=NUM_DICT["Altitude"+str(i+1)],
                      set_time=time_string,
                      index_error_minutes=str2float_or_default(
                          NUM_DICT["IndexError"+str(i+1)],0),
                      limb_correction=int(
                          NUM_DICT["LimbCorrection"+str(i+1)]),
                      artificial_horizon=str2bool(
                          NUM_DICT["ArtificialHorizon"+str(i+1)]),
                      observer_height=str2float_or_default(
                          NUM_DICT["ObserverHeight"+str(i+1)],0),
                      temperature=str2float_or_default(
                          NUM_DICT["Temperature"+str(i+1)],10),
                      dt_dh=str2float_or_default(
                          NUM_DICT["TemperatureGradient"+str(i+1)],-0.01),
                      pressure=str2float_or_default(NUM_DICT["Pressure"+str(i+1)],101)
            ))

    return SightCollection(retval)

def get_local_ip():
    """Get local IP without internet connectivity"""
    try:
        # Create socket but don't actually connect
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Use a non-routable address - doesn't need to be reachable
            s.connect(('192.168.1.1', 80))  # Local network address
            return s.getsockname()[0]
# pylint: disable=W0702
    except:
        return "127.0.0.1"
# pylint: enable=W0702

COMM_QUEUE = None
KILL_QUEUE = None

def run_plotserver():
    ''' Running the plot server worker 
        This thread starts the NMEA server, listens for position updates
        and also STOP commands for killing the NMEA server.
    '''
# pylint: disable=W0603
    global COMM_QUEUE
# pylint: enable=W0603
    server = NMEAServer(host='0.0.0.0', port=10110)
    server_thread = None
    try:
        # Start NMEA server in a separate thread
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()

        while True:
#pylint: disable=E0601
            assert isinstance (COMM_QUEUE, Queue)
#pylint: enable=E0601
            check_string = COMM_QUEUE.get ()
            assert isinstance (check_string, str)
            if check_string == "STOP":
                # The plot server will now terminate
                break
            strs = check_string.split (";")
            lat = float (strs[0])
            lon = float (strs[1])
            server.update_position (lat, lon)

    finally:
        server.stop()
        if server_thread is not None:
            server_thread.join ()
        COMM_QUEUE = None

def run_killserver ():
    ''' Running a separate "kill" server responsible for removing the NMEA server 
        This is needed to avoid Androids aggressive thread management which seems
        to cause hangups if the NMEA server is allowed to live for a longer time. 
    '''
    timestamp = 0
    has_waited = False
    while True:
        try:
# pylint: disable=W0603
            global KILL_QUEUE
# pylint: enable=W0603
            assert KILL_QUEUE is not None
            do_wait = False
            # Here we wait for the kill signal
            timestamp = KILL_QUEUE.get (block=False)
            # We got a kill signal, with a timestamp
            if not KILL_QUEUE.empty:
                pass
                # There is more data on the kill queue. Ignore this post.
            else:
                # No more data on the kill queue. Now we should wait
                do_wait = True
            if do_wait:
                # Calculate the real time difference, and add 20 seconds
                wait_time = timestamp - time.time() + 20
                if wait_time < 0:
                    wait_time = 0
                # If we have a positive net waiting time, then waut
                if wait_time > 0:
                    time.sleep (wait_time)
                else:
                    pass
                    # We cot an overdue kill request
                # Now remember we have waited
                has_waited = True
        except Empty:
            # We have an empty kill queue. See if it is time to actually kill the plot server.
            if has_waited:
                # Time to kill
                global COMM_QUEUE
                if COMM_QUEUE is not None:
                    # Sending kill command
                    COMM_QUEUE.put ("STOP")
                    # Graceful wait for 1 sec
                    time.sleep (1)
                    # Clean up
                    COMM_QUEUE = None
                    KILL_QUEUE = None
                    # We are done
                    return
            else:
                pass

def start_plotserver ():
    ''' Start the plot server'''
# pylint: disable=W0603
    global COMM_QUEUE, KILL_QUEUE
# pylint: enable=W0603
    if COMM_QUEUE is None:
        COMM_QUEUE = Queue ()
        plot_process = threading.Thread (target = run_plotserver, args = (), daemon=True)
        plot_process.start ()
    if KILL_QUEUE is None:
        KILL_QUEUE = Queue ()
        kill_process = threading.Thread (target=run_killserver, args = (), daemon=True)
        kill_process.start ()
    try:
        while True:
            KILL_QUEUE.get(False)
    except Empty:
        pass
    # KILL_QUEUE.put (20)
    KILL_QUEUE.put (time.time())

def kill_plotserver ():
    ''' Kill the plot server'''
    if COMM_QUEUE is not None:
        COMM_QUEUE.put ("STOP")

def update_plot_position (lat : float, lon : float):
    ''' Update the plot server with new coordinates '''
    if COMM_QUEUE is not None:
        COMM_QUEUE.put (str(lat)+";"+str(lon))

def sight_reduction() -> \
    tuple[str, bool, LatLonGeodetic | NoneType, SightCollection | Sight | NoneType]:
    ''' Perform a sight reduction given data entered above '''
    assert isinstance(NUM_DICT, dict)
    real_lat = parse_angle_string (NUM_DICT["DrpLat"])
    real_lon = parse_angle_string (NUM_DICT["DrpLon"])
    the_pos = LatLonGeodetic(lat=float(real_lat),
                             lon=float(real_lon))

    intersections = None
    collection = None
    try:
        the_limit = float(NUM_DICT["DrpQuality"]) * 1.852 # Convert from nm to km
        intersections, _, _, collection, calculated_diff =\
            SightCollection.get_intersections_conv(return_geodetic=True,
                                                   estimated_position=the_pos,
                                                   get_starfixes=get_starfixes,
                                                   assume_good_estimated_position=True,
                                                   limit=the_limit)

        assert isinstance (intersections, LatLonGeodetic)
        assert isinstance (collection, SightCollection)
        repr_string = get_representation(intersections, 1)
        km_per_nautical_mile = 1.852
        if calculated_diff > 0:
            diff_string = " ±" + str(round(calculated_diff/km_per_nautical_mile,1)) + " nm"
        else:
            diff_string = ""
        start_plotserver ()
        update_plot_position (intersections.get_lat(), intersections.get_lon())
        return repr_string + diff_string, True, intersections, collection

    except IntersectError as ve:
        coll_object = None
        if isinstance (ve.coll_object, SightCollection) or\
           isinstance (ve.coll_object, Sight):
            coll_object = ve.coll_object
            return "Failed sight reduction. " + str (ve), False, None, coll_object
        return "Failed sight reduction. " + str (ve), False, None, None
    except KeyError as ve:
        return "Invalid parameters." + str (ve), False, None, None
    except ValueError as ve:
        return str(ve), False, None, None

# Modified widget classes with font awareness
class AppButton (Button):
    ''' Common base class for buttons '''

    def __init__(self, active : bool, **kwargs):
        # Apply font scaling
        if 'font_size' not in kwargs:
            kwargs['font_size'] = sp(16 * font_config.get_font_size_factor())
        super().__init__(**kwargs)
        self.set_active (active)

    def set_active (self, active : bool):
        ''' Toggles the active state of the button '''
        if active:
            self.background_color = (1.0, 0.10, 0.10, 1)
        else:
            self.background_color = (0.9, 0.9, 0.9, 1)

class ExecButton (AppButton):
    ''' This is the button starting the sight reduction '''

    def __init__(self, form, **kwargs):
        super().__init__(active = True, **kwargs)
        self.form = form
        self.text = "Perform sight reduction!"
# pylint: disable=E1101
        self.bind(on_press=self.callback)
# pylint: enable=E1101

    @staticmethod
    def callback(instance):
        ''' This is the button callback function '''
        assert isinstance(instance, ExecButton)
        the_form = instance.form
        assert isinstance(the_form, InputForm)

        the_form.extract_from_widgets()
        sr, result, intersections, coll = sight_reduction()
        if result:
            # Successful sight reduction
            StarFixApp.play_click_sound ()
            assert isinstance (coll, SightCollection)
            assert isinstance (intersections, tuple) or\
                   isinstance (intersections, LatLonGeodetic) or\
                   intersections is None
            # Save collection and intersections (to be used in map presentation)
            the_form.set_active_intersections(intersections, coll)
            the_form.extract_from_widgets()
            dump_dict()
            the_form.results.text = "Your location = " + sr
            StarFixApp.message_popup ("You have made a successful sight reduction!\n"
                                      "Use the \"Show map!\" button to see the result!\n"
                                      "The settings have been copied to the clipboard.",\
                                      StarFixApp.MSG_ID_SIGHT_REDUCTION_SUCCESS)
        else:
            # Failed sight reduction
            StarFixApp.play_error_sound ()
            if coll is not None:
                # Save the collection (without intersections) on error
                the_form.set_active_intersections (None, coll)
                StarFixApp.message_popup ("You have made a failed sight reduction!\n"
                                          "The circles of equal altitude don't intersect properly\n"
                                          "Use the \"Show map!\" button for troubleshooting!",\
                                          StarFixApp.MSG_ID_SIGHT_REDUCTION_FAILURE)
            else:
                StarFixApp.message_popup ("You have made a failed sight reduction!\n"
                                          "See the message in the field above for more"+\
                                          "information!\n",\
                                          StarFixApp.MSG_ID_SIGHT_REDUCTION_FAILURE)
                StarFixApp.reset_messages()
            the_form.results.text = sr



class ShowMapButton (AppButton):
    ''' This button is used to show the active map '''

    def __init__(self, form, **kwargs):
        super().__init__(active = False, **kwargs)
        self.form = form
        self.text = "No map data (yet)"
# pylint: disable=E1101
        self.bind(on_press=self.callback)
# pylint: enable=E1101

    @staticmethod
    def callback(instance):
        ''' This is a function for showing a map '''
        assert isinstance(instance, ShowMapButton)
        the_form = instance.form
        assert isinstance(the_form, InputForm)
        i, c = the_form.get_active_intersections ()
        if c is not None:
            the_map = None
            try:
                if isinstance (c, SightCollection):
                    the_map = c.render_folium (i)
                elif isinstance (c, Sight):
                    the_map = c.render_folium_new_map ()
                StarFixApp.play_click_sound()
                assert the_map is not None
                file_name = "./map.html"
                the_map.save (file_name)
                # Keeping this message to possible future use
                #StarFixApp.message_popup ("You have generated a map.\n"
                #                          "It is visible in a web brower window.\n"
                #                          "It shows the last sight reduction\n"
                #                          "(successful or not)",
                #                          StarFixApp.MSG_ID_SHOW_MAP)
                show_or_display_file (file_name, protocol="http")
# pylint: disable=W0702
            except:
                StarFixApp.play_error_sound()
                if the_map is None:
                    instance.text = get_folium_load_error()
                else:
                    instance.text = "Error in map generation."
# pylint: enable=W0702

class PasteConfigButton (AppButton):
    ''' This button reads the JSON configuration from clipboard and repopulates all widgets '''

    def __init__(self, form, **kwargs):
        super().__init__(active = True, **kwargs)
        self.form = form
        self.text = "Paste Config"
# pylint: disable=E1101
        self.bind(on_press=self.callback)
# pylint: enable=E1101

    @staticmethod
    def callback(instance):
        ''' Responds to button click and repopulates the configuration '''
        assert isinstance (instance, PasteConfigButton)
        config_string = Clipboard.paste ()
        assert isinstance (NUM_DICT, dict)
        format_ok = _initialize_from_string (config_string, NUM_DICT)
        if format_ok:
            StarFixApp.play_click_sound ()
            instance.form.populate_widgets ()
        else:
            StarFixApp.play_error_sound ()

class OnlineHelpButton (AppButton):
    ''' A button for showing online help '''

    def __init__(self, **kwargs):
        super().__init__(active = True, **kwargs)
        self.text = "Show help!"
# pylint: disable=E1101
        self.bind(on_press=self.callback)
# pylint: enable=E1101

    @staticmethod
    def callback(_):
        ''' This is a function for showing online help '''
        StarFixApp.play_click_sound ()
        file_name = "./APPDOC.html"
        show_or_display_file (file_name, protocol="http")

class FormRow (BoxLayout):
    ''' This is used for row data in the form '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = font_config.get_element_height()

class MyLabel (Label):
    ''' This is used for labels'''

    def __init__(self, indent: bool = False, **kwargs):
        left_hint = 0.45 if indent else 0.4
        # Apply font scaling if not already specified
        if 'font_size' not in kwargs:
            kwargs['font_size'] = sp(14 * font_config.get_font_size_factor())
        super().__init__(size_hint=(left_hint, 1), **kwargs)

class LimbDropDown (Button):
    ''' This is used for the limb correction dropdown'''

    text_labels = {-1:"Lower", 0:"Center", 1:"Upper"}

    def __init__(self, **kwargs):
        # Apply font scaling
        if 'font_size' not in kwargs:
            kwargs['font_size'] = sp(14 * font_config.get_font_size_factor())
        super().__init__(text=self.text_labels[0], color = (0.8, 0.1, 0.1, 1.0), **kwargs)
        self.my_dropdown = DropDown()
        for index in [-1, 0, 1]:
            btn = Button(
                text=str(self.text_labels[index]),
                size_hint_y=None,
                height=font_config.get_element_height(),
                font_size=sp(14 * font_config.get_font_size_factor())
            )
# pylint: disable=E1101
            btn.bind(on_release=lambda btn: self.my_dropdown.select(btn.text))
# pylint: enable=E1101
            self.my_dropdown.add_widget(btn)
# pylint: disable=E1101
        self.bind(on_release=self.my_dropdown.open)
# pylint: enable=E1101

# pylint: disable=E1101
        self.my_dropdown.bind(on_select=lambda instance,
                              x: setattr(self, 'text', x))
# pylint: enable=E1101

    def set_active (self,active_state : bool):
        ''' Set the active state for this dropdown element '''
        self.disabled = not active_state
        for c in self.my_dropdown.children:
            if isinstance (c, Button):
                c.disabled = not active_state

class MyTextInput (TextInput):
    ''' The input field class used '''

    color = (1.0, 1.0, 0.2, 1.0)

    def __init__(self, **kwargs):
        self.valign = "center"
        # Apply font scaling
        if 'font_size' not in kwargs:
            kwargs['font_size'] = sp(14 * font_config.get_font_size_factor())
        super().__init__(
            size_hint = (1,1),
            padding=['10dp', '7dp', '10dp', '7dp'],
            **kwargs
        )

# New class to encapsulate a single Sight's input fields
class SightInputSection(GridLayout):
    ''' New layout for sight input segment with font awareness '''
# pylint: disable=I1101
    sight_num = kivy.properties.NumericProperty(0) # For dynamic text in KV
# pylint: enable=I1101

    def __init__(self, sight_num, **kwargs):
        super().__init__(**kwargs)
        self.sight_num = sight_num

        # Apply adaptive height based on font scale
        element_height = font_config.get_element_height()
        sight_elements = 13  # Number of elements in sight section
        self.height = element_height * sight_elements

        cb = self.ids.use_checkbox
        assert isinstance (cb, CheckBox)
        cb.bind(active=self.on_checkbox_active)
        self.on_checkbox_active (cb, cb.active)

    def on_checkbox_active(self, instance, value):
        ''' Disable/enable other inputs based on checkbox '''
        assert isinstance (instance, CheckBox)
        for child in self.children:

            if child != instance:
                if isinstance (child, LimbDropDown):
                    child.set_active (value)
                    if value:
                        child.color = (1.0, 1.0, 1.0, 1)
                    else:
                        child.color = (0.2, 0.2, 0.2, 1)
                else:
                    child.disabled = not value

class StarFixApp (App):
    ''' The application class '''

    click_sound = None
    initialized = False

    def __init__ (self, **kwargs):
        super().__init__(**kwargs)
        StarFixApp.click_sound = None

        # Create main layout with font awareness
        if font_config.should_use_scroll():
            # Force scrolling for large font scales
            layout = InputForm(size_hint_y = None)
        else:
            layout = InputForm(size_hint_y = None)

# pylint: disable=E1101
        layout.bind(minimum_height=layout.setter('height'))
# pylint: enable=E1101

        # Always use ScrollView for better compatibility
        root = ScrollView(
            size_hint= (1,1),
            do_scroll_x=False,  # Only vertical scrolling
            do_scroll_y=True
        )
        root.add_widget(layout)
        self.m_root = root

        StarFixApp.initialized = True

    @staticmethod
    def play_click_sound ():
        ''' Play the button click sound '''
        if click_sound is not None:
            click_sound.play ()

    @staticmethod
    def play_error_sound ():
        ''' Play the error sound '''
        if error_sound is not None:
            error_sound.play ()

    message_kv_string = """
<MessagePopup>:
    size_hint: 1, 0.6
    auto_dismiss: False  # Prevent dismissing by clicking outside
    title: 'Message'

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        Label:
            id: message_label
            text: root.message
            markup: True
            text_size: self.width, None
            halign: 'center'
            valign: 'middle'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: dp(10)

            CheckBox:
                id: dont_show_checkbox
                size_hint_x: None
                width: dp(40)
                on_active: root.toggle_dont_show_again(self.active)

            Label:
                text: "Don't show this message again"
                text_size: self.width, None
                halign: 'left'
                valign: 'middle'

        Button:
            text: 'Close'
            size_hint_y: None
            height: dp(50)
            on_release: root.dismiss()
"""

    Builder.load_string(message_kv_string)

    message_store_name = "message_settings.json"
    message_store = JsonStore(message_store_name)

    MSG_ID_INTRO                   = "MSG_ID_INTRO"
    MSG_ID_SIGHT_REDUCTION_SUCCESS = "MSG_ID_SIGHT_REDUCTION_SUCCESS"
    MSG_ID_SIGHT_REDUCTION_FAILURE = "MSG_ID_SIGHT_REDUCTION_FAILURE"
    #MSG_ID_SHOW_MAP                = "MSG_ID_SHOW_MAP"

    class MessagePopup (Popup) :
        ''' This is a simple popup for the message functionality '''

        def __init__ (self, msg : str, msg_id : str, **kwargs):

            self.show_popup = True
            self.message = msg
            self.msg_id = msg_id
            super().__init__ (**kwargs)

        def toggle_dont_show_again (self, active : bool):
            ''' Toggle the active state for the "dont show again" state '''
            self.show_popup = not active
            StarFixApp.message_store.put (self.msg_id, dont_show_again=active)

    @staticmethod
    def reset_messages ():
        ''' Restore all messages '''
        try:
            os.remove (StarFixApp.message_store_name)
            StarFixApp.message_store = JsonStore (StarFixApp.message_store_name)
# pylint: disable=W0702
        except:
            pass
# pylint: enable=W0702

    @staticmethod
    def _message_popup_doer (msg : str, msg_id : str, *_):

        show_popup = False
        if StarFixApp.message_store.exists(msg_id):
            b = StarFixApp.message_store.get(msg_id)
            the_val = b ["dont_show_again"]
            show_popup = not the_val
        else:
            show_popup = True

        if show_popup:
            mp = StarFixApp.MessagePopup (msg, msg_id)
            mp.open ()

    @staticmethod
    def message_popup (msg : str, msg_id : str):
        ''' Produce an informational message popup '''
        if not StarFixApp.initialized:
            Clock.schedule_once(partial(StarFixApp._message_popup_doer, msg, msg_id), 0.1)
            return
        StarFixApp._message_popup_doer (msg, msg_id)

    @staticmethod
    def _error_popup_doer (msg : str, *_):
        StarFixApp.play_error_sound ()
        if StarFixApp.initialized:
            popup = Popup(title='Error',
                          content=Label(text=msg+"\n\nClick outside to close.",\
                                        markup=True),
                          size_hint=(1, 0.5))
            popup.open (animation=False)

    @staticmethod
    def error_popup (msg : str):
        ''' Produce a warning/error message popup '''
        if not StarFixApp.initialized:
            Clock.schedule_once(partial(StarFixApp._error_popup_doer, msg), 0.1)
            return
        StarFixApp._error_popup_doer (msg)

    def get_root (self):
        ''' Return the root widget '''
        return self.m_root

def _initialize_from_string (s:str, init_dict : dict) -> bool:
# pylint: disable=W0603
    global NUM_DICT
# pylint: enable=W0603
    def handle_error (msg : str):
        StarFixApp.error_popup (msg)

    def _fill_in_defaults ():

        def _check_default (key : str, value : str):
            assert isinstance (NUM_DICT, dict)
            try:
                the_val = NUM_DICT [key]
            except KeyError:
                the_val = value
                NUM_DICT [key] = the_val

        _check_default ("DrpQuality", "100")

    error_msg = "Error loading JSON file"
    format_ok = True
    try:
        NUM_DICT = json.loads(s)
# pylint: disable=W0718
    except BaseException as be:
        handle_error (error_msg + "\n" + str(be))
        format_ok = False
# pylint: enable=W0718
    if format_ok:
        assert isinstance (NUM_DICT, dict)
        the_format = ""
        error_msg = "Invalid JSON file,\nrestoring defaults"
        try:
            the_format = NUM_DICT ["Format"]
        except KeyError:
            handle_error (error_msg)
            format_ok = False
        if the_format != "celeste.1":
            handle_error (error_msg)
            format_ok = False
        _fill_in_defaults ()
    if not format_ok:
        NUM_DICT = init_dict
    return format_ok

def initialize(fn: str, init_dict: dict):
    ''' Initialize the configuration dict '''
# pylint: disable=W0603
    global FILE_NAME
    global NUM_DICT
# pylint: enable=W0603
    FILE_NAME = fn

    try:
        # First see if we have a saved json file
        with open(FILE_NAME, "r", encoding="utf-8") as f:

            assert isinstance (NUM_DICT, dict) or\
                   NUM_DICT is None
            s = f.read()
            _initialize_from_string (s, init_dict)

    except FileNotFoundError:
        # If no file present, then load the defaults
        NUM_DICT = init_dict

def dump_dict():
    ''' Dumps the contents to a json file '''

    j_dump = json.dumps(NUM_DICT, indent=4)
    Clipboard.copy (j_dump)
    assert isinstance(FILE_NAME, str)
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(j_dump)

def do_initialize ():
    ''' Initialize data from json '''

    # Pick up last configuration
    # If no config found then use the Chicago sights
    initialize("kivyapp.1.json",
            {"ObjectName1": "Sun",
                "Altitude1": "55:8:1.1",
                "Date1": "2024-05-05",                
                "Time1": "15:55:18",
                "TimeZone1" : "Z",
                "LimbCorrection1": "0",
                "IndexError1": "0",
                "ArtificialHorizon1": "False",
                "ObserverHeight1": "0",
                "Temperature1": "10",
                "TemperatureGradient1": "-0.01",
                "Pressure1": "101",

                "ObjectName2": "Sun",
                "Altitude2": "19:28:19",
                "Date2": "2024-05-05",
                "Time2": "23:01:19",
                "TimeZone2" : "Z",
                "LimbCorrection2": "0",
                "IndexError2": "0",
                "ArtificialHorizon2": "False",
                "ObserverHeight2": "0",
                "Temperature2": "10",
                "TemperatureGradient2": "-0.01",
                "Pressure2": "101",

                "ObjectName3": "Vega",
                "Altitude3": "30:16:23.7",
                "Date3": "2024-05-06",
                "Time3": "04:04:13",
                "TimeZone3" : "Z",
                "LimbCorrection3": "0",
                "IndexError3": "0",
                "ArtificialHorizon3": "False",
                "ObserverHeight3": "0",
                "Temperature3": "10",
                "TemperatureGradient3": "-0.01",
                "Pressure3": "101",

                "DrpLat": "40",
                "DrpLon": "-90",
                "DrpQuality": "100",

                "Use1": "True",
                "Use2": "True",
                "Use3": "True",
                "Format": "celeste.1"})

class InputForm(GridLayout):
    ''' This is the main input form with font awareness '''

    nr_of_sights = 3

    def __init__(self, **kwargs):
        super().__init__(cols=1, spacing=font_config.get_spacing(), **kwargs)

        self.__active_intersections = None
        self.__active_collection    = None

        self.data_widget_container = {}

        # Add font scale info button
        if DEBUG_FONT_HANDLING:
            self.add_font_scale_info()

        bl = FormRow()
        butt = OnlineHelpButton()
        bl.add_widget(butt)
        self.add_widget(bl)

        # DRP Position Section with adaptive sizing
        self.add_widget(Label(
            text='[b]DRP Position[/b]',
            markup=True,
            size_hint_y=None,
            color = (0.8, 0.8, 1.0, 1.0),
            height=font_config.get_element_height(),
            font_size=sp(16 * font_config.get_font_size_factor())
        ))

        # Calculate section height adaptively
        drp_num = 3
        drp_section_height = font_config.get_element_height() * drp_num

        drp_section = GridLayout(
            cols=2,
            spacing=font_config.get_spacing(),
            padding=font_config.get_padding(),
            size_hint_y=None,
            height=drp_section_height
        )

        drp_section.add_widget(MyLabel(text='[b]Latitude:[/b]', markup=True))
        self.drp_lat_input = MyTextInput()
        self.data_widget_container["DrpLat"] = self.drp_lat_input
        drp_section.add_widget(self.drp_lat_input)

        drp_section.add_widget(MyLabel(text='[b]Longitude:[/b]',markup=True))
        self.drp_lon_input = MyTextInput()
        self.data_widget_container["DrpLon"] = self.drp_lon_input
        drp_section.add_widget(self.drp_lon_input)

        # DRP quality button
        drp_section.add_widget(MyLabel(text='Sight quality (nm):'))
        self.drp_quality_input = MyTextInput()
        self.data_widget_container["DrpQuality"] = self.drp_quality_input
        drp_section.add_widget (self.drp_quality_input)

        self.add_widget(drp_section)

        # Individual Sight Sections with adaptive sizing
        for sight in range(self.nr_of_sights):

            self.add_widget(Label(
                text=f'[b]Sight {sight+1} Data[/b]',
                markup=True,
                size_hint_y=None,
                height=font_config.get_element_height(),
                color=(0.5, 0.9, 0.5, 1.0),
                font_size=sp(16 * font_config.get_font_size_factor())
            ))

            # Calculate sight section height adaptively
            sight_elements = 13
            sight_section_height = font_config.get_element_height() * sight_elements

            sight_section = SightInputSection(
                sight_num=sight+1,
                height=sight_section_height,
                spacing=font_config.get_spacing(),
                padding=font_config.get_padding()
            )

            # Store references to widgets within the SightInputSection
            self.data_widget_container["Use"+str(sight+1)] =\
                  sight_section.ids.use_checkbox
            self.data_widget_container["Altitude"+str(sight+1)] =\
                  sight_section.ids.altitude
            self.data_widget_container["ObjectName"+str(sight+1)] =\
                  sight_section.ids.object_name
            self.data_widget_container["Date"+str(sight+1)] =\
                  sight_section.ids.set_time_date
            self.data_widget_container["Time"+str(sight+1)] =\
                  sight_section.ids.set_time
            self.data_widget_container["TimeZone"+str(sight+1)] =\
                  sight_section.ids.set_time_tz
            self.data_widget_container["IndexError"+str(sight+1)] =\
                  sight_section.ids.index_error
            self.data_widget_container["LimbCorrection"+str(sight+1)] =\
                  sight_section.ids.limb_correction
            self.data_widget_container["ArtificialHorizon"+str(sight+1)] =\
                  sight_section.ids.artificial_horizon
            self.data_widget_container["ObserverHeight"+str(sight+1)] =\
                  sight_section.ids.observer_height
            self.data_widget_container["Temperature"+str(sight+1)] =\
                  sight_section.ids.temperature
            self.data_widget_container["TemperatureGradient"+str(sight+1)] =\
                  sight_section.ids.temperature_gradient
            self.data_widget_container["Pressure"+str(sight+1)] =\
                  sight_section.ids.pressure

            self.add_widget(sight_section)

        bl = FormRow()
        self.results = MyLabel(text='', markup=True, indent=False)
        self.results.halign = "center"
        bl.add_widget(self.results)
        self.add_widget(bl)

        bl = FormRow()
        butt = ExecButton(self)
        bl.add_widget(butt)
        self.add_widget(bl)

        bl = FormRow()
        butt = ShowMapButton(self)
        bl.add_widget(butt)
        self.add_widget(bl)
        self.__show_map_button = butt

        bl = FormRow()
        butt = PasteConfigButton(self)
        bl.add_widget(butt)
        self.add_widget(bl)

        bl = FormRow()
        butt = OnlineHelpButton()
        bl.add_widget(butt)
        self.add_widget(bl)

        bl = FormRow()

        def get_ip_code ():
            ip_address = get_local_ip ()
            if ip_address == "127.0.0.1":
                ip_address = "No network connection"
            else:
                ip_address = "IP address = " + ip_address
            return ip_address

        def check_ip_address (_):
            code = get_ip_code ()
            self.ip_adress_status.text = code

        self.ip_adress_status = MyLabel(text=get_ip_code(), markup=True, indent=False)
        # Check for ip address changes every second
        Clock.schedule_interval(check_ip_address, 1.0)
        self.ip_adress_status.halign = "center"
        bl.add_widget(self.ip_adress_status)
        self.add_widget(bl)

        self.populate_widgets()

    def add_font_scale_info(self):
        """Add font scale information if it's unusual"""
        if font_config.font_scale > 1.1:
            bl = FormRow()
            font_info = MyLabel(
                text=f'Font Scale: {font_config.font_scale:.1f}x (Layout optimized)',
                markup=True,
                indent=False,
                color=(0.8, 0.8, 0.2, 1.0)
            )
            font_info.halign = "center"
            bl.add_widget(font_info)
            self.add_widget(bl)

    def __update_drp (self, i : tuple | LatLonGeodetic | NoneType):
        if i is None or isinstance (i, tuple):
            return
        self.drp_lat_input.text = str (round(i.get_lat(),2))
        self.drp_lon_input.text = str (round(i.get_lon(),2))

    def set_active_intersections\
        (self, i : tuple | LatLonGeodetic | NoneType, c : SightCollection | Sight | NoneType ):
        ''' Save the set of active cel nav intersection objects '''
        self.__active_intersections = i
        self.__active_collection    = c
        self.__show_map_button.text = "Show map!"
        self.__show_map_button.set_active (True)
        self.__update_drp (i)

    def get_active_intersections (self) ->\
          tuple [tuple | LatLonGeodetic | NoneType, SightCollection | Sight | NoneType]:
        ''' Return the set of active cel nav intersections objects '''
        return self.__active_intersections, self.__active_collection

    def populate_widgets(self):
        ''' Read the data from json and populate all fields '''
        assert isinstance(NUM_DICT, dict)
        for entry in NUM_DICT:
            if entry == "Format":
                continue
            w = self.data_widget_container[entry]
            if isinstance(w, TextInput):
                w.text = NUM_DICT[entry]
            elif isinstance(w, CheckBox):
                w.active = str2bool(NUM_DICT[entry])
            elif isinstance(w, LimbDropDown):
                w.text = LimbDropDown.text_labels[int(NUM_DICT[entry])]

    def extract_from_widgets(self):
        ''' Extract all widget data and populate the json structure '''
        assert isinstance(NUM_DICT, dict)
        for entry in self.data_widget_container.items():
            e = entry[0]
            w = entry[1]
            if isinstance(w, TextInput):
                NUM_DICT[e] = w.text
            elif isinstance(w, CheckBox):
                NUM_DICT[e] = str(w.active)
            elif isinstance(w, LimbDropDown):
                for key, value in LimbDropDown.text_labels.items():
                    if w.text == value:
                        NUM_DICT[e] = str(key)
                        break

if __name__ == '__main__':

    if is_windows():
        freeze_support ()
    if not is_windows ():
        # Start http server
        start_http_server ()
    # Initialize all configuration data
    do_initialize()

    # Show intro message with font scale info if needed
    INTRO_MSG = ("[b]Welcome to Celeste![/b]\n"+
                "This is an app for celestial navigation.\n"+
                "It is open source (MIT License)\nand comes with [b]NO WARRANTY[/b].\n"+
                "Use the \"Show help!\" button for documentation.")

    if font_config.font_scale > 1.2 and DEBUG_FONT_HANDLING:
        INTRO_MSG +=\
        f"\n\n[color=orange]Font Scale: {font_config.font_scale:.1f}x[/color]\n"+\
         "Layout has been optimized for large fonts."

    StarFixApp.message_popup(INTRO_MSG, StarFixApp.MSG_ID_INTRO)

    a = StarFixApp ()
    # Run the application
    runTouchApp (a.get_root())
    # Kill NMEA 0138 server (if active)
    kill_plotserver ()
    if not is_windows():
        # Kill http server
        exit_handler ()
