from django.contrib import admin
from .models import RegionModel

# Register your models here.
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region', 'number')
    
admin.site.register(RegionModel, RegionAdmin)