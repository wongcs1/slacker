__author__ = 'alexmcneill'
import cherrypy
from pymongo import MongoClient


class ChannelWebService:
    exposed = True

    def __init__(self):
        client = MongoClient()
        self.channel_db = client["channel_db"]
        self.channel_collection = self.channel_db.channels

    @cherrypy.tools.json_out()
    def GET(self, channel_id):
        channel_id = int(channel_id)
        response_root = {"channel_read_response": {"response_message": '', "response_code": 1}}
        channel_read_response = response_root["channel_read_response"]

        try:
            channel_json = self.channel_collection.find_one({"_id": channel_id})
            if channel_json is None:
                channel_read_response["response_message"] = "No matching channel"
            else:
                channel_read_response["response_code"] = 0
                channel_read_response["response_message"] = "Channel found"
                response_root["channel"] = channel_json
        except:
            channel_read_response["response_message"] = "Unable to connect to database"

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):

        response_root = {"new_channel_response": {"response_message": '', "response_code": 1}}
        new_channel_response = response_root["new_channel_response"]

        try:
            new_channel_request = cherrypy.request.json

            channel_json = self.channel_collection.find_one({"name": new_channel_request["name"]})

            if channel_json is not None:
                new_channel_response["response_message"] = "There is already a channel by that name"
            else:
                latest_channel_json = self.channel_collection.find_one({"$query":{},"$orderby":{"_id":-1}})
                new_channel_id = 0
                if latest_channel_json is not None:
                    new_channel_id = latest_channel_json["_id"] + 1

                new_channel_json = {"_id": new_channel_id, "name": new_channel_request["name"], "owner": new_channel_request["owner"]}

                self.channel_collection.insert_one(new_channel_json)
                new_channel_response["response_code"] = 0
                new_channel_response["response_message"] = "Channel added"
        except KeyError:
            new_channel_response["response_message"] = "Invalid channel request"
        except:
            new_channel_response["response_message"] = "Unable to connect to database"

if __name__ == '__main__':
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.response_headers.on": True,
            "tools.response_headers.headers": [("Content-Type", "application/json")]
            }
        }
    cherrypy.config.update({'server.socket_port': 8000})
    cherrypy.quickstart(ChannelWebService(), '/', conf)