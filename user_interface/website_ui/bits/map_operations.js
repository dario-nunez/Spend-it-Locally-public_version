/*
This file defines operations that do work on the Google Maps window map. Color overlay application, mouse event handling
and initialization.
 */

// Map realigned settings.
const initialZoom = 13
const optimalZoom = 13.7
const centerLat = 51.51100
const centerLng = -0.16337

// OA hover style.
const style_hover = {
    strokeWeight: 3,
    strokeColor: "#000000",
    fillColor: "#000000",
}

// OA clicked style.
const style_clicked = {
    strokeWeight: 3,
    strokeColor: "#a815ff",
    fillColor: "#a815ff",
}

// OA hovered and clicked style.
const style_hover_clicked = {
    strokeWeight: 3,
    strokeColor: "#5f0c90",
    fillColor: "#5f0c90",
}

let previously_clicked_oa;

/*
Default style that coloring all OAs in dark green with black borders. Applied as the default overlay.
 */
function styleDefault(feature) {
    let fill_col = "green";
    let outlineWeight = 0.5, zIndex = 1;

    if (feature['state'] === 'hover') {
        outlineWeight = zIndex = 2;
    }

    if (feature['state_clicked'] === 'on') {
        outlineWeight = zIndex = 2;
        fill_col = style_clicked.fillColor
    }

    return {
        strokeWeight: outlineWeight,
        strokeColor: borderColor,
        strokeOpacity: OPACITY,
        zIndex: zIndex,
        fillColor: fill_col,
        fillOpacity: OPACITY,
    };
}

/*
Style applied to the map when a column of type numeric continuous is selected. It uses the blue-turquoise-green-yellow-red
continuous scale in the legend.
 */
function styleContinuous(feature) {
    let dom = SCALES_MAP.get(SELECTED_DATASET).get(SELECTED_COLUMN)
    let min_value = dom.domain()[0]
    let max_value = dom.domain()[dom.domain().length - 1]

    let low = continuousLinearLow;  // color of smallest datum
    let high = continuousLinearHigh;   // color of largest datum

    let dataValue = feature.getProperty(SELECTED_DATASET)[SELECTED_COLUMN]

    // delta represents where the value sits between the min and max
    let delta = (dataValue - min_value) / (max_value - min_value);

    let color = [];
    for (let i = 0; i < 3; i++) {
        // calculate an integer color based on the delta
        color[i] = (high[i] - low[i]) * delta + low[i];
    }

    // determine whether to show this shape or not
    let showRow = true;

    let fill_col = 'hsl(' + color[0] + ',' + color[1] + '%,' + color[2] + '%)'

    let outlineWeight = 0.5, zIndex = 1;
    if (feature['state'] === 'hover') {
        outlineWeight = zIndex = 2;
    }

    if (feature['state_clicked'] === 'on') {
        outlineWeight = zIndex = 2;
        fill_col = style_clicked.fillColor
    }

    return {
        strokeWeight: outlineWeight,
        strokeColor: borderColor,
        strokeOpacity: OPACITY,
        zIndex: zIndex,
        fillColor: fill_col,
        fillOpacity: OPACITY,
        visible: showRow
    };
}

/*
Style applied to the map whenever a categorical typed column is selected. Colors depend on the OA values and their respective
color mappings.
 */
function styleCategorical(feature) {
    let cat_col_scale = SCALES_MAP.get(SELECTED_DATASET).get(SELECTED_COLUMN)
    let dataValue = feature.getProperty(SELECTED_DATASET)[SELECTED_COLUMN]

    let fill_col = cat_col_scale(dataValue)

    let outlineWeight = 0.5, zIndex = 1;
    if (feature['state'] === 'hover') {
        outlineWeight = zIndex = 2;
    }

    if (feature['state_clicked'] === 'on') {
        outlineWeight = zIndex = 2;
        fill_col = style_clicked.fillColor
    }

    return {
        strokeWeight: outlineWeight,
        strokeColor: borderColor,
        strokeOpacity: OPACITY,
        zIndex: zIndex,
        fillColor: fill_col,
        fillOpacity: OPACITY,
        visible: true
    };
}

/*
Initializes the Google Maps map object and sets some style settings.
 */
function initializeMap() {
    return new google.maps.Map(document.getElementById("map"), {
        mapTypeId: "terrain",
        zoom: initialZoom,
        minZoom: initialZoom,
        // maxZoom: initialZoom + 4,
        center: {lat: centerLat, lng: centerLng},
        restriction: {
            latLngBounds: {
                north: centerLat + 0.04,
                south: centerLat - 0.04,
                east: centerLng + 0.09,
                west: centerLng - 0.09,
            },
        },
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        }
    });
}

/*
Populates the map with the geojson boundary data and applies the default style.
 */
