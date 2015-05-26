import cherrypy
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
        """ Takes a channel anda message id. Checks validity of channel against channel service.
        submits to data store and responds. TODO: Implement channel service check. """

        r_root = {"msg_read_response": {"response_message": '', "response_code": 1 }}
        r_msg_read = r_root["msg_read_response"]

        try:
            msgs = self.mc.find({"message_id": {"$gt": int(message_id)}, "channel_id": int(channel_id)})
            if msgs.count() == 0:
                 r_msg_read["response_message"] = "No messages match query"
            else:
                r_msg_read["response_code"] = 0
                r_msg_read["response_message"] = "Messages returned successfully"
                r_root["messages"] = dumps(msgs)
        except:
            r_msg_read["response_message"] = "Cannot query database"
        return r_root

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        """ Takes a new message store request, validates against channel service, validates json
        contents, submits to database and responds. TODO: Refactor, implemented channel serv check"""

        r_root = {"new_msg_response": {"response_code": 1, "response_message": "" }}
        r_new = r_root["new_msg_response"]

        root_dict = cherrypy.request.json

        if self.valid_json(root_dict):
            msg_dict = root_dict["message"]
            # Crude way to number messages for now
            new_id = self.mc.count({"channel_id": msg_dict["channel_id"]}) + 1
            msg_dict["message_id"] = new_id
            
            try:
                self.mc.insert_one(msg_dict)
                r_new["response_code"] = 0
                r_new["response_message"] = "Message entered sucessfully"
                r_new["message_id"] = new_id

            except:
                r_new["response_message"] = "Error executing query"
        else:
            r_new["response_message"] = "JSON Payload Invalid"

        return r_root

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self):
        pass

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def DELETE(self):
        pass

    # Just check to make sure all fields are present for now
    def valid_json(self, req_dict):
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
