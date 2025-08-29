from django.contrib import admin
from .models import Recipient, BloodRequest

admin.site.register(Recipient)
admin.site.register(BloodRequest)

# Register your models here.
