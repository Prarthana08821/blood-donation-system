from django.urls import path
from . import views

urlpatterns = [
    # your existing URLs
    path('test-pillow/', views.test_pillow_view, name='test_pillow'),
]