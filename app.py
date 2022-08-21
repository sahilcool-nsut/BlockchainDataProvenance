from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/helloWorld', methods=['GET'])
def helloWorld():
    if request.method == 'GET':
        return "Hello World!"