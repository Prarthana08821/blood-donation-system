from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL - MUST be first
    path('home/', views.home, name='home'),  # Alternative home page
    path('test-pillow/', views.test_pillow, name='test_pillow'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('donor-dashboard/', views.donor_dashboard, name='donor-dashboard'),
    path('recipient-dashboard/', views.recipient_dashboard, name='recipient-dashboard'),
    path('book-appointment/', views.book_appointment, name='book-appointment'),
    path('request-blood/', views.request_blood, name='request-blood'),
    # Add other routes as needed
]
