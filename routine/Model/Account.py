from django.db import models
from .Message  import Message

# Create your models here.
class Account(models.Model):
    data    = models.JSONField()
    message = Message()