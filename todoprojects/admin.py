from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'creation_date')
    search_fields = ('owner__username', 'name')