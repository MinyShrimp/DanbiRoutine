from django.test import TestCase
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

class AuthoTest(TestCase):
    def test_autho(self):
        data = { "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NDIyMTY0LCJpYXQiOjE2NDk0MTQ5NjQsImp0aSI6IjVlMmFlNmY5OTAzNzQ3NTg4YmIxN2I3ZDk0Y2M1YTc1IiwiZW1haWwiOiJrc2s3NTg0QGdtYWlsLmNvbSJ9.hory5-sUWRy5vCssfs7Qopardc2gE-4-D0vVYt5OgGk" }
        
        autho = str( JWTAuthentication().get_validated_token( data["access_token"] ) )
        self.assertEqual( autho, data["access_token"] )
