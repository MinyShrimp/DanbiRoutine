from datetime import datetime
from django.db import models

class Account(models.Model):
    account_id   = models.AutoField(primary_key = True)
    email        = models.CharField(max_length = 100)
    pwd          = models.BinaryField()
    salt         = models.BinaryField()
    is_login     = models.SmallIntegerField(default = 0)
    is_deleted   = models.SmallIntegerField(default = 0)
    created_at   = models.DateTimeField()
    login_at     = models.DateTimeField()
    logout_at    = models.DateTimeField()
    modified_at  = models.DateTimeField(default = datetime.now())

    class Meta:
        managed  = False
        db_table = 'account'