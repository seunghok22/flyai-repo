# Generated by Django 5.1.2 on 2025-02-26 10:58

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_remove_userprofile_characterstics_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='characterstics',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None),
        ),
    ]
