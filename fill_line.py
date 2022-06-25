# load json from cache_data.json
import json
with open("cache_data.json", "r") as f:
    cache_data = json.load(f)

# select all ratios from cache_data
ratios = [item["ratio"] for item in cache_data.values()]

# print average of the ratios list
print(sum(ratios) / len(ratios))

height = 1080
width = 1920
lines = 4
height_shift = 0.01

line_height = height / lines
height_shift = height_shift * line_height
min_height = line_height - height_shift
max_height = line_height + height_shift

min_ratio = width / max_height
max_ratio = width / min_height

print("min_ratio:", min_ratio, "max_ratio:", max_ratio)

# print min and max height
print("min", min_height, "max", max_height)

min_items = max_ratio / max(ratios)
max_items = min_ratio / min(ratios)

print("min_items:", min_items, "max_items:", max_items)

import random

iters = 0
selected_ratios = []
while selected_ratios == []:
    iters += 1
    while sum(selected_ratios) < min_ratio:
        # append a random ratio to the selected_ratios list
        selected_ratios.append(random.choice(ratios))
    if sum(selected_ratios) > max_ratio:
        selected_ratios = []

print(selected_ratios, sum(selected_ratios), iters)