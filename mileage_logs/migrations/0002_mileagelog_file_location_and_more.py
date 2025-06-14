# Generated by Django 5.1.9 on 2025-05-31 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mileage_logs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="mileagelog",
            name="file_location",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="mileagelog",
            name="is_finalized",
            field=models.BooleanField(default=False),
        ),
    ]
