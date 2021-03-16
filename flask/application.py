import os.path
import json
from flask import Flask, send_from_directory, url_for, redirect
from flask import render_template, request
import logging

import datetime

delta = datetime.datetime(2021, 8, 21) - datetime.datetime.now()
delta.days

app = Flask(__name__)

# @app.before_request
# def before_request():
#     if request.url.startswith('http://'):
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)

@app.route('/')
@app.route('/index')
def index():
    print('index.html')
    return render_template('/index.html', days=delta.days)

@app.route("/travel.html")
def travel():
    return render_template('/travel.html', days=delta.days)

@app.route("/story.html")
def story():
    return render_template('/story.html', days=delta.days)

@app.route("/photos.html")
def photos():
    return render_template('/photos.html', days=delta.days)

@app.route("/registry.html")
def registry():
    return render_template('/registry.html', days=delta.days)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', days=delta.days), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
