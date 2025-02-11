from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import News

def is_news_editor(user):
    return user.groups.filter(name='News Editors').exists()


def news_list(request):
    news = News.objects.filter(is_active=True)
    return render(request, 'accounts/news.html', {'news': news})


@user_passes_test(is_news_editor)
def add_news(request):
    
    pass