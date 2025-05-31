from django.contrib import admin
from .models import MileageLog, MileageLogEntry

# Register your models here.
admin.site.register(MileageLog)
admin.site.register(MileageLogEntry)