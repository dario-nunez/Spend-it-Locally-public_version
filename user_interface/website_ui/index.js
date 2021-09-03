/*
This file handles the loading of necessary scripts, the initialization of components in the page and the handling of the
button click events.
 */

// Google maps MAPS API loading script.
let scriptPlaces = document.createElement('script');
scriptPlaces.src = "https://maps.googleapis.com/maps/api/js?key=" + apiKey + "&libraries=places&callback=initMap";
scriptPlaces.async = true;
document.head.appendChild(scriptPlaces);

/*
Initialize all the interactive components in the page.
Create a Google Maps window object, load the data, populate the map
with the geographical boundary data, add mouse events to the map, initialize the dropdowns and initialize the auxiliary
visualizations div.
 */
window.initMap = function () {
    map = initializeMap()
    new google.maps.InfoWindow();

    const legend = document.getElementById("categorical_legend");
    map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(legend);

    loadAndProcessData().then(data => {
        populateMap(map, data)
        addMouseoverOaEvent(map)
        addMouseoutOaEvent(map)
        addMouseclickOaEvent(map)
        renderDropdowns()
        visualize()
    });
};

/*
Handler for the "Realign map" button.
Resets the maps' view position and zoom.
 */
function resetMapView() {
    setCenterAndZoom()
}

/*
Handler for the "Toggle map labels" button.
Apply style settings to the map to remove all visual features except landscape and geometry.
 */
function toggleMapLabels() {
    newStyles = [
        {
            'featureType': 'all',
            'elementType': 'all',
            'stylers': [{'visibility': 'off'}]
        },
        {
            'featureType': 'landscape',
            'elementType': 'geometry',
            'stylers': [{'visibility': 'on'}, {'color': '#fcfcfc'}]
        },
        {
            'featureType': 'water',
            'elementType': 'labels',
            'stylers': [{'visibility': 'off'}]
        },
        {
            'featureType': 'water',
            'elementType': 'geometry',
            'stylers': [{'visibility': 'on'}, {'hue': '#5f94ff'}, {'lightness': 60}]
        }
    ];

    if (MAP_LABELS_ON) {
        map.setOptions({styles: []})
        MAP_LABELS_ON = false
    } else {
        map.setOptions({styles: newStyles})
        MAP_LABELS_ON = true
    }
}

/*
Handler for the "Toggle opacity" button.
Toggles the OPACITY global to change how see through the map overlay is.
 */
function toggleOpacity() {
    if (OPACITY === HIGH_OPACITY) {
        OPACITY = LOW_OPACITY
    } else {
        OPACITY = HIGH_OPACITY
    }

    if (SELECTED_COLUMN === "blank") {
        map.data.setStyle(styleDefault);
    } else {
        let dom = SCALES_MAP.get(SELECTED_DATASET).get(SELECTED_COLUMN).domain()
        if (typeof(dom[0]) === "string") {
            map.data.setStyle(styleCategorical);
        } else {
            map.data.setStyle(styleContinuous);
        }
    }
}

/*
Handler for the "Toggle log scale" button.
Applies a logarithmic scale to the current auxiliary visualization (if it supports it).
 */
function toggleLogScale() {
    LOGARITHMIC_SCALE = !LOGARITHMIC_SCALE;
    visualize();
}
