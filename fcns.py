
def get_scale(width, height, target_width=None, target_height=None):


def _get_scale_downsample(width, height, target_width=None, target_height=None):
    assert (target_width is not None) or (target_height is not None), "at least one of target_width and target height should be specified"
    scale_width = 1.0
    scale_height = 1.0

    if (target_height is None) and (width < target_width):
        scale_width = 1.0
        scale_height = 1.0
    elif (target_width is None) and (height < target_height):
        scale_width = 1.0
        scale_height = 1.0
    elif target_height is None:
        scale_width = target_width / width
        scale_height = scale_width
    elif target_width is None:
        scale_height = target_height / height
        scale_width = scale_height
    else:
        scale_width = target_width / width
        scale_height = target_height / height
    
    resized_width = int(width * scale_width)
    resized_height = int(height * scale_height)

    return scale_width, scale_height, resized_width, resized_height

