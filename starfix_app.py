''' 
    Simple skeleton demo app for celestial navigation. 
    Based on Kivy.
    Can be used for more elaborate apps, including on Android and iOS. 

    *** WORK IN PROGRESS ***

    © August Linnman, 2025, email: august@linnman.net
    MIT License (see LICENSE file)
'''
# pylint: disable=C0413
# pylint: disable=C0411
from starfix import LatLonGeodetic, SightCollection, Sight, \
    get_representation, IntersectError
import json
import kivy
kivy.require('2.3.1')
#kivy.config.Config.set('graphics', 'width', 400)
#kivy.config.Config.set('graphics', 'height', 400)
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

# pylint: enable=C0413
# pylint: enable=C0411

def str2bool(v):
    ''' Simple conversion from bool to string '''
    return v.lower() in ("yes", "true", "t", "1")


Window.clearcolor = (0.4, 0.4, 0.4, 1.0)

# Set default color and sizes of the form
Builder.load_string(
    """

<FormRow>:
    canvas:
        Color:
            rgba: root.background_color
        Rectangle:
            pos: self.pos
            size: self.size

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


def sight_reduction() -> str:
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

        assert intersections is not None
        assert collection is not None
        return get_representation(intersections, 1)

    except IntersectError as ve:
        print("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
        return "Failed sight reduction."

class ExecButton (Button):
    ''' This is the button starting the sight reduction '''

    def __init__(self, form, **kwargs):
        super().__init__(**kwargs)
        self.form = form
        self.text = "Perform sight reduction!"
# pylint: disable=E1101
        self.bind(on_press=self.callback)
# pylint: enable=E1101

    @staticmethod
    def callback(instance):
        ''' This is the button callback function '''
        print(type(instance))
        assert isinstance(instance, ExecButton)
        the_form = instance.form
        assert isinstance(the_form, InputForm)
        the_form.extract_from_widgets()
        sr = sight_reduction()
        the_form.results.text = sr

#class QuitButton (Button):
#    ''' This button quits the application '''
#    def __init__(self, form, **kwargs):
#        super().__init__(**kwargs)
#        self.form = form
#        self.text = "Quit"
# pylint: disable=E1101
#        self.bind(on_press=self.callback)
# pylint: enable=E1101

#    @staticmethod
#    def callback(_):
#        ''' This is the button callback function '''
        #quit()
#        the_app = App.get_running_app ()
#        if isinstance (the_app, StarFixApp):
#            r = the_app.get_root()
#            r.clear_widgets ()
#            the_app.stop()

class FormRow (BoxLayout):
    ''' This is used for row data in the form '''

    background_color = (0.35, 0.35, 0.35, 1)

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

    def __init__(self, **kwargs):
        super().__init__(text="0", **kwargs)
        self.my_dropdown = DropDown()
        for index in [-1, 0, 1]:
            btn = Button(text=str(index), size_hint_y=None, height=self.height/2)
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
    def __init__(self, **kwargs):
        super().__init__(size_hint = (1,1), **kwargs)

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

    #def stop (self, **kwargs):
    #    super().stop()

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

        #Window.bind(on_request_close=self.end_func)

        self.data_widget_container = {}

        bl = FormRow()
        bl.add_widget(MyLabel(text='DRP Latitude:'))
        self.drp_lat_input = MyTextInput()
        self.data_widget_container["DrpLat"] = self.drp_lat_input
        bl.add_widget(self.drp_lat_input)
        self.add_widget(bl)

        bl = FormRow()
        bl.add_widget(MyLabel(text='DRP Longitude:'))
        self.drp_lon_input = MyTextInput()
        self.data_widget_container["DrpLon"] = self.drp_lon_input
        bl.add_widget(self.drp_lon_input)
        self.add_widget(bl)

        for sight in range(self.nr_of_sights):
            bl = FormRow()
            bl.add_widget(
                MyLabel(text='[b]Use '+str(sight+1)+':[/b]', markup=True))
            x = CheckBox()
            self.data_widget_container["Use"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

            bl = FormRow()
            bl.add_widget(MyLabel(text='Name '+str(sight+1)+':', indent=True))
            x = MyTextInput()
            self.data_widget_container["ObjectName"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

            bl = FormRow()
            bl.add_widget(MyLabel(text='Altitude ' +
                          str(sight+1)+':', indent=True))
            x = MyTextInput()
            self.data_widget_container["Altitude"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

            bl = FormRow()
            bl.add_widget(MyLabel(text='Time '+str(sight+1)+':', indent=True))
            x = MyTextInput()
            self.data_widget_container["Time"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

            bl = FormRow()
            bl.add_widget(MyLabel(text='Index Error ' +
                          str(sight+1)+':', indent=True))
            x = MyTextInput()
            self.data_widget_container["IndexError"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

            bl = FormRow()
            bl.add_widget(MyLabel(text='Limb correction ' +
                          str(sight+1)+':', indent=True))
            x = LimbDropDown()
            self.data_widget_container["LimbCorrection"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

            bl = FormRow()
            bl.add_widget(MyLabel(text='Artificial Horizon ' +
                          str(sight+1)+':', indent=True))
            x = CheckBox()
            self.data_widget_container["ArtificialHorizon"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

            bl = FormRow()
            bl.add_widget(MyLabel(text='Observer Height ' +
                          str(sight+1)+":", indent=True))
            x = MyTextInput()
            self.data_widget_container["ObserverHeight"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

            bl = FormRow()
            bl.add_widget(MyLabel(text='Temperature ' +
                          str(sight+1)+':', indent=True))
            x = MyTextInput()
            self.data_widget_container["Temperature"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

            bl = FormRow()
            bl.add_widget(MyLabel(text='Temp Gradient ' +
                          str(sight+1)+':', indent=True))
            x = MyTextInput()
            self.data_widget_container["TemperatureGradient"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

            bl = FormRow()
            bl.add_widget(MyLabel(text='Pressure ' +
                          str(sight+1)+':', indent=True))
            x = MyTextInput()
            self.data_widget_container["Pressure"+str(sight+1)] = x
            bl.add_widget(x)
            self.add_widget(bl)

        bl = FormRow()
        butt = ExecButton(self)
        bl.add_widget(butt)
        self.add_widget(bl)

        bl = FormRow()
        self.results = MyLabel(text='', markup=True, indent=False)
        bl.add_widget(self.results)
        self.add_widget(bl)

        #bl = FormRow()
        #butt = QuitButton(self)
        #bl.add_widget(butt)
        #self.add_widget(bl)

        self.populate_widgets()

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
                w.text = NUM_DICT[entry]

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
                NUM_DICT[e] = w.text
        dump_dict()

if __name__ == '__main__':
    do_initialize()
    a = StarFixApp ()
    runTouchApp (a.get_root())
    #a.run()
