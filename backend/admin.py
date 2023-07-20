from django.contrib import admin
from .models import Backend


# Register your models here.
@admin.register(Backend)
class BackendAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    list_filter = ('title', )