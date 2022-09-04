from PIL import Image
#from google.cloud import vision
import os

def cropImage(file_name, locations):
    image = Image.open(file_name)
    width = image.width
    height = image.height
    factor = 0.05

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
    cropped.show()
    return cropped
