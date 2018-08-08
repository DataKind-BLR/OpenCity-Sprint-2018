import argparse
import json
import time

import overpass
import pandas as pd

api = overpass.API()

TYPES = {"railway", "highway", "landuse", "natural", "waterway", "military", "office"}
EXCLUSIONS = {
    "railway": {"halt", "platform", "station", "subway_entrance"},
    "natural": {"tree"}
}


def get_features_for_one(lat, lon, distance):
    features = []
    for type_name in TYPES:
        try_count = 0

        while try_count < 5:
            try:
                response = api.Get("node(around:{distance},"
                                   "{latitude},{longitude})"
                                   "[{type_name}]".format(distance=distance,
                                                          latitude=lat,
                                                          longitude=lon,
                                                          type_name=type_name))

                break
            except Exception as e:
                print e.message
                time.sleep(3)
            try_count += 1

        if not response:
            print "ERROR: Unable to fetch type '{}' data for {}".format(type_name, (lat, lon))
            continue

        count = 0
        for feature in response["features"]:
            properties = feature["properties"]
            sub_type = properties[type_name]

            if sub_type in EXCLUSIONS.get(type_name, []):
                print "\t\t", type_name, ",", sub_type, "is excluded"
                continue

            op = {
                "location": {
                    "longitude": feature["geometry"]["coordinates"][0],
                    "latitude": feature["geometry"]["coordinates"][1]
                },
                "name": properties.get("name", ""),
                "type": "{},{}".format(type_name, sub_type)
            }
            count += 1
            features.append(op)

        print "\t\tFor type {}, found {} entities".format(type_name, count)

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

    print "Fetching from Overpass"
    google_output = get_features(args.input, args.distance)

    with open(args.output, "w") as outfile:
        json.dump(google_output, outfile)
