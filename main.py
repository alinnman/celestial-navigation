''' 
    Simple skeleton demo app for celestial navigation. 
    Based on Kivy.
    Can be used for more elaborate apps, including on Android and iOS, Protype now working.. 

    *** WORK IN PROGRESS ***

    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
'''
# pylint: disable=C0413
# pylint: disable=C0411
from multiprocessing import freeze_support
from types import NoneType
import importlib
from starfix import LatLonGeodetic, SightCollection, Sight, \
    get_representation, IntersectError, get_folium_load_error, show_or_display_file, \
    is_windows, exit_handler
import json
import kivy
kivy.require('2.0.0')
kivy.config.Config.set('graphics', 'resizable', False)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.app import App, runTouchApp
from kivy.core.window import Window

Window.softinput_mode = 'below_target'

# pylint: enable=C0413
# pylint: enable=C0411

def str2bool(v):
    ''' Simple conversion from bool to string '''
    return v.lower() in ("yes", "true", "t", "1")


Window.clearcolor = (0.4, 0.4, 0.4, 1.0)

# Set default color and sizes of the form
USE_KV = True
if USE_KV:
    Builder.load_string(
    """
<FormSection@GridLayout>:
    cols: 2
    spacing: 5
    padding: 5
    canvas.before:
        Color:
            rgba: 0.35, 0.35, 0.35, 1
        Rectangle:
            pos: self.pos
            size: self.size

<MyLabel>:
    size_hint_x: 0.4 # Adjust for a more balanced look in a two-column grid
    halign: 'right'
    valign: 'middle'
    padding: 1
    text_size: self.width, None
    size_hint_x : 0.4    

<MyTextInput>:
    size_hint_x: 0.8 # The remaining space
    valign: 'middle'    

<LimbDropDown>:
    size_hint_x: 0.8 # Same as TextInput

<MyCheckbox@CheckBox>:
    size_hint_x: 0.8 # Same as TextInput

<SightInputSection@GridLayout>:
    cols: 2
    spacing: 5
    padding: 10
    size_hint_y: None
    size_hint_x: 0.8 # The remaining space    
    height : 800
    canvas.before:
        Color:
            rgba: 0.25, 0.25, 0.25, 1 # Slightly darker background for individual sight sections
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: '[b]Use this sight:[/b]'
        markup: True
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None    
        height : 100
        size_hint_x : 0.4 
    MyCheckbox:
        id: use_checkbox
        size_hint_x: 0.8 # The remaining space          
    Label:
        text: '[b]Name :[/b]'
        markup: True        
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        height : 100
        size_hint_x : 0.4        
    MyTextInput:
        id: object_name
        height : 100
        size_hint_x: 0.8 # The remaining space                
    Label:
        text: '[b]Altitude :[/b]'
        markup: True         
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        height : 100
        size_hint_x : 0.4                  
    MyTextInput:
        id: altitude
        height : 100
        size_hint_x: 0.8 # The remaining space
    Label:
        text: '[b]Artificial Horizon :[/b]'
        markup: True        
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        height : 100
        size_hint_x : 0.4                 
    MyCheckbox:
        id: artificial_horizon
        size_hint_x: 0.8 # The remaining space            
    Label:
        text: '[b]Time :[/b]'
        markup: True         
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        height : 100
        size_hint_x : 0.4                 
    MyTextInput:
        id: set_time
        height : 100
        size_hint_x: 0.8 # The remaining space          
    Label:
        text: 'Index Error :'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        height : 100
        size_hint_x : 0.4                  
    MyTextInput:
        id: index_error
        height : 100
        size_hint_x: 0.8 # The remaining space          
    Label:
        text: 'Limb correction :'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        height : 100
        size_hint_x : 0.4                 
    LimbDropDown:
        id: limb_correction
        height: 100
        size_hint_x: 0.8 # The remaining space                
    Label:
        text: 'Observer Height :'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        height : 100
        size_hint_x : 0.4                      
    MyTextInput:
        id: observer_height
        height : 100
        size_hint_x: 0.8 # The remaining space          
    Label:
        text: 'Temperature :'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        height : 100
        size_hint_x : 0.4                  
    MyTextInput:
        id: temperature
        height : 100
        size_hint_x: 0.8 # The remaining space          
    Label:
        text: 'Temp Gradient :'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        height : 100
        size_hint_x : 0.4                  
    MyTextInput:
        id: temperature_gradient
        height : 100
        size_hint_x: 0.8 # The remaining space          
    Label:
        text: 'Pressure :'
        halign: 'right'
        valign: 'middle'
        text_size: self.width, None
        height : 100
        size_hint_x : 0.4                 
    MyTextInput:
        id: pressure
        height : 100
        size_hint_x: 0.8 # The remaining space          

""")

