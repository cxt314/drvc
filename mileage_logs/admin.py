from django.contrib import admin
from django.db import models
from django.forms import Textarea, TextInput

# Import all models from the mileage_logs app
from .models import MonthlyMileageLog, MileageLogEntry, MileageClaim
# If you need to import Member, it's already used in MileageClaim, so it's implicitly there.
# from members.models import Member # Not strictly needed if only for admin configuration in this file

# --- Inlines ---

# Inline for MileageClaim within MileageLogEntry
class MileageClaimInline(admin.TabularInline):
    model = MileageClaim
    extra = 1
    fields = ('member', 'number_of_seats_claimed')
    #raw_id_fields = ('member',) # Use raw_id_fields if you have many members
    verbose_name = "Member Seat Claim" # Custom verbose name for the inline header
    verbose_name_plural = "Member Seat Claims"
    formfield_overrides = {
        models.PositiveIntegerField: {'widget': TextInput(attrs={'size': '5'})},
    }

# Inline for MileageLogEntry within MonthlyMileageLog
class MileageLogEntryInline(admin.TabularInline): # StackedInline gives more space, better for nested inlines
    model = MileageLogEntry
    extra = 1
    fields = ('entry_date',
               ('start_mileage', 'end_mileage'),
               'distance_traveled', # Readonly in the inline form
               'destination', 'purpose', 'is_long_distance',
               )
    readonly_fields = ('distance_traveled',) # distance_traveled is calculated
    show_change_link = True # Allow clicking to the full MileageLogEntry admin page (if registered independently)
                            # However, in your desired setup, it won't be, so this link won't work to an independent page.
                            # It's kept here for future flexibility if you re-register it.
    verbose_name = "Trip Entry"
    verbose_name_plural = "Trip Entries"
    ordering = ('entry_date', 'start_mileage')

    # Nest the MileageClaimInline within this inline
    inlines = [MileageClaimInline]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
        models.DecimalField: {'widget': TextInput(attrs={'size': '10'})},
    }


# --- ModelAdmin for each model ---

@admin.register(MonthlyMileageLog)
class MonthlyMileageLogAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle', 'year', 'month', 'start_odometer_reading',
        'end_odometer_reading', 'total_distance_logged', 'updated_at'
    )
    list_filter = ('vehicle', 'year', 'month')
    search_fields = ('vehicle__name', 'vehicle__license_plate')
    date_hierarchy = 'created_at'
    #raw_id_fields = ('vehicle',) # Use raw_id_fields for ForeignKey if many vehicles
    
    # All MileageLogEntries for this log, and their nested MileageClaims, are managed via this inline
    inlines = [MileageLogEntryInline]
    
    fieldsets = (
        (None, {
            'fields': ('vehicle', ('year', 'month'))
        }),
        ('Odometer Readings', {
            'fields': ('start_odometer_reading', 'end_odometer_reading'),
        }),
        ('Calculated Totals', {
            'fields': ('total_distance_logged',),
            'description': "This field is calculated from individual entries and used in checksums."
        }),
    )
    readonly_fields = ('total_distance_logged',)


@admin.register(MileageLogEntry)
class MileageLogEntryAdmin(admin.ModelAdmin):
    list_display = (
        'monthly_log', 'entry_date', 'start_mileage',
        'end_mileage', 'distance_traveled', 'get_members_with_seats',
        'get_total_claimed_seats',
    )
    list_filter = ('monthly_log__vehicle', 'entry_date')
    search_fields = (
        'description', 'monthly_log__vehicle__name',
        'monthly_log__vehicle__license_plate', 'mileageclaim__member__name'
    )
    date_hierarchy = 'entry_date'
    raw_id_fields = ('monthly_log',)
    readonly_fields = ('distance_traveled',)

    inlines = [MileageClaimInline] # MileageClaims are still inlined here

    fieldsets = (
        (None, {
            'fields': ('monthly_log', 'entry_date', ('start_mileage', 'end_mileage'), 'distance_traveled')
        }),
        ('Trip Details', {
            'fields': ('destination','purpose', 'is_long_distance',),
        }),
    )


# @admin.register(MileageClaim)
# class MileageClaimAdmin(admin.ModelAdmin):
#     list_display = ('mileage_log_entry', 'member', 'number_of_seats_claimed', 'updated_at')
#     list_filter = ('mileage_log_entry__monthly_log__vehicle', 'member')
#     search_fields = ('mileage_log_entry__description', 'member__name')
#     raw_id_fields = ('mileage_log_entry', 'member')
#     ordering = ('mileage_log_entry__entry_date', 'mileage_log_entry__start_mileage', 'member__name')