"""CACI datasets.

Processes all the CACI and other tabular datasets. Operations vary between datasets
but roughly include cleaning, aggregating by OA, applying statistical operations, 
deriving columns and renaming columns.

A commmon pattern used throughout to apply statistical operations to columns is the
use of a mapping function that maps operations to columns based on their type.

Input datasets:
- Postcodes_OAs_classifications.csv
- WCC_Acorn_directory_Feb2020.csv
- WCC_CACI_Paycheck_Disposable_Income_Feb2020.csv
- WCC_COICOP_directory_Feb2020.csv
- WCC_Paycheck_directory_Feb2020.csv
- WCC_Population_by_Age_and_Gender_Feb2020.csv
- WCC_PTAL_directory_Feb2020.csv
- WCC_StreetValue_directory_Feb2020.csv
- WCC_Wellbeing_Acorn_directory_Feb2020.csv

Output datasets:
- [OA]_PTAL_directory.csv
- [OA]_Street_value_directory.csv
- [Residents]_Acorn_directory.csv
- [Residents]_age_and_gender_distribution.csv
- [Residents]_disposable_income_spending_categories.csv
- [Residents]_income.csv
- [Residents]_spending_categories.csv
- [Residents]_wellbeing_directory.csv
"""

import src.common as common
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype

################################################################################
# Constants.
################################################################################

DATA_DIR = ""

ACORN_MAP = {
    1.0: "1. Affluent Achievers",
    2.0: "2. Rising Prosperity",
    3.0: "3. Comfortable Communities",
    4.0: "4. Financially Stretched",
    5.0: "5. Urban Adversity",
    6.0: "6. Not Private Households",
    "A" : "A. Lavish Lifestyles",
    "B" : "B. Executive Wealth",
    "C" : "C. Mature Money",
    "D" : "D. City Sophisticates",
    "E" : "E. Career Climbers",
    "F" : "F. Countryside Communities",
    "G" : "G. Successful Suburbs",
    "H" : "H. Steady Neighbourhoods",
    "I" : "I. Comfortable Seniors",
    "J" : "J. Starting Out",
    "K" : "K. Student Life",
    "L" : "L. Modest Means",
    "M" : "M. Striving Families",
    "N" : "N. Poorer Pensioners",
    "O" : "O. Young Hardship",
    "P" : "P. Struggling Estates",
    "Q" : "Q. Difficult Circumstances",
    "R" : "R. Active Communal Population"
}

ACORN_WELLBEING_GROUP_MAP = {
    1.0: "1. Health Challenges",
    2.0: "2. At Risk",
    3.0: "3. Caution",
    4.0: "4. Healthy",
    5.0: "5. Not Private Households"
}

ACORN_WELLBEING_TYPE_MAP = {
    1.0: "1. Limited living",
    2.0: "2. Poorly pensioners",
    3.0: "3. Hardship heartlands",
    4.0: "4. Elderly ailments",
    5.0: "5. Countryside complacency",
    6.0: "6. Dangerous dependencies",
    7.0: "7. Struggling smokers",
    8.0: "8. Despondent diversity",
    9.0: "9. Everyday excesses",
    10.0: "10. Respiratory risks",
    11.0: "11. Anxious adversity",
    12.0: "12. Perilous futures",
    13.0: "13. Regular revellers",
    14.0: "14. Rooted routines",
    15.0: "15. Borderline behaviours",
    16.0: "16. Countryside concerns",
    17.0: "17. Everything in moderation",
    18.0: "18. Cultural concerns",
    19.0: "19. Relishing retirement",
    20.0: "20. Perky pensioners",
    21.0: "21. Sensible seniors",
    22.0: "22. Gym & juices",
    23.0: "23. Happy families",
    24.0: "24. Five-a-day greys",
    25.0: "25. Healthy, wealthy & wine",
    26.0: "26. Active communal population",
    27.0: "27. Inactive communal population",
    28.0: "28. Business addresses etc."
}

