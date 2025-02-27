from django.urls import path
from .views import SaveJson, LoadJson

urlpatterns = [
    path('api/save', SaveJson, name='SaveJson'),
    path('api/load', LoadJson, name='LoadJson'),
]
