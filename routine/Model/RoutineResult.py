from django.db import models

class RoutineResult(models.Model):
    routine_result_id = models.AutoField(primary_key = True)
    routine_id        = models.PositiveIntegerField()
    result_id         = models.PositiveIntegerField()
    is_deleted        = models.SmallIntegerField()
    created_at        = models.DateTimeField()
    modified_at       = models.DateTimeField()

    class Meta:
        managed  = False
        db_table = 'routine_result'