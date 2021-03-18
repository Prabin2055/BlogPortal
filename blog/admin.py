from django.contrib import admin
from .models import *

admin.site.register((BlogPost, BlogComment))
admin.site.register(Category)

