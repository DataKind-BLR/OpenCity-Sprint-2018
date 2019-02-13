import csv
import json

# file_name = "bbmp-wards.geojson"
file_name = "bengaluru_india_amenities_metrics.geojson"
output_file = "bengaluru_india_amenities_metrics.csv"
# output_file = "geojson_to_csv_updated.csv"


with open(file_name, encoding='utf-8') as data_file:
    wards = json.loads(data_file.read())

headers = ["Name", "description", "Ward_Name", "Zone", "Division", "Subdivision", "Assembly__MLA__Constituency_",
           "Parliament__MP__Constituency", "geo.coordinates"]

with open(output_file, 'w') as myfile:
    wr = csv.writer(myfile, quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    wr.writerow(headers)
    for feature in wards["features"]:
        feat = []
        prop = feature["properties"]
        for head in headers[:-1]:
            feat.append(prop[head])
        dumps = json.dumps(feature)
        print(dumps)
        feat.append(dumps)
        wr.writerow(feat)
