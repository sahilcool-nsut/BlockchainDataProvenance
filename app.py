from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Home Page updated"

@app.route('/helloWorld', methods=['GET'])
def helloWorld():
    if request.method == 'GET':
        return "Hello World!"