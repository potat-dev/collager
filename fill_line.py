# load json from cache_data.json
import json
with open("cache_data.json", "r") as f:
    cache_data = json.load(f)

cache_data = [{"path": path, **v} for path, v in cache_data.items()]

# function to sum up all ratios in list of items from cache_data
def sum_ratios(items):
    return sum([item["ratio"] for item in items])

# select all ratios from cache_data
ratios = [item["ratio"] for item in cache_data]

height = 1080
width = 1920
lines = 4
height_shift = 0.001

line_height = height / lines
height_shift = height_shift * line_height
min_height = line_height - height_shift
max_height = line_height + height_shift

line_ratio = width / line_height
min_ratio = width / max_height
max_ratio = width / min_height

print("min_ratio:", min_ratio, "max_ratio:", max_ratio)

import random

iters = 0
selected_ratios = []
while selected_ratios == []:
    iters += 1
    while sum_ratios(selected_ratios) < min_ratio:
        # append a random ratio to the selected_ratios list
        selected_ratios.append(random.choice(cache_data))
    if sum_ratios(selected_ratios) > max_ratio:
        selected_ratios = []

# import pprint
# pprint.pprint(selected_ratios)
print("found after", iters, "iterations")

# TODO: write code to crop + resize images to fit line height and width
# вычислить пропорциональное изменение соотношения сторон для каждого изображения
# для маленьких изображений изменение будет меньше, для больших изображений изменение будет больше

curr_ratio = sum_ratios(selected_ratios)
ratio_delta = line_ratio - curr_ratio

old_ratios = [item["ratio"] for item in selected_ratios]
new_ratios = [item["ratio"] + ratio_delta * item["ratio"] / curr_ratio for item in selected_ratios]

print("line ratio:", line_ratio)
print("old_ratios:", old_ratios)
print("sum:", sum(old_ratios))
print("new_ratios:", new_ratios)
print("sum:", sum(new_ratios))
