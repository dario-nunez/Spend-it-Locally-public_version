"""Place type demographic distribution

Generates files that contain for each place type, a distribution of the 6 demographic
types (worker, student, tourist, shopper, leisurer, chorer). Supertypes are used
to reduce the time it takes to manually generate such files.

These files can be hand made (in fact the granular model is) but this script aims
at making the process less time consuming through code.

This file generates 3 model variants: supertypes, supertypes attractors and supertypes
discriminant. Their names indicate the supertypes included and the strategy used
to assign the demographic distributions in each case.

Input datasets:
- Postcodes_OAs_classifications.csv
- OA_places.json
- place_types.csv

Output datasets:
- place_types.csv
- place_types_supertypes.csv
- place_types_supertypes_attractors.csv
- place_types_supertypes_discriminant.csv
"""

import src.common as common
import pandas as pd
import json

################################################################################
# Constants.
################################################################################

DATA_DIR = ""

religion_0 = ["hindu_temple", "place_of_worship", "synagogue", "mosque", "church"]
store_1 = ["home_goods_store", "convenience_store", "liquor_store", "book_store", "shopping_mall", "grocery_or_supermarket", "supermarket", "hardware_store", "florist", "clothing_store", "department_store", "bicycle_store", "shoe_store", "movie_rental", "drugstore", "jewelry_store", "electronics_store", "pet_store", "furniture_store"]
chore_2 = ["storage", "moving_company", "car_dealer", "plumber", "car_repair", "painter", "travel_agency", "electrician", "post_office", "real_estate_agency", "car_wash", "locksmith", "laundry", "general_contractor", "roofing_contractor", "car_rental", "insurance_agency", "cemetery", "funeral_home"]
academia_3 = ["university", "secondary_school", "school", "primary_school", "library"]
medicine_4 = ["dentist", "veterinary_care", "pharmacy", "hospital", "physiotherapist"]
transport_5 = ["parking", "bus_station", "train_station", "subway_station", "transit_station", "taxi_stand"]
hospitality_6 = ["cafe", "bar", "bakery", "meal_takeaway", "restaurant", "meal_delivery", "food"]
generals_7 = ["point_of_interest", "establishment", "premise", "health", "doctor", "store"]
legal_8 = ["courthouse", "city_hall", "local_government_office", "lawyer", "embassy"]
attraction_9 = ["aquarium", "amusement_park", "lodging", "night_club", "casino", "movie_theater", "stadium", "bowling_alley", "zoo", "campground", "park"]
industry_10 = ["finance", "accounting"]
service_11 = ["atm", "bank", "police", "gas_station", "fire_station", "airport"]
selfcare_12 = ["beauty_salon", "spa", "hair_care", "gym"]
tourist_attraction_13 = ["tourist_attraction", "museum", "art_gallery"]

ATTRACTOR_SUPERTYPES = ["religion_0","store_1","chore_2","academia_3","medicine_4","transport_5","generals_7","legal_8","attraction_9","industry_10","service_11","selfcare_12", "tourist_attraction_13"]

SUPERTYPE_MAP = {
    "religion_0" :religion_0,
    "store_1":store_1,
    "chore_2":chore_2,
    "academia_3":academia_3,
    "medicine_4":medicine_4,
    "transport_5":transport_5,
    "hospitality_6":hospitality_6,
    "generals_7":generals_7,
    "legal_8":legal_8,
    "attraction_9":attraction_9,
    "industry_10":industry_10,
    "service_11":service_11,
    "selfcare_12":selfcare_12,
    "tourist_attraction_13":tourist_attraction_13
}

