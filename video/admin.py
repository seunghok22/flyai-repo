from django.contrib import admin

# Register your models here.
from .models import Video, VideoTag
admin.site.register(Video)
admin.site.register(VideoTag)