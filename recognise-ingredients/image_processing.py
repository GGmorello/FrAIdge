from PIL import Image
from google.cloud import vision
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

    cropped = image.crop(
        (left * width * (1 - factor), top * height * (1 - factor),
         right * width * (1 + factor), bottom * height * (1 + factor))
    )
    if show:
        cropped.show()
    return cropped


def cropToBuffer(file_name, obj, factor, show=False):
    cropped = cropImage(
        file_name, obj.bounding_poly.normalized_vertices, factor, show)
    buffer = io.BytesIO()
    cropped.save(buffer, format="JPEG")
    return buffer.getvalue()
