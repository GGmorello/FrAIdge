import csv
from recipe import Recipe, search
from fastapi import FastAPI
import uvicorn
import redis
import pickle

app = FastAPI()
redis = redis.Redis(
    host='localhost',
    port=6379)


@app.on_event('startup')
async def startup_event():
    datafile = 'Recipes.csv'
    f = open(datafile, 'r')
    dataset = csv.reader(f, delimiter=',')
    e = next(dataset)
    recipes = []
    for row in dataset:
        recipes.append(Recipe(row[0], row[2], row[1]))
    pickled_recipes = pickle.dumps(recipes)

    redis.set('recipes', pickled_recipes)


@app.get("/")
async def root(ingredients):
    list_ingredients = eval(ingredients)
    recipes = pickle.loads(redis.get('recipes'))
    return search(recipes, list_ingredients, '0')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

