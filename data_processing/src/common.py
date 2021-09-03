"""Common module.

Contains commonly used functionality throughout the data processing component of 
the project. It includes project constants, JSON and CSV file saving methods, schema 
explorers and pretty printing functions.
"""

import os
import pandas as pd
import json

################################################################################
# Constants
################################################################################

# Working directory of this script.
CWD = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Standard number of decimal places.
DPs = 3

################################################################################
# Functions
################################################################################

def save_json_to_file(out_dir, out_json, name):
    """Save a JSON formatted string to a JSON file.

    Args:
        out_dir (str): Target directory to save the new file.
        out_json (str): JSON formatted string to save.
        name (str): New JSON file name.
    """

    with open(out_dir + name, "w") as out_json_file:
        out_json_file.write(out_json)

def save_dataframe_to_csv(out_dir, out_df, name):
    """Save a dataframe object to a CSV file.

    Args:
        out_dir (str): Target directory to save the new file.
        out_df (obj): Dataframe object to save.
        name (str): New CSV file name.
    """

    out_df.to_csv(out_dir + name)

def json_schema_explorer(dict, margin = ""):
    """Explores recursively and prints the schema of a dictionary object.

    Args:
        dict ([dict]): The object to explore.
        margin (str, optional): Indentation padding regulator. Defaults to "".
    """

    try:
        for k in dict.keys():
            v_type = type(dict[k])
            print(margin, k, end=": ")
            print(f"[{v_type}]")

            if v_type is str:
                pass
            elif v_type is list:
                json_schema_explorer(dict[k][0], margin + "\t")
            elif type({}) == v_type:
                json_schema_explorer(dict[k], margin + "\t")
            else:
                print(margin, "not string, list or dict type")
    except:
        pass

def load_and_print_dataset_metadata(directory, dataset_name, dataset_type):
    """Loads and prints the schema of a JSON or CSV file.

    Args:
        directory (str): The directory where the target file is located.
        dataset_name (str): The target file name.
        dataset_type (str): The type of the target file (CSV or JSON).
    """

    print("-"*80)
    print(f"METADATA: {dataset_name}")
    print("-"*80)

    if dataset_type == "CSV":
        dataset =  pd.read_csv(directory + dataset_name)
        print(dataset.info())
    elif dataset_type == "JSON":
        with open(directory + dataset_name) as json_file:
            schema_data = json.load(json_file)
            json_schema_explorer(schema_data)
    else:
        print("Unrecognized dataset type")

def pretty_print_dict(d):
    """Prints a dictionary object applying line breaks at all first level objects.

    Args:
        d (dict): Target dictionary
    """

    for k in d.keys():
        print(f"{k} : {d[k]}")
