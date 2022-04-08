from django.db import models

class RoutineResult(models.Model):
    routine_result_id = models.AutoField(primary_key = True)
    routine_id        = models.PositiveIntegerField()
    result_id         = models.PositiveIntegerField()
    is_deleted        = models.PositiveSmallIntegerField()
    created_at        = models.DateTimeField()
    modified_at       = models.DateTimeField(auto_now = True)

    class Meta:
        managed  = False
        db_table = 'routine_result'