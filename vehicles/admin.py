from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'year', 'make', 'model', 'fuel_type',
        'license_plate', 'current_mileage', 'updated_at'
    )
    list_filter = ('fuel_type', 'year', 'make')
    search_fields = ('name', 'make', 'model', 'license_plate', 'vin')
    date_hierarchy = 'purchase_date'
    fieldsets = (
        (None, {
            'fields': ('name', ('year', 'make', 'model'), 'fuel_type')
        }),
        ('Purchase Details', {
            'fields': (('purchase_price', 'purchase_date'),),
            'classes': ('collapse',)
        }),
        ('Identification', {
            'fields': (('license_plate', 'vin'),),
            'classes': ('collapse',)
        }),
        ('Mileage', {
            'fields': ('current_mileage',),
            'description': "This mileage is updated automatically by log entries."
        }),
    )
    readonly_fields = ('current_mileage',)