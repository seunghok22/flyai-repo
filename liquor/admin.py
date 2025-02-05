from django.contrib import admin

# Register your models here.
from .models import Brewery, TraditionalLiquor, TopLiquor, LiquorIngredient
admin.site.register(Brewery)
admin.site.register(TraditionalLiquor)
admin.site.register(TopLiquor)
admin.site.register(LiquorIngredient)
