from django.contrib import admin
from .models import Resume, Education, WorkExperience

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'version', 'created_at', 'updated_at')
    inlines = [EducationInline, WorkExperienceInline]
    search_fields = ('user__email', 'user__full_name')
