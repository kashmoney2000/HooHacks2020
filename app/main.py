#!flask/bin/python
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import loads, dumps
import dns # required for connecting with SRV
from datetime import datetime

app = Flask(__name__)
client = MongoClient("mongodb+srv://root:aneeshisgay@cluster0-xubhe.mongodb.net/test?retryWrites=true&w=majority")  # host uri
db = client.HooHacks2020 # Select the database
homie_collection = db.Homie  # Select the collection name
updates_collection = db.Updates
donations_collection = db.Donations

@app.route('/api/donate', methods=['GET', 'POST']) #Donate
def donate():
	now = datetime.now()
	donations_collection.insert({"description": request.args.get("description"), "time": now, "amount": (int)(request.args.get("amount")), "donatorId": request.args.get("donator"), "homelessId": request.args.get("homeless")})
	return "Donated"

@app.route('/api/createUpdate', methods=['GET', 'POST']) #create Update
def createUpdate():
	now = datetime.now()
	req = request.form
	print(req)
	updates_collection.insert({"time": now, "userName": request.args.get("username"), "updateDescription": request.args.get("description"), "updatePicture": request.args.get("picture"), "updateVideo": request.args.get("video")})
	return "Created"

@app.route('/api/login', methods=['GET']) #login
def login():
	exists = homie_collection.find({'$and':[{"userName": request.args.get("username")}, {"password": request.args.get("password")}]},{"_id":0})
	task_list = []
	for task in exists:
		json_str = dumps(task)
		record2 = loads(json_str)
		task_list.append(record2)
	return jsonify(task_list)

@app.route('/api/registerDonator', methods=['GET', 'POST']) #register Donator
def registerDonator():
	exists = homie_collection.find({'$and':[{"userName": request.args.get("username")}, {"password": request.args.get("password")}]},{"_id":0})
	task_list = []
	for task in exists:
		json_str = dumps(task)
		record2 = loads(json_str)
		task_list.append(record2)
		break
	print(task_list)
	if len(task_list) == 0: 
		homie_collection.insert({"userName": request.args.get("username"), "password": request.args.get("password"), "gender": request.args.get("gender"),
			"firstName": request.args.get("firstName"), "lastName": request.args.get("lastName"), "phoneNumber": request.args.get("phoneNumber"), "userType": "Donator", "donations": []})
		return "Registered Donator"
	return "Fails"

@app.route('/api/registerHomeless', methods=['GET', 'POST']) #register homeless
def registerHomeless():
	exists = homie_collection.find({'$and':[{"userName": request.args.get("username")}, {"password": request.args.get("password")}]},{"_id":0})
	task_list = []
	for task in exists:
		json_str = dumps(task)
		record2 = loads(json_str)
		task_list.append(record2)
		break
	print(task_list)
	if len(task_list) == 0: 
		homie_collection.insert({"userName": request.args.get("username"), "password": request.args.get("password"), "gender": request.args.get("gender"),
			"firstName": request.args.get("firstName"), "lastName": request.args.get("lastName"), "phoneNumber": request.args.get("phoneNumber"), "userType": "Homeless", "Age": (int)(request.args.get("age")), "donations": [],
			"description": request.args.get("description"), "picture": request.args.get("picture"), "video": request.args.get("video"), "goal": request.args.get("goal"), "score": 100, "moneyRaised": 0, "numLikes":0})
		return "Registered Homeless"
	return "Fails"

@app.route('/api/getUpdateForUser', methods=['GET']) #gets the Cards for specified Homeless based on username
def get_Updates_for_User():
	all_tasks = updates_collection.find({"userName": request.args.get("username")},{"_id":0, "userName":0}).sort([("time", -1)])
	task_list = []
	for task in all_tasks:
		json_str = dumps(task)
		record2 = loads(json_str)
		task_list.append(record2)
	return jsonify(task_list)

@app.route('/api/getDonations', methods=['GET']) #gets the Donations for specified Homeless based on username
def get_Donations_for_User():
	all_tasks = donations_collection.find({'$or':[{"donatorId": request.args.get("username")}, {"homelessId": request.args.get("username")}]},{"_id":0}).sort([("time", -1)])
	#all_tasks = updates_collection.find({"homelessId": request.args.get("username")},{"_id":0})
	task_list = []
	for task in all_tasks:
		json_str = dumps(task)
		record2 = loads(json_str)
		task_list.append(record2)
	return jsonify(task_list)


@app.route('/api/getHomelessCard', methods=['GET']) #gets the Cards for specified Homeless based on username
def get_HomelessCard():
    all_tasks = homie_collection.find({"userName": request.args.get("username")},{"_id":0})
    task_list = []
    for task in all_tasks:
    	task_list.append({"name": task["firstName"]+task["lastName"], "description": task["description"], "moneyRaised": task["moneyRaised"],
    					"goal": task["goal"], "numLikes": task["numLikes"], "numKarma": task["score"], "picture": task["picture"]})
    return jsonify(task_list)

@app.route('/api/getUser', methods=['GET']) #gets a user based on username
def get_Homeless_Man():
    all_tasks = homie_collection.find({"userName": request.args.get("username")},{"_id":0})
    task_list = []
    for task in all_tasks:
    	json_str = dumps(task)
    	record2 = loads(json_str)
    	task_list.append(record2)
    	print(json_str)
    	print(record2)
    return jsonify(task_list)

@app.route('/api/getHomeless', methods=['GET']) #gets All the Homless 
def get_Homeless():
    all_tasks = homie_collection.find({"userType": "Homeless"},{"_id":0})
    task_list = []
    for task in all_tasks:
    	json_str = dumps(task)
    	record2 = loads(json_str)
    	task_list.append(record2)
    	print(json_str)
    	print(record2)
    return jsonify(task_list)


@app.route('/api/getDonators', methods=['GET']) #get all donators on platform
def get_Donators():
    all_tasks = homie_collection.find({"userType": "Donator"},{"_id":0})
    task_list = []
    for task in all_tasks:
    	json_str = dumps(task)
    	record2 = loads(json_str)
    	task_list.append(record2)
    	print(json_str)
    	print(record2)
    return jsonify(task_list)

@app.route("/", methods = ['GET', 'POST'])
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"


if __name__ == '__main__':
    app.run(debug=True)