FILE_NAME = None
NUM_DICT = None

# SIGHT REDUCTION.

def get_starfixes(drp_pos: LatLonGeodetic) -> SightCollection:
    ''' Returns a list of used star fixes (SightCollection) '''
    assert isinstance(NUM_DICT, dict)

    Sight.set_estimated_position(drp_pos)
    retval = []
    assert isinstance(NUM_DICT, dict)
    # assert isinstance (TYPE_ARRAY, list)
    for i in range(3):
        if str2bool(NUM_DICT["Use"+str(i+1)]):
            retval.append(
                Sight(object_name=NUM_DICT["ObjectName"+str(i+1)],
                      measured_alt=NUM_DICT["Altitude"+str(i+1)],
                      set_time=NUM_DICT["Time"+str(i+1)],
                      index_error_minutes=float(
                          NUM_DICT["IndexError"+str(i+1)]),
                      limb_correction=int(
                          NUM_DICT["LimbCorrection"+str(i+1)]),
                      artificial_horizon=str2bool(
                          NUM_DICT["ArtificialHorizon"+str(i+1)]),
                      observer_height=float(
                          NUM_DICT["ObserverHeight"+str(i+1)]),
                      temperature=float(
                          NUM_DICT["Temperature"+str(i+1)]),
                      dt_dh=float(
                          NUM_DICT["TemperatureGradient"+str(i+1)]),
                      pressure=float(NUM_DICT["Pressure"+str(i+1)])
            ))

    return SightCollection(retval)


def sight_reduction() -> \
    tuple[str, bool, LatLonGeodetic | NoneType, SightCollection | Sight | NoneType]:
    ''' Perform a sight reduction given data entered above '''
    assert isinstance(NUM_DICT, dict)
    the_pos = LatLonGeodetic(lat=float(NUM_DICT["DrpLat"]),
                             lon=float(NUM_DICT["DrpLon"]))

    intersections = None
    collection = None
    try:
        intersections, _, _, collection =\
            SightCollection.get_intersections_conv(return_geodetic=True,
                                                   estimated_position=the_pos,
                                                   get_starfixes=get_starfixes,
                                                   assume_good_estimated_position=True)

        assert isinstance (intersections, LatLonGeodetic)
        assert isinstance (collection, SightCollection)
        return get_representation(intersections, 1), True, intersections, collection

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

class AppButton (Button):
    ''' Common base class for buttons '''

    def __init__(self, active : bool, **kwargs):
        self.set_active (active)
        super().__init__(**kwargs)
        #self.background_color = (1.0, 0.10, 0.10, 1)

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
            assert isinstance (coll, SightCollection)
            assert isinstance (intersections, tuple) or\
                   isinstance (intersections, LatLonGeodetic) or\
                   intersections is None
            the_form.set_active_intersections(intersections, coll)
            dump_dict()
            the_form.results.text = "Your location = " + sr
        else:
            if coll is not None:
                the_form.set_active_intersections (None, coll)
            the_form.results.text = sr

class ShowMapButton (AppButton):
    ''' This button used to show the active map '''

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
                assert the_map is not None
                file_name = "./map.html"
                the_map.save (file_name)
                try:
                    # Activate android libraries, needed for correct webbrowser functionality
                    importlib.import_module("android")
# pylint: disable=W0702
                except:
                    pass
# pylint: enable=W0702
                show_or_display_file (file_name, protocol="http")
                # webbrowser.open (the_link)
# pylint: disable=W0702
            except:
                if the_map is None:
                    instance.text = get_folium_load_error()
                else:
                    instance.text = "Error in map generation."
