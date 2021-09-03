"""Population (daytime and nightime).

Compiles all the population information in the datasets. Joins the estimate values
for the 6 demographic types with the counts for residents. Also highlight the distinction
between the groups visitors and residents.

The numbers used in this dataset are generated using the supertypes_discriminant
demographic distributions by place model.

Input datasets:
- [OA]_Normalizing_properties.csv
- [Demographic_distribution]_supertypes_discriminant_borough_scope.csv

Output datasets:
- [Population]_total_over_24_hour.csv
"""

import src.common as common
import pandas as pd
from pandas.api.types import is_numeric_dtype

DATA_DIR = ""
DEMO_TYPES = ["worker", "student", "tourist", "shopper", "leisurer", "chorer"]
RELEVANT_COLUMNS = []

# Executer method.
def process_population(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR
    normalizers = get_normalizers()
    people = get_people_per_effective_area()
    population = compile_population_dataset(normalizers, people)
    population = round_numeric_columns(population)
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/placing_places/", population, "[Population]_total_over_24_hour.csv")

# Round any numeric columns.
def round_numeric_columns(dataset):
    for i in dataset.dtypes.index:
        if is_numeric_dtype(dataset[i]):
            dataset[i] = dataset[i].apply(lambda x: round(x, common.DPs))
    return dataset

# Read the normalizers dataset.
def get_normalizers():
    df = pd.read_csv(DATA_DIR + "processed_data/normalizers/" + "[OA]_Normalizing_properties.csv")
    df = df.drop(columns=["Unnamed: 0"])
    cols_to_keep = ["OA", "OA_population_per_meter_sqrt"]
    df = df[cols_to_keep]
    df = df.rename(columns={"OA_population_per_meter_sqrt": "[per_effective_area_square_meter] - resident_count"})
    # print(df)
    return df

# Read the demographic distribution estimate file.
def get_people_per_effective_area():
    df = pd.read_csv(DATA_DIR + "processed_data/demographic_distributions/" + "[Demographic_distribution]_supertypes_discriminant_borough_scope.csv")
    df = df.drop(columns=["Unnamed: 0"])
    cols_to_keep = ["OA"] + [f"[per_effective_area_square_meter] - {x}_count" for x in DEMO_TYPES]
    df = df[cols_to_keep]
    # print(df)
    return df

# Put together the necessary population information and create shared scale columns.
def compile_population_dataset(normalizers, people):
    df = pd.merge(people, normalizers , on="OA")

    visitors = [f"[per_effective_area_square_meter] - {x}_count" for x in DEMO_TYPES]
    all = visitors + ["[per_effective_area_square_meter] - resident_count"]

    df["[per_effective_area_square_meter] - visitors_total_count"] = df[visitors].sum(axis = 1)
    df["[per_effective_area_square_meter] - total_count"] = df[all].sum(axis = 1)

    for c in all:
        df[f"[shared_scale] - {c}"] = df[c]

    return df
