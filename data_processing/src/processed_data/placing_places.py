"""Supply/demand based place positioning index.

Calculates supply & demand metrics for bars, cafes and restaurants in regards to
all 6 demographic types throughout the borough.

Input datasets:
- [Places]_counts_normalized_by_OA_effective_area.csv
- [Population]_total_over_24_hour.csv

Output datasets:
- [Supply_demand]_example.csv
"""

import src.common as common
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

DATA_DIR = ""
DEMO_TYPES = ["worker", "student", "tourist", "shopper", "leisurer", "chorer", "resident"]

RELEVANT_COLUMNS = []

# Executer method.
def process_placing_places(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR
    places = get_places_per_effective_area()
    population = get_population_per_effective_area()
    supply_demand_index = get_supply_demand_index(places, population)
    supply_demand_index = round_numeric_columns(supply_demand_index)
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/placing_places/", supply_demand_index, "[Supply_demand]_example.csv")

def round_numeric_columns(dataset):
    for i in dataset.dtypes.index:
        if is_numeric_dtype(dataset[i]):
            dataset[i] = dataset[i].apply(lambda x: round(x, common.DPs))
    return dataset

# Return a normalized version of the places dataset between 0 and 1.
def get_places_per_effective_area():
    df = pd.read_csv(DATA_DIR + "processed_data/places/" + "[Places]_counts_normalized_by_OA_effective_area.csv")
    df = df.drop(columns=["Unnamed: 0"])
    cols_to_keep = ["OA", "bar", "cafe", "restaurant"]
    df = df[cols_to_keep]

    # Normalize them all out of 100:
    # for col in cols_to_keep:
    #     if col != "OA":
    #         col_sum = df[col].sum(axis = 0)
    #         df[f"[%_of_borough_total] - {col}"] = (df[col] / col_sum) * 100

    # Normalize them all out of 1:
    for col in cols_to_keep:
        if col != "OA":
            col_min = df[col].min()
            col_max = df[col].max()
            df[f"[normalized_to_[0-1]] - {col}"] = ((df[col] - col_min) / (col_max - col_min))

    return df

# Return a normalized version of the population dataset between 1 and 0.
def get_population_per_effective_area():
    df = pd.read_csv(DATA_DIR + "processed_data/placing_places/" + "[Population]_total_over_24_hour.csv")
    df = df.drop(columns=["Unnamed: 0"])
    cols_to_keep = ["OA"] + [f"[per_effective_area_square_meter] - {x}_count" for x in DEMO_TYPES]
    cols_to_keep = cols_to_keep + ["[per_effective_area_square_meter] - visitors_total_count", "[per_effective_area_square_meter] - total_count"]
    df = df[cols_to_keep]

    # Normalize them all out of 1:
    for col in cols_to_keep:
        if col != "OA":
            col_min = df[col].min()
            col_max = df[col].max()
            df[f"[normalized_to_[0-1]] - {col}"] = ((df[col] - col_min) / (col_max - col_min))

    return df

# Compute 2 supply and demand metrics. Supply/demand distribution differences and
# supply/demand index.
def get_supply_demand_index(places, population):
    df = pd.merge(places, population, on="OA")

    # Distribution differences.
    for type_col in ["bar", "cafe", "restaurant"]:
        for demo_col in DEMO_TYPES:
            df[f"[supply - demand] - [normalized_[0-1]_proportions] - {type_col}_{demo_col}"] = df[f"[normalized_to_[0-1]] - {type_col}"] - df[f"[normalized_to_[0-1]] - [per_effective_area_square_meter] - {demo_col}_count"]
    for type_col in ["bar", "cafe", "restaurant"]:
        for demo_col in ["visitors_total", "total"]:
            df[f"[supply - demand] - [normalized_[0-1]_proportions] - {type_col}_{demo_col}"] = df[f"[normalized_to_[0-1]] - {type_col}"] - df[f"[normalized_to_[0-1]] - [per_effective_area_square_meter] - {demo_col}_count"]

    # Supply and demand index.
    for type_col in ["bar", "cafe", "restaurant"]:
        df[f"{type_col}_or_limit"] = df[type_col].apply(lambda x: max(x, 0.02))

    for type_col in ["bar", "cafe", "restaurant"]:
        for demo_col in DEMO_TYPES:
            df[f"[supply_demand_index] - {type_col}_{demo_col}"] = (df[f"[per_effective_area_square_meter] - {demo_col}_count"] / df[f"{type_col}_or_limit"])
    for type_col in ["bar", "cafe", "restaurant"]:
        for demo_col in ["visitors_total", "total"]:
            df[f"[supply_demand_index] - {type_col}_{demo_col}"] = (df[f"[per_effective_area_square_meter] - {demo_col}_count"] / df[f"{type_col}_or_limit"])

    for type_col in ["bar", "cafe", "restaurant"]:
        df = df.drop(columns=[f"{type_col}_or_limit"])

    for type_col in ["bar", "cafe", "restaurant"]:
        for demo_col in DEMO_TYPES:
            df[f"[shared_scale] - [supply_demand_index] - {type_col}_{demo_col}"] = df[f"[supply_demand_index] - {type_col}_{demo_col}"]

    df = df.replace([np.inf, -np.inf], 0)
    return df
