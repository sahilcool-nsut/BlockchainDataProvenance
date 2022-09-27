from flask import Flask, request, jsonify, render_template
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import os
from myWeb3 import CustomWeb3
import json
from mongoDBDriver import insertOne
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"]=True
customWeb3 = CustomWeb3()

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/showData")
def showData():
    return render_template('showData.html',messages={})

@app.route("/addData")
def addDataPage():
    return render_template('addData.html',messages={})

@app.route('/helloWorld', methods=['GET'])
def helloWorld():
    if request.method == 'GET':
        return "Hello World!"


@app.route('/insertDataDB', methods=['POST'])
def insertDataDB():
    if request.method == 'POST':

        name = request.form.get('name')
        rollno = request.form.get('rollno')
        print(name)
        print(rollno)
        try:
            insertOne({"name":name,"rollNo":rollno})
            return render_template('addData.html',messages={"dataAdded":"Data Added Successfully"})
        except Exception as e:
            print(e)
            return render_template('addData.html',messages={"dataAdded":"Something went wrong"})
        

@app.route('/trigger-event', methods=['POST'])
def trigger():
    payload = request.data.decode('utf-8')

    payloadObj = json.loads(payload)

    data = payloadObj['changeEvent']

    customWeb3.insertEventInSmartContract(data)
    return "ok ji"


@app.route('/interactTest', methods=['GET'])
def interactTest():
    customWeb3.insertEventInSmartContract()
    return "ok ji"

@app.route('/getData', methods=['GET'])
def getData():
    finalData = customWeb3.retrieveBlockChainData()
    return render_template('showData.html',messages={"data":finalData})

if __name__ == "__main__":
    app.run(debug=True)