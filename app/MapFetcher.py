import overpass
import os
import geojson
import json
import overpy
import xml.etree.ElementTree as ET
from StringIO import StringIO


def get_current_map(min_lat, min_lon, max_lat, max_lon, responseformat="geojson"):
    """Gets the map-data in a given boundary. Remember min_lat < max_lat and min_lon < max_lon."""
    overpass_api = overpass.API()
    # runs query for node, way or relation
    query = lambda s:'%s(%s, %s, %s, %s);out geom;' % (s, min_lat, min_lon, max_lat, max_lon)
    get_data = lambda s: overpass_api.Get(query(s), responseformat=responseformat)

    return [get_data("node"), get_data("way")]

def get_map_by_center_point(lat, lon, responseformat="geojson"):
    """Gets the map data from a given area ID."""
    overpass_api = overpass.API()
    query = lambda s:'%s(around:100.0, %s, %s);out geom;' % (s, lat, lon)
    get_data = lambda s: overpass_api.Get(query(s), responseformat=responseformat)

    return [get_data("node"), get_data("way")]

def get_ids(f_type, get_data):
    json_string = json.dumps(get_data(f_type))
    j = json.loads(json_string)
    node_ids = [ f["id"] for f in j["features"]]
    return node_ids

# TO DO:
# compatibility with different formats // not really necessary
def save_file_in_res(data, name):
    """Save a file in the res folder."""
    # go to the res folder in the current working directory
    os.chdir(os.getcwd())
    os.chdir("res")

    with open(name, "w+") as f:
        geojson.dump(data, f)

    # we need to change back to the inital directory because otherwise the
    # program will fail the next time
    os.chdir("../")

# TO DO:
# case insensitive
def get_map_by_name(area_name):
    """Give area data from a given area name."""
    overpass_api = overpy.Overpass()
    query = lambda s:'node[name="%s"];%s(around:1000.0);out geom;' % (area_name, s)
    get_data = lambda s: overpass_api.query(query(s))
    nodes = get_data("node").nodes
    ways = get_data("way").ways
    node_ids = map(lambda x: x.id, nodes)
    way_ids = map(lambda x: x.id, ways)

    return [node_ids, way_ids]

def get_past_map(area_name, date):
    """Give area data from a given area name."""
    overpass_api = overpy.Overpass()
    query = lambda s:'[date:"%s"];node[name="%s"];%s(around:1000.0);out geom;' % (date, area_name, s)
    get_data = lambda s: overpass_api.query(query(s))
    nodes = get_data("node").nodes
    ways = get_data("way").ways
    node_ids = map(lambda x: x.id, nodes)
    way_ids = map(lambda x: x.id, ways)

    return [node_ids, way_ids]

def get_difference(area_name, date):
    old_nodes, old_ways = get_past_map2(area_name, date)
    new_nodes, new_ways = get_map_by_name(area_name)

    return [list(set(new_nodes)-set(old_nodes)), list(set(new_ways) - set(old_ways))]

# TO DO:
# get number of hostpitals, schools
def get_num_hospitals(area_name):
    overpass_api = overpass.API()
    query = 'node[name="%s"];way(around:1000.0)[amenity="hospital"];out geom;' % (area_name)
    data = overpass_api.Get(query, responseformat="xml")
    tree = ET.parse('country_data.xml')
    root = tree.getroot()
    num_hospitals = dt["elements"][0]["count"]["total"]
    return get_num_hospitals



# currently just used for testing
if __name__ == '__main__':
    date = '2015-08-10T01:01:01Z'
    # coordinates of chitambo village
    min_lat, min_lon, max_lat, max_lon = -12.92, 30.62, -12.90, 30.64
    center_lat, center_lon = -12.9153429, 30.6362802

    nodes, ways = get_map_by_name("Chitambo")
    nodes2, ways2 = get_past_map("Chitambo", date)
    nodes3, ways3 = get_difference("Chitambo", date)
    print nodes3
    print len(nodes3)
