from django.contrib.auth.models import AbstractUser
from django.db import models
from liquor.models import TraditionalLiquor
from video.models import Video


class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)  # null과 blank를 True로 설정
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'


class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    category = models.CharField(max_length=100)
    preferences = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name}'s preferences"

    class Meta:
        db_table = 'user_preferences'


class LiquorRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    liquor = models.ForeignKey(
        TraditionalLiquor, 
        on_delete=models.CASCADE, 
        related_name='user_ratings'
    )
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}'s rating for {self.liquor.name}"

    class Meta:
        db_table = 'liquor_ratings'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    liquor = models.ForeignKey(
        TraditionalLiquor, 
        on_delete=models.CASCADE, 
        related_name='user_comments'
    )
    content = models.TextField()
    sentiment_score = models.IntegerField()
    keywords = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}'s comment on {self.liquor.name}"

    class Meta:
        db_table = 'comments'


class VideoInteraction(models.Model):
    INTERACTION_CHOICES = [
        ('view', 'View'),
        ('like', 'Like'),
        ('share', 'Share'),
        ('save', 'Save'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_interactions')
    video = models.ForeignKey(
        Video, 
        on_delete=models.CASCADE, 
        related_name='user_interactions'
    )
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_CHOICES)
    duration_watched = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}'s interaction with {self.video.title}"

    class Meta:
        db_table = 'video_interactions'