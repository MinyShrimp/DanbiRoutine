from django.db import models
from ..Codes import MSG_STATUS

# Create your models here.
class Message(models.Model):
    msg    = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    @staticmethod
    def getByCode(code: str):
        return Message(msg=MSG_STATUS[code], status=code)