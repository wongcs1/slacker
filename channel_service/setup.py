__author__ = 'alexmcneill'
import cherrypy
from pymongo import MongoClient

client = MongoClient()

db = client["channel_db"]

test_channel = {"_id": 1, "name": "channel1", "owner": 1}

channels = db.channels
new_channel_id = channels.insert_one(test_channel).inserted_id

print(channels.find_one({"_id": new_channel_id}))