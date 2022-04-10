from django.db import models
from django.db.models.deletion import CASCADE
from routine.Model.Routine import Routine
from routine.Model.RoutineResult import RoutineResult

class RoutineDay(models.Model):
    day            = models.DateTimeField(primary_key = True)
    routine        = models.ForeignKey(RoutineResult, on_delete = CASCADE)
    created_at     = models.DateTimeField()
    modified_at    = models.DateTimeField()

    class Meta:
        managed  = False
        db_table = 'routine_day'