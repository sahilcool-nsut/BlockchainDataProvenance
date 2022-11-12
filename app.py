from flask import Flask, request, jsonify, render_template,session,redirect,url_for
import pymongo
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import os
from myWeb3 import CustomWeb3
import json
import bcrypt
from mongoDBDriver import insertOne
import hashlib
app = Flask(__name__)
app.secret_key = "testing"
app.config["TEMPLATES_AUTO_RELOAD"]=True
customWeb3 = CustomWeb3()
client = pymongo.MongoClient("mongodb+srv://dbUser:test@blockchaintry.uyultsy.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('backendDB')
records = db.users
print(records)
@app.route("/")
def index():
    loggedIn = True if "email" in session else False
    if loggedIn:
        databases= db.databasesLinked.find({"email":session["email"]})
        print(databases)
        dbIDs = [[entry['databaseID'],entry['balance']] for entry in databases]
        print(dbIDs)    
        return render_template('home.html',messages={"loggedIn": True,"databases":dbIDs})
    return render_template('home.html',messages={"loggedIn": False})

# Pages
@app.route("/showData")
def showData():
    return render_template('showData.html',messages={"loggedIn": True if "email" in session else False})

@app.route("/addData")
def addDataPage():
    return render_template('addData.html',messages={"loggedIn": True if "email" in session else False})

@app.route("/login", methods=['GET','POST'])
def loginPage():
    if request.method == 'GET':
        if "email" in session:
            return redirect(url_for("index"))
        return render_template('loginPage.html',messages={"loggedIn": True if "email" in session else False})
    else:
        print(session)
        if "email" in session: 
            print(session["email"])
        emailID = request.form.get('emailID')
        password = request.form.get('pass')
        print(emailID)
        print(password)
        email_found = records.find_one({"email": emailID})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('index'))
            else:
                message = 'Wrong password'
                return render_template('loginPage.html', messages={"error":message,"loggedIn": True if "email" in session else False})
        else:
            message = 'Email not found'
            return render_template('loginPage.html', messages={"error":message,"loggedIn": True if "email" in session else False})


def updateBalance(transactionCost,dbID):
    print(transactionCost)
    print(dbID)
    currentEntry = db.databasesLinked.find_one_and_update({"databaseID":dbID},{"$inc":{"balance":transactionCost}})
    print(currentEntry)
    

def addDatabase(groupID,appID,trigID,emailID):
    stringToHash = groupID + trigID + appID
    hash_object = hashlib.sha1(stringToHash.encode())
    hex_dig = hash_object.hexdigest()
    print(hex_dig)
    hashFound = db.databasesLinked.find_one({'databaseID':hex_dig})
    print(hashFound)
    if hashFound: 
        return False
    else:
        db.databasesLinked.insert_one({'databaseID':hex_dig,'email':emailID,'balance':0})
        return True

@app.route('/addNewDatabase',methods=['GET','POST'])
def addNewDatabase():
    if request.method == 'GET':
        if "email" not in session:
            return redirect(url_for("index"))
        return render_template('addNewDB.html',messages={"loggedIn": True if "email" in session else False})
    else:
        groupID = request.form.get('groupID')
        appID = request.form.get('appID')
        trigID = request.form.get('triggerID')
        addedDB = addDatabase(groupID,appID,trigID,session["email"]) #Adds database into databasesLinked collection
        if addedDB == False: 
            message = 'This database trigger is already linked'
            return render_template('addNewDB.html', messages={"error":message,"loggedIn": True if "email" in session else False})
        else:
            return render_template('addNewDB.html', messages={"error":"Added Succesfully. Check in Homepage","loggedIn": True if "email" in session else False})
@app.route("/register", methods=['GET','POST'])
def registerPage():
    if request.method == 'GET':
        if "email" in session:
            return redirect(url_for("index"))
        return render_template('register.html',messages={"loggedIn": True if "email" in session else False})
    else:
        print(session)
        if "email" in session: 
            print(session["email"])
        emailID = request.form.get('emailID')
        password = request.form.get('pass')
        print(emailID)
        print(password)
        email_found = records.find_one({"email": emailID})
        print(email_found)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', messages={"error":message,"loggedIn": True if "email" in session else False})
        else:
            groupID = request.form.get('groupID')
            appID = request.form.get('appID')
            trigID = request.form.get('triggerID')
            addedDB = addDatabase(groupID,appID,trigID,emailID) #Adds database into databasesLinked collection
            if addedDB == False: 
                message = 'This database trigger is already linked'
                return render_template('register.html', messages={"error":message,"loggedIn": True if "email" in session else False})
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_input = {'email': emailID, 'password': hashed}
            records.insert_one(user_input)
            print("inserting in records")
            user_data = records.find_one({"email": emailID})
            new_email = user_data['email']
            print(user_data)
            session["email"] = emailID
            return redirect(url_for("index"))
        # return render_template('home.html',messages={})

@app.route('/logout',methods=['GET','POST'])
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

# Request Functions
@app.route('/insertDataDB', methods=['POST'])
def insertDataDB():
    if request.method == 'POST':

        name = request.form.get('name')
        rollno = request.form.get('rollno')
        print(name)
        print(rollno)
        try:
            insertOne({"name":name,"rollNo":rollno})
            return render_template('addData.html',messages={"dataAdded":"Data Added Successfully","loggedIn": True if "email" in session else False})
        except Exception as e:
            print(e)
            return render_template('addData.html',messages={"dataAdded":"Something went wrong","loggedIn": True if "email" in session else False})
        

@app.route('/trigger-event', methods=['POST'])
def trigger():
    print("inside trigger-event")
    payload = request.data.decode('utf-8')
    print("after payload")
    payloadObj = json.loads(payload)
    print("after payloadObj")
    data = payloadObj
    print("after data")
    customWeb3.insertEventInSmartContract(data)
    # customWeb3.updateHash(data)
    return "ok ji"


# @app.route('/interactTest', methods=['GET'])
# def interactTest():
#     customWeb3.insertEventInSmartContract()
#     return "ok ji"

@app.route('/getData', methods=['POST'])
def getData():
    dbID = request.form.get('dbID')
    finalData,urlsList = customWeb3.retrieveBlockChainData(dbID)
    return render_template('showData.html',messages={"data":finalData,"urlsList":urlsList,"loggedIn": True if "email" in session else False})


# @app.route('/clearData', methods=['GET'])
# def clearData():
#     customWeb3.clearBlockChainData()
#     return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)