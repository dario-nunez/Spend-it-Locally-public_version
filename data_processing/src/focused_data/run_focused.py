"""Run focused script.

Runs all the scripts in the "focused_data" subdirectory and generates all focused
datasets (some are places in the raw subdirectory). The scripts are run in a specific
sequential order to suffice dependencies. The "run_scrape_palces.py" script is an 
exception. Due to its long running time and potential monetary costs, it requires
manual triggering.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(PROJECT_ROOT)
import src.focused_data.authorities as authorities
import src.focused_data.geodata as geodata
import src.focused_data.polygons as polygons
import src.focused_data.place_types as place_types
import src.focused_data.places as places

################################################################################
# Constants.
################################################################################

DATA_DIR = "/data/"

################################################################################
# Sequential execution.
################################################################################

# authorities.focus_authorities(DATA_DIR)
# geodata.focus_geodata(DATA_DIR)
# polygons.focus_polygons(DATA_DIR) # very slow
# places.process_places(DATA_DIR)   # slow
place_types.process_place_types(DATA_DIR)
