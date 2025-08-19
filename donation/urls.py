from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL - should be FIRST
    path('home/', views.home, name='home'),  # Alternative home page
    path('test-pillow/', views.test_pillow_view, name='test_pillow'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('donor-dashboard/', views.donor_dashboard, name='donor-dashboard'),
    path('recipient-dashboard/', views.recipient_dashboard, name='recipient-dashboard'),
    # Add all your other views here
]


