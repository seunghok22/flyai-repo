from .models import UserProfile
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'userID',
            'voiceVector',
            'accountID',
            'category',
            'description',
            'tags',
            'recentChats',
            'prefor',
            'additionalInfo',
            'characterstics',
        )
        read_only_fields = ('userID',)

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.voiceVector = validated_data.get('voiceVector',instance.voiceVector)
        instance.accountID = validated_data.get('accountID', instance.accountID)
        instance.description = validated_data.get('description', instance.description)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.recentChats = validated_data.get('recentChats', instance.recentChats)
        instance.prefor = validated_data.get('prefor', instance.prefor)
        instance.additionalInfo = validated_data.get('additionalInfo', instance.additionalInfo)
        instance.characterstics = validated_data.get('characterstics', instance.characterstics)
        instance.save()
        return instance
