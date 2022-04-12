from django.db import models
from django.db.models.deletion import DO_NOTHING
from routine.Model.Routine import Routine
from routine.Model.RoutineResult import RoutineResult

class RoutineDay(models.Model):
    day            = models.CharField(primary_key = True, max_length=10)
    routine        = models.ForeignKey(Routine, on_delete = DO_NOTHING)
    created_at     = models.DateTimeField()
    modified_at    = models.DateTimeField()

    class Meta:
        managed  = False
        db_table = 'routine_day'