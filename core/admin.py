from django.contrib import admin
from .models import PrivateTask


@admin.register(PrivateTask)
class PrivateTaskAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'date_time', 'done')
    list_filter = ('owner', 'date', 'done')
    search_fields = ('owner__username', 'title', 'description')

    def date_time(self, obj):
        return f"{obj.date} {obj.hour.strftime('%H:%M')}"

    date_time.admin_order_field = 'date' 
    
