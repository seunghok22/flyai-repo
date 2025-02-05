from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BreweryViewSet, TraditionalLiquorViewSet

router = DefaultRouter()
router.register(r'breweries', BreweryViewSet)
router.register(r'traditional-liquors', TraditionalLiquorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]