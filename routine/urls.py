from random import random
from django.urls import path
from .View.SignUp import SignUp

urlpatterns = [
    #path('hello/', helloAPI),
    path('signUp/', SignUp)
]