SUPERTYPE_DENSITY_MAP = {
    "religion_0" : {
        "worker_perc":60,
        "student_perc":10,
        "tourist_perc":5,
        "shopper_perc":5,
        "leisurer_perc":5,
        "chorer_perc":15
    },
    "store_1": {
        "worker_perc":15,
        "student_perc":5,
        "tourist_perc":10,
        "shopper_perc":60,
        "leisurer_perc":5,
        "chorer_perc":5
    },
    "chore_2": {
        "worker_perc":60,
        "student_perc":10,
        "tourist_perc":5,
        "shopper_perc":5,
        "leisurer_perc":5,
        "chorer_perc":15
    },
    "academia_3": {
        "worker_perc":12,
        "student_perc":80,
        "tourist_perc":1,
        "shopper_perc":1,
        "leisurer_perc":1,
        "chorer_perc":5
    },
    "medicine_4": {
        "worker_perc":65,
        "student_perc":10,
        "tourist_perc":5,
        "shopper_perc":5,
        "leisurer_perc":5,
        "chorer_perc":10
    },
    "transport_5": {
        "worker_perc":27,
        "student_perc":16,
        "tourist_perc":16,
        "shopper_perc":16,
        "leisurer_perc":16,
        "chorer_perc":10
    },
    "hospitality_6": {
        "worker_perc":30,
        "student_perc":5,
        "tourist_perc":25,
        "shopper_perc":5,
        "leisurer_perc":30,
        "chorer_perc":5
    },
    "generals_7": {
        "worker_perc":95,
        "student_perc":1,
        "tourist_perc":1,
        "shopper_perc":1,
        "leisurer_perc":1,
        "chorer_perc":1
    },
    "legal_8": {
        "worker_perc":75,
        "student_perc":5,
        "tourist_perc":5,
        "shopper_perc":5,
        "leisurer_perc":5,
        "chorer_perc":5
    },
    "attraction_9": {
        "worker_perc":5,
        "student_perc":5,
        "tourist_perc":30,
        "shopper_perc":5,
        "leisurer_perc":50,
        "chorer_perc":5
    },
    "industry_10": {
        "worker_perc":75,
        "student_perc":5,
        "tourist_perc":5,
        "shopper_perc":5,
        "leisurer_perc":5,
        "chorer_perc":5
    },
    "service_11": {
        "worker_perc":32,
        "student_perc":18,
        "tourist_perc":15,
        "shopper_perc":15,
        "leisurer_perc":15,
        "chorer_perc":5
    },
    "selfcare_12": {
        "worker_perc":5,
        "student_perc":5,
        "tourist_perc":5,
        "shopper_perc":5,
        "leisurer_perc":75,
        "chorer_perc":5
    },
    "tourist_attraction_13": {
        "worker_perc":5,
        "student_perc":5,
        "tourist_perc":60,
        "shopper_perc":5,
        "leisurer_perc":20,
        "chorer_perc":5
    }
}

DEMO_TYPES = ["worker_perc","student_perc","tourist_perc","shopper_perc","leisurer_perc","chorer_perc"]

