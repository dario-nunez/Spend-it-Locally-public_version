"""Generate tabular metadata

For each listed dataset, it generates metadata containing information about each
column, including its name, type, range and range values. The script also assigns
column colour mappings, ignores columns and implements shared scales.

The generated metadata entries have the following structure:
"[OA]_Normalizing_properties.csv": {
    "column_data": [
        {
            "name": "OA_area_meters",
            "type_registered": "float64",
            "type_practical": "number_float",
            "range": null,
            "min": 1099.4903374997639,
            "max": 1855902.5608250087
        },
    ...
...

The metadata file is used by the UI to decide how to interpret data and render DOM 
elements. The idea is to avoid doing as much data processing as possible in the user
interface to increase its performance. This work is delegated to the backend and 
delivered through the "output_data_metadata.json" file.

Inputs datasets:
- [OA]_Normalizing_properties.csv": "normalizers/",
- [OA]_PTAL_directory.csv" : "acorn/",
- [OA]_Street_value_directory.csv" : "acorn/",
- [Residents]_Acorn_directory.csv" : "acorn/",
- [Residents]_age_and_gender_distribution.csv" : "acorn/",
- [Residents]_spending_categories.csv" : "acorn/",
- [Residents]_disposable_income_spending_categories.csv" : "acorn/",
- [Residents]_income.csv" : "acorn/",
- [Residents]_wellbeing_directory.csv" : "acorn/",
- [Places]_counts.csv" : "places/",
- [Places]_counts_normalized_by_OA_effective_area.csv" : "places/",
- [Places]_counts_normalized_by_household_per_meter.csv" : "places/",
- [Places]_counts_normalized_by_household_per_meter_bound.csv" : "places/",
- [POC_Demographic_distribution]_granular.csv": "demographic_distributions/",
- [POC_Demographic_distribution]_granular_normalized.csv": "demographic_distributions/",
- [POC_Demographic_distribution]_granular_normalized_relevance.csv": "demographic_distributions/",
- [Demographic_distribution]_granular_OA_scope.csv": "demographic_distributions/",
- [Demographic_distribution]_granular_borough_scope.csv": "demographic_distributions/",
- [Demographic_distribution]_supertypes_OA_scope.csv": "demographic_distributions/",
- [Demographic_distribution]_supertypes_borough_scope.csv": "demographic_distributions/",
- [Demographic_distribution]_supertypes_attractors_OA_scope.csv": "demographic_distributions/",
- [Demographic_distribution]_supertypes_attractors_borough_scope.csv": "demographic_distributions/",
- [Demographic_distribution]_supertypes_discriminant_OA_scope.csv": "demographic_distributions/",
- [Demographic_distribution]_supertypes_discriminant_borough_scope.csv": "demographic_distributions/",
- [Population]_total_over_24_hour.csv": "placing_places/",
- [Supply_demand]_example.csv": "placing_places/",
- green_groups.csv" : "survey/",
- community_engagement.csv" : "survey/",
- remaining.csv" : "survey/",

Output datasets:
- output_data_metadata.json
"""

import src.common as common
import pandas as pd
import json
from pandas.api.types import is_numeric_dtype

DATA_DIR = ""

