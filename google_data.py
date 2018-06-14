import argparse
import json
import os

import pandas as pd
import requests

# specify types here
TYPES = {"airport", "atm", "bank", "bus_station", "cemetery", "church", "convenience_store", "department_store",
         "doctor", "fire_station", "gas_station", "hindu_temple", "home_goods_store", "hospital", "liquor_store",
         "local_government_office", "lodging", "mosque", "movie_theater", "park", "parking", "pharmacy", "police",
         "post_office", "real_estate_agency", "school", "shopping_mall", "stadium", "subway_station", "taxi_stand",
         "train_station", "transit_station", "university", "moving_company"}

ACCESS_KEY = os.environ.get('GOOGLE_ACCESS_KEY', None)

if ACCESS_KEY == None:
    raise ValueError("Access key is not present. Set environment property 'GOOGLE_ACCESS_KEY'")


def get_features_for_one(lat, lon, distance):
    found_entities = {}
    location = "{},{}".format(lat, lon)
    for typ in TYPES:
        request_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={type}&key={key}".format(
            location=location,
            radius=distance,
            type=typ,
            key=ACCESS_KEY)
        response = requests.get(request_url)
        if response.status_code != 200:
            print "Some error occurred!"
            continue
        found_entities[typ] = (response.json())
        print "\t\tFor type {}, found {} entities".format(typ, len(found_entities[typ]["results"]))
    features = []

    for typ, entities in found_entities.iteritems():
        for result in entities["results"]:
            op = {
                "location": {
                    "longitude": result["geometry"]["location"]["lng"],
                    "latitude": result["geometry"]["location"]["lat"]
                },
                "name": result["name"],
                "type": typ
            }
            features.append(op)

    return features


def get_features(input_file, distance):
    output = {}

    df = pd.read_csv(input_file)
    for (idx, row) in df.iterrows():
        lat = row.loc['Latitude']
        lon = row.loc['Longitude']
        id = row.loc['ID']
        print "\t{} of {}: Fetching features for {}".format(idx, df.shape[0], id)

        try:
            output[id] = {
                "location": {
                    "lat": lat,
                    "lon": lon
                },
                "features": get_features_for_one(lat, lon, distance)
            }
        except Exception as e:
            print "\t", e.message
            output[id] = {
                "location": {
                    "lat": lat,
                    "lon": lon
                },
                "features": [],
                "error": "Some error occurred for lat long: {}".format(e.message)
            }
        print "\tFetched {} features for {}".format(len(output[id]["features"]), id)

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="path of the locations csv file", required=True)
    parser.add_argument("-o", "--output", help="path to output json", required=True)
    parser.add_argument("-d", "--distance", help="radius to consider when fethcing features", required=False,
                        default=500)

    args = parser.parse_args()

    print "Distance", args.distance

    print "Fetching from Google"
    google_output = get_features(args.input, args.distance)

    with open(args.output, "w") as outfile:
        json.dump(google_output, outfile)