# Executor method.
def process_place_types(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR
    possible_place_types = get_possible_place_types()
    oas = get_oas()
    oa_place_types = get_OA_place_types(possible_place_types, oas)
    generate_place_types_dataset(oa_place_types)

    # Actual dataset generation.
    generate_place_types_dataset_supertypes(oa_place_types)
    generate_place_types_dataset_supertypes_attractors(oa_place_types)
    generate_place_types_dataset_supertype_discriminant(oa_place_types)

# Assign a relevance score of 1 to attractor supertypes and 0 to all others.
def assign_relevance_score_attractors(x):
    # Make generals_7 have no influence by setting their relevance value to 0.
    if x == "generals_7":
        return 1

    if x in ATTRACTOR_SUPERTYPES:
        return 1
    
    return 0

# Apply a hand made relevance score to each supertype.
def assign_relevance_score_discriminant(x):
    # Simulate previous relevance by setting generals_7 to 0, and distinguishing between hospitality and the rest.
    
    # Previous solution (un-tailored)
    # SUPERTYPE_RELEVANCE_MAP = {
    #     "religion_0":2,
    #     "store_1":1,
    #     "chore_2":1,
    #     "academia_3":2,
    #     "medicine_4":1,
    #     "transport_5":2,
    #     "hospitality_6":0.2,
    #     "generals_7":1,
    #     "legal_8":2,
    #     "attraction_9":2,
    #     "industry_10":2,
    #     "service_11":1,
    #     "selfcare_12":2,
    #     "tourist_attraction_13":3
    # }

    SUPERTYPE_RELEVANCE_MAP = {
        "religion_0":2,
        "store_1":1,
        "chore_2":1,
        "academia_3":2,
        "medicine_4":1,
        "transport_5":1,
        "hospitality_6":0.75,
        "generals_7":0.5,
        "legal_8":2,
        "attraction_9":2,
        "industry_10":3,
        "service_11":1,
        "selfcare_12":1,
        "tourist_attraction_13":3
    }

    return SUPERTYPE_RELEVANCE_MAP[x]

# Generates a template model with an equal distribution for all demographics.
def generate_place_types_dataset(oa_place_types):
    place_df = pd.DataFrame(list(oa_place_types), columns = ["place_type"])
    place_df["relevance"] = 1
    place_df["worker_perc"] = 17.0
    place_df["student_perc"] = 16.6
    place_df["tourist_perc"] = 16.6
    place_df["shopper_perc"] = 16.6
    place_df["leisurer_perc"] = 16.6
    place_df["chorer_perc"] = 16.6
    common.save_dataframe_to_csv(DATA_DIR + "focused_data/place_types/", place_df, "place_types.csv")

# Returns the entire list of place types as retrieved from the Places API docs.  
def get_possible_place_types():
    dataset_name = "place_types.csv"
    dataset = pd.read_csv(DATA_DIR + "raw_data/place_types/" + dataset_name)
    possible_place_types = set(dataset["place_types"].to_list())
    return possible_place_types

# Returns a unique list of OAs in Westminster.
def get_oas():
    dataset_filtered_by_westminster = pd.read_csv(DATA_DIR + "focused_data/" + "authorities/" + "Postcodes_OAs_classifications.csv")
    oas = set(dataset_filtered_by_westminster["oa11cd"].to_list())
    return oas

# Get place types present in the Westminster.
def get_OA_place_types(possible_place_types, oas):
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

###########################################################################
# Dataset generation functions.
###########################################################################

# Generate the supertypes model file.
def generate_place_types_dataset_supertypes(oa_place_types):
    place_df = pd.DataFrame(list(oa_place_types), columns = ["place_type"])

    place_df["relevance"] = 1

    for demo_type in DEMO_TYPES:
        place_df[demo_type] = 0

    for place in place_df["place_type"].tolist():
        place_type = None

        for k in SUPERTYPE_MAP.keys():
            val = SUPERTYPE_MAP[k]
            if place in val:
                place_type = k
                break

        for demo_type in DEMO_TYPES:
            place_df.loc[place_df["place_type"] == place, demo_type] = SUPERTYPE_DENSITY_MAP[place_type][demo_type]

    place_df = place_df.sort_values(by=["place_type"],ignore_index=True)
    # print(place_df)
    common.save_dataframe_to_csv(DATA_DIR + "focused_data/place_types/", place_df, "place_types_supertypes.csv")

# Generate the supertypes attractors model file.
def generate_place_types_dataset_supertypes_attractors(oa_place_types):
    place_df = pd.DataFrame(list(oa_place_types), columns = ["place_type"])

    place_df["relevance"] = 1

    for demo_type in DEMO_TYPES:
        place_df[demo_type] = 0

    for place in place_df["place_type"].tolist():
        place_type = None

        for k in SUPERTYPE_MAP.keys():
            val = SUPERTYPE_MAP[k]
            if place in val:
                place_type = k
                break

        # Only considering attractors, excluding services compleately.
        place_df.loc[place_df["place_type"] == place, "relevance"] = assign_relevance_score_attractors(place_type)

        for demo_type in DEMO_TYPES:
            place_df.loc[place_df["place_type"] == place, demo_type] = SUPERTYPE_DENSITY_MAP[place_type][demo_type]

    place_df = place_df.sort_values(by=["place_type"],ignore_index=True)
    # print(place_df)
    common.save_dataframe_to_csv(DATA_DIR + "focused_data/place_types/", place_df, "place_types_supertypes_attractors.csv")

# Generate the supertypes discriminant model file.
def generate_place_types_dataset_supertype_discriminant(oa_place_types):
    # Previous solution (un-tailored)
    # discriminant_supertype_density_map = {
    #     "religion_0" : {
    #         "worker_perc":56,
    #         "student_perc":1,
    #         "tourist_perc":1,
    #         "shopper_perc":1,
    #         "leisurer_perc":1,
    #         "chorer_perc":40
    #     },
    #     "store_1": {
    #         "worker_perc":30,
    #         "student_perc":1,
    #         "tourist_perc":1,
    #         "shopper_perc":56,
    #         "leisurer_perc":1,
    #         "chorer_perc":1
    #     },
    #     "chore_2": {
    #         "worker_perc":56,
    #         "student_perc":6,
    #         "tourist_perc":6,
    #         "shopper_perc":6,
    #         "leisurer_perc":6,
    #         "chorer_perc":20
    #     },
    #     "academia_3": {
    #         "worker_perc":10,
    #         "student_perc":86,
    #         "tourist_perc":1,
    #         "shopper_perc":1,
    #         "leisurer_perc":1,
    #         "chorer_perc":1
    #     },
    #     "medicine_4": {
    #         "worker_perc":58,
    #         "student_perc":10,
    #         "tourist_perc":5,
    #         "shopper_perc":1,
    #         "leisurer_perc":6,
    #         "chorer_perc":20
    #     },
    #     "transport_5": {
    #         "worker_perc":26,
    #         "student_perc":16,
    #         "tourist_perc":16,
    #         "shopper_perc":16,
    #         "leisurer_perc":16,
    #         "chorer_perc":10
    #     },
    #     "hospitality_6": {
    #         "worker_perc":17,
    #         "student_perc":1,
    #         "tourist_perc":40,
    #         "shopper_perc":1,
    #         "leisurer_perc":40,
    #         "chorer_perc":1
    #     },
    #     "generals_7": {
    #         "worker_perc":95,
    #         "student_perc":1,
    #         "tourist_perc":1,
    #         "shopper_perc":1,
    #         "leisurer_perc":1,
    #         "chorer_perc":1
    #     },
    #     "legal_8": {
    #         "worker_perc":95,
    #         "student_perc":1,
    #         "tourist_perc":1,
    #         "shopper_perc":1,
    #         "leisurer_perc":1,
    #         "chorer_perc":1
    #     },
    #     "attraction_9": {
    #         "worker_perc":10,
    #         "student_perc":1,
    #         "tourist_perc":38,
    #         "shopper_perc":1,
    #         "leisurer_perc":48,
    #         "chorer_perc":1
    #     },
    #     "industry_10": {
    #         "worker_perc":95,
    #         "student_perc":1,
    #         "tourist_perc":1,
    #         "shopper_perc":1,
    #         "leisurer_perc":1,
    #         "chorer_perc":1
    #     },
    #     "service_11": {
    #         "worker_perc":16,
    #         "student_perc":16,
    #         "tourist_perc":16,
    #         "shopper_perc":16,
    #         "leisurer_perc":16,
    #         "chorer_perc":20
    #     },
    #     "selfcare_12": {
    #         "worker_perc":1,
    #         "student_perc":1,
    #         "tourist_perc":1,
    #         "shopper_perc":1,
    #         "leisurer_perc":95,
    #         "chorer_perc":1
    #     },
    #     "tourist_attraction_13": {
    #         "worker_perc":10,
    #         "student_perc":1,
    #         "tourist_perc":58,
    #         "shopper_perc":1,
    #         "leisurer_perc":28,
    #         "chorer_perc":1
    #     }
    # }

    discriminant_supertype_density_map = {
        "religion_0" : {
            "worker_perc":60,
            "student_perc":10,
            "tourist_perc":1,
            "shopper_perc":1,
            "leisurer_perc":1,
            "chorer_perc":27
        },
        "store_1": {
            "worker_perc":15,
            "student_perc":1,
            "tourist_perc":10,
            "shopper_perc":77,
            "leisurer_perc":1,
            "chorer_perc":1
        },
        "chore_2": {
            "worker_perc":60,
            "student_perc":10,
            "tourist_perc":1,
            "shopper_perc":1,
            "leisurer_perc":1,
            "chorer_perc":27
        },
        "academia_3": {
            "worker_perc":12,
            "student_perc":84,
            "tourist_perc":1,
            "shopper_perc":1,
            "leisurer_perc":1,
            "chorer_perc":1
        },
        "medicine_4": {
            "worker_perc":77,
            "student_perc":10,
            "tourist_perc":1,
            "shopper_perc":1,
            "leisurer_perc":1,
            "chorer_perc":10
        },
        "transport_5": {
            "worker_perc":27,
            "student_perc":16,
            "tourist_perc":16,
            "shopper_perc":16,
            "leisurer_perc":16,
            "chorer_perc":10
        },
        "hospitality_6": {
            "worker_perc":30,
            "student_perc":1,
            "tourist_perc":32,
            "shopper_perc":1,
            "leisurer_perc":35,
            "chorer_perc":1
        },
        "generals_7": {
            "worker_perc":95,
            "student_perc":1,
            "tourist_perc":1,
            "shopper_perc":1,
            "leisurer_perc":1,
            "chorer_perc":1
        },
        "legal_8": {
            "worker_perc":95,
            "student_perc":1,
            "tourist_perc":1,
            "shopper_perc":1,
            "leisurer_perc":1,
            "chorer_perc":1
        },
        "attraction_9": {
            "worker_perc":10,
            "student_perc":1,
            "tourist_perc":37,
            "shopper_perc":1,
            "leisurer_perc":50,
            "chorer_perc":1
        },
        "industry_10": {
            "worker_perc":95,
            "student_perc":1,
            "tourist_perc":1,
            "shopper_perc":1,
            "leisurer_perc":1,
            "chorer_perc":1
        },
        "service_11": {
            "worker_perc":55,
            "student_perc":10,
            "tourist_perc":10,
            "shopper_perc":10,
            "leisurer_perc":10,
            "chorer_perc":5
        },
        "selfcare_12": {
            "worker_perc":15,
            "student_perc":10,
            "tourist_perc":5,
            "shopper_perc":5,
            "leisurer_perc":60,
            "chorer_perc":5
        },
        "tourist_attraction_13": {
            "worker_perc":7,
            "student_perc":1,
            "tourist_perc":70,
            "shopper_perc":1,
            "leisurer_perc":20,
            "chorer_perc":1
        }
    }

    place_df = pd.DataFrame(list(oa_place_types), columns = ["place_type"])
    place_df["relevance"] = 1

    for demo_type in DEMO_TYPES:
        place_df[demo_type] = 0

    for place in place_df["place_type"].tolist():
        place_type = None

        for k in SUPERTYPE_MAP.keys():
            val = SUPERTYPE_MAP[k]
            if place in val:
                place_type = k
                break

        # Relevance combined with attractors only highlights the shift in tourist distribution.
        place_df.loc[place_df["place_type"] == place, "relevance"] = assign_relevance_score_discriminant(place_type)

        for demo_type in DEMO_TYPES:
            place_df.loc[place_df["place_type"] == place, demo_type] = discriminant_supertype_density_map[place_type][demo_type]

    place_df = place_df.sort_values(by=["place_type"],ignore_index=True)
    # print(place_df)
    common.save_dataframe_to_csv(DATA_DIR + "focused_data/place_types/", place_df, "place_types_supertypes_discriminant.csv")
