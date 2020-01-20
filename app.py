# import the Flask class from the flask module
from flask import Flask, render_template, request, send_from_directory
import os
current_dir = os.curdir
# create the application object
app = Flask(__name__)

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)