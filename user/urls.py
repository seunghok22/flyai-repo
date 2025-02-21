from django.urls import path
from .views import google_login
from .views import google_callback

urlpatterns = [
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
]