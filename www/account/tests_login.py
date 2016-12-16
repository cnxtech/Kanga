__author__ = 'SRIN'

from django.contrib.auth.models import User

from django.test import Client
from django.test import TestCase

class LoginTest(TestCase):

    def setUp(self):
        User.objects.create_user('b_santoso', 'b_santoso@samsung.com', 'secret')
        self.client = Client()

    def testLogin(self):
        login = self.client.login(username = 'b_santoso', password = 'secret')
        print "Login: {}".format(login)
        self.assertTrue(login)