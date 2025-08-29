from django.shortcuts import render, redirect
from .models import Donor
from .forms import DonorForm


def donor_register(request):
    if request.method == "POST":
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("donors_list")
    else:
        form = DonorForm()
    return render(request, "donors/donor_form.html", {"form": form})

def donors_list(request):
    donors = Donor.objects.all()
    return render(request, "donors/donors_list.html", {"donors": donors})