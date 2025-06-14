from django.contrib import admin
#from .models import MileageLog, MileageLogEntry

# Register your models here.
#admin.site.register(MileageLog)
#admin.site.register(MileageLogEntry)

#class MileageLogEntryInline(admin.TabularInline):
#    model = MileageLogEntry
#    fields = ["ride_date", "start", "end", "member", "is_long_distance", "destination", "purpose"]
#    filter_horizontal = ("member", )
#    extra =  3

#class MileageLogAdmin(admin.ModelAdmin):
#    model = MileageLog
#    list_display = ["vehicle", "year", "month", "odometer_start", "odometer_end", "is_finalized", "file_location"]
#    readonly_fields = ["file_location"]
#    inlines = [MileageLogEntryInline]

#admin.site.register(MileageLog, MileageLogAdmin)