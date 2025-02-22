from django.urls import path
from .views import AudioProcessView

urlpatterns = [
    path('api/process-audio/', AudioProcessView.as_view(), name='process_audio'),
]