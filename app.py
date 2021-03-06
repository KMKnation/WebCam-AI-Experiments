# import the Flask class from the flask module
from flask import Flask, render_template, request, send_from_directory, jsonify
import os

current_dir = os.curdir
# create the application object
app = Flask(__name__)


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/check')
def check():
    try:
        return render_template('checkapi.html')  # render a template

    except Exception as err:
        print(err)

    return "404 NOT FOUND"


# use decorators to link the function to a url
@app.route('/')
def front():
    try:
        if request.args['camera']:
            data = {"camera": request.args['camera']}
            return render_template('check.html', data=data)  # render a template

    except Exception as err:
        print(err)

    return "404 NOT FOUND"


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
