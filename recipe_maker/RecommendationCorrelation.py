import pandas as pd
import random
from tqdm import tqdm


def create_data():
    collection = []
    for i in tqdm(range(10000)):
        tried_recipes = set()
        for j in range(10000):
            tried_recipes.add(random.randint(0, 2000000))
        collection.append(tried_recipes)

    ratings = open('rating.csv', 'w')
    for i in tqdm(range(1000)):
        for j in collection[i]:
            ratings.write(str(i) + ',' + str(j) + ',' + str(random.randint(1, 10)) + '\n')


# create_data()


recipe = pd.read_csv("Recipes.csv")
recipe = recipe.loc[:, ['title']]
recipe['recipeId'] = recipe.index
rating = pd.read_csv("rating.csv")
rating.columns = ['userId', 'recipeId', 'rating']
data = pd.merge(recipe, rating)
# print(data.head(10))
data = data.iloc[:1000000, :]
pivot_table = data.pivot_table(index=["userId"], columns=["title"], values="rating")
pivot_table.to_pickle("dataframe.pkl")
recipe_tried = pivot_table.query('userId == ["1"]')
recommendation = pivot_table.corrwith(recipe_tried).sort_values(ascending=False).fillna(0)
print(recommendation["Lemon Bars"])
