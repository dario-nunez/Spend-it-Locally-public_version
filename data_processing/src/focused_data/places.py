"""Consolidate the mined places datasets.

Consolidates the 783 independent OA places files from the Places API mine into a 
single JSON file. It also filters the types of each place to discard unnecessary
labels.

Input datasets:
- Postcodes_OAs_classifications.csv
- 783 files stored in "raw_data/places"

Output datasets:
- OA_places.json
"""

import src.common as common
import pandas as pd
import json

DATA_DIR = ""

# Exector method.
def process_places(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR
    oas = get_oas()
    filter_places(oas)
    
# Return a list of unique OAs in Westminster.
def get_oas():
    dataset_filtered_by_westminster = pd.read_csv(DATA_DIR + "focused_data/" + "authorities/" + "Postcodes_OAs_classifications.csv")
    oas = set(dataset_filtered_by_westminster["oa11cd"].to_list())
    return oas

# Place type class label filtering function to be applied to each place record.
def filter_func(e):
    filter_mask = ["route", "locality", "sublocality", "sublocality_level_1", "neighborhood", "political"]
    if e in filter_mask:
        return False
    else:
        return True

# Apply the filtering functionality to each OA and consolidate the results.
def filter_places(oas):
    # Save all OAs in the same file. Filter the [types] field
    filtered_map = {}

    for oa in oas:
        oa_map = {}
        f = open(DATA_DIR + "raw_data/places/" + f"{oa}_places.json")
        data = json.load(f)
        for k in data[oa].keys():
            types_list = data[oa][k]["types"]
            filtered_types_list = list(filter(filter_func, types_list)) 
            if len(filtered_types_list) > 0: # or True == True:
                data[oa][k]["types"] = filtered_types_list
                oa_map[k] = data[oa][k]

        filtered_map[oa] = oa_map
    
    output_map = json.dumps(filtered_map, indent=4)
    common.save_json_to_file(DATA_DIR + "focused_data/places/", output_map, "OA_places.json")
