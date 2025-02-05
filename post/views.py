from django.shortcuts import render
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer

from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

# Pagination class
class PostPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination

    # 추천 post list
    def recommend(self, request, *args, **kwargs):
        queryset = self.queryset.filter(category=2)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Create
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'Post created successfully', 'data': serializer.data})

    # Retrieve
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post_detail(self, request, slug=None, *args, **kwargs):
        instance = self.queryset.filter(slug=slug).first()
        if not instance:
            return Response({'error': 'Post not found'}, status=404)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Destroy
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Post deleted successfully'})

class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# 작성된 글이 많은 카테고리 순으로 4개 제공 + 이때 몇개의 글이 작성되었는지도 함께 제공
class CategoryDetail(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for category in data:
            category['post_count'] = Post.objects.filter(category=category['id']).count()
        return Response(data)