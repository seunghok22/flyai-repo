from .views import CreateProfile
from .views import LoadProfile
from .views import LoadProfileList
from django.urls import path, include

urlpatterns = [
    path('api/createprofile/', CreateProfile, name='CreateProfile'),
    path('api/loadprofile/', LoadProfile, name='LoadProfile'),
    path('api/loadprofilelist/', LoadProfileList, name='LoadProfileList'),
]