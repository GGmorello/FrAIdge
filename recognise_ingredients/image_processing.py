from PIL import Image
#from google.cloud import vision
import os
import io


def cropImage(file_name, locations, factor, show=False):
    image = Image.open(file_name)
    width = image.width
    height = image.height

    left = locations[0].x
    right = locations[0].x
    top = locations[0].y
    bottom = locations[0].y

    for vertex in locations:
        left = min(left, vertex.x)
        right = max(right, vertex.x)
        top = min(top, vertex.y)
        bottom = max(bottom, vertex.y)

    real_left = max(0, left * width * (1 - factor))
    real_right = min(width, right * width * (1 + factor))
    real_top = max(0, top * height * (1 - factor))
    real_bottom = min(height, bottom * height * (1 + factor))

    cropped = image.crop((real_left, real_top, real_right, real_bottom))
    if show:
        cropped.show()
    return cropped


def cropToBuffer(file_name, obj, factor, show=False):
    cropped = cropImage(
        file_name, obj.bounding_poly.normalized_vertices, factor, show)
    buffer = io.BytesIO()
    cropped.save(buffer, format="JPEG")
    return buffer.getvalue()
