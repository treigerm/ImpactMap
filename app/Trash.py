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
