/*
This file handles the data loading and the construction of the main "DATA" object that stores all the information aggregated
by OA. The current loading pattern is not optimal. Automatic loading using a single dataset names array would be ideal.
 */

// Dataset containing geographical boundary information
const topologyPath = "data/OAs_topojson_wgs84.json"

// All CSV datasets.
const IN_DATASETS = [
    "[OA]_Normalizing_properties.csv",

    "[Residents]_Acorn_directory.csv",
    "[Residents]_age_and_gender_distribution.csv",
    "[Residents]_spending_categories.csv",
    "[Residents]_disposable_income_spending_categories.csv",
    "[Residents]_income.csv",
    "[OA]_PTAL_directory.csv",
    "[OA]_Street_value_directory.csv",
    "[Residents]_wellbeing_directory.csv",

    "[Places]_counts.csv",
    "[Places]_counts_normalized_by_OA_effective_area.csv",
    "[Places]_counts_normalized_by_household_per_meter.csv",
    "[Places]_counts_normalized_by_household_per_meter_bound.csv",

    "[POC_Demographic_distribution]_granular.csv",
    "[POC_Demographic_distribution]_granular_normalized.csv",
    "[POC_Demographic_distribution]_granular_normalized_relevance.csv",

    "[Demographic_distribution]_granular_OA_scope.csv",
    "[Demographic_distribution]_granular_borough_scope.csv",
    "[Demographic_distribution]_supertypes_OA_scope.csv",
    "[Demographic_distribution]_supertypes_borough_scope.csv",
    "[Demographic_distribution]_supertypes_attractors_OA_scope.csv",
    "[Demographic_distribution]_supertypes_attractors_borough_scope.csv",
    "[Demographic_distribution]_supertypes_discriminant_OA_scope.csv",
    "[Demographic_distribution]_supertypes_discriminant_borough_scope.csv",

    "[Population]_total_over_24_hour.csv",
    "[Supply_demand]_example.csv",

    "community_engagement.csv",
    "green_groups.csv",
    "remaining.csv"
]

/*
Loads all the data and constructs an object of the structure:
OA_1: {
    dataset_1: {
        column_1: "column 1 value",
        column_n: "column n value",
    },
    dataset_n: {...}
},
OA_n: {...}
which intends to save processing times when looking up single data values by OA.
 */
const loadAndProcessData = () =>
    Promise
        .all([
            d3.json(topologyPath),
            d3.csv("data/" + IN_DATASETS[0]),
            d3.csv("data/" + IN_DATASETS[1]),
            d3.csv("data/" + IN_DATASETS[2]),
            d3.csv("data/" + IN_DATASETS[3]),
            d3.csv("data/" + IN_DATASETS[4]),
            d3.csv("data/" + IN_DATASETS[5]),
            d3.csv("data/" + IN_DATASETS[6]),
            d3.csv("data/" + IN_DATASETS[7]),
            d3.csv("data/" + IN_DATASETS[8]),
            d3.csv("data/" + IN_DATASETS[9]),
            d3.csv("data/" + IN_DATASETS[10]),
            d3.csv("data/" + IN_DATASETS[11]),
            d3.csv("data/" + IN_DATASETS[12]),
            d3.csv("data/" + IN_DATASETS[13]),
            d3.csv("data/" + IN_DATASETS[14]),
            d3.csv("data/" + IN_DATASETS[15]),
            d3.csv("data/" + IN_DATASETS[16]),
            d3.csv("data/" + IN_DATASETS[17]),
            d3.csv("data/" + IN_DATASETS[18]),
            d3.csv("data/" + IN_DATASETS[19]),
            d3.csv("data/" + IN_DATASETS[20]),
            d3.csv("data/" + IN_DATASETS[21]),
            d3.csv("data/" + IN_DATASETS[22]),
            d3.csv("data/" + IN_DATASETS[23]),
            d3.csv("data/" + IN_DATASETS[24]),
            d3.csv("data/" + IN_DATASETS[25]),
            d3.csv("data/" + IN_DATASETS[26]),
            d3.csv("data/" + IN_DATASETS[27]),
            d3.csv("data/" + IN_DATASETS[28]),
        ]).then(([topology, csv1,csv2,csv3,csv4,csv5,csv6,csv7,csv8,csv9,csv10,csv11,csv12,csv13,csv14,csv15,csv16,csv17,csv18,csv19,csv20,csv21,csv22,csv23,csv24,csv25,csv26,csv27,csv28,csv29]) => {
            let oas = topojson.feature(topology, topology.objects.OAs_geojson_wgs84);
            let temp = new Map()

            temp.set(IN_DATASETS[0], csv1)
            temp.set(IN_DATASETS[1], csv2)
            temp.set(IN_DATASETS[2], csv3)
            temp.set(IN_DATASETS[3], csv4)
            temp.set(IN_DATASETS[4], csv5)
            temp.set(IN_DATASETS[5], csv6)
            temp.set(IN_DATASETS[6], csv7)
            temp.set(IN_DATASETS[7], csv8)
            temp.set(IN_DATASETS[8], csv9)
            temp.set(IN_DATASETS[9], csv10)
            temp.set(IN_DATASETS[10], csv11)
            temp.set(IN_DATASETS[11], csv12)
            temp.set(IN_DATASETS[12], csv13)
            temp.set(IN_DATASETS[13], csv14)
            temp.set(IN_DATASETS[14], csv15)
            temp.set(IN_DATASETS[15], csv16)
            temp.set(IN_DATASETS[16], csv17)
            temp.set(IN_DATASETS[17], csv18)
            temp.set(IN_DATASETS[18], csv19)
            temp.set(IN_DATASETS[19], csv20)
            temp.set(IN_DATASETS[20], csv21)
            temp.set(IN_DATASETS[21], csv22)
            temp.set(IN_DATASETS[22], csv23)
            temp.set(IN_DATASETS[23], csv24)
            temp.set(IN_DATASETS[24], csv25)
            temp.set(IN_DATASETS[25], csv26)
            temp.set(IN_DATASETS[26], csv27)
            temp.set(IN_DATASETS[27], csv28)
            temp.set(IN_DATASETS[28], csv29)

            Array.from(temp.keys()).forEach(k => {
                let csv = temp.get(k)
                const rowById = csv.reduce((accumulator, d) => {
                    accumulator[d.OA] = d;
                    return accumulator;
                }, {});

                oas.features.forEach(d => {
                    d.properties[k] = rowById[d.properties.geo_code]
                })
            });

            console.log("Data:")
            console.log(oas)
            DATA = oas.features
            return oas;
    });
