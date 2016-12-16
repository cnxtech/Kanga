from django.test import TestCase
from account.services import UserService
from django.contrib.auth.models import User
from sets import Set

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


