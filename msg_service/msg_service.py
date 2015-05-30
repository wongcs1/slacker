import cherrypy
import requests
from msg_service_dicts import msg_response, msg_store
from bson.json_util import dumps
from pymongo import MongoClient
lib_path = '..'
sys.path.append(lib_path)
from slacker_config import url, port

class Root(object):

    @cherrypy.expose
    def index(self):
        return "Are you looking for /messages?"

class MessageService(object):
    exposed = True
    mc = MongoClient().message_database.messages

    @cherrypy.tools.json_out()
    def GET(self, message_id, channel_id):
        """ Takes a channel and a message id. Checks validity of channel against channel service.
        submits to data store and responds. TODO: Implement channel service check. """

        try:
            msgs = self.mc.find({"message_id": {"$gt": int(message_id)}, 
                "channel_id": int(channel_id)})
        except:
            return msg_response("Cannot query database", 1)
        else:
            if msgs.count() == 0:
                 return msg_response("No messages match query", 1)
            else:
                return msg_response("Messages returned successfully", 0, dumps(msgs))

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        """ Takes a new message store request, validates against channel service, validates json
        contents, submits to database and responds. TODO: Implement channel serv check"""

        req_dict = cherrypy.request.json
        msg_dict = req_dict["message"]

        if not self.valid_msg_json(req_dict):
            return msg_store("JSON payload invalid", 1)

        try:
            self.mc.insert_one(msg_dict)
            new_id = self.mc.count({"channel_id": msg_dict["channel_id"]}) + 1  # crude
        except:
            return msg_store("Error executing query", 1)
        else:
            return msg_store("Message entered successfully", 0, new_id)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self):
        pass

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def DELETE(self):
        """ Message deletion. Delete message according to supplied message and channel id.
        to delete all messages, check if "all" argument passed in message_id parameter """
        req_dict = cherrypy.request.json

        if not self.valid_del_json(req_dict):
            return msg_delete("JSON payload invalid", 1)
        
        q = {"channel_id": req_dict["channel_id"]}
        if req_dict["message_id"] != "all":
            q["message_id"] = req_dict["message_id"]

        try:
            self.mc.delete_many(q)
        except:
            return msg_delete("Error executing query", 1)
        else:
            return msg_delete("Messages deleted", 0)

    def valid_channel(self, channel_id):
        """ Check with channel service if channel id is valid"""
        host = url["channels"]
        hostport = port["channels"]

        r = requests.get("http://{0}:{1}/?channel_id={2}".format(host, hostport, channel_id))
        
        if r.json()['new_channel_response']['response_code'] == 0:
            return True
        return False

    def valid_msg_json(self, req_dict):
        """ Checks all required fields present in message store request """
        if 'message' in req_dict:
            if all (k in req_dict['message'] for k in ("channel_id", "user_id", "body", "timestamp")):
                return True
        return False

    def valid_del_json(self, req_dict):
        """ Checks all required fields present in deletion request """
        if all (k in req_dict for k in ("channel_id", "message_id")):
            return True
        return False

if __name__ == '__main__':
    conf = {
            '/messages': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                },
            '/': {
                }
            }
    app = Root()
    app.messages = MessageService()
    cherrypy.server.socket_host = url['messages']
    cherrypy.server.socket_port = port['messages']
    cherrypy.quickstart(app, '/', conf)
