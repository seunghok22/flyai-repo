from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class meta:
        model = User
        fields = ( )
    def create(self, validated_data):
        User = User(**validated_data)
        User.save()
        return User