# pylint: enable=W0702

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
        file_name = "./APPDOC.html"
        show_or_display_file (file_name, protocol="http")


class FormRow (BoxLayout):
    ''' This is used for row data in the form '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        #self.size = (100, 28)

class MyLabel (Label):
    ''' This is used for labels'''

    def __init__(self, indent: bool = False, **kwargs):
        left_hint = 0.45 if indent else 0.4
        super().__init__(size_hint=(left_hint, 1), **kwargs)
        # self.size_hint (0.2, 1)


class LimbDropDown (Button):
    ''' This is used for the limb correction dropdown'''

    text_labels = {-1:"Lower", 0:"Center", 1:"Upper"}

    def __init__(self, **kwargs):
        super().__init__(text=self.text_labels[0], color = (0.8, 0.1, 0.1, 1.0), **kwargs)
        self.my_dropdown = DropDown()
        for index in [-1, 0, 1]:
            btn = Button(text=str(self.text_labels[index]), size_hint_y=None, height=self.height/2)
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

class MyTextInput (TextInput):
    ''' The input field class used '''

    color = (1.0, 1.0, 0.2, 1.0)

    def __init__(self, **kwargs):
        super().__init__(size_hint = (1,1), **kwargs)

# New class to encapsulate a single Sight's input fields
class SightInputSection(GridLayout):
    ''' New layout for sight input segment '''
# pylint: disable=I1101
    sight_num = kivy.properties.NumericProperty(0) # For dynamic text in KV
# pylint: enable=I1101

    def __init__(self, sight_num, **kwargs):
        super().__init__(**kwargs)
        self.sight_num = sight_num
        self.ids.use_checkbox.bind(active=self.on_checkbox_active)

    def on_checkbox_active(self, instance, value):
        ''' Disable/enable other inputs based on checkbox '''
        for child in self.children:
            if child is not instance and not isinstance(child, Label):
                child.disabled = not value

class StarFixApp (App):
    ''' The application class '''

    def __init__ (self, **kwargs):
        super().__init__(**kwargs)
        layout = InputForm(size_hint_y = None)
# pylint: disable=E1101
        layout.bind(minimum_height=layout.setter('height'))
# pylint: enable=E1101

        root = ScrollView(
            size_hint= (1,1)
            #size_hint=(1, None),
            #size=(Window.width, Window.height)
        )
        root.add_widget(layout)
        self.m_root = root

    def build(self):
        # return a Scroll View as a root widget
        return self.m_root

    def get_root (self):
        ''' Return the root widget '''
        return self.m_root

def initialize(fn: str, init_dict: dict):
    ''' Initialize the helper '''
# pylint: disable=W0603
    global FILE_NAME
    global NUM_DICT
# pylint: enable=W0603
    FILE_NAME = fn

    try:
        # First see if we have a saved json file
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            s = f.read()
            NUM_DICT = json.loads(s)
    except FileNotFoundError:
        # If no file present, then load the defaults
        NUM_DICT = init_dict

def dump_dict():
    ''' Dumps the contents to a json file '''
    j_dump = json.dumps(NUM_DICT)
    assert isinstance(FILE_NAME, str)
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(j_dump)

def do_initialize ():
    ''' Initialize data from json '''
    initialize("kivyapp.1.json",
            {"ObjectName1": "Sun",
                "Altitude1": "55:8:1.1",
                "Time1": "2024-05-05 15:55:18+00:00",
                "LimbCorrection1": "0",
                "IndexError1": "0",
                "ArtificialHorizon1": "False",
                "ObserverHeight1": "0",
                "Temperature1": "10",
                "TemperatureGradient1": "-0.01",
                "Pressure1": "101",

                "ObjectName2": "Sun",
                "Altitude2": "19:28:19",
                "Time2": "2024-05-05 23:01:19+00:00",
                "LimbCorrection2": "0",
                "IndexError2": "0",
                "ArtificialHorizon2": "False",
                "ObserverHeight2": "0",
                "Temperature2": "10",
                "TemperatureGradient2": "-0.01",
                "Pressure2": "101",

                "ObjectName3": "Vega",
                "Altitude3": "30:16:23.7",
                "Time3": "2024-05-06 04:04:13+00:00",
                "LimbCorrection3": "0",
                "IndexError3": "0",
                "ArtificialHorizon3": "False",
                "ObserverHeight3": "0",
                "Temperature3": "10",
                "TemperatureGradient3": "-0.01",
                "Pressure3": "101",

                "DrpLat": "40",
                "DrpLon": "-90",

                "Use1": "True",
                "Use2": "True",
                "Use3": "True"})


class InputForm(GridLayout):
    ''' This is the input form '''

    nr_of_sights = 3

    def __init__(self, **kwargs):
        super().__init__(cols=1, spacing=2, **kwargs)

        self.__active_intersections = None
        self.__active_collection    = None

        self.data_widget_container = {}

        bl = FormRow()
        butt = OnlineHelpButton()
        bl.add_widget(butt)
        self.add_widget(bl)

        # DRP Position Section
        self.add_widget(Label(text='[b]DRP Position[/b]', markup=True, size_hint_y=None, height=90))
        drp_section = GridLayout(cols=2, spacing=5, padding=5, size_hint_y=None, height=150)
        drp_section.add_widget(MyLabel(text='Latitude:'))
        self.drp_lat_input = MyTextInput()
        self.data_widget_container["DrpLat"] = self.drp_lat_input
        drp_section.add_widget(self.drp_lat_input)
        drp_section.add_widget(MyLabel(text='Longitude:'))
        self.drp_lon_input = MyTextInput()
        self.data_widget_container["DrpLon"] = self.drp_lon_input
        drp_section.add_widget(self.drp_lon_input)
        self.add_widget(drp_section)

        # Individual Sight Sections
        for sight in range(self.nr_of_sights):
            self.add_widget\
                (Label(text=f'[b]Sight {sight+1} Data[/b]', \
                       markup=True, size_hint_y=None, height=40))
            sight_section = SightInputSection(sight_num=sight+1)

            # Store references to widgets within the SightInputSection
            self.data_widget_container["Use"+str(sight+1)] =\
                  sight_section.ids.use_checkbox
            self.data_widget_container["ObjectName"+str(sight+1)] =\
                  sight_section.ids.object_name
            self.data_widget_container["Altitude"+str(sight+1)] =\
                  sight_section.ids.altitude
            self.data_widget_container["Time"+str(sight+1)] =\
                  sight_section.ids.set_time
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
        butt = ExecButton(self)
        bl.add_widget(butt)
        self.add_widget(bl)

        bl = FormRow()
        self.results = MyLabel(text='', markup=True, indent=False)
        self.results.halign = "center"
        bl.add_widget(self.results)
        self.add_widget(bl)

        bl = FormRow()
        butt = ShowMapButton(self)
        bl.add_widget(butt)
        self.add_widget(bl)
        self.__show_map_button = butt

        bl = FormRow()
        butt = OnlineHelpButton()
        bl.add_widget(butt)
        self.add_widget(bl)

        self.populate_widgets()

        #self.bind(on_close=self.on_close)

    #@staticmethod
    #def on_close (instance):
    #    print ("HEJ DÅ!")

    def set_active_intersections\
        (self, i : tuple | LatLonGeodetic | NoneType, c : SightCollection | Sight | NoneType ):
        ''' Save the set of active cel nav intersection objects '''
        self.__active_intersections = i
        self.__active_collection    = c
        self.__show_map_button.text = "Show map!"
        self.__show_map_button.set_active (True)

    def get_active_intersections (self) ->\
          tuple [tuple | LatLonGeodetic | NoneType, SightCollection | Sight | NoneType]:
        ''' Return the set of active cel nav intersections objects '''
        return self.__active_intersections, self.__active_collection

    def populate_widgets(self):
        ''' Read the data from json and populate all fields '''
        assert isinstance(NUM_DICT, dict)
        for entry in NUM_DICT:
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
            # w = self.data_widget_container [entry]
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
    do_initialize()
    a = StarFixApp ()
    runTouchApp (a.get_root())
    if not is_windows():
        exit_handler ()
