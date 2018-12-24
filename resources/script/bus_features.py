import json
import pandas as pd
from shapely.geometry import Point, shape
from multiprocessing.dummy import Pool as ThreadPool


bmtc_routes = pd.read_csv('routes.csv')

bmtc_routes.info()

# The links don't work, so dropping them.
bmtc_routes.drop(['Unnamed: 0', 'map_link', 'busstops_link'], axis='columns', inplace=True)

bmtc_routes.head()

bus_stop_coordinates = bmtc_routes['map_json_content']
bus_stops_json = {}

# Map the route number and the stop coordinates
for idx, stop_coordinates in enumerate(bus_stop_coordinates):
    bus_stops_json[str(bmtc_routes['route_no'].iloc[idx]).strip()] = stop_coordinates

eg = json.loads(bus_stops_json['1'])

with open('bbmp-wards.json') as fp:
    wards_json = json.load(fp)

ward_features = wards_json['features']

for idx, var in enumerate(ward_features):
    ward_features[idx]['properties']['number_of_bus_stops'] = 0

ward_name = ward_features[0]['properties']['Ward_Name']


def number_of_bus_stops_in_ward(bus_stop_coordinates_json):
    '''
    wards_features: The ward level geojson file
    bus_stop_coordinates_geojson: Mapping between route number and the latlong
    
    return: Number of bus stops in a ward as part of the wards_geojson file
    '''

    pool = ThreadPool(6)
    # for route_number, details in bus_stop_coordinates_json.items():

    pool.map(populate_for_route, bus_stop_coordinates_json.values())
    # populate_for_route(details)

    return ward_features


def populate_for_route(details):
    if not isinstance(details, str):
        return
    location = json.loads(details)
    for idx, stop_location in enumerate(location):
        lat_long = stop_location['latlons']
        bus_stop = Point(float(lat_long[1]), float(lat_long[0]))
        for idx, ward_feature in enumerate(ward_features):
            ward_coordinates = shape(ward_features[idx]['geometry'])
            if bus_stop.within(ward_coordinates):
                known_bus_stops = ward_features[idx]['properties'].get('bus_stop_coordinates', None)
                if known_bus_stops is None:
                    known_bus_stops = {'bus_stops': [lat_long]}
                    ward_features[idx]['properties']['number_of_bus_stops'] += 1
                elif lat_long in known_bus_stops.values():
                    continue
                else:
                    known_bus_stops['bus_stops'].append(lat_long)
                    ward_features[idx]['properties']['number_of_bus_stops'] += 1
                ward_features[idx]['properties']['bus_stop_coordinates'] = known_bus_stops
            else:
                continue


updated_ward_details = number_of_bus_stops_in_ward(bus_stops_json)


