# recipients/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Recipient URLs
    path('list/', views.recipient_list, name='recipient_list'),
    path('add/', views.recipient_create, name='recipient_create'),
    path('details/<int:pk>/', views.recipient_details, name='recipient_details'),

    # Blood Request URLs
    path('requests/', views.blood_request_list, name='blood_request_list'),
    path('requests/add/', views.create_request, name='create_request'),
    path('recipients/<int:pk>/edit/', views.edit_recipient, name='edit_recipient'),
    path('recipients/<int:pk>/delete/', views.delete_recipient, name='delete_recipient'),
    # Add this new URL for the detail view
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('requests/<int:pk>/delete/', views.delete_request, name='delete_request'),
    path("requests/<int:pk>/edit/", views.edit_request, name="edit_request"),
]