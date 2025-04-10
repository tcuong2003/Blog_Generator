from django.urls import path
from . import views

app_name = 'blog_generator'

urlpatterns = [
    path('', views.blog_generator_form, name='blog_generator_form'),  # Trang chủ (http://127.0.0.1:8000/)
    # path('blog_generator/', views.blog_generator_form, name='blog_generator_home'),  # Fix lỗi 404 khi truy cập /blog_generator/
    path('generate-blog/', views.generate_blog, name='generate_blog'),
]
