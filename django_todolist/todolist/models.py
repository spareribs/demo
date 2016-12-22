from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class Todolist(models.Model):
    body = models.CharField(max_length=1000)
    tag_type = models.IntegerField(default=0)
    add_date = models.DateTimeField()
