
def get_resize_dims(
        width, height, target_width=None, target_height=None, downsample=True, upsample=True):
    assert (target_width is not None) or (target_height is not None), "at least one of target_width and target height should be specified"
        
    def _oneway_process(statement):
        if (target_height is None) and (statement):
            scale_width = 1.0
            scale_height = 1.0
        elif (target_width is None) and (statement):
            scale_width = 1.0
            scale_height = 1.0
        else:
            scale_width, scale_height = _get_scale(width, height, target_width, target_height)
        return scale_width, scale_height
    
    if downsample and (not upsample):
        scale_width, scale_height = _oneway_process(width < target_width)
    elif upsample and (not downsample):
        scale_width, scale_height = _oneway_process(width > target_width)
    else:
        scale_width, scale_height = _get_scale(width, height, target_width, target_height)
    
    resized_width = int(width * scale_width)
    resized_height = int(height * scale_height)

    return scale_width, scale_height, resized_width, resized_height


def _get_scale(width, height, target_width=None, target_height=None):
    if target_height is None:
        scale_width = target_width / width
        scale_height = scale_width
    elif target_width is None:
        scale_height = target_height / height
        scale_width = scale_height
    else:
        scale_width = target_width / width
        scale_height = target_height / height

    return scale_width, scale_height




# def _get_scale_downsample(width, height, target_width=None, target_height=None):
#     assert (target_width is not None) or (target_height is not None), "at least one of target_width and target height should be specified"
#     scale_width = 1.0
#     scale_height = 1.0

#     if (target_height is None) and (width < target_width):
#         scale_width = 1.0
#         scale_height = 1.0
#     elif (target_width is None) and (height < target_height):
#         scale_width = 1.0
#         scale_height = 1.0
#     elif target_height is None:
#         scale_width = target_width / width
#         scale_height = scale_width
#     elif target_width is None:
#         scale_height = target_height / height
#         scale_width = scale_height
#     else:
#         scale_width = target_width / width
#         scale_height = target_height / height
    
#     resized_width = int(width * scale_width)
#     resized_height = int(height * scale_height)

#     return scale_width, scale_height, resized_width, resized_height

