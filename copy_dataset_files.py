"""Copy dataset files

A script used to copy all the required datasets from the data processing directory
to the user interface's data directory.
"""

import shutil
import os

CWD = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TO = CWD + "/Spend-it-Locally/user_interface/website_ui/data/"
FROM = CWD + "/Spend-it-Locally/data_processing/data/"

DATASETS = [
    "processed_data/normalizers/[OA]_Normalizing_properties.csv",
    "processed_data/acorn/[OA]_PTAL_directory.csv",
    "processed_data/acorn/[OA]_Street_value_directory.csv",

    "processed_data/acorn/[Residents]_Acorn_directory.csv",
    "processed_data/acorn/[Residents]_age_and_gender_distribution.csv",
    "processed_data/acorn/[Residents]_spending_categories.csv",
    "processed_data/acorn/[Residents]_disposable_income_spending_categories.csv",
    "processed_data/acorn/[Residents]_income.csv",
    "processed_data/acorn/[Residents]_wellbeing_directory.csv",

    "processed_data/places/[Places]_counts.csv",
    "processed_data/places/[Places]_counts_normalized_by_OA_effective_area.csv",
    "processed_data/places/[Places]_counts_normalized_by_household_per_meter.csv",
    "processed_data/places/[Places]_counts_normalized_by_household_per_meter_bound.csv",

    "processed_data/demographic_distributions/[POC_Demographic_distribution]_granular.csv",
    "processed_data/demographic_distributions/[POC_Demographic_distribution]_granular_normalized.csv",
    "processed_data/demographic_distributions/[POC_Demographic_distribution]_granular_normalized_relevance.csv",

    "processed_data/demographic_distributions/[Demographic_distribution]_granular_OA_scope.csv",
    "processed_data/demographic_distributions/[Demographic_distribution]_granular_borough_scope.csv",
    "processed_data/demographic_distributions/[Demographic_distribution]_supertypes_OA_scope.csv",
    "processed_data/demographic_distributions/[Demographic_distribution]_supertypes_borough_scope.csv",
    "processed_data/demographic_distributions/[Demographic_distribution]_supertypes_attractors_OA_scope.csv",
    "processed_data/demographic_distributions/[Demographic_distribution]_supertypes_attractors_borough_scope.csv",
    "processed_data/demographic_distributions/[Demographic_distribution]_supertypes_discriminant_OA_scope.csv",
    "processed_data/demographic_distributions/[Demographic_distribution]_supertypes_discriminant_borough_scope.csv",
    
    "processed_data/placing_places/[Population]_total_over_24_hour.csv",
    "processed_data/placing_places/[Supply_demand]_example.csv",

    "processed_data/survey/community_engagement.csv",
    "processed_data/survey/green_groups.csv",
    "processed_data/survey/remaining.csv",

    "processed_data/tabular_metadata/output_data_metadata.json",

    "focused_data/geodata/OAs_topojson_wgs84.json",
]

print("CWD:", CWD)
print("FROM:", FROM)
print("TO:", TO)

for d in DATASETS:
    shutil.copy(FROM + d, TO)
