from urllib.request import urlopen
import pandas as pd

def search(recipes, ingredients, userId):
    matches = []
    for recipe in recipes:
        for ingredient in ingredients:
            if ingredient in recipe.ingredients:
                recipe.matches += 1

        matches.append(recipe)

    matches.sort(key=lambda lol: (len(lol.ingredients) - lol.matches))
    for i, match in enumerate(matches):
        if i > 4:
            break
        match.request()
    head = matches[:5]
    head.sort(key=lambda lol: (len(lol.ingredients) - lol.matches, lol.get_recommendation(userId)))
    return head


class Recipe:
    def __init__(self, name: str, ingredients: str, link: str):
        self.name = name
        self.ingredients = eval(ingredients)
        self.link = link
        self.html = ''
        self.matches = 0
        self.similarity_with_other_recipes = []

    def request(self):
        self.html = urlopen(self.link).read()

    def get_recommendation(self, userId):
        table = pd.read_pickle("dataframe.pkl")
        if self.name in table.index:
            user = table.query('userId == [' + userId + ']')
            recommendation = table.corrwith(user).sort_values(ascending=False)
            return recommendation[self.name]
