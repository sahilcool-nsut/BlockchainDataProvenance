from flask import Flask, request, jsonify, render_template
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import os
from myWeb3 import insertEventInSmartContract
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route('/helloWorld', methods=['GET'])
def helloWorld():
    if request.method == 'GET':
        return "Hello World!"

@app.route('/trigger-event', methods=['POST'])
def trigger():
    # Request.data me se samaan nikalna h, timestamp, id, database, collection, document
    # is function me as parameter bhejna h (json bhejdiyo)
    payload = request.data.decode('utf-8')

    payloadObj = json.loads(payload)

    data = payloadObj['changeEvent']

    insertEventInSmartContract(data)
    return "ok ji"




if __name__ == "__main__":
    app.run(debug=True)