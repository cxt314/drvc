from django.shortcuts import render
from django.views import generic
from .models import Vehicle

# Create your views here.
class VehicleListView(generic.ListView):
    model = Vehicle
    template_name = "vehicles/vehicle_list.html"

    