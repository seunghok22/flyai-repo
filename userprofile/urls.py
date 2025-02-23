from .views import *
from django.urls import path, include

urlpatterns = [
    path('api/createprofile/', CreateProfile, name='CreateProfile'),
    path('api/loadprofile/', LoadProfile, name='LoadProfile'),
    path('api/loadprofilelist/', LoadProfileList, name='LoadProfileList'),
    path('api/deleteprofile/', DeleteProfile, name='DeleteProfile'),
    path('api/updateprofile/', UpdateProfile, name='UpdateProfile'),
    path('api/loadfromcategory/', LoadFromCategory, name='LoadFromCategory'),
]