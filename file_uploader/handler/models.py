# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="pictures/%Y/%m/%d")
    location_path = models.CharField(max_length=200)
    size = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
