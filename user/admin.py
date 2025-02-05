from django.contrib import admin

# Register your models here.
from .models import User, UserPreference, LiquorRating, Comment
admin.site.register(User)
admin.site.register(UserPreference)
admin.site.register(LiquorRating)
admin.site.register(Comment)