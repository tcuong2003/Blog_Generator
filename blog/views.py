from django.shortcuts import render, redirect
from .models import BlogPost


def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "blog_list.html", {'blog_articles': blog_articles})

def blog_detail(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request, 'blog_detail.html', {'blog_article_detail': blog_article_detail})
    else:
        return redirect('/')