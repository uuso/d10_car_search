from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'vendor', 'model', 'gearbox', 'web_color')
