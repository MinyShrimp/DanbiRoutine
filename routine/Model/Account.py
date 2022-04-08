from django.db import models

# Create your models here.
class Account(models.Model):
    account_id   = models.AutoField(primary_key=True)
    email        = models.CharField(max_length=100)
    pwd          = models.BinaryField()
    salt         = models.BinaryField()
    is_login     = models.PositiveSmallIntegerField(default=0)
    is_deleted   = models.PositiveSmallIntegerField(default=0)
    created_at   = models.DateTimeField()
    login_at     = models.DateTimeField()
    logout_at    = models.DateTimeField()
    modified_at  = models.DateTimeField(auto_now=True)

    class Meta:
        managed  = False
        db_table = 'account'