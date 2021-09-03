"""Demographic distribution density estimation.

Taking as an input the place tally datasets and the demographic distribution models
this file computes an estimate for the demographic distribution density per OA of
the 6 defined demographic types. Intermediate steps to computation are applied.

Input datasets:
- [Places]_counts_no_shared_scale.csv
- [OA]_Normalizing_properties.csv
- place_types_granular.csv
- place_types_supertypes.csv
- place_types_supertypes_attractors.csv
- place_types_supertypes_discriminant.csv

Output datasets:
- [Demographic_distribution]_granular_borough_scope.csv
- [Demographic_distribution]_granular_OA_scope.csv
- [Demographic_distribution]_supertypes_attractors_borough_scope.csv
- [Demographic_distribution]_supertypes_attractors_OA_scope.csv
- [Demographic_distribution]_supertypes_borough_scope.csv
- [Demographic_distribution]_supertypes_discriminant_borough_scope.csv
- [Demographic_distribution]_supertypes_discriminant_OA_scope.csv
- [Demographic_distribution]_supertypes_OA_scope.csv
- [POC_Demographic_distribution]_granular_normalized_relevance.csv
- [POC_Demographic_distribution]_granular_normalized.csv
- [POC_Demographic_distribution]_granular.csv
"""

import src.common as common
import pandas as pd
from pandas.api.types import is_numeric_dtype
import math

DATA_DIR = ""
TOTAL_DAYTIME_POPULATION = 1000000 # Estimate backed with evidence.
DEMO_TYPES = ["worker", "student", "tourist", "shopper", "leisurer", "chorer"]
RELEVANT_COLUMNS = []

# Defines how to process each demographic distribution model dataset.
dataset_processing_tasks = {
    "[POC_Demographic_distribution]_granular.csv": {
        "demo_dists_filename": "place_types_granular.csv",
        "relevance": False,
        "normalize": False,
        "poc": True
    },
    "[POC_Demographic_distribution]_granular_normalized.csv": {
        "demo_dists_filename": "place_types_granular.csv",
        "relevance": False,
        "normalize": True,
        "poc": True
    },
    "[POC_Demographic_distribution]_granular_normalized_relevance.csv": {
        "demo_dists_filename": "place_types_granular.csv",
        "relevance": True,
        "normalize": True,
        "poc": True
    },
    "[Demographic_distribution]_granular": {
        "demo_dists_filename": "place_types_granular.csv",
        "relevance": True,
        "normalize": True,
        "poc": False
    },
    "[Demographic_distribution]_supertypes": {
        "demo_dists_filename": "place_types_supertypes.csv",
        "relevance": True,
        "normalize": True,
        "poc": False
    },
    "[Demographic_distribution]_supertypes_attractors": {
        "demo_dists_filename": "place_types_supertypes_attractors.csv",
        "relevance": True,
        "normalize": True,
        "poc": False
    },
    "[Demographic_distribution]_supertypes_discriminant": {
        "demo_dists_filename": "place_types_supertypes_discriminant.csv",
        "relevance": True,
        "normalize": True,
        "poc": False
    }
}

