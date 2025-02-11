from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'is_active')
    list_filter = ('is_active', 'date_posted')
    search_fields = ('title', 'description')
    
    def has_add_permission(self, request):
        return request.user.groups.filter(name='News Editors').exists()
    
    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='News Editors').exists()
    
    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='News Editors').exists()