__author__ = 'amit1.nagar'

import unittest
from django.test import Client

# This is the Test case for JSON GET Request from Access Control Module
class HttpJsonTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_fetchAllPermission(self):
        # Issue a GET request.
        response = self.client.get('/account/fetchAllPermission')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the response content-type is Json.
        self.assertEqual(response.get('Content-Type'), 'application/json')

    def test_fetchall_user(self):
        response = self.client.get('/account/fetch_all_user')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/json')

    def test_getall_user_details(self):
        response = self.client.get('/account/get_all_user_details')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/json')

    def test_getall_role_details(self):
        response = self.client.get('/account/get_all_role_details')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/json')

    def test_fetchAllRole(self):
        response = self.client.get('/account/fetchAllRole')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/json')
