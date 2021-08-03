from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
from bson import json_util, ObjectId

url=f"mongodb+srv://sg-user:{'<password>'}@cluster0.vulo8.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(url)
db = cluster['sample_mflix']
movies = db['movies_short']

app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_data():
    data = movies.find({}).limit(10)
    response = json_util.dumps(data)

    return Response(response, mimetype="application/json")

@app.route("/delete/<id>", methods=['GET'])
def delete(id):
    try:
        deleted = movies.delete_one({ '_id': ObjectId(id) })

        return f"{deleted.acknowledged}, {deleted.deleted_count}"
    except Exception as e:
        return jsonify({ 'error': str(e)}), 400

@app.route("/create", methods=['POST', 'PUT'])
def create():
    try:
        data = request.json
        name = data['name']
        year = data['year']

        created = movies.insert_one({ "name":name, "year":year })

        return str(created.inserted_id)
    except Exception as e:
        return jsonify({ 'error': str(e)}), 400

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