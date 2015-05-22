__author__ = 'alexmcneill'

import unittest
import requests
import json

class ChannelServiceTests(unittest.TestCase):

    def setUp(self):
        self.service_url = "http://127.0.0.1:8080/"
        self.heads = {'Content-Type' : 'application/json'}

        #Variable's for testing the get channel
        self.valid_channel_id = 0
        self.invalid_channel_id = 43453

        self.valid_new_channel_json = {}
        self.invalid_new_channel_json = {}



    def test_get_channel(self):
        get_channel_response = requests.get('http://localhost:8080/?channel_id=0').json()

    def test_add_channel(self):
        add_channel_response = requests.post('http://localhost:8080/', headers=self.heads,
                      data=json.dumps(self.valid_new_channel_json))