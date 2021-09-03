/*
This file contains functionality that maps all possible dataset-column-oa selections to an auxiliary visualization.
 */

/*
Wrapper function that triggers the visualization mapping and constructs an indexable string containing information about
the selected dataset, column and OA.
 */
function visualize() {
    let oa = "yes_oa";

    if (SELECTED_OA === null) {
        oa = "no_oa"
    }

    let key = SELECTED_DATASET + "#" + SELECTED_COLUMN + "#" + oa
    applyToVisualizationMap(key)
}

/*
Triggers the rendering of a different auxiliary visualization for any combination of selected dataset, column and OA. A switch
statement with regular expressions is used to reduce as much as possible the number of individual case that require an explicit
definition.
The general default cases are:
- A blank column (regardless of the dataset) will produce the placeholder information text.
- A selected dataset, a blank column and a selected OA will produce a data table.
- A selected dataset and column will produce a histogram for numeric columns and a frequency count for categorical columns.
 */
function applyToVisualizationMap(key) {
    switch(key) {
        // Places datasets.
        case (key.match(/\[Places].*#\[shared_scale].*#yes_oa/) || {}).input:
            dataTableSelectedOA()
            break;
        case (key.match(/\[Places].*#.*#yes_oa/) || {}).input:
            barChartPlacesSelectedOA()
            break;
        // PTAL directory.
        case (key.match(/\[OA]_PTAL_directory.csv#Public_Transport_Accessibility_Level#yes_oa/) || {}).input:
            freqDistColumnChartPlot("Public Transport Accessibility Level_frequency_count")
            break;
        // Acorn directory.
        case (key.match(/\[Residents]_Acorn_directory.csv#Acorn_category#yes_oa/) || {}).input:
            freqDistColumnChartPlot("Acorn Category_frequency_count")
            break;
        case (key.match(/\[Residents]_Acorn_directory.csv#Acorn_group#yes_oa/) || {}).input:
            freqDistColumnChartPlot("Acorn Group_frequency_count")
            break;
        // Wellbeing directory.
        case (key.match(/\[Residents]_wellbeing_directory.csv#Wellbeing_Acorn_group#yes_oa/) || {}).input:
            freqDistColumnChartPlot("Wellbeing Acorn Group_frequency_count");
            break;
        case (key.match(/\[Residents]_wellbeing_directory.csv#Wellbeing_Acorn_type#yes_oa/) || {}).input:
            freqDistColumnChartPlot("Wellbeing Acorn Type_frequency_count");
            break;
        // Age distribution.
        case (key.match(/\[Residents]_age_and_gender_distribution.csv#\[count].*#yes_oa/) || {}).input:
            ageGenderGroupCountColumnChartSelectedOA()
            break;
        case (key.match(/\[Residents]_age_and_gender_distribution.csv#\[%_in_OA].*#yes_oa/) || {}).input:
            ageGenderGroupCountColumnChartSelectedOA()
            break;
        case (key.match(/\[Residents]_age_and_gender_distribution.csv#Females total#yes_oa/) || {}).input:
            ageGenderGenderTotalsSelectedOA()
            break;
        case (key.match(/\[Residents]_age_and_gender_distribution.csv#Males total#yes_oa/) || {}).input:
            ageGenderGenderTotalsSelectedOA()
            break;
        // Spending categories.
        case (key.match(/\[Residents]_spending_categories.csv#\[sum_in_OA].*#yes_oa/) || {}).input:
            spendingCategoriesCategoryComparisonSelectedOA("[sum_in_OA]")
            break;
        case (key.match(/\[Residents]_spending_categories.csv#\[average_per_person_in_OA].*#yes_oa/) || {}).input:
            spendingCategoriesCategoryComparisonSelectedOA("[average_per_person_in_OA]")
            break;
        // Disposable income spending categories.
        case (key.match(/\[Residents]_disposable_income_spending_categories.csv#Mean over all households in an OA: Income tax.*#yes_oa/) || {}).input:
            disposableIncomeSpendingCategoriesCategoryComparisonSelectedOA("Mean over all households in an OA: Income tax")
            break;
        case (key.match(/\[Residents]_disposable_income_spending_categories.csv#Mean over relevant households in an OA.*#yes_oa/) || {}).input:
            disposableIncomeSpendingCategoriesCategoryComparisonSelectedOA("Mean over relevant households in an OA")
            break;
        case (key.match(/\[Residents]_disposable_income_spending_categories.csv#Proportion of households paying %.*#yes_oa/) || {}).input:
            disposableIncomeSpendingCategoriesCategoryComparisonSelectedOA("Proportion of households paying %")
            break;
        case (key.match(/\[Residents]_disposable_income_spending_categories.csv#CACI_Essential_Outgoings.*#yes_oa/) || {}).input:
            disposableIncomeSpendingCategoriesCategoryComparisonSelectedOA("CACI_Essential_Outgoings")
            break;
        // Income brackets.
        case (key.match(/\[Residents]_income.csv#\[count_in_OA].*#yes_oa/) || {}).input:
            incomeBracketSelectedOA("[count_in_OA]")
            break;
        case (key.match(/\[Residents]_income.csv#\[%_in_OA].*#yes_oa/) || {}).input:
            incomeBracketSelectedOA("[%_in_OA]")
            break;
        // POC demographic distribution densities.
        case (key.match(/\[POC_Demographic_distribution]_granular.*.csv#.*#yes_oa/) || {}).input:
            let components = SELECTED_COLUMN.split(" - ")
            if (SELECTED_COLUMN === "blank") {
                dataTableSelectedOA()
                break;
            }

            if (components[0] === "[per_effective_area_square_meter]") {
                if (components[1].includes("units")){    // units
                    demographicTypeValueSelectedOAColumnChart("[per_effective_area_square_meter] - ", "_units")
                } else {    // values
                    demographicTypeUnitsSelectedOAPieChart("[per_effective_area_square_meter] - ", "_value")
                }
            } else if (components[0] === "[%_of_borough_total]") {
                if (components[2].includes("units")){    // units
                    demographicTypeValueSelectedOAColumnChart("[%_of_borough_total] - [per_effective_area_square_meter] - ", "_units")
                } else {    // values
                    demographicTypeValueSelectedOAColumnChart("[%_of_borough_total] - [per_effective_area_square_meter] - ", "_value")
                }
            } else if (components[0] === "[%_of_OA_total]") {
                if (components[2].includes("units")){    // units
                    demographicTypeUnitsSelectedOAPieChart("[%_of_OA_total] - [per_effective_area_square_meter] - ", "_units")
                } else {    // values
                    demographicTypeUnitsSelectedOAPieChart("[%_of_OA_total] - [per_effective_area_square_meter] - ", "_value")
                }
            } else if (components[0].includes("units")){    // units
                demographicTypeValueSelectedOAColumnChart("", "_units")
            } else {    // values
                demographicTypeUnitsSelectedOAPieChart("", "_value")
            }

            break;
        // Demographic distribution densities OA scope.
        case (key.match(/\[Demographic_distribution]_.*_OA_scope.csv#\[%_of_OA_total].*#yes_oa/) || {}).input:
            demographicTypeUnitsSelectedOAPieChart("[%_of_OA_total] - [per_effective_area_square_meter] - ", "")
            break;
        // Demographic distribution densities borough scope.
        case (key.match(/\[Demographic_distribution]_.*_borough_scope.csv#\[total].*#yes_oa/) || {}).input:
            demographicTypeUnitsSelectedOAPieChart("[total] - ", "_count")
            break;
        case (key.match(/\[Demographic_distribution]_.*_borough_scope.csv#\[per_effective_area_square_meter].*#yes_oa/) || {}).input:
            demographicTypeValueSelectedOAColumnChart("[per_effective_area_square_meter] - ", "_count")
            break;
        case (key.match(/\[Demographic_distribution]_.*_borough_scope.csv#\[%_of_borough_total].*#yes_oa/) || {}).input:
            demographicTypeValueSelectedOAColumnChart("[%_of_borough_total] - [per_effective_area_square_meter] - ", "")
            break;
        // Total population.
        case (key.match(/\[Population]_total_over_24_hour.csv#\[per_effective_area_square_meter].*#yes_oa/) || {}).input:
            populationDemographicTypeSelectedOAPieChart("[per_effective_area_square_meter] - ", "_count")
            break;
        case (key.match(/\[Population]_total_over_24_hour.csv#\[shared_scale].*#yes_oa/) || {}).input:
            populationDemographicTypeSelectedOAColumnChart("[shared_scale] - [per_effective_area_square_meter] - ", "_count")
            break;
        // Supply/demand example.
        case (key.match(/\[Supply_demand]_example.csv#\[supply - demand].*#yes_oa/) || {}).input:
            supplyMinusDemandByPlaceType()
            break;
        case (key.match(/\[Supply_demand]_example.csv#\[supply_demand_index].*#yes_oa/) || {}).input:
            supplyDemandIndexScoreByPlaceType()
            break;
        // Default fallback cases.
        case (key.match(/.*.csv#.*#yes_oa/) || {}).input:
            // When an OA is selected.
            dataTableSelectedOA()
            break;
        default:
            // When an OA is not selected.
            let dom = SCALES_MAP.get(SELECTED_DATASET).get(SELECTED_COLUMN).domain()
            if (SELECTED_COLUMN === "blank") {
                defaultVisualization()
            } else {
                if (typeof(dom[0]) === "string") {
                    // String columns
                    categoricalColumnCountColumnChart(SELECTED_COLUMN)
                } else {
                    // Numeric columns.
                    numericColumnHistogram(SELECTED_COLUMN)
                }
            }
            break;
    }
}
