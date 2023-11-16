import json
from random import seed, uniform


FILE_PATH = "data_10000000_flex.json"
LENGTH = 1_000_000
SEED = 123456


# Produce data
seed(SEED)
pairs = [
    {
        "x0": uniform(-360, 360), "y0": uniform(-360, 360),
        "x1": uniform(-360, 360), "y1": uniform(-360, 360),
    }
    for _ in range(LENGTH)
]
json_data = {}
json_data["pairs"] = pairs

# Save data to file
with open(FILE_PATH, "w") as json_file:
    json.dump(json_data, json_file, indent=4)    
