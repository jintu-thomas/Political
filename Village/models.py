from django.db import models
import uuid
from State.models import State_Name,Assembly_Name
from Mandal.models import Mandal_Name

# Create your models here.

class Village_Name(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state_name = models.ForeignKey(State_Name, on_delete=models.CASCADE)
    assembly_name = models.ForeignKey(Assembly_Name, on_delete=models.CASCADE)
    mandal_name = models.ForeignKey(Mandal_Name, on_delete=models.CASCADE)
    village_name = models.CharField(max_length=64, null=True, blank=True)
    status = models.BooleanField(default=True)
    added_datetime = models.DateTimeField(null=True, blank=True)
    updated_datetime = models.DateTimeField(null=True, blank=True)