def process_places_demographic_densities(in_DATA_DIR):
    """Handles the computation of each processing task in a sequential order:
    1. Load the regular (not normalized) tally dataset.
    2. Normalize the tally dataset by type total count.
    3. Load the appropriate demographic distribution by place file.
    4. Apply the relevance multiplier.
    5. Calculate demographic score per OA.
    6. Normalize demographic scores per OA by OA effective area.
    7. Calculate demographic values per OA.
    8. Normalize demographic values per OA by OA effective area.
    9. Calculate demographic percentages at the OA and borough level.
    10. Round numeric columns.
    11. Save both OA and borough level datasets.
    """

    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR

    places_tally = pd.read_csv(DATA_DIR + "processed_data/places/" + "[Places]_counts_no_shared_scale.csv")
    places_tally = places_tally.drop(columns=["Unnamed: 0"])
    
    # Not including this also generates very nice results.
    places_tally = normalize_place_tally_by_type_count(places_tally)
    
    normalizers = pd.read_csv(DATA_DIR + "processed_data/normalizers/" + "[OA]_Normalizing_properties.csv")

    for k in dataset_processing_tasks.keys():
        RELEVANT_COLUMNS = []
        filename_to_save = k
        demo_dists_filename = dataset_processing_tasks[k]["demo_dists_filename"]
        relevance = dataset_processing_tasks[k]["relevance"]
        normalize = dataset_processing_tasks[k]["normalize"]
        poc = dataset_processing_tasks[k]["poc"]

        demo_dists = pd.read_csv(DATA_DIR + "focused_data/place_types/" + demo_dists_filename)
        demo_dists = demo_dists.drop(columns=["Unnamed: 0"])

        if relevance:   # Applying relevance multiplier.
            demo_dists = apply_relevance_multiplier_to_demographic_distributions(demo_dists)
        else:
            demo_dists = demo_dists.drop(columns=["relevance"])

        result = multiply_demographic_distributions_by_place_tallies(places_tally, demo_dists)

        if normalize:   # Normalize by effective area and calculate proportions at OA and borough level.
            result = normalise_distributions_by_oa_effective_area(result, normalizers)
            result = calculate_demographic_percentages_out_of_borough_demographic_total(result)
            result = calculate_demographic_percentages_out_of_OA_demographic_total(result)
        
        result = calculate_demographic_values(result)

        if normalize:   # Normalize total values by effective area.
            result = normalise_demographic_values_by_oa_effective_area(result, normalizers)

        result = round_numeric_columns(result)

        if poc: # If it is Prove Of Concept, don't clean it or add shared columns.
            common.save_dataframe_to_csv(DATA_DIR + "processed_data/demographic_distributions/", result, filename_to_save)
        else:   
            datasets_to_save = split_dataset_and_introduce_scale_sharing_and_save(result)
            # datasets_to_save[0] is OA scope
            # datasets_to_save[1] is borough scope
            common.save_dataframe_to_csv(DATA_DIR + "processed_data/demographic_distributions/", datasets_to_save[0], filename_to_save+"_OA_scope.csv")
            common.save_dataframe_to_csv(DATA_DIR + "processed_data/demographic_distributions/", datasets_to_save[1], filename_to_save+"_borough_scope.csv")

def normalize_place_tally_by_type_count(tally):
    ##################################################################################
    # Divide each cell by the square root of the row total.
    # Trying to account for crowding in an area. The more places, the less people each can attract.
    # THIS DOES NOT WORK WELL.
    ##################################################################################
    # tally["row_total"] = tally.loc[:, "accounting":"zoo"].sum(axis = 1)
    # tally["row_total"] = tally["row_total"].apply(lambda x: math.sqrt(x))
    # print(tally)
    # for c in tally.columns[1:]:
    #     tally[c] = tally[c] / tally["row_total"]
    # print(tally)
    # tally = tally.drop(columns=["row_total"])
    # print(tally)

    ##################################################################################
    # Divide each cell by the square root of the column total.
    # The more common the place, the more each of its OA counts gets penalized.
    # Works well for countering the effects of supertypes like "establishment".
    # This simulates unique places attracting more people. E.g. museums vs art galleries.
    ##################################################################################
    types_counts = tally.loc[:, "accounting":].sum()
    
    # print(types_counts)
    # print(tally["bar"])

    # Recalculate type counts, dividing each by a metric of their column total.
    for c in tally.columns[1:]:
        tally[c] = tally[c] / math.sqrt(types_counts[c])
        # tally[c] = tally[c] / types_counts[c]
    
    # print(tally)
    # print(tally["bar"])

    ##################################################################################
    # Replace each cell with its square root.
    ##################################################################################
    # print(tally)
    # for c in tally.columns[1:]:
    #     tally[c] = tally[c].apply(lambda x: math.sqrt(x))
    # print(tally)

    return tally

def apply_relevance_multiplier_to_demographic_distributions(dists):
    # Recalculate distributions, multiplying each row by its relevance.

    dists = dists.sort_values(by=["place_type"])
    for c in dists.columns[2:]:
        dists[c] = dists[c] * dists["relevance"] # Marginally better with it (I think :())
    dists = dists.drop(columns=["relevance"])
    return dists    

