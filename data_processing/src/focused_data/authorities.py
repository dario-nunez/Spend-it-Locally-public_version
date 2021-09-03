"""Authorities datasets.

Gathers information about the hierarchical structure of authorities in the UK. Establishing
a mapping between postcodes, output areas (OAs) and wards.

Input datasets:
- OA_Ward_LA_2011.csv
- UK_Postcode_to_Output_Area_Hierarchy_with_Classifications.csv

Output datasets:
- OAs_ward.csv
- Postcodes_OAs_classifications.csv
"""

import src.common as common
import pandas as pd

DATA_DIR = ""

# Executer method.
def focus_authorities(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR
    oas_postcodes()
    oas_wards()

# Postcodes to Census Output Areas dataset. Filter by Westminster.
def oas_postcodes():
    dataset_name = "UK_Postcode_to_Output_Area_Hierarchy_with_Classifications.csv"
    dataset = pd.read_csv(DATA_DIR + "raw_data/authorities/" + dataset_name, encoding='latin-1')
    dataset_filtered_by_westminster = dataset.loc[dataset["ladnm"] == "Westminster"]
    common.save_dataframe_to_csv(DATA_DIR + "focused_data/authorities/", dataset_filtered_by_westminster, "Postcodes_OAs_classifications.csv")

# Output Areas to Wards. Filter by Westminster.
def oas_wards():
    dataset_name = "OA_Ward_LA_2011.csv"
    dataset = pd.read_csv(DATA_DIR + "raw_data/authorities/" + dataset_name)
    dataset.columns = ["OA", "LSOA", "ward", "MSOA", "council", "outer/inner"]
    dataset_filtered_by_westminster = dataset.loc[dataset["council"] == "Westminster"]
    common.save_dataframe_to_csv(DATA_DIR + "focused_data/authorities/", dataset_filtered_by_westminster, "OAs_ward.csv")
