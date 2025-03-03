from django.contrib import admin

from .models import Slip


@admin.register(Slip)
class SlipAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'json_preview', 'created_at', 'updated_at')
    search_fields = ('id', 'wallet__name')
    list_filter = ('wallet', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 100

    def json_preview(self, obj):
        return str(obj.json_result)[:100] + '...' if len(str(obj.json_result)) > 100 else obj.json_result
    json_preview.short_description = 'JSON Preview'