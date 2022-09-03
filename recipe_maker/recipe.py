from urllib.request import urlopen


def search(recipes, ingredients):
    matches = []
    for recipe in recipes:
        for ingredient in ingredients:
            if ingredient in recipe.ingredients:
                recipe.matches += 1

        matches.append(recipe)

    matches.sort(key=lambda lol: lol.matches, reverse=True)
    for i, match in enumerate(matches):
        if i > 4:
            break
        match.request()
    return matches[:5]


class Recipe:
    def __init__(self, name: str, ingredients: str, link: str):
        self.name = name
        self.ingredients = eval(ingredients)
        self.link = link
        self.html = ''
        self.matches = 0

    def request(self):
        self.html = urlopen(self.link).read()

