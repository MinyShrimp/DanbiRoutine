from django.test import TestCase
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

class AuthoTest(TestCase):
    def test_autho(self):
        data = { "access_token": "" }
        
        autho = str( JWTAuthentication().get_validated_token( data["access_token"] ) )
        self.assertEqual( autho, data["access_token"] )
