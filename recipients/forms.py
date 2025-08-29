from django import forms
from .models import Recipient, BloodRequest

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["name", "age", "gender", "blood_group", "phone", "email", "address"]



class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ["recipient", "blood_group", "units_required", "status"]

