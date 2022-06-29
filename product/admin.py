from django.contrib import admin
from .models import BaseProducts, Products, Pictures, Materials, Creator, LargeCategory, SmallCategory, Seasons, SeasonsRelation

# Register your models here.
admin.site.register(
    [BaseProducts, Products, Pictures, Materials, Creator, LargeCategory, SmallCategory, Seasons, SeasonsRelation]
)