def multiply_demographic_distributions_by_place_tallies(tally, dists):
    oas = tally["OA"].to_list()
    demo_types = dists.columns.to_list()[1:]
    OA_demos = pd.DataFrame(columns=(["OA"] + demo_types))

    for oa in oas:
        oa_place_count = tally.loc[tally["OA"] == oa].values.tolist()[0][1:]
        demo_type_summed_values = []

        for demo_type in demo_types:
            demo_place_percs = dists[demo_type].values.tolist()
            multiplied = [a * b for a, b in zip(oa_place_count, demo_place_percs)]
            summed = round(sum(multiplied), 3)
            demo_type_summed_values.append(summed)
    
        new_row = [oa] + demo_type_summed_values
        new_df = pd.DataFrame([new_row], columns=["OA"] + demo_types)
        OA_demos = pd.concat([OA_demos, new_df])

    OA_demos = OA_demos.reset_index(drop=True)
    OA_demos = OA_demos.rename(columns={"worker_perc": "worker_units", "student_perc": "student_units", "tourist_perc": "tourist_units", "shopper_perc": "shopper_units", "leisurer_perc": "leisurer_units", "chorer_perc": "chorer_units"})
    return OA_demos

def normalise_distributions_by_oa_effective_area(demographic_distributions, normalizers):
    normalizers = normalizers[["OA", "OA_area_meters_sqrt", "OA_households", "OA_population"]]
    merged = pd.merge(normalizers, demographic_distributions, on="OA")

    for c in merged.loc[:, merged.columns[4]:merged.columns[9]]:
        RELEVANT_COLUMNS.append(f"[per_effective_area_square_meter] - {c}")
        merged[f"[per_effective_area_square_meter] - {c}"] = round(merged[c] / merged["OA_area_meters_sqrt"], common.DPs)

    merged = merged.drop(columns=["OA_area_meters_sqrt", "OA_households", "OA_population"])
    return merged

def calculate_demographic_percentages_out_of_borough_demographic_total(normalized_by_effective_area):
    # Calculate the percentage the units of a type in an OA out of the total units of that type in the borough (all the OAs)
    
    for focus_col in RELEVANT_COLUMNS:
        col_sum = normalized_by_effective_area[focus_col].sum(axis = 0)
        normalized_by_effective_area[f"[%_of_borough_total] - {focus_col}"] = (normalized_by_effective_area[focus_col] / col_sum) * 100

    return normalized_by_effective_area

def calculate_demographic_percentages_out_of_OA_demographic_total(normalized_by_effective_area):
    # Calculate the percentage the units of a type in an OA out of the total units of any types in that OA.
    cols_to_sum = [
        "[per_effective_area_square_meter] - worker_units",
        "[per_effective_area_square_meter] - student_units",
        "[per_effective_area_square_meter] - tourist_units",
        "[per_effective_area_square_meter] - shopper_units",
        "[per_effective_area_square_meter] - leisurer_units",
        "[per_effective_area_square_meter] - chorer_units"
    ]

    normalized_by_effective_area["[per_effective_area_square_meter] - total_units"] = normalized_by_effective_area[cols_to_sum].sum(axis = 1)

    for col in cols_to_sum:
        normalized_by_effective_area[f"[%_of_OA_total] - {col}"] = (normalized_by_effective_area[col] / normalized_by_effective_area["[per_effective_area_square_meter] - total_units"]) * 100

    return normalized_by_effective_area

def calculate_demographic_values(in_df):
    type_map = {
        "worker" : {},
        "student" : {},
        "tourist" : {},
        "shopper" : {},
        "leisurer" : {},
        "chorer" : {}
    }

    # Total units of each demographic.
    for k in type_map.keys():
        type_map[k]["units"] = in_df[f"{k}_units"].sum(axis=0)

    # Sum of total units of all demographics.
    totals = [type_map[x]["units"] for x in type_map.keys()]
    totals_sum = sum(totals)

    # Units normalized by total units. Proportion of each demographic.
    for k in type_map.keys():
        type_map[k]["proportion"] = type_map[k]["units"] / totals_sum

    # Daytime demographic quantity. Total * proportion of each demographic.
    for k in type_map.keys():
        type_map[k]["value"] = type_map[k]["proportion"] * TOTAL_DAYTIME_POPULATION
    
    cols_to_sum = []

    # Multiply each cell (a proportion of the total) by the column total. Also normalize them.
    for k in type_map.keys():
        cols_to_sum.append(f"{k}_value")
        col_sum = in_df[f"{k}_units"].sum(axis = 0) # Same value as the "units" in the map.
        in_df[f"{k}_value"] = (in_df[f"{k}_units"] / col_sum) * type_map[k]["value"]

    in_df["total_value"] = in_df[cols_to_sum].sum(axis = 1)

    return in_df

