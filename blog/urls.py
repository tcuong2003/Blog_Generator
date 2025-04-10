from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog-detail/<int:pk>/', views.blog_detail, name='blog_detail'),
]