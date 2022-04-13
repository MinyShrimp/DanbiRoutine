from django.db import models
from django.db.models.deletion import DO_NOTHING
from routine.Model.Routine import Routine

class RoutineDay(models.Model):
    day            = models.DateTimeField(primary_key = True)
    routine        = models.ForeignKey(Routine, on_delete = DO_NOTHING)
    created_at     = models.DateTimeField()
    modified_at    = models.DateTimeField()

    class Meta:
        managed  = False
        db_table = 'routine_day'