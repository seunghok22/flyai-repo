from rest_framework import serializers
from .models import Video, VideoTag

class VideoCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False
    )
    
    class Meta:
        model = Video
        fields = [
            'id',
            'liquor',
            'title',
            'video_url',
            'thumbnail_url',
            'duration',
            'tags'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        video = Video.objects.create(**validated_data)
        
        # Create tags
        VideoTag.objects.bulk_create([
            VideoTag(video=video, tag_name=tag)
            for tag in tags
        ])
        
        return video

class VideoListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = [
            'id',
            'liquor',
            'title',
            'video_url',
            'thumbnail_url',
            'duration',
            'tags',
            'created_at'
        ]
    
    def get_tags(self, obj):
        return obj.tags.values_list('tag_name', flat=True)