function populateMap(map, data) {
    map.data.addGeoJson(data);

    // This sets the default style, called every time style methods are called.
    map.data.setStyle(function(feature) {
        let color = "green";
        let strokeWeight = 1;
        let strokeColor = "black"

        if (feature["state_clicked"] === "on") {
            color = style_clicked.fillColor
            strokeWeight = style_clicked.strokeWeight
            strokeColor = style_clicked.strokeColor
        }

        return ({
            fillColor: color,
            strokeWeight: strokeWeight,
            strokeColor: strokeColor,
            strokeOpacity: OPACITY,
            fillOpacity: OPACITY,
        })
    })
}

/*
Centers the map positioning and fits the map zoom using the predefined properties.
 */
function setCenterAndZoom() {
    map.setCenter({lat: centerLat, lng: centerLng})
    map.setZoom(optimalZoom)
}

/*
Handle the mouse hover in event over the OA polygons in the map. Change the appearance of the polygons to reflect a hovering
selection and if a numeric column is selected, update the value indicator in the legend.
 */
function addMouseoverOaEvent(map) {
    map.data.addListener('mouseover', function(e) {
        let feat = e.feature
        map.data.revertStyle();

        // Apply hovering style.
        if (feat["state_clicked"] !== undefined && feat["state_clicked"] === "on") {
            map.data.overrideStyle(feat, style_hover_clicked);
        } else {
            map.data.overrideStyle(feat, style_hover);
        }

        feat["state"] = "hover";

        let key = feat.getProperty("geo_code");
        let value = "undenfined"

        // Update the value indicator in the continuous legend. No defined action for the categorical legend.
        if (SELECTED_DATASET !== "none" && SELECTED_COLUMN !== "blank") {
            let feat_dataset = feat.getProperty(SELECTED_DATASET)
            key = feat_dataset['OA'];
            value = feat_dataset[SELECTED_COLUMN].toLocaleString();

            let dom = SCALES_MAP.get(SELECTED_DATASET).get(SELECTED_COLUMN).domain()

            if (typeof(dom[0]) === "string") {
                // Maybe highlight OAs of the same category.
            } else {
                let legend_body = document.getElementById("legend");
                legend_body.innerHTML = ""

                let min_div = document.createElement("div")
                min_div.id = "census-min"
                min_div.classList.add("legend_text")
                min_div.textContent = "min"
                legend_body.appendChild(min_div)

                let color_key_div = document.createElement("div")
                color_key_div.classList.add("color-key")
                const span = document.createElement("span")
                span.id = "data-caret"
                span.classList.add("legend_text")
                span.textContent = "◆"
                color_key_div.appendChild(span)
                legend_body.appendChild(color_key_div)

                let max_div = document.createElement("div")
                max_div.id = "census-max"
                max_div.classList.add("legend_text")
                max_div.textContent = "max"
                legend_body.appendChild(max_div)

                // Update continuous legend's min and max with the new selected column
                let min_value = (dom[0]).toFixed(3)
                let max_value = (dom[dom.length - 1]).toFixed(3)

                document.getElementById('census-min').textContent = min_value;
                document.getElementById('census-max').textContent = max_value;
                let percent = (feat_dataset[SELECTED_COLUMN] - min_value) / (max_value - min_value) * 100;
                document.getElementById('data-caret').style.paddingLeft = percent + '%';
            }
        }

        document.getElementById('data-label').textContent = key;
        document.getElementById('data-value').textContent = value;
    });
}

/*
Handles the mouse hover out event over OA polygons. Return the hovered polygon back to its previous state.
 */
function addMouseoutOaEvent(map) {
    map.data.addListener('mouseout', function(e) {
        let feat = e.feature
        map.data.revertStyle();

        let key = "unhovered";
        let value = "undenfined"

        feat["state"] = "normal";

        document.getElementById('data-label').textContent = key;
        document.getElementById('data-value').textContent = value;
    });
}

/*
Handles the click event on OA polygons in the map. Clicks toggle the selection of a single OA. A click triggers a change
in the appearance of the polygon and the rendering of any associated auxiliary visualizations.
 */
function addMouseclickOaEvent(map) {
    map.data.addListener('click', function(e) {
        let newly_selected_oa = e.feature

        let key = newly_selected_oa.getProperty("geo_code");
        let value = "undenfined"

        if (newly_selected_oa === SELECTED_OA) {
            // OFF
            SELECTED_OA = null
            newly_selected_oa["state_clicked"] = "off";
            key = "unclicked"
        } else {
            // ON

            // Set SELECTED_OA to off
            if (SELECTED_OA !== null) {
                SELECTED_OA["state_clicked"] = "off";
                map.data.revertStyle(previously_clicked_oa);
            }

            SELECTED_OA = newly_selected_oa
            newly_selected_oa["state_clicked"] = "on";

            if (SELECTED_DATASET !== "none" && SELECTED_COLUMN !== "blank") {
                let feat_dataset = newly_selected_oa.getProperty(SELECTED_DATASET)
                key = feat_dataset['OA'];
                value = feat_dataset[SELECTED_COLUMN].toLocaleString();
            }
        }

        document.getElementById('data-label-clicked').textContent = key;
        document.getElementById('data-value-clicked').textContent = value;

        visualize()

        if (SELECTED_OA !== null) {
            previously_clicked_oa = newly_selected_oa
        }
    });
}
