from django.test import Client
from django.test import TestCase
from account.services import UserService, AuthService
from django.contrib.auth.models import User
from sets import Set
import unittest

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


# This is the Unit test case for User Service
class UserServiceTestCase(TestCase):

    # Setup the env and adding test user for testcase
    def setUp(self):
        user_service = UserService()
        user_service.addUser('update1', 'amit', 'amit1.nagar@samsung.com', 'amit')

    def test_addUser(self):
        user_service = UserService()
        self.assertEqual(user_service.addUser('test1', 'amit', 'amit1.nagar@samsung.com', 'amit'), 'user_added')

    def test_updateUser(self):
        user_service = UserService()
        role_list = []
        self.assertEqual(user_service.updateUser('update1', 'amit', 'amit1.nagar@samsung.com', 'amit', role_list), 'user_updated' )

    def test_recover_password(self):
        user = User.objects.get(username = 'update1')
        user_service = UserService()
        self.assertEqual(user_service.recoverPassword(user), 'recover_password_successful' )

    def test_getuser_permission(self):
        user_service = UserService()
        permisssion_list = Set()
        self.assertEqual(user_service.get_user_permission('update1'), permisssion_list )

class AuthServiceTestCase(TestCase):

    # Setup the env and adding test user for testcase
    def setUp(self):
        auth_service = AuthService()
        permission_list = []
        role_list = []
        auth_service.createRole('updaterol1', permission_list, role_list, 'FOTA', -1, 3,6,50,100,100, 'test','test')

    def test_add_role(self):
        print 'adding role....'
        auth_service = AuthService()
        permission_list = []
        role_list = []
        self.assertEqual(auth_service.createRole('testrole1', permission_list, role_list, 'FOTA', -1, 3,6,50,100,100, 'test','test'), 'role_added')

    def test_edit_role(self):
        print 'updating role....'
        auth_service = AuthService()
        permission_list = []
        role_list = []
        self.assertEqual(auth_service.editRole('updaterol1', permission_list, role_list, 'FOTA', -1, 3,6,50,100,100, 'test','test'), 'role_updated')
