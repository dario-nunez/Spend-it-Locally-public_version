"""Run processed script.

Runs all the scripts in the "processed_data" subdirectory and generates all processed
datasets. It is recommended to only run sub scripts that will perform an effective
data update, due to occasional long running times.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(PROJECT_ROOT)
import src.processed_data.acorn as acorn
import src.processed_data.tabular_metadata as tabular_metadata
import src.processed_data.places as places
import src.processed_data.places_demos_dists as places_demos_dists
import src.processed_data.normalizers as normalizers
import src.processed_data.placing_places as placing_places
import src.processed_data.population as population

################################################################################
# Constants.
################################################################################

DATA_DIR = "/data/"

################################################################################
# Sequential execution.
################################################################################

# normalizers.process_normalizers(DATA_DIR)
# acorn.process_acorn(DATA_DIR)
# places.process_places(DATA_DIR)
places_demos_dists.process_places_demographic_densities(DATA_DIR)
population.process_population(DATA_DIR)
placing_places.process_placing_places(DATA_DIR)

tabular_metadata.process_tabular_metadata(DATA_DIR)
