from .models import Post, Category
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category_title = serializers.CharField(write_only=True, required=False)
    date = serializers.DateField(read_only=True)
    thumbnail = serializers.ImageField(max_length=None, use_url=True, required=False)
    class Meta:
        model = Post
        fields = ['id','title','thumbnail', 'excerpt', 'readTime', 'body', 'slug', 'category_title','date']

    def create(self, validated_data):
        category_title = validated_data.pop('category_title', None)
        if category_title:
            category, created = Category.objects.get_or_create(title=category_title)
            validated_data['category'] = category.id
        slug = validated_data.get('slug', None)
        slug = slug.replace(' ', '-').lower()
        slug = slug + '-' + category_title
        # Ensure the slug is unique
        original_slug = slug
        counter = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        print(slug)
        validated_data['slug'] = slug
        return Post.objects.create(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']