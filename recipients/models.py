from django.db import models

class Recipient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    BLOOD_GROUPS = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"


class BloodRequest(models.Model):
    recipient = models.ForeignKey(
        Recipient,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    blood_group = models.CharField(max_length=5)
    units_required = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Completed", "Completed"),
        ],
        default="Pending"
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient} - {self.blood_group} ({self.status})"
