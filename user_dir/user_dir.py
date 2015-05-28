from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import sys
import cherrypy
lib_path = '..'
sys.path.append(lib_path)
import slacker_config

from user_dir_model import User, Base

engine = create_engine('sqlite:///sqlalchemy_users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
session = DBSession()

# Author: Matt Ankerson
# Date: 28 May 2015

# This is a micro-service intended to recieve and store new users, and validate existing user
# credentials.

class UserDirectory(object):
    exposed = True  # expose all methods
    
    # Add a new user to the db
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        raw_user = cherrypy.request.json  # get the new user
        new_user = User(email = raw_user['email'], password = raw_user['password'], screen_name = raw_user['screen_name'])
        # we should only add this user if a user with the same email doesn't already exist.
        # implement query for existing user here...
        session.add(new_user)
        session.commit()        # can we get a response from sqlalchemy?
        return {'response': 'success'}  # assume success for now.
        
    # Accept an email and a password
    #   Indicate whether or not the user exists (based on email)
    #   Indicate whether or not the password matches the email
    @cherrypy.tools.json_out()
    def GET(self, email="", password=""):
        # query the sqlite db to find out if this email already exists
        
# switch from the default mechanism of matching URLs to methods
# for one that is aware of the whole HTTP method shenanigan with: MethodDispatcher()
if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        }
    }
    
    cherrypy.config.update({'server.socket_port' : slacker_config.urls.port['user_directory']})
    cherrypy.quickstart(UserDirectory(), '/', conf)
        
          