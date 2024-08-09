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

from fcns import get_resize_dims

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
skip_if_video_exists = params["skip_if_video_exists"]

if (not downsample) and (not upsample):
    sys.exit("Not processing as both 'downsample' and 'upsample' are False")


out_root = os.path.join(root, params["out_folder"])
out_video = os.path.join(out_root, "videos")
out_label = os.path.join(out_root, "labeled-data")
os.makedirs(out_video, exist_ok=True)
os.makedirs(out_label, exist_ok=True)


scale_df_vid = pd.DataFrame()

videos = [
    folder for folder in glob.glob(os.path.join(root, "videos/*")) ]


for i,v in enumerate(videos):
    vid_name = os.path.basename(v)
    print(f"({i+1}/{len(videos)}) Processing video {vid_name}")
    cap = cv2.VideoCapture(v)
    if not cap.isOpened():
        raise ValueError("Error opening video file")
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    scale_width, scale_height, resized_width, resized_height = \
        get_resize_dims(
            width, height, target_width, target_height, 
            downsample=downsample, upsample=upsample)

    
    outpath_vid = os.path.join(out_video, vid_name)

    if skip_if_video_exists and os.path.exists(outpath_vid):
        print(f"File already exist at '{outpath_vid}', skipped")
        cap.release()
        scale_df_vid = pd.concat([scale_df_vid, pd.DataFrame(
        {
            # "video_name": os.path.splitext(os.path.basename(v))[0],
            "name": os.path.splitext(vid_name)[0],
            "video": False,
            "labeled": False,
            "original_width": width,
            "original_height": height,
            "resized_width": resized_width,
            "resized_height": resized_height,
            "scale_width": scale_width,
            "scale_height": scale_height
        }, index=[0])], ignore_index=True)
        continue

    scale_df_vid = pd.concat([scale_df_vid, pd.DataFrame(
        {
            # "video_name": os.path.splitext(os.path.basename(v))[0],
            "name": os.path.splitext(vid_name)[0],
            "video": True,
            "labeled": False,
            "original_width": width,
            "original_height": height,
            "resized_width": resized_width,
            "resized_height": resized_height,
            "scale_width": scale_width,
            "scale_height": scale_height
        }, index=[0])], ignore_index=True)

    if (scale_width == 1) and (scale_height == 1):
        shutil.copy(v, outpath_vid)
        cap.release()
        continue
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        outpath_vid, fourcc, cap.get(cv2.CAP_PROP_FPS), 
        (resized_width, resized_height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (resized_width, resized_height))
        out.write(resized_frame)
    
    cap.release()
    out.release()


scale_df_lab = pd.DataFrame()
labeled_folders = [
    folder for folder in glob.glob(os.path.join(root, "labeled-data/*")) 
    if not folder.endswith("_labeled")]

for i, fd in enumerate(labeled_folders):
    h5_filename = glob.glob(os.path.join(fd, "CollectedData_*.h5"))[0]
    filename = os.path.splitext(os.path.basename(h5_filename))[0]
    vid_name_noext = os.path.splitext(
        os.path.basename(os.path.dirname(h5_filename)))[0]
    images = glob.glob(os.path.join(fd, "*.png"))

    print(f"({i+1}/{len(labeled_folders)}) Processing labels {vid_name_noext}")
    
    if (vid_name_noext == scale_df_vid["name"]).any():
        scale_df_vid.loc[scale_df_vid["name"]==vid_name_noext, "labeled"] = True
        sub_df = scale_df_vid[scale_df_vid["name"] == vid_name_noext]
        scale_width = sub_df["scale_width"].values[0]
        scale_height = sub_df["scale_height"].values[0]
        resized_width = sub_df["resized_width"].values[0]
        resized_height = sub_df["resized_height"].values[0]

    else:
        img = Image.open(images[0])
        width, height = img.size
        scale_width, scale_height, resized_width, resized_height = \
            get_resize_dims(
                width, height, target_width, target_height, 
                downsample=downsample, upsample=upsample)
        scale_df_lab = pd.concat([scale_df_lab, pd.DataFrame({
            "name": vid_name_noext,
            "video": False,
            "labeled": True,
            "original_width": width,
            "original_height": height,
            "resized_width": resized_width,
            "resized_height": resized_height,
            "scale_width": scale_width,
            "scale_height": scale_height
        }, index=[0])], ignore_index=True)

    df = pd.read_hdf(h5_filename)
    for col in df.columns:
        if 'x' in col:
            df[col] = df[col] * scale_width
        elif 'y' in col:
            df[col] = df[col] * scale_height
    save_folder = os.path.join(out_label, vid_name_noext)
    os.makedirs(save_folder, exist_ok=True)
    df.to_hdf(os.path.join(save_folder, f"{filename}.h5"), key='df')
    df.to_csv(os.path.join(save_folder, f"{filename}.csv"))

    for img_path in tqdm.tqdm(images):
        img = Image.open(img_path)
        img = img.resize((resized_width, resized_height))
        img.save(os.path.join(save_folder, os.path.basename(img_path)))

scale_df = pd.concat([scale_df_vid, scale_df_lab], ignore_index=True)
scale_df = scale_df.reset_index(drop=True)
scale_df.to_csv(os.path.join(out_root, "_scale_info.csv"))
