/*
This file handles the implementation of all the auxiliary visualizations corresponding to the user Dario Nunez.
Although some visualizations are fully dynamic and will work with any reasonably structured dataset, others are bespoke
to the structure and column naming convention of the original datasets of this project.
"Material Charts" and the older "corechart" from Google Charts are both used. The latter is preferred due to its style and
developer support.
 */

google.charts.load('current', {packages: ['corechart', 'bar', 'table', 'line']});

let DEMO_TYPES = ["worker", "student", "tourist", "shopper", "leisurer", "chorer"]

/*
Gray placeholder text indicating to select a dataset, column and OA.
 */
function defaultVisualization() {
    const myNode = document.getElementById("chart_div");
    myNode.innerHTML = '<p class="h2 m-4" style="color: #cecece; text-align:center;">Select a dataset / column / OA</p>';
}

/*
A data table that displays all the available columns (and their values) of a given dataset.
 */
function dataTableSelectedOA() {
    let subtractive_columns = ["", "Unnamed: 0"]
    let selected_oa_dataset = SELECTED_OA.getProperty(SELECTED_DATASET)
    selected_oa_dataset = Object.fromEntries(Object.entries(selected_oa_dataset).filter(([key]) => !subtractive_columns.includes(key)))
    selected_oa_dataset = Object.fromEntries(Object.entries(selected_oa_dataset).filter(([key]) => !key.includes(["shared_scale"])))

    var data = new google.visualization.DataTable();

    let rows = []
    data.addColumn("string", "Property")
    data.addColumn("string", "Value")

    for (const entry of Object.entries(selected_oa_dataset)) {
        let key = entry[0]
        let value = entry[1]

        rows.push([key, value])
    }

    data.addRows(rows);

    let configs = {
        allowHtml:true,
        showRowNumber: false,
        sort: "disable",
        width: '100%',
        height: (Object.entries(selected_oa_dataset).length * 35) + 20,
        cssClassNames: {
            headerRow: 'table_vis_header',
            tableCell: 'tableFont'
        }
    }

    var table = new google.visualization.Table(document.getElementById('chart_div'));
    table.draw(data, configs);
}

/*
Material Charts bar chart for the places dataset.
 */
function barChartPlacesSelectedOA() {
    let subtractive_columns = ["", "OA", "Unnamed: 0", "point_of_interest", "establishment", "premise", "health", "doctor", "store", "food"]
    let selected_oa_dataset = SELECTED_OA.getProperty(SELECTED_DATASET)
    let columns = Object.keys(selected_oa_dataset)
    let filtered_columns = columns.filter(x => !subtractive_columns.includes(x))
    filtered_columns = filtered_columns.filter(x => !x.includes(["shared_scale"]))
    let sorted_columns = filtered_columns.sort()

    let rows = [["Place type", "Number of places in OA"]]
    for (const col of sorted_columns) {
        rows.push([col, parseFloat(selected_oa_dataset[col])])
    }

    let data = google.visualization.arrayToDataTable(rows);

    // Material bar
    let options = {
        // chart: {
        //     title: SELECTED_DATASET + " - selected_OA: " + SELECTED_OA.getProperty("geo_code")
        // },
        height: 1400,
        bars: 'horizontal', // Required for Material Bar Charts.
        legend: { position: 'none' },
        axes: {
            x: {
                0: {
                    side: 'top',
                    label: 'Value'
                },
            }
        }
    };
    let chart = new google.charts.Bar(document.getElementById('chart_div'));
    chart.draw(data, google.charts.Bar.convertOptions(options));
}

/*
Column chart for visualizing frequency columns for categorical columns.
 */
