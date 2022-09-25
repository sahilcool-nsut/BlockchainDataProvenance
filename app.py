from flask import Flask, request, jsonify, render_template
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import os
from myWeb3 import insertEventInSmartContract

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route('/helloWorld', methods=['GET'])
def helloWorld():
    if request.method == 'GET':
        return "Hello World!"

@app.route('/interact',methods=['GET'])
def connect():
    insertEventInSmartContract()
    return "ok ji"

@app.route('/trigger-event', methods=['POST'])
def trigger():
    print(request.data)
    return "done"



if __name__ == "__main__":
    app.run(debug=True)