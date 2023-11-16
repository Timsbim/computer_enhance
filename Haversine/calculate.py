import json
from math import asin, cos, radians, sin, sqrt
from statistics import fmean
from time import perf_counter


FILE_PATH = "data_10000000_flex.json"
EARTH_RADIUS = 6371


def haversine_of_degrees(x0, y0, x1, y1, radius):
    sdx = sin(radians(x1 - x0) / 2)
    sdy = sin(radians(y1 - y0) / 2)
    cy0 = cos(radians(y0))
    cy1 = cos(radians(y1))
    root = sqrt(sdy * sdy + cy0 * cy1 * sdx * sdx)
    return 2 * radius * asin(root)


def haversine_average(json_data):
    return fmean(
        haversine_of_degrees(
            pair["x0"], pair["y0"], pair["x1"], pair["y1"], EARTH_RADIUS
        )
        for pair in json_data["pairs"]
    )


# Loading JSON-data
start = perf_counter()
with open(FILE_PATH, "r") as json_file:
    json_data = json.load(json_file)
end = perf_counter()
loading_duration = end - start


# Calculating average distance
start = perf_counter()
average_distance = haversine_average(json_data)
end = perf_counter()
math_duration = end - start


# Print stats
total_duration = loading_duration + math_duration
length = len(json_data["pairs"])
print(f"Result: {average_distance:.2f}")
print(f"Loading: {loading_duration:.2f} seconds")
print(f"Math: {math_duration:.2f} seconds")
print(f"Total: {total_duration:.2f} seconds")
print(f"Throughput: {length / total_duration:.0f} haversines/second")
