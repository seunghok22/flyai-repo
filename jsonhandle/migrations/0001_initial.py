# Generated by Django 5.1.2 on 2025-02-27 02:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JsonHandle',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('js', models.JSONField(default=dict)),
            ],
            options={
                'db_table': 'json_handle',
            },
        ),
    ]
