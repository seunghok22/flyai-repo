# Generated by Django 5.1.2 on 2025-02-26 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_userprofile_imageurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='characterstics',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='imageUrl',
        ),
    ]
