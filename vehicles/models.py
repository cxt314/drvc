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

    name = models.CharField(max_length=200, help_text="Friendly name for the vehicle (e.g., 'Family Minivan')")
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text="Manufacturing year of the vehicle"
    )
    make = models.CharField(max_length=50, help_text="Vehicle manufacturer (e.g., 'Toyota', 'Ford')")
    model = models.CharField(max_length=50, help_text="Vehicle model (e.g., 'Camry', 'F-150')")
    fuel_type = models.CharField(
        max_length=2,
        choices=FUEL_TYPE,
        default=HYBRID,
        help_text="Type of fuel the vehicle uses"
    )
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Purchase price of the vehicle (optional)")
    purchase_date = models.DateField(default=date.today, blank=True, null=True, help_text="Date the vehicle was purchased (optional)")
    license_plate = models.CharField(max_length=20, blank=True, help_text="License plate number for the vehicle (optional)")
    vin = models.CharField(max_length=17, blank=True, null=True, unique=True, help_text="Vehicle Identification Number (optional, 17 characters)")
    current_mileage = models.DecimalField(max_digits=10, decimal_places=1, default=0.0, help_text="Current odometer reading of the vehicle")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.year} {self.make} {self.model})"

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ['name'] # Order by friendly name