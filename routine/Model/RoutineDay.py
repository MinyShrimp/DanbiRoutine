from django.db import models
from django.db.models.deletion import CASCADE
from routine.Model.Routine import Routine

class RoutineDay(models.Model):
    day            = models.CharField(max_length = 100, primary_key = True)
    routine        = models.OneToOneField(Routine, on_delete = CASCADE)
    created_at     = models.DateTimeField()
    modified_at    = models.DateTimeField()

    class Meta:
        managed  = False
        db_table = 'routine_day'