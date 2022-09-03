from PIL import Image
from google.cloud import vision
import os


def cropImage(file_name, locations):
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

    # cropped = image.crop(
    #     (left * width * 0.9, top * height * 0.9,
    #      right * width * 1.1, bottom * height * 1.1)
    # )
    factor = 0.05
    cropped = image.crop(
        (left * width * (1 - factor), top * height * (1 - factor),
         right * width * (1 + factor), bottom * height * (1 + factor))
    )
    cropped.show()
    return cropped
