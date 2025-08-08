''' Simple sample representing a trip at sea with supporting celestial navigation
    © August Linnman, 2025, email: august@linnman.net

    This is a simple refactoring of common code used in the notebooks

    MIT License (see LICENSE file)       
'''

import json
from types import NoneType
from pydoc import locate
import ipywidgets as widgets
from ipywidgets import Layout, VBox
from folium import Map as Folium_Map
from starfix import LatLonGeodetic, SightCollection, Sight, IntersectError,\
                    get_representation, get_google_map_string

NUM_DICT = None
FILE_NAME = None
TYPE_ARRAY = None

def get_dict () -> dict:
    ''' Return the genererated dictionary'''
    assert isinstance (NUM_DICT, dict)
    return NUM_DICT

def get_type_array () -> dict:
    ''' Return the generated type array '''
    assert isinstance (TYPE_ARRAY, dict)
    return TYPE_ARRAY

def str2bool(v):
    ''' Simple conversion from bool to string '''
    return v.lower() in ("yes", "true", "t", "1")

def initialize (fn : str, init_dict : dict) :
    ''' Initialize the helper '''
#pylint: disable=W0603
    global FILE_NAME
    global NUM_DICT
#pylint: enable=W0603
    FILE_NAME = fn

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            s = f.read ()
            NUM_DICT = json.loads (s)
    except FileNotFoundError:
        NUM_DICT = init_dict

def dump_dict ():
    ''' Dumps the contents to a json file '''
    j_dump = json.dumps (NUM_DICT)
    assert isinstance (FILE_NAME, str)
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(j_dump)

def handle_change (change):
    ''' Handler for widget events '''
    if change['type'] == 'change' and change['name'] == 'value':
        the_owner = change['owner']
        the_owner.handle_event (change)

style = {'description_width': '100px'}

#pylint: disable=R0901
class MyTextWidget (widgets.Text):

    ''' This class represents simple text input'''

    def __init__ (self, attr_name, description):
        self.__attr_name = attr_name
        assert isinstance (NUM_DICT, dict)
        super().__init__ (NUM_DICT[self.__attr_name],
                          description=description, disabled=False,
                          style=style,
                          layout=Layout(width='90%'))
        self.observe (handle_change)

    def __copy__ (self):
        raise NotImplementedError

    def __deepcopy__ (self, _):
        raise NotImplementedError

    def handle_event (self, change):
        ''' Event terminator '''
        assert isinstance (NUM_DICT, dict)
        NUM_DICT[self.__attr_name]=change['new']
        dump_dict ()

class MyCheckboxWidget (widgets.Checkbox):
    ''' This class represents checkboxes '''

    def __init__ (self, attr_name, description):
        self.__attr_name = attr_name
        assert isinstance (NUM_DICT, dict)
        super().__init__ (str2bool(NUM_DICT[self.__attr_name]),
                          description=description, disabled=False,
                          style=style)
        self.observe (handle_change)

    def __copy__ (self):
        raise NotImplementedError

    def __deepcopy__ (self, _):
        raise NotImplementedError

    def handle_event (self, change):
        ''' Event terminator '''
        assert isinstance (NUM_DICT, dict)
        NUM_DICT[self.__attr_name]=str(change['new'])
        dump_dict ()

class MyLimbDropdown (widgets.Dropdown):
    ''' This class represents dropdowns '''
    def __init__ (self, attr_name, description):
        self.__attr_name = attr_name
        assert isinstance (NUM_DICT, dict)
        super().__init__ (value=NUM_DICT[self.__attr_name],
                          options=[("Lower",'-1'),("Central", '0'),("Upper",'1')],
                          description=description, disabled=False, style=style)
        self.observe (handle_change)

    def __copy__ (self):
        raise NotImplementedError

    def __deepcopy__ (self, _):
        raise NotImplementedError

    def handle_event (self, change):
        ''' Event terminator '''
        assert isinstance (NUM_DICT, dict)
        NUM_DICT[self.__attr_name]=str(change['new'])
        dump_dict ()
#pylint: enable=R0901

