from django.db import models

from django.db.models.deletion import CASCADE

from routine.Model.Account import Account
from routine.Model.Category import Category

class Routine(models.Model):
    routine_id   = models.AutoField(primary_key = True)
    account      = models.OneToOneField(Account, on_delete=CASCADE)
    category     = models.OneToOneField(Category, on_delete=CASCADE)
    title        = models.CharField(max_length = 100)
    is_alarm     = models.SmallIntegerField()
    is_deleted   = models.SmallIntegerField()
    created_at   = models.DateTimeField()
    modified_at  = models.DateTimeField()

    class Meta:
        managed  = False
        db_table = 'routine'
        