# Generated by Django 4.0.1 on 2022-01-18 10:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Mandal', '0001_initial'),
        ('State', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Village_Name',
            fields=[
                ('primary_key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('village_name', models.CharField(blank=True, max_length=64, null=True)),
                ('status', models.BooleanField(default=True)),
                ('added_datetime', models.DateTimeField(blank=True, null=True)),
                ('updated_datetime', models.DateTimeField(blank=True, null=True)),
                ('assembly_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='State.assembly_name')),
                ('mandal_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mandal.mandal_name')),
                ('state_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='State.state_name')),
            ],
        ),
    ]
