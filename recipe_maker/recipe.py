import requests
import json
from urllib.request import urlopen

class Recipe:
    def __init__(self, name: str, ingredients: list, link: str):
        self.name = name
        self.ingredients = ingredients
        self.link = link
        self.html = ''

    def request(self):
        self.html = urlopen(self.link).read()

