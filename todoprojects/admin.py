from django.contrib import admin
from .models import Project, ProjectMember, ProjectTable, ProjectTask


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


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('assigned_to', 'project_table', 'title', 'date_time', 'done')
    list_filter = ('assigned_to', 'project_table', 'date', 'done')
    search_fields = ('assigned_to__username', 'project_table__name', 'title', 'description')

    def date_time(self, obj):
        return f"{obj.date} {obj.hour.strftime('%H:%M')}"

    date_time.admin_order_field = 'date' 