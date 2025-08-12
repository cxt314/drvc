from django.urls import path
from . import views

urlpatterns = [
    # MileageLog list view
    path('', views.MileageLogListView.as_view(), name='mileage_logs_list'),
    # MileageLog detail view
    path('<int:pk>/', views.MileageLogDetailView.as_view(), name='detail_mileage_log'),
    # URL to create a new mileage log
    path('add/', views.create_mileage_log_view, name='add_new_mileage_log'),
    # Assumes a URL like `/mileage_logs/1/update/`
    path('<int:pk>/update/', views.update_mileage_log_view, name='update_mileage_log'),
    # delete a mileage log
    path('<int:pk>/delete/', views.delete_mileage_log_view, name='delete_mileage_log'),
]
