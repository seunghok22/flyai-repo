from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

class UserProfile(models.Model):
    category = ArrayField(
        models.TextField(max_length=20),
        blank=True,
        null=True
    )
    userID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    description= ArrayField(
        models.TextField(max_length=100),
        blank=True,
        null=True
    )
    tags= ArrayField(
        models.TextField(max_length=20),
        blank=True,
        null=True
    )
    recentChats= ArrayField(
        models.TextField(max_length=100),
        blank=True,
        null=True
    )
    prefor= ArrayField(
        models.TextField(max_length=100),
        blank=True,
        null=True
    )
    characterstics= ArrayField(
        models.TextField(),
        blank=True,
        null=True
    )
    additionalInfo = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return str(self.userID)
    
    def create(self, validated_data):
        user_profile = UserProfile(**validated_data)
        user_profile.save()
        return user_profile