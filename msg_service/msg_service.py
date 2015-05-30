import cherrypy
from msg_service_dicts import msg_response, msg_store
from bson.json_util import dumps
from pymongo import MongoClient

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

        if not self.valid_json(req_dict):
            r_msg = "JSON payload invalid"
            return msg_store(r_msg, 1)

        try:
            self.mc.insert_one(msg_dict)
            new_id = self.mc.count({"channel_id": msg_dict["channel_id"]}) + 1  # crude
        except:
            return msg_store("Error executing query", 1)
        else:
            return msg_store("Message enterred successfully", 0, new_id)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self):
        pass

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def DELETE(self):
        pass

    def valid_json(self, req_dict):
        """ Checks all required fields present in message store request """
        if 'message' in req_dict:
            if all (k in req_dict['message'] for k in ("channel_id", "user_id", "body", "timestamp")):
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
    cherrypy.server.socket_host = 'meat.stewpot.nz'
    cherrypy.quickstart(app, '/', conf)
