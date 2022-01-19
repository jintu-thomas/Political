from django.db import models
import uuid

# Create your models here.

class Party_Name(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    party_name = models.CharField(max_length=64, null=True, blank=True)
    party_image = models.FileField(upload_to='Political/User/party_images/', null=True, blank=True)
    status = models.BooleanField(default=True)
    added_datetime = models.DateTimeField(null=True, blank=True)
    updated_datetime = models.DateTimeField(null=True, blank=True)