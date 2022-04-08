from django.db import models

class Routine(models.Model):
    routine_id   = models.AutoField(primary_key = True)
    account_id   = models.PositiveIntegerField()
    category_id  = models.PositiveIntegerField()
    title        = models.CharField(max_length = 100)
    is_alarm     = models.PositiveSmallIntegerField()
    is_deleted   = models.PositiveSmallIntegerField()
    created_at   = models.DateTimeField()
    modified_at  = models.DateTimeField(auto_now = True)

    class Meta:
        managed  = False
        db_table = 'routine'