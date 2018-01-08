from rest_framework.test import APIClient, APITestCase
from rest_framework import status, exceptions
from rest_framework.reverse import reverse
from mongoengine.errors import DoesNotExist

from .models import *


def create_superuser():
    """
    Creates and retuns a superuser - instance of settings.MONGOENGINE_USER_DOCUMENT
    """
    new_admin = User(
        username="admin",
        email="admin@example.com",
        first_name="admin",
        last_name="nimda",
        is_active=True,
        is_staff=True
    )
    new_admin.set_password('foobar')
    new_admin.save()
    return new_admin


def create_user():
    """
    Creates and returns a regular user - object of settings.MONGOENGINE_USER_DOCUMENT
    """
    new_user = User(
        username="testuser",
        email="testuser@test.com",
        first_name="test",
        last_name="user",
        bio="A funny guy!",
        is_active=True,
        is_staff=False
    )
    new_user.set_password('foobar')
    new_user.save()
    return new_user


class UserViewTest(APITestCase):
    def setUp(self):
        self.new_user = create_user()
        self.superuser = create_superuser()
        self.url = reverse("rest-auth:user_profile")
        
        self.auth_header = "Token 2c7e9e9465e917dcd34e620193ed2a7447140e5b"
        self.token = Token.objects.create(key='2c7e9e9465e917dcd34e620193ed2a7447140e5b', user=self.new_user)
    
    def doCleanups(self):
        #self.new_user.delete()
        #token.delete()
        
        User.drop_collection()
        Token.drop_collection()
        
    def test_get_unauthorized(self):
        c = APIClient()
        
        response = c.post(self.url)
        print (response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_read_user_info(self):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION = self.auth_header)
        response = c.get(self.url)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_existing_username(self):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=self.auth_header)
        fresh_updates = {"username":"admin","first_name":"fresh_firstname","last_name":"mimi"\
                            ,"bio":"fresh bio my friend", "email":"fresh_email@gmail.com"}
        response = c.put(self.url, fresh_updates)
        print (response.content, response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_existing_email(self):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=self.auth_header)
        fresh_updates = {"username":"freshuser","first_name":"fresh_firstname","last_name":"mimi"\
                            ,"bio":"fresh bio my friend", "email":"admin@example.com"}
        response = c.put(self.url, fresh_updates)
        print (response.content, response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #TODO: add unique emails to the DB
    
class PasswordChangeViewTest(APITestCase):
    def setUp(self):
        self.new_user = create_user()
        self.url = reverse("rest-auth:pwd_change")
        
        self.auth_header = "Token 2c7e9e9465e917dcd34e620193ed2a7447140e5b"
        self.token = Token.objects.create(key='2c7e9e9465e917dcd34e620193ed2a7447140e5b', user=self.new_user)
    
    def doCleanups(self):
        #self.new_user.delete()
        #token.delete()
        
        User.drop_collection()
        Token.drop_collection()

    def test_old_password(self):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=self.auth_header)
        data = {"old_password":"oldpwd", "new_password1":"azerty123", "new_password2":"azerty123"}
        response = c.post(self.url, data)
        print (response.content, response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_new_password_no_match(self):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=self.auth_header)
        data = {"old_password":"foobar", "new_password1":"azerty", "new_password2":"azdqsd"}
        response = c.post(self.url, data)
        print (response.content, response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_new_password_constraints(self):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=self.auth_header)
        data = {"old_password":"foobar", "new_password1":"azerty1", "new_password2":"azerty1"}
        response = c.post(self.url, data)
        print (response.content, response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_everything_is_ok(self):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=self.auth_header)
        data = {"old_password":"foobar", "new_password1":"azerty123", "new_password2":"azerty123"}
        response = c.post(self.url, data)
        print (response.content, response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.new_user = User.objects.get(username=self.new_user.username)
        # Check if password edited
        if self.new_user.check_password("azerty123"): print ("Password did change.")
        else:
            print ("Something went wrong, password has not been changed.")
        
class SignUpTest(APITestCase):
    def setUp(self):
        self.new_user = create_user()
        self.url = reverse("rest-auth:signup")
        
    def doCleanups(self):
        User.drop_collection()
        Token.drop_collection()
        EmailValidationToken.drop_collection()
    
    def test_signup(self):
        c = APIClient()
        my_user_data = {"username": "Mehdi6", "email":"mehdiessebbar@gmail.com", "password1": "azerty123", "password2":"azerty123"}
        response = c.post(self.url, my_user_data)
        print ("test_signup\n", response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        try:
            usr = User.objects.get(username="Mehdi6")
        except DoesNotExist:
            print ("User was not created")
        
    def test_signup_email_exist(self):
        c = APIClient()
        my_user_data = {"username": "Mehdi6", "email":"testuser@test.com", "password1": "azerty123", "password2":"azerty123"}
        response = c.post(self.url, my_user_data)
        print ("test_signup_email_exist", response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_signup_username_exist(self):
        c = APIClient()
        my_user_data = {"username": "testuser", "email":"mehdiessebbar@test.com", "password1": "azerty123", "password2":"azerty123"}
        response = c.post(self.url, my_user_data)
        print ("test_signup_username_exist",response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_signup_password_mismatch(self):
        c = APIClient()
        my_user_data = {"username": "mehdiess", "email":"mehdiessebbar@test.com", "password1": "azerty123", "password2":"blabla123"}
        response = c.post(self.url, my_user_data)
        print ("test_signup_password_mismatch", response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_signup_username_constraints(self):
        c = APIClient()
        my_user_data = {"username": "tt", "email":"mehdiessebbar@test.com", "password1": "azerty123", "password2":"blabla123"}
        response = c.post(self.url, my_user_data)
        print ("test_signup_username_constraints", response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
class LoginViewTest(APITestCase):
    def setUp(self):
        self.new_user = create_user()
        #self.superuser = create_superuser()
        self.url = reverse("rest-auth:login")
        
        self.auth_header = "Token 2c7e9e9465e917dcd34e620193ed2a7447140e5b"
        self.token = Token.objects.create(key='2c7e9e9465e917dcd34e620193ed2a7447140e5b', user=self.new_user)
    
    def doCleanups(self):
        #self.new_user.delete()
        #token.delete()
        
        User.drop_collection()
        Token.drop_collection()
        EmailValidationToken.drop_collection()
    
    def test_username_not_valid(self):
        c = APIClient()
        
        credentials = {"username":"resutset", "password":"foobar"}
        response = c.post(self.url, credentials)
        print ("test_username_not_valid", response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_email_is_valid(self):
        c = APIClient()
        
        credentials = {"username":"testuser", "password":"foobar"}
        response = c.post(self.url, credentials)
        print ("test_email_is_valid", response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_no_match(self):
        c = APIClient()
        
        credentials = {"username":"testuser", "password":"foo"}
        response = c.post(self.url, credentials)
        print ("test_password_no_match", response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login(self):
        c = APIClient()
        self.new_user.email_is_valid = True
        self.new_user.save()
        credentials = {"username":"testuser", "password":"foobar"}
        response = c.post(self.url, credentials)
        print ("test_login", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Same token
        self.assertEqual(response.content.decode('UTF-8'), r'{"token":"2c7e9e9465e917dcd34e620193ed2a7447140e5b"}')

class LogoutViewTest(APITestCase):
    def setUp(self):
        self.new_user = create_user()
        #self.superuser = create_superuser()
        self.url = reverse("rest-auth:logout")
        
        self.auth_header = "Token 2c7e9e9465e917dcd34e620193ed2a7447140e5b"
        self.token = Token.objects.create(key='2c7e9e9465e917dcd34e620193ed2a7447140e5b', user=self.new_user)
    
    def doCleanups(self):
        #self.new_user.delete()
        #token.delete()
        
        User.drop_collection()
        Token.drop_collection()
        EmailValidationToken.drop_collection()
    
    def test_logout(self):
        c = APIClient()
        
        response = c.get(self.url, HTTP_AUTHORIZATION=self.auth_header)
        print ("test_logout", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check if the token was deleted
        token = Token.objects.filter(user=self.new_user)
        self.assertEqual(str(token), str([]))
        
    