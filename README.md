# VideoHelper_DeepLabCut
Video processing helper for DeepLabCut


to run, type in terminal:

```
python3 main.py params.yaml
```

change `params.yaml` to the parameter file location

example `params.yaml` file:

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

As of 08/09/2024, make sure to include all above parameters in the yaml file, since there are no default values set in the code