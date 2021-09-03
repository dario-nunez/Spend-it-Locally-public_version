# Data visualization & User interface

A Javascript application used to interact with and visualize the data generated in the data processing Python project. The main visualization method is an interactive choropleth map of Westminster segmented into Output Areas (OAs). Auxiliary visualizations are also available for all dataset-column combinations. These include variants of data tables, histograms, bar charts and pie charts. 

## Project file structure

The lines labelled (F) indicate a folder containing one or more data files.

```
user_interface
|    website_ui
|    |    bits
|    |    |    auxiliaryVisualizationMapping.js
|    |    |    auxiliaryVisualizationDario.js
|    |    |    dropdownMenu.js
|    |    |    generateScales.js
|    |    |    load_and_process_data.js
|    |    |    map_operations.js
|    |    |    projectColours.js
|    |    |    state.js
|    |    credentials
|    |    |    google_maps_api_credentials.js
|    |    data (F)
|    |    index.html
|    |    index.js
|    |    styles.css
|    common.py
|    README.md
```
