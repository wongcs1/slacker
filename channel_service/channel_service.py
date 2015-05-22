__author__ = 'alexmcneill'
import cherrypy
from pymongo import MongoClient


class ChannelWebService:
    exposed = True

    def __init__(self):
        client = MongoClient()
        self.channel_db = client["channel_db"]

    @cherrypy.tools.json_out()
    def GET(self, channel_id):
        channel_id = int(channel_id)
        try:
            channel_json = self.get_channel_json(channel_id)
            return {"channel_read_response":
                        {
                            "response_code": 0,
                        },
                    "channel_data": channel_json
                    }
        except IndexError:
            return {"channel_read_response":
                        {
                            "response_code": 1,
                            "error": "No such channel"
                        },
                    }


    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        try:
            new_channel_json = cherrypy.request.json
            valid = self.check_valid_input(new_channel_json)

            already_exists = self.check_channel_exists(new_channel_json)
        except:
            #respond to if it fails by the input not being valid or the channel already exising
            pass

    def check_valid_input(self, channel_json):
        return False

    def get_channel_json(self, channel_id):
        channel = self.channel_db.find_one({"id": channel_id})

        if channel is None:
            raise IndexError
        else:
            return channel


if __name__ == '__main__':
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.response_headers.on": True,
            "tools.response_headers.headers": [("Content-Type", "application/json")]
            }
        }