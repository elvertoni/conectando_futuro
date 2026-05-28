from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'city', 'state', 'is_active', 'expires_at', 'created_at')
    list_filter = ('job_type', 'is_active', 'state', 'source')
    search_fields = ('title', 'company', 'description', 'city', 'area')
    ordering = ('-created_at',)
