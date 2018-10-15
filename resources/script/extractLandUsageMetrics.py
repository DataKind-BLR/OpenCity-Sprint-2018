import shapely
import json
#import geojson
import os
import pandas as pd
import numpy as np

from collections import Counter
from shapely.geometry import shape,Point



# READ JSON AND GEOJSON FILE

with open('bengaluru_india_amenities_metrics.geojson', 'r') as h:
    metrics_data = json.load(h)

with open('bengaluru_india_landusages.geojson', 'r') as f:
    js = json.load(f)

    


list_land_type = ['cinema','garden','orchard','park','playground','recreation_ground','sports_centre','theatre']

list_all = []
for ward_feature in metrics_data['features']:                    # Loop within Ward JSON
    ward_shape = shape(ward_feature['geometry'])                 # Define Ward_Shape as shapely Obj
    
    land_type = Counter()                                        # Initialize Counter to count by amenity types
    
    for land_feature in js['features']:                          # Loop within amenities JSON
        land_area = shape(land_feature['geometry'])          # Define Amenity_Point as shapely obj
        if(land_area.within(ward_shape) or land_area.intersection(ward_shape)) and (land_feature['properties']['type'] in list_land_type):        # Check if LandShape lies within/intersects WardShape
            land_type[land_feature['properties']['type']] +=1 # Update Counter

    # Add COUNT_CINEMA METRIC
    if 'cinema' in land_type:
        ward_feature['properties']['count_cinema'] = land_type['cinema']
    else:
        ward_feature['properties']['count_cinema'] = 0
        
    # Add COUNT_GARDEN METRIC
    if 'garden' in land_type:
        ward_feature['properties']['count_garden'] = land_type['garden']
    else:
        ward_feature['properties']['count_garden'] = 0
        
    # Add COUNT_ORCHARD METRIC
    if 'orchard' in land_type:
        ward_feature['properties']['count_orchard'] = land_type['orchard']
    else:
        ward_feature['properties']['count_orchard'] = 0
        
    # Add COUNT_LIBRARY METRIC
    if 'park' in land_type:
        ward_feature['properties']['count_park'] = land_type['park']
    else:
        ward_feature['properties']['count_park'] = 0
        
    # Add COUNT_PLAYGROUND METRIC
    if 'playground' in land_type:
        ward_feature['properties']['count_playground'] = land_type['playground']
    else:
        ward_feature['properties']['count_playground'] = 0
        
    # Add COUNT_REC_GROUND METRIC
    if 'recreation_ground' in land_type:
        ward_feature['properties']['count_recreation_ground'] = land_type['recreation_ground']
    else:
        ward_feature['properties']['count_recreation_ground'] = 0
        
    # Add COUNT_SPORTS_CENTRE METRIC
    if 'sports_centre' in land_type:
        ward_feature['properties']['count_sports_centre'] = land_type['sports_centre']
    else:
        ward_feature['properties']['count_sports_centre'] = 0
        
    # Add COUNT_THEATRE METRIC
    if 'theatre' in land_type:
        ward_feature['properties']['count_theatre'] = land_type['theatre']
    else:
        ward_feature['properties']['count_theatre'] = 0
        
    feature_list = [ward_feature['properties']['Ward_Name'],
                    ward_feature['properties']['count_cinema'],
                    ward_feature['properties']['count_garden'],
                    ward_feature['properties']['count_orchard'],
                    ward_feature['properties']['count_park'],
                    ward_feature['properties']['count_playground'],
                    ward_feature['properties']['count_recreation_ground'],
                    ward_feature['properties']['count_sports_centre'],
                    ward_feature['properties']['count_theatre']]
    
    list_all.append(feature_list)


# WRITE GEOJSON FILE
with open('bengaluru_india_indicator_metrics.geojson', 'w') as outfile:
    json.dump(metrics_data, outfile)