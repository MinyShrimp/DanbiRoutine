from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key = True)
    title       = models.CharField(max_length = 100)
    created_at  = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed  = False
        db_table = 'category'