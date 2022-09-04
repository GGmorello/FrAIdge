import pandas as pd

def search(recipes, ingredients, userId):
    matches = []
    for recipe in recipes:
        for ingredient in ingredients:
            if ingredient in recipe.ingredients:
                recipe.matches += 1

        recipe.missing_ingredients = [item for item in recipe.ingredients if item not in ingredients]
        matches.append(recipe)

    matches.sort(key=lambda lol: lol.matches, reverse=True)
    matches.sort(key=lambda lol: len(lol.ingredients) - lol.matches)

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
        self.similarity_with_other_recipes = []
        self.missing_ingredients = []

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
