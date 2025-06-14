from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import calendar # For getting month/year info
from vehicles.models import Vehicle
from members.models import Member

class MonthlyMileageLog(models.Model):
    """
    Represents a monthly mileage log for a specific vehicle.
    Contains multiple MileageLogEntries.
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='monthly_logs', help_text="The vehicle this monthly log belongs to")
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text="Year of the mileage log (e.g., 2023)"
    )
    month = models.IntegerField(
        choices=[(i, calendar.month_name[i]) for i in range(1, 13)],
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Month of the mileage log (1 for January, 12 for December)"
    )
    start_odometer_reading = models.DecimalField(
        max_digits=10, decimal_places=1,
        help_text="Odometer reading at the start of the month (for checksum)"
    )
    end_odometer_reading = models.DecimalField(
        max_digits=10, decimal_places=1,
        help_text="Odometer reading at the end of the month (for checksum)"
    )
    total_distance_logged = models.DecimalField(
        max_digits=10, decimal_places=1, default=0.0,
        help_text="Sum of distances from all associated MileageLogEntries (for checksum)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('vehicle', 'year', 'month') # Ensures only one log per vehicle per month
        verbose_name = "Monthly Mileage Log"
        verbose_name_plural = "Monthly Mileage Logs"
        ordering = ['-year', '-month'] # Order by most recent month first

    def __str__(self):
        return f"{self.vehicle.name} - {calendar.month_name[self.month]} {self.year} Log"

    def clean(self):
        # Validate that end odometer reading is greater than or equal to start odometer reading
        if self.start_odometer_reading is not None and self.end_odometer_reading is not None:
            if self.end_odometer_reading < self.start_odometer_reading:
                raise ValidationError(
                    {'end_odometer_reading': _("End odometer reading must be greater than or equal to start odometer reading.")}
                )

    def calculate_total_distance(self):
        """Calculates the sum of distance_traveled from all associated entries."""
        # Use .annotate() and .aggregate() for efficient summing
        return self.log_entries.aggregate(total_dist=models.Sum('distance_traveled'))['total_dist'] or 0.0

    def validate_checksum(self):
        """
        Validates the checksum for the monthly log:
        1. (End Odometer - Start Odometer) == Sum of individual trip distances.
        2. First entry's start_mileage matches the monthly log's start_odometer_reading.
        3. Last entry's end_mileage matches the monthly log's end_odometer_reading.
        """
        calculated_total_distance = self.calculate_total_distance()
        expected_total_distance = self.end_odometer_reading - self.start_odometer_reading

        if expected_total_distance != calculated_total_distance:
            raise ValidationError(
                _("Checksum mismatch: (End Odometer - Start Odometer) does not equal the total distance logged from individual entries.")
            )

        # Get first and last entries based on the logical ordering defined in MileageLogEntry
        first_entry = self.log_entries.order_by('entry_date', 'start_mileage').first()
        last_entry = self.log_entries.order_by('-entry_date', '-start_mileage').first()

        if first_entry and self.start_odometer_reading != first_entry.start_mileage:
             raise ValidationError(
                 _("Checksum mismatch: Monthly log's start odometer reading does not match the first entry's start mileage.")
             )

        if last_entry and self.end_odometer_reading != last_entry.end_mileage:
             raise ValidationError(
                 _("Checksum mismatch: Monthly log's end odometer reading does not match the last entry's end mileage.")
             )


class MileageLogEntry(models.Model):
    """
    Represents a single mileage log entry within a MonthlyMileageLog.
    """
    # Django will automatically create an 'id' AutoField as the primary key.
    monthly_log = models.ForeignKey(
        MonthlyMileageLog, on_delete=models.CASCADE, related_name='log_entries',
        help_text="The monthly log this entry belongs to"
    )
    entry_date = models.DateField(help_text="Date of the mileage entry (should be within the monthly log's month/year)")
    start_mileage = models.DecimalField(max_digits=10, decimal_places=1, help_text="Odometer reading at the start of the trip")
    end_mileage = models.DecimalField(max_digits=10, decimal_places=1, help_text="Odometer reading at the end of the trip")
    distance_traveled = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True, editable=False, help_text="Calculated distance (end_mileage - start_mileage)")
    destination = models.TextField(blank=True, help_text="Optional destination of the trip")
    purpose = models.TextField(blank=True, help_text="Optional purpose of the trip")
    is_long_distance = models.BooleanField(default=False)
    # Many-to-Many relationship with Member
    members = models.ManyToManyField(
        Member,
        related_name='mileage_entries',
        help_text="Select members associated with this trip. At least one member is required."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mileage Log Entry"
        verbose_name_plural = "Mileage Log Entries"
        # Enforce uniqueness of the (monthly_log, entry_date, start_mileage) combination
        unique_together = ('monthly_log', 'entry_date', 'start_mileage')
        # This ordering is crucial for retrieving "previous" entries correctly
        # and for how entries are displayed by default.
        ordering = ['monthly_log__vehicle', 'monthly_log__year', 'monthly_log__month', 'entry_date', 'start_mileage']


    def clean(self):
        super().clean()

        # 1. Validate that end_mileage is greater than or equal to start_mileage
        if self.start_mileage is not None and self.end_mileage is not None:
            if self.end_mileage < self.start_mileage:
                raise ValidationError(
                    {'end_mileage': _("End mileage must be greater than or equal to start mileage.")}
                )

        # 2. Validate that the entry date falls within the monthly log's year and month
        if self.monthly_log and self.entry_date:
            if self.entry_date.year != self.monthly_log.year or \
               self.entry_date.month != self.monthly_log.month:
                raise ValidationError(
                    {'entry_date': _("Entry date must be within the selected monthly log's year and month.")}
                )

        # 3. Enforce continuity with the previous entry (if one exists within the same monthly log)
        if self.monthly_log_id and self.start_mileage is not None:
            # Find the immediately preceding entry in the logical order
            # This query must be robust to correctly identify the "previous" entry
            # based on the defined ordering: monthly_log, entry_date, start_mileage.
            previous_entries = MileageLogEntry.objects.filter(
                monthly_log=self.monthly_log
            ).exclude(pk=self.pk).filter( # Exclude self to avoid self-comparison
                models.Q(entry_date__lt=self.entry_date) | # Earlier date
                models.Q(entry_date=self.entry_date, start_mileage__lt=self.start_mileage) # Same date, earlier start mileage
            ).order_by('-entry_date', '-start_mileage') # Order descending to get the "latest previous" first

            previous_entry = previous_entries.first() # Get the immediately preceding one

            if previous_entry and previous_entry.end_mileage is not None:
                if self.start_mileage != previous_entry.end_mileage:
                    raise ValidationError(
                        {'start_mileage': _(f"Start mileage must match the previous entry's end mileage ({previous_entry.end_mileage}).")}
                    )

        # 4. Enforce at least one member is selected (will be handled in forms too, but good as a model-level check)
        # This check needs to be done after the instance has an ID, meaning during a form's clean or post_save.
        # For a model's clean method, ManyToManyFields are not yet set if the object is new.
        # It's better to enforce this in a ModelForm's clean_members method.
        # However, for a basic check if saving directly to model:
        # if not self.pk and not self.members.exists(): # This won't work for new objects.
        pass # Better handled in forms.




    def save(self, *args, **kwargs):
        """
        Calculates distance_traveled before saving and updates related MonthlyMileageLog
        and Vehicle's current_mileage.
        """
        # Calculate distance_traveled
        if self.start_mileage is not None and self.end_mileage is not None:
            self.distance_traveled = self.end_mileage - self.start_mileage
        
        super().save(*args, **kwargs)

        # Update the MonthlyMileageLog's total_distance_logged
        if self.monthly_log:
            self.monthly_log.total_distance_logged = self.monthly_log.calculate_total_distance()

            # Update the monthly log's end_odometer_reading if this is currently the latest entry for that month
            latest_entry_for_month = self.monthly_log.log_entries.order_by('-entry_date', '-start_mileage').first()
            if latest_entry_for_month and latest_entry_for_month.pk == self.pk: # Only update if this is truly the latest
                self.monthly_log.end_odometer_reading = self.end_mileage
                self.monthly_log.save(update_fields=['total_distance_logged', 'end_odometer_reading', 'updated_at'])
            else:
                self.monthly_log.save(update_fields=['total_distance_logged', 'updated_at'])

        # Update the Vehicle's current_mileage based on the end_mileage of this entry,
        # only if this entry's end_mileage is higher than the vehicle's current_mileage.
        # This assumes new entries are mostly chronological and reflect higher mileage.
        if self.monthly_log and self.monthly_log.vehicle:
            if self.monthly_log.vehicle.current_mileage < self.end_mileage:
                self.monthly_log.vehicle.current_mileage = self.end_mileage
                self.monthly_log.vehicle.save(update_fields=['current_mileage', 'updated_at'])


    def __str__(self):
        return f"{self.monthly_log.vehicle.name} - Trip on {self.entry_date}: {self.distance_traveled or 0} miles"

