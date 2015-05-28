import unittest
import requests
import json
import sys
lib_path = '..'
sys.path.append(lib_path)
import slacker_config

# Author: Matt Ankerson
# Date: 28 May 2015


class UserDirTest(unittest.TestCase):
    
    def setUp(self):
        self.service_url = slacker_config.urls.url['user_directory'] + ":" + str(slacker_config.urls.port['user_directory'])
        self.heads = {'Content-Type': 'application/json'}
        self.good_user = {'email': 'yogi@bear', 'password': 'yellowstone', 'screen_name': 'picnic_baskets'}
        self.addition_success = {'response': 'success'}
        
    def test_post(self):
        good_user_result = requests.post(self.service_url, data=json.dumps(self.good_user), headers=self.heads).json()
        self.assertDictEqual(good_user_result, self.addition_success)
        
if __name__ == '__main__':
    unittest.main()