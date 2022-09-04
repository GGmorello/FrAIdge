import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import requests
from recognise_ingredients.main import objectLocalization, filterIngredients

import shutil

UPLOAD_FOLDER = 'uploads'
SHOW = False

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

# opens the start page of our app - index.html
# @app.route('/')
# def home():
  # print('home')
  # return send_from_directory('.', 'static/upload/index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  print('upload file')
  
  if request.method == 'POST':
    # breakpoint()
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)

    if file:
      print('file sent')
      filename = secure_filename('photo.jpg')
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect('/ingredients')
      # return "success"
  
  return send_from_directory('.', 'static/upload/index.html')
  # return '''
  #   <!doctype html>
  #   <title>Upload new File</title>
  #   <h1>Upload new File</h1>
  #   <form method=post enctype=multipart/form-data>
  #     <input type=file name=file>
  #     <input type=submit value=Upload>
  #   </form>
  #   <script type='text/javascript' src="static/upload/script.js"></script>
  #   '''

# # Uploads dropped image to /uploads folder (then we can access it as an image file for recognition)
# @app.route('/upload', methods=('POST',))
# def upload():
#   files = request.files.getlist('files')
#   for file in files:
#     fn = secure_filename(file.filename)
#     file.save(os.path.join('uploads', fn))  # replace FILES_DIR with your own directory
#   return redirect("/recipes")
#   # return render

@app.route('/ingredients', methods=['GET', 'POST'])
def show_ingredients():
  
  if request.method == 'POST':
    ingredients = request.form.getlist("ingredients")
    ingredients = [i.lower() for i in ingredients]

    req_res = requests.get('http://0.0.0.0:8001', params={'ingredients' : str(ingredients)})
    
    recipes = req_res.text

    # recipes = [{"name":"Crinkle Cookies","ingredients":["cake mix","egg"],"link":"http://www.cookbooks.com/Recipe-Print.aspx?id=631042","matches":1},{"name":"Baked Eggs","ingredients":["egg","Cheddar cheese"],"link":"http://www.cookbooks.com/Recipe-Print.aspx?id=277469","matches":1},{"name":"Lemon Cookies","ingredients":["Duncan","egg"],"link":"http://www.cookbooks.com/Recipe-Print.aspx?id=231612","matches":1},{"name":"Orange Peel Cup","ingredients":["oranges","egg"],"link":"http://www.cookbooks.com/Recipe-Print.aspx?id=934341","matches":1},{"name":"Lemon Drop Cookies","ingredients":["egg","lemon cake mix"],"link":"http://www.cookbooks.com/Recipe-Print.aspx?id=604217","matches":1}]

    return get_recipes_html(recipes, ingredients)

  else:

    # Detect the ingredients
    file_name = os.path.abspath('uploads/photo.jpg')
    objects = objectLocalization(file_name, 0.02, show=SHOW)
    
    # Filter ingredients
    ingredients = filterIngredients(objects)
    print(ingredients)

    js_file = open("static/ingredients/script.js", "r")
    list_of_lines = js_file.readlines()
    
    tags_line = "tags =  ["

    for ingredient in ingredients:
      tags_line += f'''"{ingredient}", '''
    tags_line += "]\n"

    # breakpoint()

    list_of_lines[5] = tags_line

    js_file = open("static/ingredients/script.js", "w")
    js_file.writelines(list_of_lines)
    js_file.close()

    
    
    return send_from_directory('.', 'static/ingredients/index.html')


RECIPES_HEAD = '''
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <title>FrAIdge</title>
        <link rel="stylesheet" href="static/recipes/style.css">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Unicons CDN Link for Icons -->
        <link rel="stylesheet" href="https://unicons.iconscout.com/release/v4.0.0/css/thinline.css">
      </head>
      <body>
        <div class="container">
    '''

RECIPES_TAIL = '''
    </div>
  
    <script type='text/javascript' src="static/recipes/script.js"></script>
    
    </body>
    </html>
    '''


def get_recipes_html(recipes, our_ingredients):

  recipes = eval(recipes)

  n_our_ingredients = len(our_ingredients)

  recipes_html = ""
  
  for recipe in recipes:
    ingredients = ""
    for i in range(len(recipe['ingredients'])):
      if i == (len(recipe['ingredients'])-1):
        ingredients += recipe['ingredients'][i]
      else:
        ingredients += recipe['ingredients'][i] + ', '
    
    recipes_html += f'''
     <div class="wrapper" onclick="openPage('google.com')" style="cursor: pointer;">
          <div class="title">
            <img src="static/ingredients/recipe.svg" alt="icon">
            <h2><a href={recipe['link']}>{recipe["name"]}</a></h2>
          </div>
          <div class="content">
            <p>{ingredients}</p>
            <p>number of missing ingredients: {len(recipe['ingredients']) - recipe['matches']}</p>
          </div>
      </div>
    '''

  return RECIPES_HEAD + recipes_html + RECIPES_TAIL














