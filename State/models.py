from django.db import models
import uuid

# Create your models here.

class State_Name(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state_name = models.CharField(max_length=64, null=True, blank=True)
    state_code = models.CharField(max_length=16, null=True, blank=True)
    status = models.BooleanField(default=True)
    added_datetime = models.DateTimeField(null=True, blank=True)
    updated_datetime = models.DateTimeField(null=True, blank=True)

class Assembly_Name(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state_name = models.ForeignKey(State_Name, on_delete=models.CASCADE)
    assembly_name = models.CharField(max_length=64, null=True, blank=True)
    status = models.BooleanField(default=True)
    added_datetime = models.DateTimeField(null=True, blank=True)
    updated_datetime = models.DateTimeField(null=True, blank=True)