# TO-DO:
# - get the current map data - works
# - get the map data from the past - might work
# - get the difference between the maps
import xml.etree.ElementTree as ET
import overpass


# ATTENTION: right know just nodes
def get_current_map_data(min_lat, min_lon, max_lat, max_lon):
    """Gets the map-data in a given boundary. Remember min_lat < max_lat and min_lon < max_lon."""
    overpass_api = overpass.API()
    query = lambda s:'%s(%s, %s, %s, %s);out;' % (s, min_lat, min_lon, max_lat, max_lon)
    get_xml = lambda s: overpass_api.Get(query(s), responseformat="xml")
    #you have to get the ways and relations as well
    return get_xml("node")

def get_map_by_area_id(area_id):
    """Gets the map data from a given area ID."""
    query_node = 'node(area:%s);out;' % (area_id)

def get_past_map_data(min_lat, min_lon, max_lat, max_lon, date):
    """Gets the map-data of a given data. Date in format 'YYYY-MM-DDTHH:MM:SSZ'"""
    end = 'http://overpass-api.de/api/interpreter?data=[date:"%s"];' % date
    overpass_api = overpass.API(endpoint=end)
    query = lambda s:'%s(%s, %s, %s, %s);out;' % (s, min_lat, min_lon, max_lat, max_lon)
    nodes = overpass_api.Get(query("node"), responseformat="xml")
    return nodes

def get_difference(min_lat, min_lon, max_lat, max_lon, past_date):
    """Gets the difference from a given event in XML."""
    end = 'http://overpass-api.de/api/interpreter?data=[diff:"%s"];' % date
    overpass_api = overpass.API(endpoint=end)
    query = lambda s:'%s(%s, %s, %s, %s);out;' % (s, min_lat, min_lon, max_lat, max_lon)
    nodes = overpass_api.Get(query("node"), responseformat="xml")
    return nodes

# currently just used for testing
if __name__ == '__main__':
    date = '2015-02-10T01:01:01Z'
    # coordinates of chitambo village
    min_lat, min_lon, max_lat, max_lon = -12.92, 30.62, -12.90, 30.64
    xml_result = get_current_map_data(min_lat, min_lon, max_lat, max_lon)
    xml2 = get_past_map_data(min_lat, min_lon, max_lat, max_lon, date)
    xml3 = get_difference(min_lat, min_lon, max_lat, max_lon, date)
    print xml3
