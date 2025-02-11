from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='news_images/', verbose_name='Изображение')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date_posted']

    def __str__(self):
        return self.title
    
    
def create_news_editor_group():
    
    news_editors, created = Group.objects.get_or_create(name='News Editors')
    
   
    content_type = ContentType.objects.get_for_model(News)
    news_permissions = Permission.objects.filter(content_type=content_type)
    
    
    news_editors.permissions.add(*news_permissions)
    return news_editors