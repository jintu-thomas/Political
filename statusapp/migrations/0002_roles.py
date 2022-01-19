# Generated by Django 4.0.1 on 2022-01-13 08:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('statusapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('primary_key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role_name', models.CharField(default='Role', max_length=128)),
                ('status', models.BooleanField(default=True)),
                ('added_by', models.CharField(blank=True, max_length=128, null=True)),
                ('added_datetime', models.DateTimeField(blank=True, null=True)),
                ('updated_datetime', models.DateTimeField(blank=True, null=True)),
                ('department_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statusapp.departments')),
            ],
        ),
    ]
