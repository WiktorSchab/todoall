from django.contrib import admin
from .models import Project, ProjectMember, ProjectTable


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'creation_date')
    search_fields = ('owner__username', 'name')

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')
    search_fields = ('user__username', 'project__name')

@admin.register(ProjectTable)
class ProjectTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'project')
    search_fields = ('name', 'project__name')