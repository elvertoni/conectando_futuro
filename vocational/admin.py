from django.contrib import admin
from .models import Question, QuestionOption, VocationalProfile

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'text', 'created_at')
    list_display_links = ('text',)
    list_editable = ('order',)
    inlines = [QuestionOptionInline]
    ordering = ('order', 'id')

@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'value', 'order')
    list_display_links = ('text',)
    list_editable = ('order',)
    list_filter = ('question', 'value')
    ordering = ('question__order', 'order', 'id')

@admin.register(VocationalProfile)
class VocationalProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
