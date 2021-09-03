"""OA polygon metadata.

Using the geodata for all the OAs in Westminster, it generates metadata about the
properties of each OA polygon. I.e. polygon area, centroid and bounds. This data
is used to generate normalization factors and define the influence or search area
for OAs when mining Google Maps Places API.

Input datasets:
- OAs_geojson_osgb36.json
- OAs_geojson_wgs84.json

Output datasets:
- OAs_influence_area.csv
"""

import src.common as common
import geopandas as gpd
import json
import geopy
import geopy.distance as distance
from shapely.geometry import Polygon

DATA_DIR = ""

# Executer method.
def focus_polygons(in_DATA_DIR):
    global DATA_DIR
    DATA_DIR = common.CWD + in_DATA_DIR
    process_geometadata()

# Load the geodata, apply operations to it, compile the new information and save.
def process_geometadata():
    # Load the file and clean it.
    geo_file_meters = "OAs_geojson_osgb36.json"    # Geojson in British coords. In meters.
    geo_file = "OAs_geojson_wgs84.json"     # Geojson in wgs84. Easier to handle. In degrees.
    gdf = gpd.read_file(DATA_DIR + "focused_data/geodata/" + geo_file)
    gdf = gdf.drop(["label", "name"], axis=1)

    # Get geometry information of the file in degrees.
    gdf["polygon_area_centroid"] = gdf["geometry"].apply(lambda x: get_centroid(x))
    gdf["polygon_area"] = gdf["geometry"].apply(lambda x: x.area)
    gdf["polygon_bounds"] = gdf["geometry"].apply(lambda x: calculate_bounds(x))
    gdf["axes_radius_degrees"] = gdf.apply(lambda x : calculate_axes_bound_radius(x), axis=1)
    gdf = gdf.drop(["geometry"], axis=1)

    # Get radius in meters by using the other file (in a different projection).
    gdf_meters = gpd.read_file(DATA_DIR + "focused_data/geodata/" + geo_file_meters)
    gdf_meters["polygon_area_centroid"] = gdf_meters["geometry"].apply(lambda x: get_centroid(x))
    gdf_meters["polygon_bounds"] = gdf_meters["geometry"].apply(lambda x: calculate_bounds(x))
    gdf_meters["axes_radius"] = gdf_meters.apply(lambda x : calculate_axes_bound_radius(x), axis=1)
    gdf_meters["polygon_area"] = gdf_meters["geometry"].apply(lambda x: x.area)
    gdf["polygon_area_meters"] = gdf_meters["polygon_area"]
    gdf["axes_radius_meters"] = gdf_meters["axes_radius"]
    gdf["axes_radius_meters_extended"] = gdf["axes_radius_meters"].apply(lambda x: calculate_axes_bound_radius_extended(x))

    # print(gdf.info())
    # print_dataframe_row_by_geo_code(gdf, "E00023945") # The long OA by the river.
    common.save_dataframe_to_csv(DATA_DIR + "focused_data/geodata/", gdf, "OAs_influence_area.csv")

# Return the centroid of a polygon in latitude and longitude components.
def get_centroid(x):
    centroid = x.centroid
    return json.dumps({"lat": centroid.y, "lng": centroid.x})

# Return the minimum and maximum coordinates of a polygon in the x and y axes.
def calculate_bounds(x):
    bounds = x.bounds
    minx = bounds[0]
    miny = bounds[1]
    maxx = bounds[2]
    maxy = bounds[3]
    return json.dumps({"lng_min":minx, "lat_min":miny, "lng_max":maxx, "lat_max":maxy})

# Return the maximum distance from a polygon's centroid to its x and y bounds.
def calculate_axes_bound_radius(x):
    centroid = json.loads(x["polygon_area_centroid"])
    bounds = json.loads(x["polygon_bounds"])

    lat_max_radius = max(abs(centroid["lat"] - bounds["lat_min"]), abs(centroid["lat"] - bounds["lat_max"]))
    lng_max_radius = max(abs(centroid["lng"] - bounds["lng_min"]), abs(centroid["lng"] - bounds["lng_max"]))

    return json.dumps({"lat":lat_max_radius, "lng":lng_max_radius})

# Return an extended maximum bounds of a polygon by 300 meters.
def calculate_axes_bound_radius_extended(x):
    radii = json.loads(x)
    extension_in_meters = 300
    return json.dumps({"lat":radii["lat"] + extension_in_meters, "lng":radii["lng"] + extension_in_meters})

# Return a square polygon that fully encapsulates an irregular polygon.
# Not currently in use but can be used for defining search areas explicitely.
def get_bounds_square(centroid, axes_lengths):
    centroid = json.loads(centroid)
    centre = (centroid["lat"], centroid["lng"])
    axes_lengths = json.loads(axes_lengths)
    length = max(axes_lengths["lat"], axes_lengths["lng"])
    
    d = distance.distance((length/1000) * 2)
    p1 = geopy.Point(centre)
    p2 = d.destination(point=p1, bearing=0)
    p3 = d.destination(point=p2, bearing=90)
    p4 = d.destination(point=p3, bearing=180)

    points = [(p.longitude, p.latitude) for p in [p1,p2,p3,p4]]
    polygon = Polygon(points)
    return polygon

# Lookup a record by its geo_code and print its properties.
def print_dataframe_row_by_geo_code(df, geo_code):
    df = df.loc[df['geo_code'] == geo_code]

    for c in df.columns:
        print(f"-" * 80)
        print(f"Column: {c}")
        print(f"-" * 80)
        print(df[c].to_list())

# Return the bounds of a square polygon over its x and y components.
# Not currently in use but can be used for defining search areas explicitely.
def calculate_bounds_and_center_bounds_square(x):
    bounds = x.bounds
    minx = bounds[0]
    miny = bounds[1]
    maxx = bounds[2]
    maxy = bounds[3]

    x_delta = maxx - minx
    y_delta = maxy - miny

    maxx = maxx - x_delta / 2
    minx = minx - x_delta / 2
    maxy = maxy - y_delta / 2
    miny = miny - y_delta / 2

    return json.dumps({"lng_min":minx, "lat_min":miny, "lng_max":maxx, "lat_max":maxy})

# Subdivide a square polygon into squares of 400 ft by 400 ft.
# Not currently in use but can be used for defining search areas explicitely.
def subdivide_square(square_bounds):
    # Projects a square of reasonable predetermined size on the map. 120 meters or 400 ft.
    lat_delta_factor = 0.0010810912550027751
    lng_delta_factor = 0.0017325629696289258

    subs = []
    bounds = json.loads(square_bounds)

    lng_delta = bounds["lng_max"] - bounds["lng_min"]
    lat_delta = bounds["lat_max"] - bounds["lat_min"]

    squares_per_axis = int(round(((lng_delta / lng_delta_factor) + (lat_delta / lat_delta_factor))/2, 0))
    print(squares_per_axis)

    for lng in range(squares_per_axis):
        for lat in range(squares_per_axis):
            new_lng_max = bounds["lng_max"] + (lng * lng_delta_factor) - (lng_delta_factor * (squares_per_axis - 1))
            new_lat_max = bounds["lat_max"] + (lat * lat_delta_factor) - (lat_delta_factor * (squares_per_axis - 1))
            new_lng_min = new_lng_max - lng_delta_factor
            new_lat_min = new_lat_max - lat_delta_factor
            subs.append(json.dumps({"lng_min":new_lng_min, "lat_min":new_lat_min, "lng_max":new_lng_max, "lat_max":new_lat_max}))
    
    return subs
