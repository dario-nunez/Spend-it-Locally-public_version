"""Google Maps Places API data mining.

Scrapes Google Maps Places data by OA from the Place API. Due to the restrictions
on the API limiting response size, the search area for each OA is broken down into
many small searchable units. The responses are also filtered to only retain desired
information. The result of each OA query is stored in a separate file in the /raw
data subdirectory to enforce an implicit backup progress system.

Input datasets:
- None (Google Maps Places API)

Output datasets:
- 783 files stored in "raw_data/places"

IMPORTANT, MUST READ!
- Due to API response time restrictions, the mining process is very lengthy if done
sequentially. To alleviate this issue, the handling of the 783 OAs is split accross
threads (in this case 100). This reduces mining time from days to around 40 minutes.
- When the multi-threaded approach is run, a large volume of requests is submitted
to the Places API. Their frequency decreases as the execution nears the end. This
mining method consumes API resources rapidly and this results in monetary charges
by Google Developer Console.
- A full 783 OA mine costs around $300 (taking into account the other mining parameters
used in this script).
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(PROJECT_ROOT)
from api import api_key
import googlemaps
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import json
import math
import multiprocessing
import time
import src.common as common

################################################################################
# Globals.
################################################################################

INPUT_DATA_DIR = common.CWD + "/data/focused_data/" + "geodata/"
OUTPUT_DATA_DIR =  common.CWD + "/data/focused_data/" + "places/"
GMAPS = googlemaps.Client(key=api_key)
geo_file = "OAs_influence_area.csv"

fieldsToKeep = ["geometry", "name", "place_id", "types", "rating", "user_ratings_total"]
files_dir = OUTPUT_DATA_DIR[:len(OUTPUT_DATA_DIR)-1]
onlyfiles = [f for f in listdir(files_dir) if isfile(join(files_dir, f))]
existingOAs = [x[:9] for x in onlyfiles] # Skip mining existing OAs.
OAs_counter = 1

lat_unit_length = 0.0010810912550027751
lng_unit_length = 0.0017325629696289258
unit_radius_meters = 60
buffer_size = 1

################################################################################
# Functions.
################################################################################

# Executer method. As a precaution, the single threaded mine mode is default.
def scrape_places():
    gdf = pd.read_csv(INPUT_DATA_DIR + geo_file)
    no_threads = 100
    gdfs = np.array_split(gdf, no_threads)
    single_thread_mine(gdfs) # runs in TOO MANY seconds.
    # multi_thread_mine(gdfs, no_threads) # runs in around 40 minutes.

# A single threadable operation.
def do_work(gdf):
    gdf.apply(lambda x: getNearbyPlaces(x), axis=1)

# Filters results by containment in the OA influence area and also results fields
# by their name (desired fields specified in a global variable)
def filterFields(x, search_area):
    out = {}
    x_lat = x["geometry"]["location"]["lat"]
    x_lng = x["geometry"]["location"]["lng"]

    if (x_lat >= search_area["lat_min"] and x_lat <= search_area["lat_max"]):
        if (x_lng >= search_area["lng_min"] and x_lng <= search_area["lng_max"]):
            for f in fieldsToKeep:
                if f in x:
                    out[f] = x[f]

    return out

# Runs a raw response through the fields filter and returns a well-formed object.
def filterResults(places_nearby, search_area):
    response_json = json.dumps(places_nearby)    
    response_results = json.loads(response_json)["results"]
    filtered_results = [filterFields(x, search_area) for x in response_results if filterFields(x, search_area)]
    return filtered_results

# Given the "polygon_bounds" field of an OA, it segments it into searchable units
# of roughly 100 meters squared. These units are computed as squares and later converted
# to a collection of overlapping circles. The Google Maps Places API for Python is
# only capable of submitting radius requests, not square bound requests.
def generateSearchableUnits(row):
    poly_bounds = json.loads(row["polygon_bounds"])
    lat_buffer = lat_unit_length * buffer_size
    lng_buffer = lng_unit_length * buffer_size

    # True search area.
    lat_max = poly_bounds["lat_max"] + lat_buffer
    lat_min = poly_bounds["lat_min"] - lat_buffer
    lng_max = poly_bounds["lng_max"] + lng_buffer
    lng_min = poly_bounds["lng_min"] - lng_buffer
    search_area = {"lng_min":lng_min, "lat_min":lat_min, "lng_max":lng_max, "lat_max":lat_max}

    lat_range = lat_max - lat_min
    lng_range = lng_max - lng_min

    units_in_lng_axis = math.ceil(lng_range / lng_buffer)
    units_in_lat_axis = math.ceil(lat_range / lat_buffer)

    # Generate circles.
    in_square_circles = []
    in_between_square_circles = []

    # In square circles.
    for lng in range(0, units_in_lng_axis):
        for lat in range(0, units_in_lat_axis):
            new_lng_max = lng_max - (lng_unit_length * lng)
            new_lat_max = lat_max - (lat_unit_length * lat)
            new_lng_min = new_lng_max - lng_unit_length
            new_lat_min = new_lat_max - lat_unit_length
            in_square_circles.append({"lat":((new_lat_max + new_lat_min)/2), "lng":((new_lng_max+new_lng_min)/2)})
    
    # In-between square circles.
    for lng in range(-1, units_in_lng_axis):
        for lat in range(0, units_in_lat_axis+1):
            new_lng_max = lng_max - (lng_unit_length * lng)
            new_lat_max = lat_max - (lat_unit_length * lat)
            new_lng_min = new_lng_max - lng_unit_length
            new_lat_min = new_lat_max - lat_unit_length
            in_between_square_circles.append({"lat":new_lat_max, "lng":new_lng_min})

    circles = in_square_circles + in_between_square_circles
    return (search_area, circles)

# For each OA: generate searchable units, mine each one, and combine the results
# in a JSON file (ensuring no repeated entries are present).
def getNearbyPlaces(row):
    oa_name = row["geo_code"]

    global OAs_counter
    print(f"Working on: {oa_name}")

    # Avoid mining already mined OAs.
    if oa_name in existingOAs:
        print(f"- Already explored - {OAs_counter}/782 - {round((OAs_counter/782) * 100, 2)}%")
        print(f"Total number of unique results = ## - {OAs_counter}/782 - {round((OAs_counter/782) * 100, 2)}%")
        OAs_counter = OAs_counter + 1
        return

    print("- ", end="")
    existingOAs.append(oa_name)

    # Generate and mine searchable units.
    search_area, circles = generateSearchableUnits(row)
    oa_results = {oa_name:[]}
    
    for ci in range(len(circles)):
        c = circles[ci]
        location = (c["lat"], c["lng"])

        places_nearby = GMAPS.places_nearby(
            location = location,    # (lat,lng)
            radius = unit_radius_meters
        )

        filtered_results = filterResults(places_nearby, search_area)

        while "next_page_token" in places_nearby:
            time.sleep(2) # it does not work with 1 second!!!
            next_page_token = places_nearby["next_page_token"]
            places_nearby = GMAPS.places_nearby(
                location = location,
                radius = unit_radius_meters,
                page_token = next_page_token
            )
            new_filtered_results = filterResults(places_nearby, search_area)
            filtered_results = filtered_results + new_filtered_results

        print(f"{ci}-{len(filtered_results)}", end=" ", flush=True)
        oa_results[oa_name] = oa_results[oa_name] + filtered_results

    # Ensure all places results associated with an OA are unique.
    print()
    temp_dict = {}
    for place in oa_results[oa_name]:
        if place:
            id = place["place_id"]
            temp_dict[id] = place
    oa_results[oa_name] = temp_dict

    # Write results to file. Out of 783 OAs but since count starts at 0 max is 782.
    print(f"Total number of unique results = {len(oa_results[oa_name])} - {OAs_counter}/782 - {round((OAs_counter/782) * 100, 2)}%")
    output_json = json.dumps(oa_results)
    common.save_json_to_file(OUTPUT_DATA_DIR, output_json, f"{oa_name}_places.json")
    OAs_counter = OAs_counter + 1

# Single threaded mining procedure. 
def single_thread_mine(gdfs):
    start = time.time()
    for gdf in gdfs:
        do_work(gdf)
    end = time.time()
    print(end - start)

# Multi threaded mining procedure.
def multi_thread_mine(gdfs, no_threads):
    start = time.time()
    threads = no_threads

    jobs = []
    for i in range(0, threads):
        thread = multiprocessing.Process(target=do_work, args=(gdfs[i],))
        jobs.append(thread)

    print("Threads: ",len(jobs))
    print(jobs)

    # Start the threads (i.e. calculate the random number lists)
    for j in jobs:
        j.start()

    # Ensure all of the threads have finished
    for j in jobs:
        j.join()

    end = time.time()
    print(end - start)

# Script executer.
scrape_places()
