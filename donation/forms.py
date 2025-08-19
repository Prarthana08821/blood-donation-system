from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

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

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    blood_group = forms.ChoiceField(choices=BLOOD_GROUPS)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    is_donor = forms.BooleanField(required=False)
    is_recipient = forms.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 
                 'blood_group', 'phone', 'address', 'is_donor', 'is_recipient']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['blood_group', 'phone', 'address', 'last_donation']