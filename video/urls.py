from django.urls import path
from .views import VideoViewSet

urlpatterns = [
    path('videos/', VideoViewSet.as_view({'get': 'list'}), name='video-list'),
    path('videos/presigned-url/', VideoViewSet.as_view({'post': 'presigned_url'}), name='video-presigned-url'),
    path('videos/feed/', VideoViewSet.as_view({'get': 'feed'}), name='video-feed'),
]