# Executer method.
def process_tabular_metadata(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR
    generate_metadata(DATASETS, DATASETS_SKIP_COLUMNS, DATASETS_P_TYPE, SKIP_COLUMNS)

DATASETS = {
    "[OA]_Normalizing_properties.csv": "normalizers/",
    "[OA]_PTAL_directory.csv" : "acorn/",
    "[OA]_Street_value_directory.csv" : "acorn/",

    "[Residents]_Acorn_directory.csv" : "acorn/",
    "[Residents]_age_and_gender_distribution.csv" : "acorn/",
    "[Residents]_spending_categories.csv" : "acorn/",
    "[Residents]_disposable_income_spending_categories.csv" : "acorn/",
    "[Residents]_income.csv" : "acorn/",
    "[Residents]_wellbeing_directory.csv" : "acorn/",

    "[Places]_counts.csv" : "places/",
    "[Places]_counts_normalized_by_OA_effective_area.csv" : "places/",
    "[Places]_counts_normalized_by_household_per_meter.csv" : "places/",
    "[Places]_counts_normalized_by_household_per_meter_bound.csv" : "places/",

    "[POC_Demographic_distribution]_granular.csv": "demographic_distributions/",
    "[POC_Demographic_distribution]_granular_normalized.csv": "demographic_distributions/",
    "[POC_Demographic_distribution]_granular_normalized_relevance.csv": "demographic_distributions/",

    "[Demographic_distribution]_granular_OA_scope.csv": "demographic_distributions/",
    "[Demographic_distribution]_granular_borough_scope.csv": "demographic_distributions/",
    "[Demographic_distribution]_supertypes_OA_scope.csv": "demographic_distributions/",
    "[Demographic_distribution]_supertypes_borough_scope.csv": "demographic_distributions/",
    "[Demographic_distribution]_supertypes_attractors_OA_scope.csv": "demographic_distributions/",
    "[Demographic_distribution]_supertypes_attractors_borough_scope.csv": "demographic_distributions/",
    "[Demographic_distribution]_supertypes_discriminant_OA_scope.csv": "demographic_distributions/",
    "[Demographic_distribution]_supertypes_discriminant_borough_scope.csv": "demographic_distributions/",

    "[Population]_total_over_24_hour.csv": "placing_places/",
    "[Supply_demand]_example.csv": "placing_places/",

    "green_groups.csv" : "survey/",
    "community_engagement.csv" : "survey/",
    "remaining.csv" : "survey/",
}

DATASETS_SKIP_COLUMNS = {
    "[OA]_Normalizing_properties.csv": [],
    "[OA]_PTAL_directory.csv" : ["Public Transport Accessibility Level_frequency_count"],
    "[OA]_Street_value_directory.csv" : ["Banding Description"],

    "[Residents]_Acorn_directory.csv" : ["Acorn Category_frequency_count", "Acorn Group_frequency_count"],
    "[Residents]_age_and_gender_distribution.csv" : [],
    "[Residents]_spending_categories.csv" : [],
    "[Residents]_disposable_income_spending_categories.csv" : [],
    "[Residents]_income.csv" : [],
    "[Residents]_wellbeing_directory.csv": ["Wellbeing Acorn Group_frequency_count", "Wellbeing Acorn Type_frequency_count"],
    
    "[Places]_counts.csv" : [],
    "[Places]_counts_normalized_by_OA_effective_area.csv" : [],
    "[Places]_counts_normalized_by_household_per_meter.csv" : [],
    "[Places]_counts_normalized_by_household_per_meter_bound.csv" : [],

    "[POC_Demographic_distribution]_granular.csv" : [],
    "[POC_Demographic_distribution]_granular_normalized.csv" : [],
    "[POC_Demographic_distribution]_granular_normalized_relevance.csv" : [],

    "[Demographic_distribution]_granular_OA_scope.csv": [],
    "[Demographic_distribution]_granular_borough_scope.csv": [],
    "[Demographic_distribution]_supertypes_OA_scope.csv": [],
    "[Demographic_distribution]_supertypes_borough_scope.csv": [],
    "[Demographic_distribution]_supertypes_attractors_OA_scope.csv": [],
    "[Demographic_distribution]_supertypes_attractors_borough_scope.csv": [],
    "[Demographic_distribution]_supertypes_discriminant_OA_scope.csv": [],
    "[Demographic_distribution]_supertypes_discriminant_borough_scope.csv": [],

    "[Population]_total_over_24_hour.csv": [],
    "[Supply_demand]_example.csv": [],

    "green_groups.csv" : [],
    "community_engagement.csv": [],
    "remaining.csv": []
}

DATASETS_P_TYPE = {
    "[OA]_Normalizing_properties.csv": [],
    "[OA]_PTAL_directory.csv" : ["PTAL", "default"],
    "[OA]_Street_value_directory.csv" : [],

    "[Residents]_Acorn_directory.csv" : [],
    "[Residents]_age_and_gender_distribution.csv" : [],
    "[Residents]_spending_categories.csv" : [],
    "[Residents]_disposable_income_spending_categories.csv" : [],
    "[Residents]_income.csv" : [],
    "[Residents]_wellbeing_directory.csv": [],

    "[Places]_counts.csv" : [],
    "[Places]_counts_normalized_by_OA_effective_area.csv" : [],
    "[Places]_counts_normalized_by_household_per_meter.csv" : [],
    "[Places]_counts_normalized_by_household_per_meter_bound.csv" : [],

    "[POC_Demographic_distribution]_granular.csv" : [],
    "[POC_Demographic_distribution]_granular_normalized.csv" : [],
    "[POC_Demographic_distribution]_granular_normalized_relevance.csv" : [],

    "[Demographic_distribution]_granular_OA_scope.csv": [],
    "[Demographic_distribution]_granular_borough_scope.csv": [],
    "[Demographic_distribution]_supertypes_OA_scope.csv": [],
    "[Demographic_distribution]_supertypes_borough_scope.csv": [],
    "[Demographic_distribution]_supertypes_attractors_OA_scope.csv": [],
    "[Demographic_distribution]_supertypes_attractors_borough_scope.csv": [],
    "[Demographic_distribution]_supertypes_discriminant_OA_scope.csv": [],
    "[Demographic_distribution]_supertypes_discriminant_borough_scope.csv": [],

    "[Population]_total_over_24_hour.csv": [],
    "[Supply_demand]_example.csv": [],

    "green_groups.csv" : [],
    "community_engagement.csv": [],
    "remaining.csv" : []
}

SHARED_SCALE_PAYCKECK_DIRECTORY = ['[shared_scale] - [%_in_OA] - 0-5K', '[shared_scale] - [%_in_OA] - 5-10K', '[shared_scale] - [%_in_OA] - 10-15K', '[shared_scale] - [%_in_OA] - 15-20K', '[shared_scale] - [%_in_OA] - 20-25K', '[shared_scale] - [%_in_OA] - 25-30K', '[shared_scale] - [%_in_OA] - 30-35K', '[shared_scale] - [%_in_OA] - 35-40K', '[shared_scale] - [%_in_OA] - 40-45K', '[shared_scale] - [%_in_OA] - 45-50K', '[shared_scale] - [%_in_OA] - 50-55K', '[shared_scale] - [%_in_OA] - 55-60K', '[shared_scale] - [%_in_OA] - 60-65K', '[shared_scale] - [%_in_OA] - 65-70K', '[shared_scale] - [%_in_OA] - 70-75K', '[shared_scale] - [%_in_OA] - 75-80K', '[shared_scale] - [%_in_OA] - 80-85K', '[shared_scale] - [%_in_OA] - 85-90K', '[shared_scale] - [%_in_OA] - 90-95K', '[shared_scale] - [%_in_OA] - 95-100K', '[shared_scale] - [%_in_OA] - 100-120K', '[shared_scale] - [%_in_OA] - 120-140K', '[shared_scale] - [%_in_OA] - 140-160K', '[shared_scale] - [%_in_OA] - 160-180K', '[shared_scale] - [%_in_OA] - 180-200K', '[shared_scale] - [%_in_OA] - 200K+']

SHARED_SCALE_AGE_DISTRIBUTION_COLUMNS = ['[shared_scale] - [%_in_OA] - Total - Infant [0-4]', '[shared_scale] - [%_in_OA] - Total - Primary student [5-9]', '[shared_scale] - [%_in_OA] - Total - Secondary student [10-15]', '[shared_scale] - [%_in_OA] - Total - College student [16-17]', '[shared_scale] - [%_in_OA] - Total - Universitarian / apprentice [18-24]', '[shared_scale] - [%_in_OA] - Total - Young adult [25-39]', '[shared_scale] - [%_in_OA] - Total - Middle-aged adult [40-49]', '[shared_scale] - [%_in_OA] - Total - Senior adult [50-64]', '[shared_scale] - [%_in_OA] - Total - Senior [65+]']

SHARED_SCALE_COICOP_COLUMNS = ['[shared_scale] - [average_per_person_in_OA] - Food', '[shared_scale] - [average_per_person_in_OA] - Non-alcoholic Drink', '[shared_scale] - [average_per_person_in_OA] - Alcoholic drink (off sales)', '[shared_scale] - [average_per_person_in_OA] - Tobacco', '[shared_scale] - [average_per_person_in_OA] - Clothing', '[shared_scale] - [average_per_person_in_OA] - Footwear', '[shared_scale] - [average_per_person_in_OA] - Actual rentals for housing', '[shared_scale] - [average_per_person_in_OA] - House Repair, Maintenance & Decoration', '[shared_scale] - [average_per_person_in_OA] - Water and miscellaneous services', '[shared_scale] - [average_per_person_in_OA] - Gas, Electricity & Other Fuel', '[shared_scale] - [average_per_person_in_OA] - Furniture, Furnishings & Floorcoverings', '[shared_scale] - [average_per_person_in_OA] - Household Textiles', '[shared_scale] - [average_per_person_in_OA] - Household Hardware', '[shared_scale] - [average_per_person_in_OA] - Glassware, Tableware and Household Utensils', '[shared_scale] - [average_per_person_in_OA] - Tools & Equipment for House & Garden', '[shared_scale] - [average_per_person_in_OA] - Goods & Services for Household Maintenance', '[shared_scale] - [average_per_person_in_OA] - Medical Products, Appliances & Equipment', '[shared_scale] - [average_per_person_in_OA] - Medical, Dental, Optical & Nursing Fees', '[shared_scale] - [average_per_person_in_OA] - Hospital services', '[shared_scale] - [average_per_person_in_OA] - Purchase of vehicles', '[shared_scale] - [average_per_person_in_OA] - Operation of Cars, Vans & Motorcycles', '[shared_scale] - [average_per_person_in_OA] - Transport Services', '[shared_scale] - [average_per_person_in_OA] - Postal Services', '[shared_scale] - [average_per_person_in_OA] - Telephone and Fax Equipment', '[shared_scale] - [average_per_person_in_OA] - Telephone and Fax Services', '[shared_scale] - [average_per_person_in_OA] - A/V, Photographic, Computing Equipment', '[shared_scale] - [average_per_person_in_OA] - Recreational Durables', '[shared_scale] - [average_per_person_in_OA] - Recreational Items', '[shared_scale] - [average_per_person_in_OA] - Recreational Services', '[shared_scale] - [average_per_person_in_OA] - Newspapers, Books and Stationery', '[shared_scale] - [average_per_person_in_OA] - Educational Services', '[shared_scale] - [average_per_person_in_OA] - Catering Services', '[shared_scale] - [average_per_person_in_OA] - Accommodation Services', '[shared_scale] - [average_per_person_in_OA] - Personal Care', '[shared_scale] - [average_per_person_in_OA] - Personal Goods', '[shared_scale] - [average_per_person_in_OA] - Social Protection', '[shared_scale] - [average_per_person_in_OA] - Insurance', '[shared_scale] - [average_per_person_in_OA] - Financial services not elsewhere classified', '[shared_scale] - [average_per_person_in_OA] - Other services not elsewhere classified']

SHARED_SCALE_COLS_OA_SCOPE = ['[shared_scale] - [%_of_OA_total] - [per_effective_area_square_meter] - worker', '[shared_scale] - [%_of_OA_total] - [per_effective_area_square_meter] - student', '[shared_scale] - [%_of_OA_total] - [per_effective_area_square_meter] - tourist', '[shared_scale] - [%_of_OA_total] - [per_effective_area_square_meter] - shopper', '[shared_scale] - [%_of_OA_total] - [per_effective_area_square_meter] - leisurer', '[shared_scale] - [%_of_OA_total] - [per_effective_area_square_meter] - chorer']

SHARED_SCALE_COLS_BOROUGH_SCOPE = ['[shared_scale] - [%_of_borough_total] - [per_effective_area_square_meter] - worker', '[shared_scale] - [%_of_borough_total] - [per_effective_area_square_meter] - student', '[shared_scale] - [%_of_borough_total] - [per_effective_area_square_meter] - tourist', '[shared_scale] - [%_of_borough_total] - [per_effective_area_square_meter] - shopper', '[shared_scale] - [%_of_borough_total] - [per_effective_area_square_meter] - leisurer', '[shared_scale] - [%_of_borough_total] - [per_effective_area_square_meter] - chorer']

SHARED_SCALE_COLS_PLACES = ['[shared_scale] - accounting', '[shared_scale] - airport', '[shared_scale] - amusement_park', '[shared_scale] - aquarium', '[shared_scale] - art_gallery', '[shared_scale] - atm', '[shared_scale] - bakery', '[shared_scale] - bank', '[shared_scale] - bar', '[shared_scale] - beauty_salon', '[shared_scale] - bicycle_store', '[shared_scale] - book_store', '[shared_scale] - bowling_alley', '[shared_scale] - bus_station', '[shared_scale] - cafe', '[shared_scale] - campground', '[shared_scale] - car_dealer', '[shared_scale] - car_rental', '[shared_scale] - car_repair', '[shared_scale] - car_wash', '[shared_scale] - casino', '[shared_scale] - cemetery', '[shared_scale] - church', '[shared_scale] - city_hall', '[shared_scale] - clothing_store', '[shared_scale] - convenience_store', '[shared_scale] - courthouse', '[shared_scale] - dentist', '[shared_scale] - department_store', '[shared_scale] - doctor', '[shared_scale] - drugstore', '[shared_scale] - electrician', '[shared_scale] - electronics_store', '[shared_scale] - embassy', '[shared_scale] - establishment', '[shared_scale] - finance', '[shared_scale] - fire_station', '[shared_scale] - florist', '[shared_scale] - food', '[shared_scale] - funeral_home', '[shared_scale] - furniture_store', '[shared_scale] - gas_station', '[shared_scale] - general_contractor', '[shared_scale] - grocery_or_supermarket', '[shared_scale] - gym', '[shared_scale] - hair_care', '[shared_scale] - hardware_store', '[shared_scale] - health', '[shared_scale] - hindu_temple', '[shared_scale] - home_goods_store', '[shared_scale] - hospital', '[shared_scale] - insurance_agency', '[shared_scale] - jewelry_store', '[shared_scale] - laundry', '[shared_scale] - lawyer', '[shared_scale] - library', '[shared_scale] - liquor_store', '[shared_scale] - local_government_office', '[shared_scale] - locksmith', '[shared_scale] - lodging', '[shared_scale] - meal_delivery', '[shared_scale] - meal_takeaway', '[shared_scale] - mosque', '[shared_scale] - movie_rental', '[shared_scale] - movie_theater', '[shared_scale] - moving_company', '[shared_scale] - museum', '[shared_scale] - night_club', '[shared_scale] - painter', '[shared_scale] - park', '[shared_scale] - parking', '[shared_scale] - pet_store', '[shared_scale] - pharmacy', '[shared_scale] - physiotherapist', '[shared_scale] - place_of_worship', '[shared_scale] - plumber', '[shared_scale] - point_of_interest', '[shared_scale] - police', '[shared_scale] - post_office', '[shared_scale] - premise', '[shared_scale] - primary_school', '[shared_scale] - real_estate_agency', '[shared_scale] - restaurant', '[shared_scale] - roofing_contractor', '[shared_scale] - school', '[shared_scale] - secondary_school', '[shared_scale] - shoe_store', '[shared_scale] - shopping_mall', '[shared_scale] - spa', '[shared_scale] - stadium', '[shared_scale] - storage', '[shared_scale] - store', '[shared_scale] - subway_station', '[shared_scale] - supermarket', '[shared_scale] - synagogue', '[shared_scale] - taxi_stand', '[shared_scale] - tourist_attraction', '[shared_scale] - train_station', '[shared_scale] - transit_station', '[shared_scale] - travel_agency', '[shared_scale] - university', '[shared_scale] - veterinary_care', '[shared_scale] - zoo']

SHARED_SCALE_COLS_POPULATION = ['[shared_scale] - [per_effective_area_square_meter] - worker_count', '[shared_scale] - [per_effective_area_square_meter] - student_count', '[shared_scale] - [per_effective_area_square_meter] - tourist_count', '[shared_scale] - [per_effective_area_square_meter] - shopper_count', '[shared_scale] - [per_effective_area_square_meter] - leisurer_count', '[shared_scale] - [per_effective_area_square_meter] - chorer_count', '[shared_scale] - [per_effective_area_square_meter] - resident_count']

SHARED_SCALE_COLS_SUPPLY_DEMAND = ['[shared_scale] - [supply_demand_index] - bar_worker', '[shared_scale] - [supply_demand_index] - bar_student', '[shared_scale] - [supply_demand_index] - bar_tourist', '[shared_scale] - [supply_demand_index] - bar_shopper', '[shared_scale] - [supply_demand_index] - bar_leisurer', '[shared_scale] - [supply_demand_index] - bar_chorer', '[shared_scale] - [supply_demand_index] - bar_resident', '[shared_scale] - [supply_demand_index] - bar_visitors_total', '[shared_scale] - [supply_demand_index] - bar_total', '[shared_scale] - [supply_demand_index] - cafe_worker', '[shared_scale] - [supply_demand_index] - cafe_student', '[shared_scale] - [supply_demand_index] - cafe_tourist', '[shared_scale] - [supply_demand_index] - cafe_shopper', '[shared_scale] - [supply_demand_index] - cafe_leisurer', '[shared_scale] - [supply_demand_index] - cafe_chorer', '[shared_scale] - [supply_demand_index] - cafe_resident', '[shared_scale] - [supply_demand_index] - cafe_visitors_total', '[shared_scale] - [supply_demand_index] - cafe_total', '[shared_scale] - [supply_demand_index] - restaurant_worker', '[shared_scale] - [supply_demand_index] - restaurant_student', '[shared_scale] - [supply_demand_index] - restaurant_tourist', '[shared_scale] - [supply_demand_index] - restaurant_shopper', '[shared_scale] - [supply_demand_index] - restaurant_leisurer', '[shared_scale] - [supply_demand_index] - restaurant_chorer', '[shared_scale] - [supply_demand_index] - restaurant_resident', '[shared_scale] - [supply_demand_index] - restaurant_visitors_total', '[shared_scale] - [supply_demand_index] - restaurant_total']

DATASET_SHARE_RANGE = {
    "[OA]_Normalizing_properties.csv": [],
    "[OA]_PTAL_directory.csv" : [],
    "[OA]_Street_value_directory.csv" : [],

    "[Residents]_Acorn_directory.csv" : [],
    "[Residents]_age_and_gender_distribution.csv" : SHARED_SCALE_AGE_DISTRIBUTION_COLUMNS,
    "[Residents]_spending_categories.csv" : SHARED_SCALE_COICOP_COLUMNS,
    "[Residents]_disposable_income_spending_categories.csv" : [],
    "[Residents]_income.csv" : SHARED_SCALE_PAYCKECK_DIRECTORY,
    "[Residents]_wellbeing_directory.csv": [],
    
    "[Places]_counts.csv" : SHARED_SCALE_COLS_PLACES,
    "[Places]_counts_normalized_by_OA_effective_area.csv" : SHARED_SCALE_COLS_PLACES,
    "[Places]_counts_normalized_by_household_per_meter.csv" : SHARED_SCALE_COLS_PLACES,
    "[Places]_counts_normalized_by_household_per_meter_bound.csv" : SHARED_SCALE_COLS_PLACES,

    "[POC_Demographic_distribution]_granular.csv" : [],
    "[POC_Demographic_distribution]_granular_normalized.csv" : [],
    "[POC_Demographic_distribution]_granular_normalized_relevance.csv" : [],

    "[Demographic_distribution]_granular_OA_scope.csv": SHARED_SCALE_COLS_OA_SCOPE,
    "[Demographic_distribution]_granular_borough_scope.csv": SHARED_SCALE_COLS_BOROUGH_SCOPE,
    "[Demographic_distribution]_supertypes_OA_scope.csv": SHARED_SCALE_COLS_OA_SCOPE,
    "[Demographic_distribution]_supertypes_borough_scope.csv": SHARED_SCALE_COLS_BOROUGH_SCOPE,
    "[Demographic_distribution]_supertypes_attractors_OA_scope.csv": SHARED_SCALE_COLS_OA_SCOPE,
    "[Demographic_distribution]_supertypes_attractors_borough_scope.csv": SHARED_SCALE_COLS_BOROUGH_SCOPE,
    "[Demographic_distribution]_supertypes_discriminant_OA_scope.csv": SHARED_SCALE_COLS_OA_SCOPE,
    "[Demographic_distribution]_supertypes_discriminant_borough_scope.csv": SHARED_SCALE_COLS_BOROUGH_SCOPE,

    "[Population]_total_over_24_hour.csv": SHARED_SCALE_COLS_POPULATION,
    "[Supply_demand]_example.csv": SHARED_SCALE_COLS_SUPPLY_DEMAND,

    "green_groups.csv" : [],
    "community_engagement.csv" : [],
    "remaining.csv" : [],
}

SKIP_COLUMNS = ["Unnamed: 0", "OA", "Unnamed: 0.1"]

# Metadata file generation method.
def generate_metadata(datasets, dataset_skip_columns, dataset_p_type, skip_columns):
    dict = {}

    for dataset_name in datasets.keys():
        dataset_folder = datasets[dataset_name]
        dataset = pd.read_csv(DATA_DIR + "processed_data/" + dataset_folder + dataset_name)
        
        dict[dataset_name] = {}
        
        # Get description mapping key. The mode operations on processing are messing things up!
        skipableColumns = dataset_skip_columns[dataset_name] + skip_columns

        # for each column
        column_data = []
        for i in dataset.dtypes.index:
            if str(i) not in skipableColumns:
                col_name = i
                col_type = dataset.dtypes[i]
                col_type_simplified = None
                range = sorted(dataset[i].dropna().unique().tolist())
                min_val = None
                max_val = None

                if "acorn" in col_name.lower():
                    granularity = "category"
                    if "group" in col_name.lower():
                        granularity = "group"
                    if "type" in col_name.lower():
                        granularity = "type"
                    if "wellbeing" in col_name.lower():
                        col_type_simplified = ["wellbeing", granularity]
                    else:
                        col_type_simplified = ["household", granularity]
                    range = [str(x) for x in range]
                elif is_numeric_dtype(dataset[i]):
                    if str(col_type) == "float64":
                        is_float_column_integer = dataset[i].dropna().apply(float.is_integer).all()

                        if is_float_column_integer: # float casted as int
                            col_type_simplified = "number_int"
                            min_val = min(range)
                            max_val = max(range)
                        else:   # actual float
                            col_type_simplified = "number_float"
                            min_val = min(range)
                            max_val = max(range)
                            range = None
                    else:
                        col_type_simplified = "number_int"
                        min_val = min(range)
                        max_val = max(range)
                else:
                    col_type_simplified = "string"
                    range = [str(x) for x in range]

                    if len(dataset_p_type[dataset_name]) > 0:
                        col_type_simplified = dataset_p_type[dataset_name]

                if range is not None and len(range) > 70:
                    range = None

                column_data_summary = {
                    "name": col_name,
                    "type_registered": str(col_type),
                    "type_practical": col_type_simplified,
                    "range": range,
                    "min": min_val,
                    "max": max_val
                }

                column_data.append(column_data_summary)

        dict[dataset_name]["column_data"] = column_data

        # Sharing ranges amongst columns.
        if dataset_name in DATASET_SHARE_RANGE.keys() and len(DATASET_SHARE_RANGE[dataset_name]) > 0:
            shared_min = 1111111111
            shared_max = -1111111111

            for c in dict[dataset_name]["column_data"]:
                if c["name"] in DATASET_SHARE_RANGE[dataset_name]:
                    if c["min"] < shared_min:
                        shared_min = c["min"]

                    if c["max"] > shared_max:
                        shared_max = c["max"]

            for c in dict[dataset_name]["column_data"]:
                if c["name"] in DATASET_SHARE_RANGE[dataset_name]:
                    c["min"] = shared_min
                    c["max"] = shared_max

    json_dict = json.dumps(dict)
    common.save_json_to_file(DATA_DIR + "processed_data/tabular_metadata/" ,json_dict, "output_data_metadata.json")
