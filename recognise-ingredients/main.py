# Imports the Google Cloud client library
from google.cloud import vision
import io
import os
from image_processing import *

RELATIVE_PATH = 'images/fridge.jpg'
SHOW = False

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
    result = []
    for object_ in objects:
        # Crop object
        buffer_value = cropToBuffer(file_name, object_, factor, show)
        buffer_image = vision.Image(content=buffer_value)

        object_recognition = client.object_localization(
            image=buffer_image).localized_object_annotations
        for i in range(min(3, len(object_recognition))):
            result.append(object_recognition[i].name)
        # result.append(object_.name)
    return set(result)


def filterIngredients(set):
    removables = {
        'Food',
        'Container',
        'Animal',
        'Clock',
        'Fruit',
        'Person'
    }

    return set.difference(removables)


def main():
    file_name = os.path.abspath(RELATIVE_PATH)
    objects = objectLocalization(file_name, 0.02, show=SHOW)
    # Filter ingredients
    ingredients = filterIngredients(objects)
    print(ingredients)


if __name__ == "__main__":
    main()
