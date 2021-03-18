from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('blogComment/', views.blogComment, name="blogComment"),
    path('', views.blogHome, name="bloghome"),
    path('<str:slug>', views.blogPost, name="blogPost")
    ]