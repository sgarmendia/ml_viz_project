import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import json_util

load_dotenv()

MONGO_URL=os.getenv('MONGO_URL')

cluster = MongoClient(MONGO_URL)
db = cluster['bdml_project_1']
inmigration_col = db['inmigration_bcn']

def get_data_limit(lim):
    limit = int(lim) if lim else 0
    data = inmigration_col.find({},{ '_id': 0}).limit(limit)
    return json_util.dumps(data)

def get_unique(field):
    data={}
    if field:
        data=inmigration_col.distinct(key=field)
    return json_util.dumps(data)

def get_aggregate(name):
    data=inmigration_col.aggregate([
        { '$group': { '_id': f'${name}', 'total': { '$sum': '$Number'} } },
        { '$sort': { 'total': -1 } }
    ])
    return json_util.dumps(data)

def get_by_field(field, value):
    data=inmigration_col.find({ field:value }, { '_id': 0 })
    return json_util.dumps(data)

def delete_doc(field, value):
    deleted = inmigration_col.delete_one({ field: value })
    return f"{deleted.acknowledged}, {deleted.deleted_count}"
    