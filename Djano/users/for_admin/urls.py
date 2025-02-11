from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('news/', views.news_list, name='news'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)