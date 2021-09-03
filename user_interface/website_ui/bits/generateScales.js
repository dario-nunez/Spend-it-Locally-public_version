/*
This file reads the "output_data_metadata" file and: populates the datasets list, generates the scales map, and the scales
labels map.
 */

const metadataPath = "data/output_data_metadata.json"
let continuousColumns = []

// Defines the default blank color scale.
const blankColorScale = d3.scaleThreshold()
    .domain(["blank"])
    .range([blankPathFill]);

/*
Based on the information in the metadata file about each column in each dataset, generate a d3 ordinal or linear scale that
contains the column's range and any relevant color mappings. Also generate a label map that can be used to convert between
equivalent categorical values.
 */
d3.json(metadataPath).then(data => {
    let keys = Object.keys(data)

    // For each dataset k.
    keys.forEach(k => {
        DATASETS.push(k)
        let inColumns = data[k]["column_data"]

        // For each column c.
        let columnMap = new Map()
        inColumns.forEach(c => {
            let scale;

            if (c["type_practical"] === "string") {
                // Categorical scale.
                scale = d3.scaleOrdinal()
                    .domain(c["range"])
                    .range(d3.schemePaired)
                    .unknown(blankPathFill);
            } else if (c["type_practical"] === "number_int" || c["type_practical"] === "number_float"){
                // Numeric continuous scale.
                scale = d3.scaleLinear()
                    .domain([c["min"], c["max"]])
                    .range([continuousLinearLow, continuousLinearHigh])
                    .unknown(blankPathFill);
                continuousColumns.push(c["name"])
            } else {
                // Categorical scale that requires specific color mappings. Taken from the project colors.
                let at = c["type_practical"][0]
                let as = c["type_practical"][1]

                // If there is no defined colour mapping.
                if (colourMappingsSimple[at][as] === undefined){
                    scale = d3.scaleOrdinal()
                        .domain(c["range"])
                        .range(d3.schemePaired)
                        .unknown(blankPathFill);
                } else {
                    let colourRange = c["range"].map(x => colourMappingsSimple[at][as][x]["colour"])
                    let labelRange = c["range"].map(x => colourMappingsSimple[at][as][x]["name"])

                    scale = d3.scaleOrdinal()
                        .domain(c["range"])
                        .range(colourRange)
                        .unknown(blankPathFill);

                    SCALES_LABEL_MAP.set(c["name"], labelRange)
                }
            }

            columnMap.set(c["name"], scale)
        })

        columnMap.set("blank", blankColorScale)
        SCALES_MAP.set(k, columnMap)
    })

    let noneDataset = new Map()
    noneDataset.set("blank", blankColorScale)
    SCALES_MAP.set("none", noneDataset)

    console.log("Scales map:")
    console.log(SCALES_MAP)
    console.log("Labels map:")
    console.log(SCALES_LABEL_MAP)
})