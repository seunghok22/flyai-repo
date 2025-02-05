from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Brewery, TraditionalLiquor
from .serializers import BrewerySerializer, TraditionalLiquorSerializer

class BreweryViewSet(viewsets.ModelViewSet):
    queryset = Brewery.objects.all()
    serializer_class = BrewerySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Brewery.objects.all()
        name = self.request.query_params.get('name', None)
        location = self.request.query_params.get('location', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

class TraditionalLiquorViewSet(viewsets.ModelViewSet):
    queryset = TraditionalLiquor.objects.all()
    serializer_class = TraditionalLiquorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TraditionalLiquor.objects.all()
        name = self.request.query_params.get('name', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    @action(detail=True, methods=['get'])
    def ingredients(self, request, pk=None):
        liquor = self.get_object()
        ingredients = liquor.ingredients.all()
        ingredient_data = [
            {
                'name': ingredient.name,
                'percentage': ingredient.percentage,
                'description': ingredient.description
            }
            for ingredient in ingredients
        ]
        return Response(ingredient_data)