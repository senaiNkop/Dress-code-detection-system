from django.contrib import admin
from .models import DataModel


# Register your models here.
@admin.register(DataModel)
class DataModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'category', 'sex', 'no_of_images')
    list_filter = ('sex', 'category')
