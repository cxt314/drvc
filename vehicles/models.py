from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date

# Create your models here.
class Vehicle(models.Model):
    HYBRID = "HY"
    GASOLINE = "GS"
    DIESEL = "DS"
    ELECTRIC = "EC"
    FUEL_TYPE = (
        (HYBRID, "Hybrid"),
        (ELECTRIC, "Electric"),
        (DIESEL, "Diesel"),
        (GASOLINE, "Gasoline"),
    )

    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    fuel_type = models.CharField(
        max_length=2, 
        choices=FUEL_TYPE, 
        default=HYBRID,
    )
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    purchase_date = models.DateField(default=date.today, blank=True)
    license_plate = models.CharField(max_length=20, blank=True, help_text="Unique license plate number")
    vin = models.CharField(max_length=17, blank=True, null=True, unique=True, help_text="Vehicle Identification Number (optional)")
    current_mileage = models.DecimalField(max_digits=10, decimal_places=1, default=0.0, help_text="Current odometer reading")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ['name']