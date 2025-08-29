from django.db import models

class Donor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    blood_type = models.CharField(max_length=5)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.blood_type})"


class DonorProfile(models.Model):
    donor = models.OneToOneField(Donor, on_delete=models.CASCADE)
    last_donation = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.donor.name




# Create your models here.
