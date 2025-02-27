from .models import Character
from rest_framework import serializers

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = (
                'userID',
                'characteristics',
                'imageUrl'
                )
        read_only_fields = ('userID',)

    def create(self, validated_data):
        return Character.object.create(**validated_data)

    def update(self, instance, validated_data):
        instance.characteristics = validated_data.get('characteristics', instance.characteristics)
        instance.imageUrl = validated_data.get('imageUrl', instance.imageUrl)
        instance.save()
        return instance
