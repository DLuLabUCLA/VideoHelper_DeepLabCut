import os
import sys
import yaml
import shutil
import argparse

import cv2
import glob
import tqdm
import pandas as pd
from PIL import Image


parser = argparse.ArgumentParser("Parameter file location")
parser.add_argument(
    "params", 
    help="Location of the parameter file for processing the labels", type=str,
    nargs='?', default="multi2single_params.yaml")
args = parser.parse_args()
PARAMS_FILE = args.params
# PARAMS_FILE = "params.yaml"

with open(PARAMS_FILE, 'r') as file:
    params = yaml.safe_load(file)

root = params["root"]
out_root = os.path.join(root, params["out_folder"])


labeled_folders = [
    folder for folder in glob.glob(os.path.join(root, "labeled-data/*")) 
    if not folder.endswith("_labeled")]

for i, fd in tqdm.tqdm(enumerate(labeled_folders)):
    h5_filename = glob.glob(os.path.join(fd, "CollectedData_*.h5"))[0]
    df = pd.read_hdf(h5_filename)

    # with pd.HDFStore(h5_filename, 'r') as store:
    #     # Get the list of keys
    #     keys = store.keys()
    # print(f"before: {keys}")

    if df.columns.nlevels > 3:
        df.columns = df.columns.droplevel(1)
    else:
        continue

    relative_path = os.path.relpath(h5_filename, root)
    os.makedirs(os.path.join(out_root, os.path.dirname(relative_path)), exist_ok=True)

    df.to_hdf(os.path.join(out_root, relative_path), key='keypoints', mode='w')
    df.to_csv(os.path.join(out_root, relative_path)[:-2]+"csv")

    # with pd.HDFStore(os.path.join(out_root, relative_path), 'r') as store:
    #     # Get the list of keys
    #     keys = store.keys()
    # print(f"after: {keys}")