# Executor method.
def process_acorn(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR

    postcode_oa_df = get_postcode_oa_link()
    oa_acorn_directory(postcode_oa_df)
    oa_acorn_paycheck_disposable(postcode_oa_df)
    oa_coicop_directory()
    oa_paycheck_directory(postcode_oa_df)
    oa_age_gender_distribution(postcode_oa_df)
    oa_ptal_directory(postcode_oa_df)
    oa_street_value_directory(postcode_oa_df)
    oa_wellbeing_directory(postcode_oa_df)

################################################################################
# Helper functions.
################################################################################

# Applies a description mapping to the keys of a dictionary object. 
def apply_description_mapping(MAP, x):
    new_freq_count = {}

    for k in x.keys():
        new_freq_count[MAP[k]] = x[k]
        
    return new_freq_count

# Dataframe groupby operation to return a frequency count of series group.
def get_frequencies(x):
    return x.value_counts().to_dict()

# Return the mode of a frequency count. 
def convert_frequency_count_to_mode(x):
    if len(x.keys()) <= 0:
        return "undefined"
    else:
        # print(x, max(x, key = x.get))
        return max(x, key = x.get)

# Return a cleaned dataframe containing the mapping between postcodes and OAs.
def get_postcode_oa_link():
    postcode_oa_df = pd.read_csv(DATA_DIR + "focused_data/authorities/" + "Postcodes_OAs_classifications.csv")
    # Filter by postcode and oa.
    postcode_oa_df = postcode_oa_df[["pcd7","oa11cd"]].rename(columns={"pcd7": "Postcode", "oa11cd": "OA"})
    # Rid postcode of whitespace.
    postcode_oa_df["Postcode"] = postcode_oa_df["Postcode"].apply(lambda x: x.replace(" ", ""))
    return postcode_oa_df

# Return the mode of a frequency count. Done using numpy instead of dataframe operations.
def digest_mode_array(x):
    # pd.Series.mode returns an array in descending order of frequency. 
    if type(x) is np.ndarray:
        if len(x) > 0:
            return x[0]
        else:
            return np.NaN
    else:
        return x

# Return a dataframe with all numeric columns rounded to the global DP setting.
def round_numeric_columns(dataset):
    for i in dataset.dtypes.index:    
        if is_numeric_dtype(dataset[i]):
            dataset[i] = dataset[i].apply(lambda x: round(x, common.DPs))
    
    return dataset   

################################################################################
# WCC_Acorn_directory_Feb2020.csv -> [Residents]_Acorn_directory.csv.
################################################################################
def oa_acorn_directory(postcode_oa_df):
    """[Residents]_Acorn_directory.
    1. Clean dataset.
    2. Aggregate by OA.
    3. Calculate categorical columns' mode.
    4. Round numeric columns.
    5. Rename columns.
    """

    acorn_directory_df = pd.read_csv(DATA_DIR + "focused_data/acorn/" + "WCC_Acorn_directory_Feb2020.csv")
    # Rid postcode of whitespace.
    acorn_directory_df["Postcode"] = acorn_directory_df["Postcode"].apply(lambda x: x.replace(" ", ""))
    # Filter unnecessary columns.
    acorn_directory_df = acorn_directory_df.drop(["Large User", "Deleted Flag"], axis=1)
    # Join dataframes on postcode column.
    joined_df = postcode_oa_df.merge(acorn_directory_df, on = "Postcode")

    # Groupby OA.
    COLS_TO_AGGREGATE = ["Acorn Category", "Acorn Group"]

    grouped_df = joined_df.groupby("OA")[COLS_TO_AGGREGATE].agg(lambda x: x.value_counts().to_dict())

    for k in COLS_TO_AGGREGATE:
        grouped_df[k] = grouped_df[k].apply(lambda x: apply_description_mapping(ACORN_MAP, x))

    for k in COLS_TO_AGGREGATE:
        grouped_df[k+"_frequency_count"] = grouped_df[k]

    for k in COLS_TO_AGGREGATE:
        grouped_df[k] = grouped_df[k].apply(lambda x: convert_frequency_count_to_mode(x))

    grouped_df = round_numeric_columns(grouped_df)

    # Renaming columns
    grouped_df = grouped_df.rename(columns={"Acorn Category": "Acorn_category", "Acorn Group": "Acorn_group"})

    # Previous name: "OA_Acorn_directory.csv"
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/acorn/", grouped_df, "[Residents]_Acorn_directory.csv")

################################################################################
# WCC_CACI_Paycheck_Disposable_Income_Feb2020.csv -> [Residents]_disposable_income_spending_categories.csv.
################################################################################
def convert_range_to_scalar(x):
    if type(x) is str:
        x = x.replace("+", "")
        x = x.split("-")
        int_x = [int(i) for i in x]
        return np.mean(int_x)

def generate_aggregation_map_disposable(column_types):
    dict = {}
    for i in range(len(column_types.index)):
        c_type = column_types.values[i]
        if str(c_type) == "float64":
            dict[column_types.index[i]] = np.nanmean
    return dict

def oa_acorn_paycheck_disposable(postcode_oa_df):
    """[Residents]_disposable_income_spending_categories.
    1. Clean dataset.
    2. Aggregate by OA.
    3. Calculate aggregated means.
    4. Round numeric columns.
    5. Rename columns.
    """

    acorn_paycheck_df = pd.read_csv(DATA_DIR + "focused_data/acorn/" + "WCC_CACI_Paycheck_Disposable_Income_Feb2020.csv")
    # Rid postcode of whitespace.
    acorn_paycheck_df["Postcode"] = acorn_paycheck_df["Postcode"].apply(lambda x: x.replace(" ", ""))
    # Filter unnecessary columns.
    acorn_paycheck_df = acorn_paycheck_df.drop(["Large User", "Deleted Flag"], axis=1)
    # Join dataframes on postcode column.
    joined_df = postcode_oa_df.merge(acorn_paycheck_df, on = "Postcode")
    # Replace NaN with 0.
    joined_df = joined_df.applymap(lambda x: 0 if x is np.NaN else x)
    # Convert ranges to scalars.
    joined_df["Mean Net Disposable Income Band"] = joined_df["Mean Net Disposable Income Band"].apply(lambda x: convert_range_to_scalar(x))
    # Groupby.
    AGG_DICT = generate_aggregation_map_disposable(joined_df.dtypes)
    grouped_df = joined_df.groupby("OA").agg(AGG_DICT).reset_index()
    # Round to 2 dp.
    grouped_df = grouped_df.apply(lambda x: np.round(x,common.DPs) if x.name != "OA" else x)
    # Fill empties.
    grouped_df = grouped_df.fillna(0)
    # Previous name: "OA_disposable_paycheck.csv"

    # Rename postcode column names to OA.
    for col in grouped_df.columns:
        if "a postcode" in col:
            new_col = col.replace("a postcode", "an OA")
            grouped_df = grouped_df.rename(columns={col: new_col})

    common.save_dataframe_to_csv(DATA_DIR + "processed_data/acorn/", grouped_df, "[Residents]_disposable_income_spending_categories.csv")

################################################################################
# WCC_COICOP_directory_Feb2020.csv -> [Residents]_spending_categories.csv.
################################################################################
def oa_coicop_directory():
    """[Residents]_spending_categories.
    1. Clean dataset.
    2. Normalize numerical columns by population
    3. Rename columns.
    4. Round numeric columns.
    """

    coicop_directory_df = pd.read_csv(DATA_DIR + "focused_data/acorn/" + "WCC_COICOP_directory_Feb2020.csv")

    COLS = []
    for i in coicop_directory_df.dtypes.index:
        if i not in ["OA", "Total Households 2019", "Total Population 2019"]:
            COLS.append(i)

    # # Normalize by population.
    # for col in COLS:
    #     coicop_directory_df[col + "_norm_pop"] = coicop_directory_df[col] / coicop_directory_df["Total Population 2019"]

    # for col in COLS: 
    #     coicop_directory_df[col + "_percentage_in_OA_shared_scale"] = coicop_directory_df[col + "_norm_pop"]

    for col in COLS:
        coicop_directory_df["[average_per_person_in_OA] - " + col] = coicop_directory_df[col] / coicop_directory_df["Total Population 2019"]

    for col in COLS:
        coicop_directory_df["[shared_scale] - [average_per_person_in_OA] - " + col] = coicop_directory_df["[average_per_person_in_OA] - " + col]

    # temp = []
    # for col in coicop_directory_df.columns:
    #     temp.append(col)

    # print(temp)

    for col in COLS:
        coicop_directory_df = coicop_directory_df.rename(columns={col: "[sum_in_OA] - " + col})

    coicop_directory_df = coicop_directory_df.drop(columns=["Total Households 2019", "Total Population 2019"])
    coicop_directory_df = coicop_directory_df.fillna(0)
    coicop_directory_df = round_numeric_columns(coicop_directory_df)

    # Previous name: "OA_coicop_directory.csv"
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/acorn/", coicop_directory_df, "[Residents]_spending_categories.csv")

################################################################################
# WCC_Paycheck_directory_Feb2020.csv -> [Residents]_income.csv.
################################################################################
def generate_aggregation_map_paycheck(column_types, dist_cols, non_numeric):
    dict = {}

    dist_cols_ops = {
        "Mean Income" : np.nanmean,
        "Median Income" : np.median,
        "Mode Income" : np.nanmean,
        "Lower Quartile" : np.median,
    }

    for i in range(len(column_types.index)):
        c = column_types.index[i]
        if c in dist_cols:
            dict[column_types.index[i]] = dist_cols_ops[c]
        elif c not in non_numeric:
            dict[column_types.index[i]] = np.sum
        else:
            pass
    return dict

def clean_dist_columns(x):
    return float(str(x).replace('£', '').replace(',',''))

def oa_paycheck_directory(postcode_oa_df):
    """[Residents]_income.
    1. Clean dataset.
    2. Aggregate by OA.
    3. Calculate aggregated statistical operations.
    4. Normalize numeric columns by number of households.
    5. Round numeric columns.
    6. Rename columns.
    """

    paycheck_directory_df = pd.read_csv(DATA_DIR + "focused_data/acorn/" + "WCC_Paycheck_directory_Feb2020.csv")
    # Rename column
    paycheck_directory_df = paycheck_directory_df.rename(columns={"Area Name": "Postcode"})
    # Rid postcode of whitespace.
    paycheck_directory_df["Postcode"] = paycheck_directory_df["Postcode"].apply(lambda x: x.replace(" ", ""))
    # Filter unnecessary columns.
    paycheck_directory_df = paycheck_directory_df.drop(["Large User", "Deleted Flag"], axis=1)
    # Join dataframes on postcode column.
    joined_df = postcode_oa_df.merge(paycheck_directory_df, on = "Postcode")
    # Clean distribution columns
    dist_cols = ["Mean Income", "Median Income", "Mode Income", "Lower Quartile"]
    non_numeric_cols = ["Postcode", "OA"]

    joined_df = joined_df.fillna(0)

    for col in dist_cols:
        joined_df[col] = joined_df[col].apply(lambda x: clean_dist_columns(x))

    AGG_DICT = generate_aggregation_map_paycheck(joined_df.dtypes, dist_cols, non_numeric_cols)
    grouped_df = joined_df.groupby("OA").agg(AGG_DICT).reset_index()

    # 1. Normalise total households by square root of OA area.
    normalizers = pd.read_csv(DATA_DIR + "processed_data/normalizers/" + "[OA]_Normalizing_properties.csv")
    normalizers = normalizers[["OA", "OA_area_meters", "OA_area_meters_sqrt", "OA_area_meters_sqrt_or_limit"]]
    merged = pd.merge(normalizers, grouped_df, on="OA")
    for c in ["Total Households"]:
        # Eliminates a little bit of the outliers and brightens the plot.
        merged[c+"_per_sq_meter"] = round(merged[c] / merged["OA_area_meters_sqrt_or_limit"],common.DPs)
    grouped_df = merged

    # Normalize by households.
    COLS = []
    for i in grouped_df.dtypes.index:
        if i not in dist_cols + non_numeric_cols + ["Total Households", "Total Households_per_sq_meter", "OA_area_meters", "OA_area_meters_sqrt", "OA_area_meters_sqrt_or_limit", "Lower Quartile"]:
            COLS.append(i)

    for col in COLS:
        grouped_df["[%_in_OA] - " + col] = (grouped_df[col] / grouped_df["Total Households"]) * 100
    
    for col in COLS:
        grouped_df["[shared_scale] - [%_in_OA] - " + col] = grouped_df["[%_in_OA] - " + col]

    for col in COLS:
        grouped_df = grouped_df.rename(columns={col: "[count_in_OA] - " + col})

    grouped_df = grouped_df.drop(columns=["Total Households", "Total Households_per_sq_meter", "OA_area_meters", "OA_area_meters_sqrt", "OA_area_meters_sqrt_or_limit"])

    grouped_df = grouped_df.apply(lambda x: np.round(x,common.DPs) if x.name != "OA" else x)
    grouped_df = grouped_df.fillna(0)
    # Previous name: "OA_paycheck_directory.csv"
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/acorn/", grouped_df, "[Residents]_income.csv")

################################################################################
# WCC_Population_by_Age_and_Gender_Feb2020.csv -> [Residents]_age_and_gender_distribution.csv.
################################################################################
AGE_GROUPS = {
    "Infant [0-4]": ["0-4"],
    "Primary student [5-9]": ["5-9"],
    "Secondary student [10-15]": ["10-14", "15"],
    "College student [16-17]" : ["16-17"],
    "Universitarian / apprentice [18-24]" : ["18-19", "20-24"],
    "Young adult [25-39]" : ["25-29", "30-34", "35-39"],
    "Middle-aged adult [40-49]": ["40-44", "45-49"],
    "Senior adult [50-64]": ["50-54","55-59","60-64"],
    "Senior [65+]" : ["65+"]
}

AGE_GROUPED_COLUMNS = {
    "Females": {
        "Infant [0-4]": list(),
        "Primary student [5-9]": list(),
        "Secondary student [10-15]": list(),
        "College student [16-17]" : list(),
        "Universitarian / apprentice [18-24]" : list(),
        "Young adult [25-39]" : list(),
        "Middle-aged adult [40-49]": list(),
        "Senior adult [50-64]": list(),
        "Senior [65+]" : list()
    },
    "Males": {
        "Infant [0-4]": list(),
        "Primary student [5-9]": list(),
        "Secondary student [10-15]": list(),
        "College student [16-17]" : list(),
        "Universitarian / apprentice [18-24]" : list(),
        "Young adult [25-39]" : list(),
        "Middle-aged adult [40-49]": list(),
        "Senior adult [50-64]": list(),
        "Senior [65+]" : list()
    },
    "Total": {
        "Infant [0-4]": list(),
        "Primary student [5-9]": list(),
        "Secondary student [10-15]": list(),
        "College student [16-17]" : list(),
        "Universitarian / apprentice [18-24]" : list(),
        "Young adult [25-39]" : list(),
        "Middle-aged adult [40-49]": list(),
        "Senior adult [50-64]": list(),
        "Senior [65+]" : list()
    }
}

def generate_aggregation_map_age(column_types):
    dict = {}
    for i in range(len(column_types.index)):
        c_type = column_types.values[i]
        if str(c_type) == "float64":
            dict[column_types.index[i]] = np.nansum
    return dict

def oa_age_gender_distribution(postcode_oa_df):
    """[Residents]_age_and_gender_distribution.
    1. Clean dataset.
    2. Aggregate by OA.
    3. Apply the sum operation to all aggregated groups.
    4. Segment the dataset by gender/type: Females, Males, Total
    5. Segment the dataset by 9 age ranges.
    6. Aggregate the dataset by gender and by age ranges.
    7. Normalize numeric columns by population.
    8. Compute derived columns.
    9. Round numeric columns.
    10. Rename columns.
    """

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
    
    # Group and filter columns. Populate the AGE_GROUPED_COLUMNS map.
    for g in ["Females", "Males"]:
        for c in grouped_df.columns:
            split = c.split(" ")
            if len(split) > 1 and split[0] == g:
                age_group = split[2]
                for k in AGE_GROUPS.keys():
                    if age_group in AGE_GROUPS[k]:
                        temp = AGE_GROUPED_COLUMNS[g][k]
                        temp.append(c)
                        AGE_GROUPED_COLUMNS[g][k] = temp
                        temp = AGE_GROUPED_COLUMNS["Total"][k]
                        temp.append(c)
                        AGE_GROUPED_COLUMNS["Total"][k] = temp

    # common.pretty_print_dict(AGE_GROUPED_COLUMNS)

    new_df = pd.DataFrame()
    new_df["OA"] = grouped_df["OA"]
    new_df["Total households"] = grouped_df["Total households"]
    new_df["Total population"] = grouped_df["Total population"]
    new_df["Females total"] = grouped_df["Females"]
    new_df["Males total"] = grouped_df["Males"]

    COLS = []
    # Use the AGE_GROUPED_COLUMNS map to compute new columns.
    for gender in AGE_GROUPED_COLUMNS.keys():
        for group in AGE_GROUPED_COLUMNS[gender].keys():
            c = f"{gender} - {group}"
            COLS.append(c)
            cols_to_sum = AGE_GROUPED_COLUMNS[gender][group]
            new_df[f"[count] - {c}"] = grouped_df.loc[:, cols_to_sum].sum(axis=1)

    # Normalizing by population works better than by households.
    for col in COLS:
        new_df["[%_in_OA] - " + col] = (new_df["[count] - " + col] / new_df["Total population"]) * 100

    temp = []

    # Compute derived columns.
    for gender in AGE_GROUPED_COLUMNS.keys():
        for group in AGE_GROUPED_COLUMNS[gender].keys():
            if gender == "Total":
                c = f"{gender} - {group}"
                temp.append(f"[shared_scale] - [%_in_OA] - {c}")
                new_df[f"[shared_scale] - [%_in_OA] - {c}"] = new_df["[%_in_OA] - " + c]

    new_df = new_df.drop(columns=["Total households", "Total population"])

    # Round to 2 dp.
    new_df = new_df.apply(lambda x: np.round(x,common.DPs) if x.name != "OA" else x)
    # Fill empties. Should not be done because EMPTY indicates missing data.
    new_df = new_df.fillna(0)
    new_df = new_df.replace([np.inf, -np.inf], 0)
    # Previous name: "OA_age_gender_distribution.csv"
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/acorn/", new_df, "[Residents]_age_and_gender_distribution.csv")
    
################################################################################
# WCC_PTAL_directory_Feb2020.csv -> [OA]_PTAL_directory.csv.
################################################################################
def oa_ptal_directory(postcode_oa_df):
    """[OA]_PTAL_directory.
    1. Clean dataset.
    2. Aggregate by OA.
    3. Calculate categorical columns' mode.
    4. Round numeric columns.
    5. Rename columns.
    """

    ptal_directory_df = pd.read_csv(DATA_DIR + "focused_data/acorn/" + "WCC_PTAL_directory_Feb2020.csv")
    # Rid postcode of whitespace.
    ptal_directory_df["Postcode"] = ptal_directory_df["Postcode"].apply(lambda x: x.replace(" ", ""))
    # Filter unnecessary columns.
    ptal_directory_df = ptal_directory_df.drop(["Large User", "Deleted"], axis=1)
    # Join dataframes on postcode column.
    joined_df = postcode_oa_df.merge(ptal_directory_df, on = "Postcode")
    
    # Groupby OA.
    AGG_DICT = {
        "Public Transport Accessibility Index": np.nanmean,
        "Public Transport Accessibility Level": get_frequencies
    }

    # Groupby OA.
    FREQUENCY_COLS = ["Public Transport Accessibility Level"]

    grouped_df = joined_df.groupby("OA").agg(AGG_DICT).reset_index()

    for k in FREQUENCY_COLS:
        grouped_df[k+"_frequency_count"] = grouped_df[k]

    for k in FREQUENCY_COLS:
        grouped_df[k] = grouped_df[k].apply(lambda x: convert_frequency_count_to_mode(x))

    # Renaming columns
    grouped_df = grouped_df.rename(columns={"Public Transport Accessibility Index": "Public_Transport_Accessibility_Index", "Public Transport Accessibility Level": "Public_Transport_Accessibility_Level"})

    grouped_df = round_numeric_columns(grouped_df)
    # Previous name: "OA_PTAL_directory.csv"
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/acorn/", grouped_df, "[OA]_PTAL_directory.csv")

################################################################################
# WCC_StreetValue_directory_Feb2020.csv -> [OA]_Street_value_directory.csv.
################################################################################
def generate_aggregation_map_street(column_types, string_cols, integer_cols, categorical_cols):
    dict = {}
    for i in range(len(column_types.index)):
        c = column_types.index[i]
        if c in categorical_cols:
            dict[column_types.index[i]] = pd.Series.mode
        elif c in integer_cols:
            dict[column_types.index[i]] = np.sum
        elif c in string_cols:
            pass
        else:
            dict[column_types.index[i]] = np.nanmean
    return dict

def clean_monetary_columns(x):
    return float(str(x).replace('£', '').replace(',',''))

def oa_street_value_directory(postcode_oa_df):
    """[OA]_Street_value_directory.
    1. Clean dataset.
    2. Aggregate by OA.
    3. Calculate aggregated statistical operations.
    4. Round numeric columns.
    5. Rename columns.
    """

    paycheck_directory_df = pd.read_csv(DATA_DIR + "focused_data/acorn/" + "WCC_StreetValue_directory_Feb2020.csv")
    # Rid postcode of whitespace.
    paycheck_directory_df["Postcode"] = paycheck_directory_df["Postcode"].apply(lambda x: x.replace(" ", ""))
    # Filter unnecessary columns.
    paycheck_directory_df = paycheck_directory_df.drop(["Large User", "Deleted", "County", "District"], axis=1)
    # Join dataframes on postcode column.
    joined_df = postcode_oa_df.merge(paycheck_directory_df, on = "Postcode")
    # Clean monetary columns
    string_cols = ["Postcode", "OA"]
    integer_cols = ["Household Count"]
    categorical_cols = ["Banding", "Banding Description"]
    # joined_df = joined_df.fillna(0)

    for col in joined_df.columns:
        if col in integer_cols + string_cols + categorical_cols:
            pass
        else:
            joined_df[col] = joined_df[col].apply(lambda x: clean_monetary_columns(x))

    AGG_DICT = generate_aggregation_map_street(joined_df.dtypes, string_cols, integer_cols, categorical_cols)
    grouped_df = joined_df.groupby("OA").agg(AGG_DICT).reset_index()
    # Break mode ties
    for col in categorical_cols:
        grouped_df[col] = grouped_df[col].apply(lambda x: digest_mode_array(x))
   
    filtered_df = grouped_df[["OA"] + categorical_cols]
    filtered_df["[mean] - Value"] = grouped_df["Mean value for postcode"]
    filtered_df["[median] - Value"] = grouped_df["Median value for postcode"]
    filtered_df["[total] - Value"] = grouped_df["Total Value"]

    # This sets a new min in the visualizations of 0 and a new category too.
    # filtered_df = filtered_df.fillna(0)

    filtered_df = filtered_df.rename(columns={"Banding": "Value_band"})

    filtered_df = round_numeric_columns(filtered_df)
    # Previous name: "OA_street_value_directory.csv"
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/acorn/", filtered_df, "[OA]_Street_value_directory.csv")

################################################################################
# WCC_Wellbeing_Acorn_directory_Feb2020.csv -> [Residents]_wellbeing_directory.csv.
################################################################################
def oa_wellbeing_directory(postcode_oa_df):
    """[Residents]_wellbeing_directory.
    1. Clean dataset.
    2. Aggregate by OA.
    3. Calculate categorical columns' mode.
    4. Round numeric columns.
    5. Rename columns.
    """

    acorn_wellbeing_df = pd.read_csv(DATA_DIR + "focused_data/acorn/" + "WCC_Wellbeing_Acorn_directory_Feb2020.csv")
    # Rid postcode of whitespace.
    acorn_wellbeing_df["Postcode"] = acorn_wellbeing_df["Postcode"].apply(lambda x: x.replace(" ", ""))
    # Filter unnecessary columns.
    acorn_wellbeing_df = acorn_wellbeing_df.drop(["Large User", "Deleted Flag"], axis=1)
    # Join dataframes on postcode column.
    joined_df = postcode_oa_df.merge(acorn_wellbeing_df, on = "Postcode")
    
    AGG_DICT = {
        "Wellbeing Acorn Group": get_frequencies,
        "Wellbeing Acorn Type": get_frequencies
    }

    COLUMN_VERBOSE_MAPPING = {
        "Wellbeing Acorn Group": ACORN_WELLBEING_GROUP_MAP,
        "Wellbeing Acorn Type": ACORN_WELLBEING_TYPE_MAP
    }

    grouped_df = joined_df.groupby("OA").agg(AGG_DICT).reset_index()

    for k in COLUMN_VERBOSE_MAPPING.keys():
        grouped_df[k] = grouped_df[k].apply(lambda x: apply_description_mapping(COLUMN_VERBOSE_MAPPING[k], x))

    for k in COLUMN_VERBOSE_MAPPING.keys():
        grouped_df[k+"_frequency_count"] = grouped_df[k]

    for k in COLUMN_VERBOSE_MAPPING.keys():
        grouped_df[k] = grouped_df[k].apply(lambda x: convert_frequency_count_to_mode(x))

    # Rename columns.
    grouped_df = grouped_df.rename(columns={"Wellbeing Acorn Group": "Wellbeing_Acorn_group", "Wellbeing Acorn Type": "Wellbeing_Acorn_type"})

    grouped_df = round_numeric_columns(grouped_df)
    # Previous name: "OA_wellbeing_directory.csv"
    common.save_dataframe_to_csv(DATA_DIR + "processed_data/acorn/", grouped_df, "[Residents]_wellbeing_directory.csv")