def normalise_demographic_values_by_oa_effective_area(in_df, normalizers):
    normalizers = normalizers[["OA", "OA_area_meters_sqrt", "OA_households", "OA_population"]]
    merged = pd.merge(normalizers, in_df, on="OA")

    cols_to_sum = []

    for k in ["worker", "student", "tourist", "shopper", "leisurer", "chorer"]:
        cols_to_sum.append(f"[per_effective_area_square_meter] - {k}_value")
        merged[f"[per_effective_area_square_meter] - {k}_value"] = (merged[f"{k}_value"] / merged["OA_area_meters_sqrt"])

    merged["[per_effective_area_square_meter] - total_value"] = merged[cols_to_sum].sum(axis = 1)

    merged = merged.drop(columns=["OA_area_meters_sqrt", "OA_households", "OA_population"])
    return merged

def round_numeric_columns(dataset):
    for i in dataset.dtypes.index:
        # Sanity check to make sure percentage columns add up to 100.
        # print(i)
        # print(dataset[i].sum(axis=0))

        if is_numeric_dtype(dataset[i]):
            dataset[i] = dataset[i].apply(lambda x: round(x, common.DPs))
    
    return dataset

def column_cleaning(in_df):
    cols_to_remove = [
        "worker_units", 
        "student_units", 
        "tourist_units", 
        "shopper_units", 
        "leisurer_units", 
        "chorer_units",
        "[per_effective_area_square_meter] - worker_units", 
        "[per_effective_area_square_meter] - student_units", 
        "[per_effective_area_square_meter] - tourist_units", 
        "[per_effective_area_square_meter] - shopper_units", 
        "[per_effective_area_square_meter] - leisurer_units", 
        "[per_effective_area_square_meter] - chorer_units",
        "[per_effective_area_square_meter] - total_units"
    ]

    effective_cols_to_remove = []

    for col in in_df.columns:
        if col in cols_to_remove:
            effective_cols_to_remove.append(col)

    in_df = in_df.drop(columns=effective_cols_to_remove)
    return in_df

def split_dataset_and_introduce_scale_sharing_and_save(in_df):
    oa_scope = pd.DataFrame()
    borough_scope = pd.DataFrame()

    # OA scope dataframe.
    shared_scale_cols = []
    oa_scope["OA"] = in_df["OA"]
    for dt in DEMO_TYPES:
        shared_scale_cols.append(f"[%_of_OA_total] - [per_effective_area_square_meter] - {dt}")
        oa_scope[f"[%_of_OA_total] - [per_effective_area_square_meter] - {dt}"] = in_df[f"[%_of_OA_total] - [per_effective_area_square_meter] - {dt}_units"]
    for col in shared_scale_cols:
        oa_scope[f"[shared_scale] - {col}"] = oa_scope[col]

    # Borough scope dataframe.
    shared_scale_cols = []
    borough_scope["OA"] = in_df["OA"]
    for dt in DEMO_TYPES:
        borough_scope[f"[total] - {dt}_count"] = in_df[f"{dt}_value"]
    borough_scope[f"[total] - total_count"] = in_df[f"total_value"]
    for dt in DEMO_TYPES:
        borough_scope[f"[per_effective_area_square_meter] - {dt}_count"] = in_df[f"[per_effective_area_square_meter] - {dt}_value"]
    borough_scope[f"[per_effective_area_square_meter] - total_count"] = in_df[f"[per_effective_area_square_meter] - total_value"]
    for dt in DEMO_TYPES:
        shared_scale_cols.append(f"[%_of_borough_total] - [per_effective_area_square_meter] - {dt}")
        borough_scope[f"[%_of_borough_total] - [per_effective_area_square_meter] - {dt}"] = in_df[f"[%_of_borough_total] - [per_effective_area_square_meter] - {dt}_units"]
    for col in shared_scale_cols:
        borough_scope[f"[shared_scale] - {col}"] = borough_scope[col]

    return [oa_scope, borough_scope]
