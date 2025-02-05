from django.db import models


def get_image_upload_path(instance, filename):
    return f'post/images/{instance.id}/{filename}'
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)
    category = models.IntegerField()
    readTime = models.IntegerField()
    body = models.JSONField()
    thumbnail = models.ImageField(upload_to=get_image_upload_path)
    slug = models.SlugField(max_length=100, unique=True)
    def __str__(self):
        return self.title
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

# class A(models.Model):
# = 모델 A 생성 (테이블)

    # readTime = models.IntegerField()
    # body = models.JSONField()
    # thumbnail = models.ImageField(upload_to=get_image_upload_path)
    # slug = models.SlugField(max_length=100, unique=True)
    # = column 생성

# if 모델을 생성하고 싶다?
# 메서드로 
