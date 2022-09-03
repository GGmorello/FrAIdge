from urllib.request import urlopen


def search(recipes, ingredients):
    matches = []
    for recipe in recipes:
        ingredient_matches = 0
        for ingredient in ingredients:
            if ingredient in recipe.ingredients:
                ingredient_matches += 1

        matches.append((recipe, ingredient_matches))

    matches.sort(key=lambda tup: tup[1])
    return matches[:5]


class Recipe:
    def __init__(self, name: str, ingredients: list, link: str):
        self.name = name
        self.ingredients = ingredients
        self.link = link
        self.html = ''

    def request(self):
        self.html = urlopen(self.link).read()

