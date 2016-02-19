import overpass
import os
import geojson
import json
import overpy


def get_ids(data):
    json_string = json.dumps(data)
    j = json.loads(json_string)
    node_ids = [ f["id"] for f in j["features"]]
    return node_ids

def count_response(response):
    json_string = json.dumps(response)
    j = json.loads(json_string)
    return len(j["features"])

def get_coords(data):
    json_string = json.dumps(data)
    j = json.loads(json_string)
    first_result = j["elements"][0]
    return [first_result["lat"], first_result["lon"] ]



# TO DO:
# case insensitive
def get_map_by_name(area_name):
    """Give area data from a given area name."""
    overpass_api = overpy.Overpass()
    query = lambda s:'node[name="%s"];%s(around:1000.0);out geom;' % (area_name, s)
    get_data = lambda s: overpass_api.query(query(s))
    ways = get_data("way").ways
    way_ids = map(lambda x: x.id, ways)

    return way_ids

def get_past_map(area_name, date):
    """Give area data from a given area name."""
    date = format_date(date)
    overpass_api = overpy.Overpass()
    query = lambda s:'[date:"%s"];node[name="%s"];%s(around:1000.0);out geom;' % (date, area_name, s)
    get_data = lambda s: overpass_api.query(query(s))
    ways = get_data("way").ways
    way_ids = map(lambda x: x.id, ways)

    return way_ids

# Can be made more efficient
def get_difference(area_name, start_date, end_date):
    """Gets the nodes which were added after a certain time."""
    old_ways = get_past_map(area_name, start_date)
    new_ways = get_past_map(area_name, end_date)
    difference_ways = set(new_ways) - set(old_ways)

    if len(difference_ways) == len(set(new_ways)):
        return []

    return [list(difference_ways), old_ways, new_ways]

def get_start(area_name):
    """Gets the starting coodrinates of the map."""
    overpass_api = overpass.API()
    query = 'node[name="%s"];out geom;' % area_name
    data = data = overpass_api.Get(query)
    return get_coords(data)


def get_num_hospitals(area_name):
    """Gives the number of hospitals in the area and the corresponding ids."""
    overpass_api = overpass.API()
    query = 'node[name="%s"];way(around:1000.0)[amenity="hospital"];' % (area_name)
    data = overpass_api.Get(query)
    return [count_response(data), get_ids(data)]

def get_num_schools(area_name):
    """Gives the number of schools in the area and the corresponding ids."""
    overpass_api = overpass.API()
    query = 'node[name="%s"];way(around:1000.0)[amenity="school"];' % (area_name)
    data = overpass_api.Get(query)
    return [count_response(data), get_ids(data)]

def format_date(date):
    """Format date from YYYYMMDD to YYYY-MM-DDTHH-MM:SSZ."""
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    return "%s-%s-%sT00-01-00Z" % (year, month, day)


# just used for testing
if __name__ == '__main__':
    date2 = "20130811"
    today = "20160218"
    # coordinates of chitambo village
    min_lat, min_lon, max_lat, max_lon = -12.92, 30.62, -12.90, 30.64
    center_lat, center_lon = -12.9153429, 30.6362802

    print get_num_schools("Chitambo")
