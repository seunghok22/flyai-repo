from rest_framework import serializers
from .models import Brewery, TraditionalLiquor

class BrewerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brewery
        fields = ['id', 'name', 'location', 'description', 'created_at']
        read_only_fields = ['created_at']

class TraditionalLiquorSerializer(serializers.ModelSerializer):
    brewery_name = serializers.CharField(source='brewery.name', read_only=True)
    
    class Meta:
        model = TraditionalLiquor
        fields = [
            'id', 'brewery', 'brewery_name', 'name', 'description',
            'characteristics', 'alcohol_percentage', 'price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']