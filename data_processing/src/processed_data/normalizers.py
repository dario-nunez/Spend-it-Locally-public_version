"""Normalization factors.

Generates a dataset that contains various normalization factors to be applied to 
numeric columns belonging to OAs.

Input datasets:
- Postcodes_OAs_classifications.csv
- OAs_influence_area.csv
- WCC_Population_by_Age_and_Gender_Feb2020.csv

Output datasets:
- [OA]_Normalizing_properties.csv
"""

import src.common as common
import pandas as pd
import numpy as np
import math

DATA_DIR = ""

# Executer method.
def process_normalizers(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR
    OA_age_dist = get_age_dist_dataset()
    normalizers_df = generate_dataset(OA_age_dist)
    # Previous name: OA_normalizers.csv
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/normalizers/", normalizers_df, "[OA]_Normalizing_properties.csv")

# Dataframe function defining what the "limit" is for the area per meter column.
def area_limit(x):
    result = max(x, 100)
    # if x < 4000:
    #     result = (x * 2)
    return result

# Dataframe function defining what the "limit" is for the households per meter column.
def house_limit(x):
    if x > 0.031:
        # return x / 2
        return 0.02
        # return math.sqrt(x)
    else:
        return x

# Defines groupby aggregation functions for columns based on their type.
def generate_aggregation_map_age(column_types):
    dict = {}
    for i in range(len(column_types.index)):
        c_type = column_types.values[i]
        if str(c_type) == "float64":
            dict[column_types.index[i]] = np.nansum
    return dict

# Returns the cleaned and aggregated age and gender distribution dataset.
def get_age_dist_dataset():
    postcode_oa_df = pd.read_csv(DATA_DIR + "focused_data/authorities/" + "Postcodes_OAs_classifications.csv")
    # Filter by postcode and oa.
    postcode_oa_df = postcode_oa_df[["pcd7","oa11cd"]].rename(columns={"pcd7": "Postcode", "oa11cd": "OA"})
    # Rid postcode of whitespace.
    postcode_oa_df["Postcode"] = postcode_oa_df["Postcode"].apply(lambda x: x.replace(" ", ""))

    age_distribution_df = pd.read_csv(DATA_DIR + "focused_data/acorn/" + "WCC_Population_by_Age_and_Gender_Feb2020.csv")
    # Rid postcode of whitespace.
    age_distribution_df["Postcode"] = age_distribution_df["Postcode"].apply(lambda x: x.replace(" ", ""))
    # Filter unnecessary columns.
    age_distribution_df = age_distribution_df.drop(["Large User", "Deleted"], axis=1)
    # Join dataframes on postcode column.
    joined_df = postcode_oa_df.merge(age_distribution_df, on = "Postcode")
    
    # Groupby.
    AGG_DICT = generate_aggregation_map_age(joined_df.dtypes)
    grouped_df = joined_df.groupby("OA").agg(AGG_DICT).reset_index()
    
    return grouped_df

# Derive columns and produce the normalizers dataset.
def generate_dataset(OA_age_dist):
    OA_influence = pd.read_csv(DATA_DIR + "focused_data/" + "geodata/" + "OAs_influence_area.csv")

    OA_influence = OA_influence.rename(columns={"geo_code":"OA"})
    merged = pd.merge(OA_influence, OA_age_dist, on="OA")
    
    normalizers = pd.DataFrame()

    normalizers["OA"] = merged["OA"]
    normalizers["OA_area_meters"] = merged["polygon_area_meters"]
    normalizers["OA_area_meters_sqrt"] = normalizers["OA_area_meters"].apply(lambda x: math.sqrt(x))
    normalizers["OA_area_meters_sqrt_or_limit"] = normalizers["OA_area_meters_sqrt"].apply(lambda x: area_limit(x))
    normalizers["OA_households"] = merged["Total households"]
    normalizers["OA_households_per_meter"] = normalizers["OA_households"] / normalizers["OA_area_meters"]
    normalizers["OA_households_per_meter_or_limit"] = normalizers["OA_households_per_meter"].apply(lambda x: house_limit(x))
    normalizers["OA_population"] = merged["Total population"]
    normalizers["OA_population_per_meter"] = normalizers["OA_population"] / normalizers["OA_area_meters"]
    normalizers["OA_population_per_meter_sqrt"] = normalizers["OA_population"] / normalizers["OA_area_meters_sqrt"]

    return normalizers
