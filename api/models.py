from django.db import models


class Task(models.Model):
    task_name = models.CharField(max_length=40)
    task_duration = models.DurationField()
    task_status = models.IntegerField(default=0)
    task_priority = models.IntegerField(default=3)
