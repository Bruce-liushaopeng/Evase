from flask import Flask, request, jsonify
from flask_cors import CORS
from vul import newUserToDB, getUserFromDB
app = Flask(__name__)
CORS(app)

@app.route('/addUser', methods=['POST'], strict_slashes=False)
def addUser():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    print(firstName, lastName)
    response = newUserToDB(firstName, lastName)
    return response

@app.route('/getUser', methods=['GET'], strict_slashes=False)
def getUser():
    firstName = request.json['firstName']
    response = getUserFromDB(firstName)
    return response
