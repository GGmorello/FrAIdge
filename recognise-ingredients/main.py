# Imports the Google Cloud client library
from google.cloud import vision
import io
import os
from image_processing import *

# Load an instance of the image annotator
client = vision.ImageAnnotatorClient()


def printObj(object_):
    print('\n{} (confidence: {})'.format(object_.name, object_.score))


def loadContent(file_name):
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    return content


def objectLocalization(file_name, factor, show=False):
    content = loadContent(file_name)
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))

    for object_ in objects:
        # Crop object
        buffer_value = cropToBuffer(file_name, object_, factor, show)
        buffer_image = vision.Image(content=buffer_value)

        response = client.label_detection(image=buffer_image)
        labels = response.label_annotations
        # print("I'm a: ")
        print(f"labels thinks: {labels[0].description}")
        # printObj(object_)


def main():
    file_name = os.path.abspath('images/fridge.jpg')
    objectLocalization(file_name, 0.02, show=False)


if __name__ == "__main__":
    main()
