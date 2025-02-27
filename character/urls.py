from django.urls import path
from .views import process_image
from .views import LoadCharacter

urlpatterns = [
    path('api/process-image/', process_image, name='process_image'),
    path('api/loadcharacter/', LoadCharacter, name='LoadCharacter'),
]

