from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Cnword(models.Model):
    # 词,解释,全拼
    words = models.CharField(max_length=255, blank=True)
    explain = models.TextField()
    searchcount = models.IntegerField(default=0, verbose_name='查询次数')

    class Meta:
        db_table = 'cnword'
        ordering = ('-searchcount',)  # 按照查询次数排序
    def __unicode__(self):
        return self.words
