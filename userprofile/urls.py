from .views import CreateProfile
from .views import LoadProfile
from django.urls import path, include

urlpatterns = [
    path('api/createprofile/', CreateProfile, name='CreateProfile'),
    path('api/loadprofile/', LoadProfile, name='LoadProfile'),
]