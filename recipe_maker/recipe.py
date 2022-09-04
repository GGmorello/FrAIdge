from urllib.request import urlopen
import pandas as pd

def search(recipes, ingredients, userId):
    matches = []
    for recipe in recipes:
        for ingredient in ingredients:
            if ingredient in recipe.ingredients:
                recipe.matches += 1

        matches.append(recipe)
    matches.sort(key=lambda lol: lol.matches, reverse=True)
    matches.sort(key=lambda lol: len(lol.ingredients) - lol.matches)
    for i, match in enumerate(matches):
        if i > 4:
            break

    head = matches[:5]
    print(head)
    head.sort(key=lambda lol: lol.get_recommendation(userId), reverse=True)
    head.sort(key=lambda lol: len(lol.ingredients) - lol.matches)
    return head


class Recipe:
    def __init__(self, name: str, ingredients: str, link: str):
        self.name = name
        self.ingredients = eval(ingredients)
        self.link = link
        self.matches = 0

    def get_recommendation(self, userId):
        table = pd.read_pickle("dataframe.pkl")
        if self.name in table.index:
            user = table.query('userId == [' + userId + ']')
            recommendation = table.corrwith(user).sort_values(ascending=False).fillna(0)
            if type(recommendation[self.name]) is None:
                return 0
            return recommendation[self.name]
        else:
            return 0
