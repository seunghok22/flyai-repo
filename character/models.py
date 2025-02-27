from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.

class Character(models.Model):
    userID = models.TextField(
        primary_key=True,
    )
    imageUrl=models.TextField(
            blank =True,
            null=True,
            )
    characteristics=ArrayField(
        models.TextField(),
        blank=True,
        null=True
    )
    class Meta:
        db_table = 'character'
    def __str__(self):
        return str(self.userID)
    
    def create(self, validated_data):
        character = Character(**validated_data)
        character.save()
        return character
