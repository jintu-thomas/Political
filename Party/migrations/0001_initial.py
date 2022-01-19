# Generated by Django 4.0.1 on 2022-01-18 10:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Party_Name',
            fields=[
                ('primary_key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('party_name', models.CharField(blank=True, max_length=64, null=True)),
                ('party_image', models.FileField(blank=True, null=True, upload_to='Political/User/party_images/')),
                ('status', models.BooleanField(default=True)),
                ('added_datetime', models.DateTimeField(blank=True, null=True)),
                ('updated_datetime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
