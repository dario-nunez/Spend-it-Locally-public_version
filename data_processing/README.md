# Data processing

A Data Science pipeline that generates datasets to be visualized by the user interface Javascript project.

## Project file structure

The lines labelled (F) indicate a folder containing one or more data files.

```
data_processing
|    data
|    |    focused_data
|    |    |    acorn (F)
|    |    |    authorities (F)
|    |    |    geodata (F)
|    |    |    places_types (F)
|    |    |    places (F)
|    |    processed_data
|    |    |    acorn (F)
|    |    |    acorn_backup (F)
|    |    |    demographic_distributions (F)
|    |    |    normalizers (F)
|    |    |    places (F)
|    |    |    placing_places (F)
|    |    |    survey (F)
|    |    |    tabular_metadata (F)
|    |    raw_data
|    |    |    acorn (F)
|    |    |    authorities (F)
|    |    |    city_survey (F)
|    |    |    geodata (F)
|    |    |    places_types (F)
|    |    |    places (F)
|    src
|    |    focused_data
|    |    |    acorn.py
|    |    |    api.py
|    |    |    authorities.py
|    |    |    geodata.py
|    |    |    places_types.py
|    |    |    places.py
|    |    |    polygons.py
|    |    |    run_focused.py
|    |    |    run_scrape_places.py
|    |    processed_data
|    |    |    acorn.py
|    |    |    normalizers.py
|    |    |    places_demos_dists.py
|    |    |    places.py
|    |    |    placing_places.py
|    |    |    population.py
|    |    |    run_processed.py
|    |    |    tabular_metadata.py
|    common.py
|    README.md
```
