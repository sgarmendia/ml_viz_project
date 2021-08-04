from flask import Flask, request, jsonify, Response
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import json_util, ObjectId

load_dotenv()

PORT=os.getenv('PORT') or 8000

ATLAS_USER=os.getenv('ATLAS_USER')
ATLAS_PASS=os.getenv('ATLAS_PASS')

mongo_url=f"mongodb+srv://{ATLAS_USER}:{ATLAS_PASS}@cluster0.vulo8.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(mongo_url)
db = cluster['sample_mflix']
movies = db['movies_short']

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_data():
    print('get')
    data = movies.find({}).limit(10)
    response = json_util.dumps(data)

    return Response(response, mimetype="application/json")

@app.route("/delete/<id>", methods=['DELETE'])
def delete(id):
    try:
        deleted = movies.delete_one({ '_id': ObjectId(id) })

        return f"{deleted.acknowledged}, {deleted.deleted_count}"
    except Exception as e:
        return jsonify({ 'error': str(e)}), 400

@app.route("/create", methods=['POST'])
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
    app.run(debug=True, port=PORT, host='0.0.0.0')