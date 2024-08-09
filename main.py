import os
import sys
import yaml
import argparse

# parser = argparse.ArgumentParser("Parameter file location")
# parser.add_argument(
#     "params", 
#     help="Location of the parameter file for processing the video", type=str,
#     nargs='?', default="params.yaml")
# args = parser.parse_args()
# PARAMS_FILE = args.params
PARAMS_FILE = "params.yaml"

with open(PARAMS_FILE, 'r') as file:
    params = yaml.safe_load(file)

root, downsample, upsample, target_width, target_height = \
    params["root"], params["downsample"], params["upsample"], \
    params["target_width"], params["target_height"]

if (not downsample) and (not upsample):
    sys.exit("Not processing as both 'downsample' and 'upsample' are False")


out_root = os.path.join(root, params["out_folder"])
out_video = os.path.join(out_root, "videos")
out_label = os.path.join(out_root, "labeled-data")
os.makedirs(out_video, exist_ok=True)
os.makedirs(out_label, exist_ok=True)
