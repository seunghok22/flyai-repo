from .models import JsonHandle
from rest_framework import serializers

class JsonHandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonHandle
        fields = (
                'id',
                'js'
                )
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        return JsonHandle.object.create(**validated_data)

    def update(self, instance, validated_data):
        instance.js = validated_data,get('js', instance.js)
        instance.save()
        return instance