def render_widget (ta : list, nr_of_views : int, include_drp : bool = True) -> list:
    ''' Renders the widget layout used by the notebooks '''
#pylint: disable=W0603
    global TYPE_ARRAY
#pylint: enable=W0603
    widget_array = []
    TYPE_ARRAY = ta
    if include_drp:
        widget_array.append (MyTextWidget ("DrpLat","𝗗𝗥𝗣_𝗟𝗔𝗧"))
        widget_array.append (MyTextWidget ("DrpLon","𝗗𝗥𝗣_𝗟𝗢𝗡"))
    for i in range (nr_of_views):
        widget_array.append (MyCheckboxWidget("Use"+str(i+1),\
                                              description="Use " + str(i+1)))
        vbox_array = []
        for _,v in enumerate (TYPE_ARRAY):
            cl = locate ("notebook_helper." + v[2])
            assert isinstance (cl, type)
            obj = cl (v[0]+str(i+1),
                      description=v[1]+"_"+str(i+1))
            vbox_array.append (obj)
        widget_array.append (VBox(vbox_array, layout=Layout(margin='0 0 0 20px')))
    return widget_array

def get_starfixes (drp_pos : LatLonGeodetic) -> SightCollection :
    ''' Returns a list of used star fixes (SightCollection) '''

    Sight.set_estimated_position (drp_pos)
    retval = []
    assert isinstance (NUM_DICT, dict)
    assert isinstance (TYPE_ARRAY, list)
    for i in range (3):
        if str2bool(NUM_DICT["Use"+str(i+1)]):
            retval.append (Sight ( object_name          =
                                       NUM_DICT         [TYPE_ARRAY[0][0]+str(i+1)],
                                   measured_alt         =
                                       NUM_DICT         [TYPE_ARRAY[1][0]+str(i+1)],
                                   set_time             =
                                       NUM_DICT         [TYPE_ARRAY[2][0]+str(i+1)],
                                   index_error_minutes  =
                                       float(NUM_DICT   [TYPE_ARRAY[3][0]+str(i+1)]),
                                   limb_correction      =
                                       int(NUM_DICT     [TYPE_ARRAY[4][0]+str(i+1)]),
                                   artificial_horizon   =
                                       str2bool(NUM_DICT[TYPE_ARRAY[5][0]+str(i+1)]),
                                   observer_height      =
                                       float(NUM_DICT   [TYPE_ARRAY[6][0]+str(i+1)]),
                                   temperature          =
                                       float(NUM_DICT   [TYPE_ARRAY[7][0]+str(i+1)]),
                                   dt_dh                =
                                       float(NUM_DICT   [TYPE_ARRAY[8][0]+str(i+1)]),
                                   pressure             =
                                       float(NUM_DICT   [TYPE_ARRAY[9][0]+str(i+1)])
                                 ))

    return SightCollection (retval)


# SIGHT REDUCTION.

def sight_reduction () -> Folium_Map | NoneType:
    ''' Perform a sight reduction given data entered above '''
    assert isinstance (NUM_DICT, dict)
    the_pos = LatLonGeodetic (float(NUM_DICT["DrpLat"]),
                              float(NUM_DICT["DrpLon"]))

    intersections = None
    collection = None
    the_map = None
    try:
        intersections, _, _, collection, _ =\
                SightCollection.get_intersections_conv (return_geodetic=True,
                                                        estimated_position=the_pos,
                                                        get_starfixes=get_starfixes,
                                                        assume_good_estimated_position=True)

        assert intersections is not None
        assert collection is not None
        print (get_representation(intersections,1))
        assert isinstance (intersections, LatLonGeodetic)
        print ("Google Map Coordinate = " + get_google_map_string(intersections,4))

    except IntersectError as ve:
        print ("Cannot perform a sight reduction. Bad sight data.\n" + str(ve))
        if ve.coll_object is not None:
            if isinstance (ve.coll_object, SightCollection):
                collection = ve.coll_object

    if isinstance (intersections, tuple):
        intersections = None

    if collection is not None:
        the_map = collection.render_folium (intersections)
        assert isinstance (the_map, Folium_Map)
        return the_map
    else:
        return None
