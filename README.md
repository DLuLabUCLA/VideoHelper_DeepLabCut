# VideoHelper_DeepLabCut
Video processing helper for DeepLabCut, video examples downloaded from https://github.com/MaureenAscona/DLC-MotorBox/tree/main

In terminal, install required packages using 

```
pip install -r requirements.txt
```

## Resizing Function
to run, type in terminal (in the package folder):

```
python3 resize.py resize_params.yaml
```

change `resize_params.yaml` to the parameter file location

example `resize_params.yaml` file:

```
root: ./example_dlc
out_folder: resized

downsample: True
upsample: False

video: True
labeled-data: True

target_width: 1200
target_height: null

skip_if_video_exists: False
```

## Changing labels made by multi-animal project to single animal labels

to run, type in terminal (in the package folder):

```
python3 labels_multi2single.py multi2single_params.yaml
```

`multi2single_params.yaml` only contains the root folder and output folder name

## Other notes

As of 10/10/2024, make sure to include all above parameters in the yaml file, since there are no default values set in the code


