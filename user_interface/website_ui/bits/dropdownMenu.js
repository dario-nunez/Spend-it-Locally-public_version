/*
This file handles the creation, event processing and updating of the dataset and column selection dropdown menus.
 */

/*
Create a reusable template dropdown menu component.
 */
const dropdownMenu = (selection, props) => {
    const {
        options,
        onOptionClicked,
        selectedOption
    } = props;

    let select = selection.selectAll('select').data([null]);
    select = select.enter().append('select')
        .merge(select)
        .on('change', function() {
            onOptionClicked(this.value);
        });

    const option = select.selectAll('option').data(options);
    option.enter()
        .append('option')
        .merge(option)
        .attr('value', d => d)
        .attr("class", "dropDownText")
        .property('selected', d => d === selectedOption)
        .text(d => d);

    option.exit()
        .remove();
};

/*
Handles the click event on the column selection drop down menu.
It triggers a re-rendering of the dropdowns to acknowledge the new selection, renders any corresponding auxiliary visualizations
and updates the contents of the scale div (continuous or categorical) according to the type of the selected column.
 */
let onColumnDropdownClicked = column => {
    SELECTED_COLUMN = column;
    renderDropdowns();
    visualize();

    let legend_body = document.getElementById("legend");

    if (SELECTED_COLUMN === "blank") {
        map.data.setStyle(styleDefault);
        const legend_body = document.getElementById("legend");
        legend_body.innerHTML = ""
    } else {
        let dom = SCALES_MAP.get(SELECTED_DATASET).get(SELECTED_COLUMN).domain()

        if (typeof(dom[0]) === "string") {
            // Categorical columns
            map.data.setStyle(styleCategorical);
            let cat_col_scale = SCALES_MAP.get(SELECTED_DATASET).get(SELECTED_COLUMN)

            let icons = [];
            for (const dom_el of cat_col_scale.domain()) {
                icons.push({
                    name: dom_el,
                    color: cat_col_scale(dom_el)
                });
            }

            const legend_body = document.getElementById("legend");
            legend_body.innerHTML = ""
            let outer_div = document.createElement("div")
            outer_div.style.overflow = "auto"
            outer_div.style.maxHeight = "80px"

            for (const icon of icons) {
                const name = icon["name"];
                const color = icon["color"];
                const span = document.createElement("span")
                span.classList.add("badge")
                span.classList.add("mr-1")
                span.classList.add("mt-1")
                span.classList.add("legend_text")
                span.style.backgroundColor = color
                span.textContent = name
                outer_div.appendChild(span);
            }

            legend_body.appendChild(outer_div);
        } else {
            // Continuous columns
            map.data.setStyle(styleContinuous);
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
        }
    }
};

/*
Handles the click event on the dataset selection drop down menu.
Resets the column dropdown selector and renders any corresponding auxiliary visualizations.
 */
let onDatasetDropdownClicked = dataset => {
    SELECTED_DATASET = dataset;
    SELECTED_COLUMN = "blank";
    COLUMNS = Array.from(SCALES_MAP.get(SELECTED_DATASET).keys());
    renderDropdowns();
    visualize();

    let legend_body = document.getElementById("legend");

    if (SELECTED_DATASET === "none" && SELECTED_COLUMN === "blank") {
        map.data.setStyle(styleDefault);
        legend_body.innerHTML = ""
    }
};

/*
Updates the both dropdown menu components with a new selection and list of options.
 */
const renderDropdowns = () => {
    d3.select('#columnDropdown').call(dropdownMenu, {
        options: COLUMNS,
        onOptionClicked: onColumnDropdownClicked,
        selectedOption: SELECTED_COLUMN
    });

    d3.select('#datasetDropdown').call(dropdownMenu, {
        options: DATASETS,
        onOptionClicked: onDatasetDropdownClicked,
        selectedOption: SELECTED_DATASET
    });
}
