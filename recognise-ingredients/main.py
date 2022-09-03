from google.cloud import vision
import io
import os
from image_processing import cropImage


def printObj(object_):
    print('\n{} (confidence: {})'.format(object_.name, object_.score))
    # print('Normalized bounding polygon vertices: ')
    # print(object_.bounding_poly)
    # for vertex in object_.bounding_poly.normalized_vertices:
    #     print(' - ({}, {})'.format(vertex.x, vertex.y))


# Imports the Google Cloud client library

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('images/fridge.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

enable_label = False


objects = client.object_localization(
    image=image).localized_object_annotations
print('Number of objects found: {}'.format(len(objects)))
for object_ in objects:
    # printObj(object_)
    cropped = cropImage(file_name, object_.bounding_poly.normalized_vertices)
    buffer = io.BytesIO()
    cropped.save(buffer, format="JPEG")
    buffer_image = vision.Image(content=buffer.getvalue())
    # PNG = buffer.getvalue()
    # print(PNG[:20])

    response = client.label_detection(image=buffer_image)
    labels = response.label_annotations
    print()
    print("I'm a: ")
    objects = client.object_localization(
        image=buffer_image).localized_object_annotations
    printObj(objects[0])
