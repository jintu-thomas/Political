from __future__ import unicode_literals
from django.db import models

from django.db.models.fields import UUIDField
import uuid
# Create your models here.

class Departments(models.Model):
    primary_key = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    department_name = models.CharField(max_length=200,default='Department')
    status = models.BooleanField(default=True)
    added_by = models.CharField(max_length=128,null=True,blank=True)
    added_datetime = models.DateTimeField(null=True,blank=True)
    updated_datetime = models.DateTimeField(null=True,blank=True)

class Roles(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_name = models.ForeignKey(Departments, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=128, default='Role')
    status = models.BooleanField(default=True)
    added_by = models.CharField(max_length=128, null=True, blank=True)
    added_datetime = models.DateTimeField(null=True, blank=True)
    updated_datetime = models.DateTimeField(null=True, blank=True)

