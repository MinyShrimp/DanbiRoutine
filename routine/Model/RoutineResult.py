from django.db import models
from django.db.models.deletion import CASCADE

from routine.Model.Result  import Result
from routine.Model.Routine import Routine

class RoutineResult(models.Model):
    routine_result_id = models.AutoField(primary_key = True)
    routine           = models.OneToOneField(Routine, on_delete = CASCADE)
    result            = models.OneToOneField(Result, on_delete = CASCADE)
    is_deleted        = models.SmallIntegerField()
    created_at        = models.DateTimeField()
    modified_at       = models.DateTimeField()

    class Meta:
        managed  = False
        db_table = 'routine_result'