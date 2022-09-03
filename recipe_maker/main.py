import csv
from recipe import Recipe
def main():
    datafile = 'Recipes.csv'
    ingredientsfile = 'ingredients'
    outfile = 'output.json'
    dataset = csv.reader(datafile, delimiter=',')
    ingredients = csv.reader(ingredientsfile, delimiter=',')
    next(dataset)
    recipes = []
    for count, row in enumerate(dataset):
        recipes.append(Recipe(row[0], row[2], row[1]))



if __name__ == '__main__':
    main()
