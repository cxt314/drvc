from django.urls import path
from . import views

urlpatterns = [
    path('', views.MemberListView.as_view(), name="member_list"),
    path("<int:pk>/", views.MemberDetailView.as_view(), name="member_detail")
]