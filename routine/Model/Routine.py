from django.db import models

class Routine(models.Model):
    routine_id   = models.AutoField(primary_key = True)
    account_id   = models.PositiveIntegerField()
    category_id  = models.PositiveIntegerField()
    title        = models.CharField(max_length = 100)
    is_alarm     = models.SmallIntegerField()
    is_deleted   = models.SmallIntegerField()
    created_at   = models.DateTimeField()
    modified_at  = models.DateTimeField(auto_now = True)

    class Meta:
        managed  = False
        db_table = 'routine'