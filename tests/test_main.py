import os
import json
import unittest

# make the test secret available to main
os.environ['JWT_SECRET'] = 'abc123abc1234'
from src.flask import main


class TestEndpoints(unittest.TestCase):

    def setUp(self):
        main.APP.config['TESTING'] = True
        self.client = main.APP.test_client()
        self.email = 'wolf@thedoor.com'
        self.password = 'huff-puff'

    def test_health(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, 'Healthy')

    def test_auth(self):
        response = self.client.post(
            '/auth',
            data=json.dumps({'email': self.email, 'password': self.password}),
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json['token'])

    def test_use_token(self):
        # get token
        response = self.client.post(
            '/auth',
            data=json.dumps({'email': self.email, 'password': self.password}),
            content_type='application/json'
        )
        token = response.json['token']
        # use token for further access
        response = self.client.get(
            '/contents',
            headers={"Authorization": f"Bearer {token}"},
            content_type='application/json'
        )
        self.assertEqual("wolf@thedoor.com", response.json["email"])


if __name__ == "__main__":
    unittest.main()
