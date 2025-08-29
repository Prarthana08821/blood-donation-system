# recipients/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Recipient, BloodRequest
from .forms import RecipientForm, BloodRequestForm

# ============================
# Recipient Views
# ============================

def recipient_list(request):
    recipients = Recipient.objects.all()
    return render(request, "recipients/recipient_list.html", {"recipients": recipients})

def recipient_details(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    return render(request, "recipients/recipient_details.html", {"recipient": recipient})

def delete_recipient(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    if request.method == "POST":
        recipient.delete()
        messages.success(request, 'Recipient deleted successfully!')
        return redirect('recipient_list')  # redirect to recipient list
    # If GET, redirect back to detail page
    return redirect('recipient_detail', pk=pk)

def recipient_create(request):
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    
    if request.method == "POST":
        form = RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("recipient_list")
    else:
        form = RecipientForm()
    
    return render(request, "recipients/recipient_form.html", {
        "form": form,
        "blood_groups": blood_groups,
    })
    
def edit_recipient(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    if request.method == "POST":
        form = RecipientForm(request.POST, instance=recipient)
        if form.is_valid():
            form.save()
            return redirect("recipient_list")  # redirect to your recipient list page
    else:
        form = RecipientForm(instance=recipient)

    return render(request, "recipients/recipient_form.html", {"form": form})


# ============================
# Blood Request Views
# ============================
def edit_request(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if request.method == "POST":
        form = BloodRequestForm(request.POST, instance=blood_request)
        if form.is_valid():
            form.save()
            return redirect("blood_request_list")
    else:
        form = BloodRequestForm(instance=blood_request)

    return render(request, "recipients/blood_request_form.html", {"form": form})

def blood_request_list(request):
    """
    Retrieves all blood requests and renders them on a list page.
    """
    requests = BloodRequest.objects.all()
    context = {
        'requests': requests
    }
    return render(request, 'recipients/blood_request_list.html', context)


# Add this new function for detailed view
def request_detail(request, pk):
    """Display details of a single blood request"""
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    return render(request, 'recipients/request_detail.html', {'blood_request': blood_request})


# Add this new function to handle deletion
def delete_request(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if request.method == "POST":
        blood_request.delete()
        messages.success(request, 'Blood request deleted successfully!')
        return redirect('blood_request_list')
    # If a GET request, you could render a confirmation page.
    # For now, we'll just redirect back.
    return redirect('request_detail', pk=pk)


def create_request(request):
    if request.method == "POST":
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("blood_request_list")
    else:
        form = BloodRequestForm()

    recipients = Recipient.objects.all()
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    return render(request, "recipients/blood_request_form.html", {
        "form": form,
        "recipients": recipients,
        "blood_groups": blood_groups,
    })