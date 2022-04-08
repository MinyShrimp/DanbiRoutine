from django.db import models

class RoutineDay(models.Model):
    day            = models.CharField(max_length = 100)
    routine_id     = models.PositiveIntegerField(primary_key=True)
    created_at     = models.DateTimeField()
    modified_at    = models.DateTimeField(auto_now = True)

    class Meta:
        managed  = False
        db_table = 'routine_day'