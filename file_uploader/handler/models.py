# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=200)
    location_path = models.CharField(max_length=200)
    size = models.IntegerField(default=0)
