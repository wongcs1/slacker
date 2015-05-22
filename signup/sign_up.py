import cherrypy
import requests

# Author: Matt Ankerson
# Date: 20 May 2015

# This is a micro-service intended to receive new details/credentials from a user
# and send them off to the user directory for storage.


class SignUpService(object):
    exposed = True  # expose all methods

    # Validate a new user. Validate any given fields, return an appropriate response
    @cherrypy.tools.json_out()
    def GET(self, email="", password="", screen_name=""):
        new_user = {'email': email, 'password': password, 'screen_name': screen_name}
        response = {'email': 'valid', 'password': 'valid', 'screen_name': 'valid'}  # Assume all valid
        for key, value in new_user.iteritems():
            if value == "":     # implement more complex criteria
                response[key] = "invalid"   # include more detailed errors
        return response

    # A sample request to the above ^^ function would be as follows:
    # r = s.get('http://127.0.0.1:8080/', params={'email':'yoyo@yoyo', 'password':'yoyo', 'screen_name':'yoyo'})

    # create a request to the user-directory module for storage of a new user
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        new_user = cherrypy.request.json()  # get the new user
        proceed = True                      # check the new user
        response = "{'response': 'user is invalid'}"
        user_assessment = self.GET(new_user['email'], new_user['password'], new_user['screen_name'])
        for key, value in user_assessment.iteritems():
            if value == 'invalid':
                proceed = False

        if proceed:
            heads = {'Content-Type': 'application/json'}
            response = requests.post("url to user directory", headers=heads, data=new_user).json()
        return response


# switch from the default mechanism of matching URLs to methods
# for one that is aware of the whole HTTP method shenanigan with: MethodDispatcher()
if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            # 'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        }
    }
    cherrypy.quickstart(SignUpService(), '/', conf)