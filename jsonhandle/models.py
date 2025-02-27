from django.db import models
import uuid

# Create your models here.

class JsonHandle(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    js = models.JSONField(default=dict)
    class Meta:
        db_table = 'json_handle'

    def __str__(self):
        return str(self.id)
    def create(self, validated_data):
        json_handle = JsonHandle(**validated_data)
        json_handle.save()
        return json_handle

