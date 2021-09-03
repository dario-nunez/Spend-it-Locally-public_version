"""Place type by OA tally. 

From the OA_places.json file, it reduces the complexity of the dataset by tabulating
the count of each place type per OA. Further normalization operations on the vanilla
tally dataset are then applied.

Input datasets:
- place_types.csv
- OA_places.json
- Postcodes_OAs_classifications.csv
- [OA]_Normalizing_properties.csv
- [Places]_counts.csv (requested after the script generates it)

Output datasets:
- [Places]_counts_normalized_by_OA_effective_area.csv
- [Places]_counts_normalized_by_household_per_meter.csv
- [Places]_counts_normalized_by_household_per_meter_bound.csv
- [Places]_counts_no_shared_scale.csv
- [Places]_counts.csv
"""

import src.common as common
import pandas as pd
import json
import numpy as np
from pandas.api.types import is_numeric_dtype

DATA_DIR = ""

# Executer method. The time consuming operations are disabled by default.
def process_places(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR
    # possible_place_types = get_possible_place_types()
    # oas = get_oas()
    # oa_place_types = get_OA_place_types(possible_place_types, oas)
    # tally_place_types_in_OA(oa_place_types, oas)
    normalise_oa_place_tally()

################################################################################
# Helper functions.
################################################################################

def round_numeric_columns(dataset):
    for i in dataset.dtypes.index:    
        if is_numeric_dtype(dataset[i]):
            dataset[i] = dataset[i].apply(lambda x: round(x, common.DPs))
    
    return dataset   

def get_possible_place_types():
    dataset_name = "place_types.csv"
    dataset = pd.read_csv(DATA_DIR + "raw_data/place_types/" + dataset_name)
    possible_place_types = set(dataset["place_types"].to_list())
    return possible_place_types

def get_oas():
    dataset_filtered_by_westminster = pd.read_csv(DATA_DIR + "focused_data/" + "authorities/" + "Postcodes_OAs_classifications.csv")
    oas = set(dataset_filtered_by_westminster["oa11cd"].to_list())
    return oas

def get_OA_place_types(possible_place_types, oas):
    # Get place types present in the Westminster data.
    # Maybe get the frequency with which each subset appears in one entity?
    types = set()

    f = open(DATA_DIR + "focused_data/places/" + "OA_places.json")
    data = json.load(f)

    for oa in oas:
        for k in data[oa].keys():
            types_list = data[oa][k]["types"]
            
            for t in types_list:
                if t in possible_place_types:
                    types.add(t)
                
    return types

################################################################################
# Relevant dataset generation.
################################################################################

# Generates the count of each place type by OA dataset.
def tally_place_types_in_OA(place_types_list, oas):
    sorted_places_types_list = list(place_types_list)
    sorted_places_types_list.sort()

    OA_place_tally = pd.DataFrame(columns = (["OA"] + sorted_places_types_list))

    f = open(DATA_DIR + "focused_data/places/" + "OA_places.json")
    data = json.load(f)

    counter = 1

    for oa in oas:
        print(f"{counter} - {oa}")
        OA_place_tally = OA_place_tally.append({"OA":oa}, ignore_index=True)
        OA_place_tally = OA_place_tally.replace(np.nan, 0)

        for k in data[oa].keys():
            types_list = data[oa][k]["types"]

            for t in types_list:
                if t in place_types_list:
                    OA_place_tally.loc[OA_place_tally["OA"] == oa, t] = OA_place_tally.loc[OA_place_tally["OA"] == oa, t] + 1
        
        counter = counter + 1

    print(OA_place_tally)

    for col in sorted_places_types_list:
        OA_place_tally = OA_place_tally.rename(columns={col: f"{col}"})

    OA_place_tally = round_numeric_columns(OA_place_tally)
    # Previous name: OA_place_tally.csv
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/places/", OA_place_tally, "[Places]_counts_no_shared_scale.csv")
    OA_place_tally = add_shared_scale_columns(OA_place_tally)
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/places/", OA_place_tally, "[Places]_counts.csv")

# Generates 3 normalization variants on the original tally:
# 1. Normalized by effective area.
# 2. Normalized by households.
# 3. Normalized by households with an applied limit.
def normalise_oa_place_tally():
    normalizers = pd.read_csv(DATA_DIR + "processed_data/normalizers/" + "[OA]_Normalizing_properties.csv")
    oa_type_tally = pd.read_csv(DATA_DIR + "processed_data/places/" + "[Places]_counts.csv")
    oa_type_tally = oa_type_tally.drop(['Unnamed: 0'], axis=1)
    normalizers = normalizers[["OA", "OA_area_meters", "OA_area_meters_sqrt", "OA_households_per_meter", "OA_households_per_meter_or_limit"]]

    # print(normalizers)
    # print(oa_type_tally)

    merged = pd.merge(normalizers, oa_type_tally, on="OA")
    
    # Normalize by area.
    normalized_by_effective_area = pd.DataFrame()
    normalized_by_effective_area["OA"] = merged["OA"]
    for c in merged.loc[:, "accounting":"zoo"]:
        # Attempt at trying other normalization options.
        # sum_col = merged[c].sum(axis=0)
        # print(c, sum_col)
        # merged[c+"_test"] = merged[c] / sum_col

        # Square root of area creates a much better estimate. Usable/buildable area of OAs in London is well estimated 
        # by the square root of the total area.

        # merged[c+"_by_area_sqr"] = merged[c] / merged["OA_area_meters_sqrt"]
        normalized_by_effective_area[c] = merged[c] / merged["OA_area_meters_sqrt"]
    normalized_by_effective_area = add_shared_scale_columns(normalized_by_effective_area)
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/places/", normalized_by_effective_area, "[Places]_counts_normalized_by_OA_effective_area.csv")

    # Normalize by households.
    normalized_by_household_per_meter = pd.DataFrame()
    normalized_by_household_per_meter["OA"] = merged["OA"]
    for c in merged.loc[:, "accounting":"zoo"]:
        # Accurate regarding number of homes but not indicative of much information.
        # merged[c+"_by_house_per_meter"] = merged[c] * merged["OA_households_per_meter"]
        normalized_by_household_per_meter[c] = merged[c] * merged["OA_households_per_meter"]
    normalized_by_household_per_meter = add_shared_scale_columns(normalized_by_household_per_meter)
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/places/", normalized_by_household_per_meter, "[Places]_counts_normalized_by_household_per_meter.csv")

    # Normalize by households limit.
    normalized_by_household_per_meter_bounded = pd.DataFrame()
    normalized_by_household_per_meter_bounded["OA"] = merged["OA"]
    for c in merged.loc[:, "accounting":"zoo"]:
        # Lightens up the map from above.
        # merged[c+"_by_house_per_meter_or_limit"] = merged[c] * merged["OA_households_per_meter_or_limit"]
        normalized_by_household_per_meter_bounded[c] = merged[c] * merged["OA_households_per_meter_or_limit"]
    normalized_by_household_per_meter_bounded = add_shared_scale_columns(normalized_by_household_per_meter_bounded)
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/places/", normalized_by_household_per_meter_bounded, "[Places]_counts_normalized_by_household_per_meter_bound.csv")

# Adds a selection of columns that contain a prefix that will cause visualizations
# to render on a shared scale in the user interface.
def add_shared_scale_columns(df):
    exempt_columns = ["establishment", "point_of_interest", "health", "doctor", "food", "store"]
    for col in df.loc[:, "accounting":"zoo"].columns:
        if col not in exempt_columns:
            df[f"[shared_scale] - {col}"] = df[col]
        
    return df
