# Generated by Django 5.1.9 on 2025-06-14 21:41

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0002_alter_vehicle_options_vehicle_current_mileage_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="current_mileage",
            field=models.DecimalField(
                decimal_places=1,
                default=0.0,
                help_text="Current odometer reading of the vehicle",
                max_digits=10,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="fuel_type",
            field=models.CharField(
                choices=[
                    ("HY", "Hybrid"),
                    ("EC", "Electric"),
                    ("DS", "Diesel"),
                    ("GS", "Gasoline"),
                ],
                default="HY",
                help_text="Type of fuel the vehicle uses",
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="license_plate",
            field=models.CharField(
                blank=True,
                help_text="License plate number for the vehicle (optional)",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="make",
            field=models.CharField(
                help_text="Vehicle manufacturer (e.g., 'Toyota', 'Ford')", max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="model",
            field=models.CharField(
                help_text="Vehicle model (e.g., 'Camry', 'F-150')", max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="name",
            field=models.CharField(
                help_text="Friendly name for the vehicle (e.g., 'Family Minivan')",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="purchase_date",
            field=models.DateField(
                blank=True,
                default=datetime.date.today,
                help_text="Date the vehicle was purchased (optional)",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="purchase_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="Purchase price of the vehicle (optional)",
                max_digits=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="vin",
            field=models.CharField(
                blank=True,
                help_text="Vehicle Identification Number (optional, 17 characters)",
                max_length=17,
                null=True,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="year",
            field=models.PositiveIntegerField(
                help_text="Manufacturing year of the vehicle",
                validators=[
                    django.core.validators.MinValueValidator(1900),
                    django.core.validators.MaxValueValidator(2100),
                ],
            ),
        ),
    ]
