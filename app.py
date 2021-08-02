from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
from bson import json_util

url=f"mongodb+srv://sg-user:{'<password>'}@cluster0.vulo8.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(url)
db = cluster['sample_mflix']
movies = db['movies']

app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_data():
    data = movies.find({},{ "title", "year" }).limit(10)
    response = json_util.dumps(data)

    return Response(response, mimetype="application/json")

@app.route("/<id>", methods=['GET'])
def get_param(id):
    return f"Id is --> {id}"

@app.route("/create", methods=['POST', 'PUT'])
def create():
    data = request.json
    user = data['username']
    password = data['password']

    # save to mongo new user

    return f"New user {user} has been created"

@app.route("/args", methods=['GET'])
def get_args():
    return request.args

@app.errorhandler(404)
def page_not_found(error=None):
    response = jsonify({
        "message":f"Page {request.url} was not found, status 404"
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')