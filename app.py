import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'

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
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect('/recipes')
      # return "success"
  
  # return send_from_directory('.', 'static/upload/index.html')
  return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <script type='text/javascript' src="static/upload/script.js"></script>
    '''




# # Uploads dropped image to /uploads folder (then we can access it as an image file for recognition)
# @app.route('/upload', methods=('POST',))
# def upload():
#   files = request.files.getlist('files')
#   for file in files:
#     fn = secure_filename(file.filename)
#     file.save(os.path.join('uploads', fn))  # replace FILES_DIR with your own directory
#   return redirect("/recipes")
#   # return render

@app.route('/recipes', methods=['GET', 'POST'])
def show_recipes():
  print('showing recipes')
  # breakpoint()
  return send_from_directory('.', 'static/recipes/index.html')















