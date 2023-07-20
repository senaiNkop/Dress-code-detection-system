from django.contrib import admin

# Register your models here.
from .models import DataAnalysis


@admin.register(DataAnalysis)
class DataAnalysisAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_date')
    list_filter = ('title', )
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('title', 'published_date')
