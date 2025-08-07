from django.urls import path
from . import views

urlpatterns = [
    path('', views.MileageLogListView.as_view(), name='list_mileage_logs'),
    # URL to create a new mileage log
    path('add/', views.create_mileage_log_view, name='add_new_mileage_log'),
    # Assumes a URL like `/mileage_logs/1/update/`
    path('<int:pk>/update/', views.update_mileage_log_view, name='update_mileage_log'),
    # Add other URLs as needed
]
