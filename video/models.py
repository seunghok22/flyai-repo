from django.db import models
from liquor.models import TraditionalLiquor


class Video(models.Model):
    liquor = models.ForeignKey(
        TraditionalLiquor, 
        on_delete=models.CASCADE, 
        related_name='videos'
    )
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    thumbnail_url = models.URLField()
    duration = models.IntegerField(help_text="Duration in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'videos'


class VideoTag(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='tags')
    tag_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tag_name} for {self.video.title}"

    class Meta:
        db_table = 'video_tags'