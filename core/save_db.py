import pymongo
from bson.objectid import ObjectId
import datetime

class DB_CONNECT(object):
    def __init__(self, config: dict):
        self.config = config
        #self.timezone = datetime.datetime.strptime(self.config["timezone"], "%z").tzinfo
        self.db = self.db_init(self.config)

    def db_init(self, config):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = config["database"]["connection"]
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = pymongo.MongoClient(CONNECTION_STRING)
        return client

    def save_msg(self, msg):
        db = self.db
        db_connect = db[self.config["database"]["name"]]
        collection = db_connect[self.config["database"]["collections"]["comments"]]
        timestamp = datetime.datetime.now()
        msg["createdAt"] = timestamp
        msg["updateAt"] = timestamp
        res = collection.insert_one(msg)
        return res.inserted_id

    def update_msg(self, id, msg):
        filter = { '_id': ObjectId(id) }
        db = self.db
        db_connect = db[self.config["database"]["name"]]
        collection = db_connect[self.config["database"]["collections"]["comments"]]
        timestamp = datetime.datetime.now()
        newvalues = { "$set": { "comment": msg["comment"] , "sentiment":msg["sentiment"], "updateAt":timestamp} }
        collection.update_one(filter, newvalues)
        return id