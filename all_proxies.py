import json
import argparse
import 
import get_proxies_google

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="path of the locations csv file", required=True)
    parser.add_argument("-o", "--output", help="path to output json", required=True)
    parser.add_argument("-d", "--distance", help="radius to consider when fethcing features", required=False,
                        default=500)

    args = parser.parse_args()

    print "Distance", args.distance

    print "Fetching from Google"
    google_output = get_proxies_google.get_features(args.input, args.distance)
    print "Fetching from Overpass"
    overpass_output = get_proxies_overpass.get_features(args.input, args.distance)

    for community_id, community in google_output.iteritems():
        overpass_output[community_id]['features'].extend(community["features"])
        print "Merged google place and overpass responses for community : ", community_id

    with open(args.output, "w") as outfile:
        json.dump(overpass_output, outfile
