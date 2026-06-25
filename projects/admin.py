from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description', 'owner', 'created_at', 'github_url', 'status')
    list_editable = ('owner', 'github_url', 'status')
    filter_horizontal = ('participants',)
    search_fields = ('name',)
    list_filter = ('status',)
    empty_value_display = 'Не задано'
