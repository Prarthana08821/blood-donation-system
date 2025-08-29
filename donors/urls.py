from django.urls import path
from . import views
from donors.views import donors_list

urlpatterns = [
    path("list/", views.donors_list, name="donors_list"),
    path('register/', views.donor_register, name='donor_register'),
]


