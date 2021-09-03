"""Geodata (geographical boundary data) datasets.

Filters the UK geojson file by the region of Westminster and its contained OAs. The
resulting file still requires transformations that in this case, are done by hand.

The following operations can be done with the online tool Mapshaper:
1. Its coordinate system is the British OSGB36 which is not the global standard. It
must be converted to WGS84.
2. To reduce its large size and improve efficiency, a topojson copy of the file can
be produced. This is an equivalent format to geojson but more space efficient.

Mapshaper url: https://mapshaper.org/

Input datasets:
- OAs_ward.csv
- OAs_geojson.json

Output datasets:
- OAs_geojson_osgb36.json
- OAs_geojson_wgs84.json
- OAs_topojson_wgs84.json
"""

import src.common as common
import pandas as pd
import json

DATA_DIR = ""

# Executer method.
def focus_geodata(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR
    oas = get_oas()
    # oas_geojson(oas) # The raw OAs_geojson.json file must be downloaded first.

# Retrieve list of OAs.
def get_oas():
    dataset_filtered_by_westminster = pd.read_csv(DATA_DIR + "focused_data/authorities/" + "OAs_ward.csv")
    oas = set(dataset_filtered_by_westminster["OA"].to_list())
    return oas

# Output Areas GeoJson. Filter by Westminster OAs.
def oas_geojson(oas):
    dataset_name = "OAs_geojson.json"
    with open(DATA_DIR + "raw_data/geodata/" + dataset_name) as json_file:
        input_dict = json.load(json_file)
        output_dict_features = [x for x in input_dict["features"] if x["properties"]["geo_code"] in oas]
        output_dict = input_dict
        output_dict["features"] = output_dict_features
        output_json = json.dumps(output_dict)
    common.save_json_to_file(DATA_DIR + "focused_data/geodata/", output_json, "OAs_geojson.json")
