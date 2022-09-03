import csv
from recipe import Recipe
from fastapi import FastAPI
import uvicorn
import redis

app = FastAPI()
redis = redis.Redis(
    host='localhost',
    port=6379)


@app.on_event('startup')
async def startup_event():
    datafile = 'Recipes.csv'
    dataset = csv.reader(datafile, delimiter=',')
    next(dataset)
    recipes = []
    for count, row in enumerate(dataset):
        recipes.append(Recipe(row[0], row[2], row[1]))
    redis.set('recipes', repr(recipes))


@app.get("/")
async def root(ingredients):
    recipes = eval(redis.get('recipes'))
    search()
    return {"message": "Hello World"}

if __name__ == "__main__":
    main()
    uvicorn.run(app, host="0.0.0.0", port=8000)