function freqDistColumnChartPlot(freqDistColName) {
    let selectedOaDataset = SELECTED_OA.getProperty(SELECTED_DATASET)
    let freqDistColumnString = selectedOaDataset[freqDistColName]
    let jsonFreqDistColumn = JSON.parse(freqDistColumnString.replaceAll("'",'"'))

    let rows = [["Class", "Frequency"]]

    for (const entry of Object.entries(jsonFreqDistColumn)) {
        let key = entry[0]
        let value = entry[1]
        rows.push([key, value])
    }

    if (rows.length === 1) {
        rows.push(["undefined", 1])
    }

    let data = google.visualization.arrayToDataTable(rows)
    data.sort({column: 0, desc: false});

    let options = {
        title: "Column chart: " + SELECTED_COLUMN + " category count in OA",
        hAxis: {
            title: SELECTED_COLUMN,
            maxAlternation: 0
        },
        vAxis: {
            title: ((LOGARITHMIC_SCALE) ? "OA count (logarithmic axis)" : "OA count"),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null')
        },
        // backgroundColor: '#f1f8e9',
        legend: {position: "none"},
        height: "100%",
        width: "100%"
    };
    let chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

/*
Bespoke corechart charts.
 */
function ageGenderGroupCountColumnChartSelectedOA() {
    let selected_oa_dataset = SELECTED_OA.getProperty(SELECTED_DATASET)
    let typePrefix = SELECTED_COLUMN.split(" - ")[0]
    let genderPrefix = SELECTED_COLUMN.split(" - ")[1]
    let datasetPrefixed = Object.fromEntries(Object.entries(selected_oa_dataset).filter(([key]) => key.split(" - ")[0] === typePrefix))

    let chartData = new google.visualization.DataTable();
    let chartTitle
    let chartLegend

    if (genderPrefix === "Total") {
        selected_oa_dataset = Object.fromEntries(Object.entries(datasetPrefixed).filter(([key]) => key.split(" - ")[1] === genderPrefix))
        let rows = []
        for (const entry of Object.entries(selected_oa_dataset)) {
            let key = entry[0]
            let value = parseFloat(entry[1])
            let prettyKey = key.split(" - ")[2]
            rows.push([prettyKey, value])
        }

        chartData.addColumn('string', 'Age range');
        chartData.addColumn('number', "Total");
        chartData.addRows(rows)

        chartTitle = "Column chart: Total " + typePrefix + " - " + "by age range and gender in OA"
        chartLegend = {position: "none"}
    } else {
        selected_oa_dataset = Object.fromEntries(Object.entries(datasetPrefixed).filter(([key]) => key.split(" - ")[1] !== "Total"))
        let rows = []
        let seenAgeRanges = []
        for (const entry of Object.entries(selected_oa_dataset)) {
            let key = entry[0]
            let keyAgeRange = key.split(" - ")[2]

            if (!seenAgeRanges.includes(keyAgeRange)) {
                let femVal = selected_oa_dataset[typePrefix + " - " + "Females" + " - " + keyAgeRange]
                let malVal = selected_oa_dataset[typePrefix + " - " + "Males" + " - " + keyAgeRange]
                rows.push([keyAgeRange, parseFloat(femVal), parseFloat(malVal)])
                seenAgeRanges.push(keyAgeRange)
            }
        }

        chartData.addColumn('string', 'Age range');
        chartData.addColumn('number', "Female");
        chartData.addColumn('number', "Male");
        chartData.addRows(rows)

        chartTitle = "Column chart: " + typePrefix + " - " + "by age range and gender in OA"
        chartLegend = { position: 'top'}
    }

    let options = {
        title: chartTitle,
        hAxis: {
            title: "Gender by age range",
            maxAlternation: 0
        },
        vAxis: {
            title: ((LOGARITHMIC_SCALE) ? "Value (logarithmic axis)" : "Value"),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null')
        },
        // backgroundColor: '#f1f8e9',
        legend: chartLegend,
        height: "100%",
        width: "100%"
    };

    let chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(chartData, options);
}

function ageGenderGenderTotalsSelectedOA() {
    let selected_oa_dataset = SELECTED_OA.getProperty(SELECTED_DATASET)
    let femaleVal = parseFloat(selected_oa_dataset["Females total"])
    let maleVal = parseFloat(selected_oa_dataset["Males total"])


    let data = google.visualization.arrayToDataTable([
        ['Gender', 'Value'],
        ['Female',     femaleVal],
        ['Male',      maleVal]
    ]);

    let total = femaleVal + maleVal

    let options = {
        title: "TOTAL: " + total + "\n\nDonut chart: Gender totals.",
        pieHole: 0.4,
        legend: {
            position: 'top',
            maxLines: 3
        }
    };

    let chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function spendingCategoriesCategoryComparisonSelectedOA(operationPrefix) {
    let selected_oa_dataset = SELECTED_OA.getProperty(SELECTED_DATASET)
    let datasetPrefixed = Object.fromEntries(Object.entries(selected_oa_dataset).filter(([key]) => key.split(" - ")[0] === operationPrefix))

    let data = new google.visualization.DataTable();

    let rows = []
    for (const entry of Object.entries(datasetPrefixed)) {
        let key = entry[0]
        let prettyKey = key.split(" - ")[1]
        let value = parseFloat(entry[1])
        rows.push([prettyKey, value])
    }

    data.addColumn('string', 'Category');
    data.addColumn('number', "Amount spent");
    data.addRows(rows)
    data.sort({column: 0, desc: false});

    let options = {
        title: "Column chart: Spending categories breakdown",
        hAxis: {
            title: "Category",
            maxAlternation: 0,
            showTextEvery: true,
            // textStyle: {fontSize: 7}
        },
        vAxis: {
            title: ((LOGARITHMIC_SCALE) ? "Value (logarithmic axis)" : "Value"),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null')
        },
        // backgroundColor: '#f1f8e9',
        legend: { position: 'none'},
        height: "100%",
        width: "100%",
        // fontSize: "5", // all fonts in the chart
    };

    let chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function disposableIncomeSpendingCategoriesCategoryComparisonSelectedOA(operationPrefix) {
    let selected_oa_dataset = SELECTED_OA.getProperty(SELECTED_DATASET)
    let datasetPrefixed = Object.fromEntries(Object.entries(selected_oa_dataset).filter(([key]) => key.split(" - ")[0] === operationPrefix))

    let data = new google.visualization.DataTable();

    let rows = []
    for (const entry of Object.entries(datasetPrefixed)) {
        let key = entry[0]
        let prettyKey = key.split(" - ")[1]
        let value = parseFloat(entry[1])
        rows.push([prettyKey, value])
    }

    data.addColumn('string', 'Category');
    data.addColumn('number', "Amount spent");
    data.addRows(rows)
    data.sort({column: 0, desc: false});

    let options = {
        title: "Column chart: Disposable income spending categories breakdown",
        hAxis: {
            title: "Category",
            maxAlternation: 0,
            showTextEvery: true,
            textStyle: {fontSize: 12}
        },
        vAxis: {
            title: ((LOGARITHMIC_SCALE) ? "Value (logarithmic axis)" : "Value"),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null')
        },
        // backgroundColor: '#f1f8e9',
        legend: { position: 'none'},
        height: "100%",
        width: "100%",
        // fontSize: "5", // all fonts in the chart
    };

    let chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function incomeBracketSelectedOA(operationPrefix) {
    let selected_oa_dataset = SELECTED_OA.getProperty(SELECTED_DATASET)
    let datasetPrefixed = Object.fromEntries(Object.entries(selected_oa_dataset).filter(([key]) => key.split(" - ")[0] === operationPrefix))

    let data = new google.visualization.DataTable();

    let rows = []
    for (const entry of Object.entries(datasetPrefixed)) {
        let key = entry[0]
        let prettyKey = key.split(" - ")[1]
        let value = parseFloat(entry[1])
        rows.push([prettyKey, value])
    }

    data.addColumn('string', 'Income range');
    data.addColumn('number', "Value");
    data.addRows(rows)

    let options = {
        title: "Column chart: Income ranges breakdown in OA",
        hAxis: {
            title: "Category",
            maxAlternation: 0,
            showTextEvery: true,
            // textStyle: {fontSize: 12},
            slantedTextAngle: 90
        },
        vAxis: {
            title: ((LOGARITHMIC_SCALE) ? "Value (logarithmic axis)" : "Value"),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null')
        },
        legend: { position: 'none'},
        height: "100%",
        width: "100%",
    };

    let chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

/*
POC Population demographic density estimation charts.
 */
function demographicTypeUnitsSelectedOAPieChart(prefix, unit) {
    let dataset = SELECTED_OA.getProperty(SELECTED_DATASET)

    let total = 0
    let rows = []
    for (const type of DEMO_TYPES) {
        let value = parseFloat(dataset[prefix + type + unit])
        rows.push([type, value])
        total = total + value
    }
    total = total.toFixed(3)

    let data = new google.visualization.DataTable();
    data.addColumn('string', 'Demographic type');
    data.addColumn('number', "Value");
    data.addRows(rows)

    let options = {
        title: "TOTAL: " + total + "\n\nDonut chart: Demographic types " + prefix + unit + " totals.",
        // pieHole: 0.4,
        legend: {
            position: 'top',
            maxLines: 3
        }
    };

    let chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function demographicTypeValueSelectedOAColumnChart(prefix, unit) {
    let dataset = SELECTED_OA.getProperty(SELECTED_DATASET)

    let total = 0
    let rows = []
    for (const type of DEMO_TYPES) {
        let value = parseFloat(dataset[prefix + type + unit])
        rows.push([type, value])
        total = total + value
    }
    total = total.toFixed(3)

    let data = new google.visualization.DataTable();
    data.addColumn('string', 'Demographic type');
    data.addColumn('number', "Value");
    data.addRows(rows)

    let options = {
        title: "TOTAL: " + total + "\n\nColumn chart: Demographic types " + prefix + unit + " totals.",
        hAxis: {
            title: "Category",
            maxAlternation: 0,
            showTextEvery: true,
        },
        vAxis: {
            title: ((LOGARITHMIC_SCALE) ? "Value (logarithmic axis)" : "Value"),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null'),
            viewWindow:{
                // max:100,
                min: 0
            }
        },
        legend: { position: 'none'},
        height: "100%",
        width: "100%",
    };

    let chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

/*
Total population.
 */
function populationDemographicTypeSelectedOAPieChart(prefix, unit) {
    let dataset = SELECTED_OA.getProperty(SELECTED_DATASET)

    let total = 0
    let rows = []

    let generalColumns = ["resident_count", "visitors_total_count"]

    if (SELECTED_COLUMN === prefix+"total_count") {
        for (const type of DEMO_TYPES.concat(["resident"])) {
            let value = parseFloat(dataset[prefix + type + unit])
            rows.push([type, value])
            total = total + value
        }
    } else if (generalColumns.includes(SELECTED_COLUMN.split(" - ")[1])) {
        for (const colName of generalColumns) {
            let value = parseFloat(dataset[prefix + colName])
            rows.push([colName, value])
            total = total + value
        }
    } else {
        for (const type of DEMO_TYPES) {
            let value = parseFloat(dataset[prefix + type + unit])
            rows.push([type, value])
            total = total + value
        }
    }

    total = total.toFixed(3)

    let data = new google.visualization.DataTable();
    data.addColumn('string', 'Demographic type');
    data.addColumn('number', "Value");
    data.addRows(rows)

    let options = {
        title: "TOTAL: " + total + "\n\nDonut chart: Demographic types " + prefix + unit + " totals.",
        // pieHole: 0.4,
        legend: {
            position: 'top',
            maxLines: 3
        }
    };

    let chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function populationDemographicTypeSelectedOAColumnChart(prefix, unit) {
    let dataset = SELECTED_OA.getProperty(SELECTED_DATASET)

    let total = 0
    let rows = []

    for (const type of DEMO_TYPES.concat(["resident"])) {
        let value = parseFloat(dataset[prefix + type + unit])
        rows.push([type, value])
        total = total + value
    }
    total = total.toFixed(3)

    let data = new google.visualization.DataTable();
    data.addColumn('string', 'Demographic type');
    data.addColumn('number', "Value");
    data.addRows(rows)

    let options = {
        title: "TOTAL: " + total + "\n\nColumn chart: Demographic types " + prefix + unit + " totals.",
        hAxis: {
            title: "Category",
            maxAlternation: 0,
            showTextEvery: true,
        },
        vAxis: {
            title: ((LOGARITHMIC_SCALE) ? "Value (logarithmic axis)" : "Value"),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null'),
            viewWindow:{
                // max:100,
                min: 0
            }
        },
        legend: { position: 'none'},
        height: "100%",
        width: "100%",
    };

    let chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

/*
Supply/demand.
 */
function supplyMinusDemandByPlaceType() {
    let dataset = SELECTED_OA.getProperty(SELECTED_DATASET)
    let rows = []

    let data = new google.visualization.DataTable();
    data.addColumn('string', 'Place');

    if (SELECTED_COLUMN.split("] - ")[2].includes("total")) {
        for (const place of ["bar", "cafe", "restaurant"]) {
            let demoValues = []
            for (const demo of ["resident", "visitors_total", "total"]) {
                let key = place + "_" + demo
                let value = parseFloat(dataset["[supply - demand] - [normalized_[0-1]_proportions] - " + key])
                demoValues.push(value)
            }
            rows.push([place].concat(demoValues))
        }

        data.addColumn('number', 'resident');
        data.addColumn('number', 'visitors_total');
        data.addColumn('number', 'total');
    } else {
        for (const place of ["bar", "cafe", "restaurant"]) {
            let demoValues = []
            for (const demo of DEMO_TYPES.concat(["resident"])) {
                let key = place + "_" + demo
                let value = parseFloat(dataset["[supply - demand] - [normalized_[0-1]_proportions] - " + key])
                demoValues.push(value)
            }
            rows.push([place].concat(demoValues))
        }

        data.addColumn('number', 'worker');
        data.addColumn('number', 'student');
        data.addColumn('number', 'shopper');
        data.addColumn('number', 'tourist');
        data.addColumn('number', 'leisurer');
        data.addColumn('number', 'chorer');
        data.addColumn('number', 'resident');
    }

    data.addRows(rows)

    let options = {
        title: "Column chart: Supply - Demand distribution breakdown.",
        hAxis: {
            title: ((LOGARITHMIC_SCALE) ? "Supply dist. - Demand dist. (logarithmic axis)" : "Supply dist. - Demand dist."),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null'),
            viewWindow:{
                // max:100,
                // min: 0
            }
        },
        vAxis: {
            title: "Place type",
            maxAlternation: 0,
            showTextEvery: true,
        },
        legend: {
            position: 'top',
            maxLines: 3
        },
        height: "100%",
        width: "100%",
    };

    let chart = new google.visualization.BarChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function supplyDemandIndexScoreByPlaceType() {
    let dataset = SELECTED_OA.getProperty(SELECTED_DATASET)
    let rows = []

    let data = new google.visualization.DataTable();
    data.addColumn('string', 'Place');

    if (SELECTED_COLUMN.split("] - ")[1].includes("total")) {
        for (const place of ["bar", "cafe", "restaurant"]) {
            let demoValues = []
            for (const demo of ["resident", "visitors_total", "total"]) {
                let key = place + "_" + demo
                let value = parseFloat(dataset["[supply_demand_index] - " + key])
                demoValues.push(value)
            }
            rows.push([place].concat(demoValues))
        }

        data.addColumn('number', 'resident');
        data.addColumn('number', 'visitors_total');
        data.addColumn('number', 'total');
    } else {
        for (const place of ["bar", "cafe", "restaurant"]) {
            let demoValues = []
            for (const demo of DEMO_TYPES.concat(["resident"])) {
                let key = place + "_" + demo
                let value = parseFloat(dataset["[supply_demand_index] - " + key])
                demoValues.push(value)
            }
            rows.push([place].concat(demoValues))
        }

        data.addColumn('number', 'worker');
        data.addColumn('number', 'student');
        data.addColumn('number', 'shopper');
        data.addColumn('number', 'tourist');
        data.addColumn('number', 'leisurer');
        data.addColumn('number', 'chorer');
        data.addColumn('number', 'resident');
    }

    data.addRows(rows)

    let options = {
        title: "Column chart: Supply & Demand index breakdown.",
        hAxis: {
            title: "Place type",
            maxAlternation: 0,
            showTextEvery: true,
        },
        vAxis: {
            title: ((LOGARITHMIC_SCALE) ? "Supply & demand index. (logarithmic axis)" : "Supply & demand index"),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null'),
            viewWindow:{
                // max:100,
                // min: 0
            }
        },
        legend: {
            position: 'top',
            maxLines: 3
        },
        height: "100%",
        width: "100%",
    };

    let chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

/*
General selections. No OA.
 */
function numericColumnHistogram(columnName) {
    let total = 0.0
    let rows = []
    for (const oa of DATA) {
        let properties = oa["properties"][SELECTED_DATASET]
        let floatValue = parseFloat(properties[columnName])
        rows.push([properties["OA"], floatValue])
        total = total + floatValue
    }
    total = total.toFixed(3)

    let data = new google.visualization.DataTable();
    data.addColumn('string', 'Value');
    data.addColumn('number', columnName);
    data.addRows(rows)
    data.sort({column: 0, desc: false});

    let options = {
        title: "COLUMN TOTAL: " + total + "\n\nHistogram: " + SELECTED_COLUMN + " distribution in borough.",
        hAxis: {
            title: columnName,
            maxAlternation: 0 // 1 also looks good.
        },
        vAxis: {
            title: ((LOGARITHMIC_SCALE) ? "Value (logarithmic axis)" : "Value"),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null')
        },
        // backgroundColor: '#f1f8e9',
        legend: {position: "none"},
        height: "100%",
        width: "100%",
        histogram: {}
    };

    // Set the length of the horizontal axis if the column has a shared scale.
    if (columnName.includes("[shared_scale]")) {
        let dom = SCALES_MAP.get(SELECTED_DATASET).get(columnName)
        let max_value = dom.domain()[dom.domain().length - 1]
        options.histogram = {
            maxValue: max_value
        }
    }

    let chart = new google.visualization.Histogram(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function categoricalColumnCountColumnChart(columnName) {
    let typeTally = new Map()
    for (const oa of DATA) {
        let properties = oa["properties"][SELECTED_DATASET]
        let type = properties[columnName]

        if (typeTally.has(type)) {
            let previousValue = typeTally.get(type)
            typeTally.set(type, previousValue + 1)
        } else {
            typeTally.set(type, 1)
        }
    }

    let rows = []
    for (const type of typeTally.keys()) {
        rows.push([type, typeTally.get(type)])
    }

    let data = new google.visualization.DataTable();
    data.addColumn('string', 'OA count');
    data.addColumn('number', columnName);
    data.addRows(rows)
    data.sort({column: 0, desc: false});

    let options = {
        title: "Column chart: " + SELECTED_COLUMN + " category count in borough",
        hAxis: {
            title: columnName,
            maxAlternation: 0
        },
        vAxis: {
            title: ((LOGARITHMIC_SCALE) ? "OA count (logarithmic axis)" : "OA count"),
            // Puts everything in a closer scope.
            scaleType: ((LOGARITHMIC_SCALE) ? 'mirrorLog' : 'null')
        },
        // backgroundColor: '#f1f8e9',
        legend: {position: "none"},
        height: "100%",
        width: "100%"
    };
    let chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}
