from flask import render_template

def hello_world():
    return "Hello World"

def index():
    return render_template('index.html')