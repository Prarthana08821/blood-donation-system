from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

BLOOD_GROUPS = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    is_donor = models.BooleanField(default=False)
    is_recipient = models.BooleanField(default=False)
    last_donation = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

class BloodStock(models.Model):
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, unique=True)
    units = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.blood_group} - {self.units} units'

class DonationAppointment(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    donation_center = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.donor.username} - {self.appointment_date}'

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units = models.PositiveIntegerField(default=1)
    hospital = models.CharField(max_length=100)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    urgent = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_required = models.DateField()
    
    def __str__(self):
        return f'{self.patient_name} - {self.blood_group}'

# Create your models here.
