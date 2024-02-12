from django.db import models


class WeightRecord(models.Model):
    user_id = models.CharField(max_length=100)
    weight = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
