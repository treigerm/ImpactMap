# TO-DO:
# - get an account for the API
# - get map data from a region:
#    - use Map() function
# - get map from the past:
#    - get history of nodes and remove all timestamps?

from osmapi import OsmApi
from datetime import datetime

osm_api = OsmApi()

# this is a list of dictionaries
# [{ type of element : { element data }  }]
# ATTENTION: still have to define parameters for Map
elements_in_area = osm_api.Map()

def is_before_date(first_date, second_date):
    """Returns true if the first date is before the second one."""
    date_format = "%Y-%m-%d %H:%M:%S"
    formated_first = datetime.strptime(first_date, date_format)
    formated_second = datetime.strptime(second_date, date_format)
    return formated_first < formated_second

# idea: pass this function a parameter so it knows which element-type it processes
# TO DO: What is actually in elemem
def get_elements_after_event(event_time, elements):
    """Given the time of an event and a list of element ID's we return the element ID's which are added after the event."""
    result = []
    for element in elements:
        first_version = get_first_version(element['type'], element['data']['id'])
        time_created = convert_timestamp(first_version['timestamp'])
        if not is_before_date(event_time, time_created):
            result.append(first_version['id'])

    return result

def get_first_version(element_type, element_id):
    """Gets the first_version of the given element."""
    if element_type == "Node":
        first_version = osm_api.NodeGet(element_id, version=1)
    elif element_type == "Way":
        first_version = osm_api.WayGet(element_id, version=1)
    elif element_type == "Relation":
        first_version = osm_api.RelationGet(element_id, version=1)

    return first_version

def convert_timestamp(timestamp):
    """Converts timestamp from the format 'YYYY-MM-DDTHH:MM:SSZ' to  'YYYY-MM-DD HH:MM:SS'"""
    date, time_with_Z = timestamp.split('T')
    clean_time = time_with_Z[:-2]
    return "%s %s" % (date, clean_time)
