from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from vehicles.models import Vehicle
from members.models import Member

# Create your models here.
class MileageLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    month = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    odometer_start = models.PositiveIntegerField()
    odometer_end = models.PositiveIntegerField()
    is_finalized = models.BooleanField(default=False)
    file_location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle} {self.year}-{self.month}"
    
class MileageLogEntry(models.Model):
    mileage_log = models.ForeignKey(MileageLog, on_delete=models.CASCADE)
    ride_date = models.DateField()
    member = models.ManyToManyField(Member)
    start = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)]
    )
    end = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)]
    )
    is_long_distance = models.BooleanField(default=False)
    destination = models.CharField(max_length=100, blank=True)
    purpose = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mileage_log} {self.ride_date} {self.member}"