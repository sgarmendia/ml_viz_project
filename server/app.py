from flask import Flask, request, jsonify, Response
import os
from dotenv import load_dotenv

from utils.db import get_data_limit, get_unique, get_aggregate, get_by_field, delete_doc

load_dotenv()

PORT=os.getenv('PORT') or 8000

app = Flask(__name__)

@app.route("/data", methods=['GET'])
def get_data():
    limit = request.args.get('limit')
    try:
        response=get_data_limit(limit)
        return Response(response, mimetype="application/json")
    except Exception as e:
        return jsonify({ 'error': str(e)}), 400
    
@app.route("/aggregate", methods=['GET'])
def get_agg():
    name = request.args.get('field')
    try:
        response=get_aggregate(name)
        return Response(response, mimetype="application/json")
    except Exception as e:
        return jsonify({ 'error': str(e)}), 400

@app.route("/unique/<field>", methods=['GET'])
def get_unique_data(field):
    try:
        response=get_unique(field)
        return Response(response, mimetype="application/json")
    except Exception as e:
        return jsonify({ 'error': str(e)}), 400

@app.route("/by_field", methods=['GET'])
def get_by():
    try:
        field = request.args.get('field')
        name = request.args.get('name')

        response=get_by_field(field, name)
        return Response(response, mimetype="application/json")
    except Exception as e:
        return jsonify({ 'error': str(e)}), 400

# ------------------------ WIP ------------------------------

@app.route("/delete", methods=['DELETE'])
def delete():
    try:
        field = request.args.get('field')
        value = request.args.get('value')
        return delete_doc(field,value)
    except Exception as e:
        return jsonify({ 'error': str(e)}), 400

@app.route("/create", methods=['POST'])
def create():
    try:
        data = request.json
        return str(data)
    except Exception as e:
        return jsonify({ 'error': str(e)}), 400

# ------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(error=None):
    response = jsonify({
        "message":f"Page {request.url} was not found, status 404"
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True, port=PORT, host='0.0.0.0')