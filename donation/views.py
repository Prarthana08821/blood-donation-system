from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm
from .models import Profile, BloodStock, DonationAppointment, BloodRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import io


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                blood_group=form.cleaned_data.get('blood_group'),
                phone=form.cleaned_data.get('phone'),
                address=form.cleaned_data.get('address'),
                is_donor=form.cleaned_data.get('is_donor'),
                is_recipient=form.cleaned_data.get('is_recipient')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'donation/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'donation/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def donor_dashboard(request):
    if not request.user.profile.is_donor:
        return redirect('home')
    
    appointments = DonationAppointment.objects.filter(donor=request.user)
    context = {
        'appointments': appointments,
    }
    return render(request, 'donation/donor_dashboard.html', context)

@login_required
def book_appointment(request):
    if not request.user.profile.is_donor:
        return redirect('home')
    
    if request.method == 'POST':
        donation_center = request.POST.get('donation_center')
        appointment_date = request.POST.get('appointment_date')
        
        appointment = DonationAppointment.objects.create(
            donor=request.user,
            donation_center=donation_center,
            appointment_date=appointment_date
        )
        return redirect('donor-dashboard')
    
    return render(request, 'donation/book_appointment.html')

@login_required
def donation_history(request):
    if not request.user.profile.is_donor:
        return redirect('home')
    
    donations = DonationAppointment.objects.filter(donor=request.user, completed=True)
    return render(request, 'donation/donation_history.html', {'donations': donations})

@login_required
def recipient_dashboard(request):
    if not request.user.profile.is_recipient:
        return redirect('home')
    
    requests = BloodRequest.objects.filter(requester=request.user)
    context = {
        'requests': requests,
    }
    return render(request, 'donation/recipient_dashboard.html', context)

@login_required
def request_blood(request):
    if not request.user.profile.is_recipient:
        return redirect('home')
    
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        blood_group = request.POST.get('blood_group')
        units = request.POST.get('units')
        hospital = request.POST.get('hospital')
        reason = request.POST.get('reason')
        urgent = request.POST.get('urgent') == 'on'
        date_required = request.POST.get('date_required')
        
        blood_request = BloodRequest.objects.create(
            requester=request.user,
            patient_name=patient_name,
            blood_group=blood_group,
            units=int(units),
            hospital=hospital,
            reason=reason,
            urgent=urgent,
            date_required=date_required
        )
        return redirect('recipient-dashboard')
    
    return render(request, 'donation/request_blood.html')

@login_required
def track_request(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if blood_request.requester != request.user:
        return redirect('home')
    
    return render(request, 'donation/track_request.html', {'request': blood_request})

@staff_member_required
def admin_dashboard(request):
    pending_requests = BloodRequest.objects.filter(status='Pending')
    low_stock = BloodStock.objects.filter(units__lt=5)
    donors = Profile.objects.filter(is_donor=True).count()
    
    context = {
        'pending_requests': pending_requests,
        'low_stock': low_stock,
        'donors': donors,
    }
    return render(request, 'donation/admin_dashboard.html', context)

@staff_member_required
def manage_request(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    
    try:
        blood_stock = BloodStock.objects.get(blood_group=blood_request.blood_group)
    except BloodStock.DoesNotExist:
        blood_stock = None
        messages.warning(request, f'No stock found for blood group {blood_request.blood_group}')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':  # Fixed typo: was 'approve'
            if blood_stock and blood_stock.units >= blood_request.units:
                blood_stock.units -= blood_request.units
                blood_stock.save()
                blood_request.status = 'Approved'
                blood_request.save()
                messages.success(request, 'Request approved successfully!')
            else:
                messages.warning(request, 'Not enough blood in stock!')
        elif action == 'reject':
            blood_request.status = 'Rejected'
            blood_request.save()
            messages.success(request, 'Request rejected!')
        
        return redirect('admin-dashboard')
    
    return render(request, 'donation/manage_request.html', {
        'request': blood_request,
        'stock': blood_stock,
    })

@staff_member_required
def update_stock(request):
    if request.method == 'POST':
        blood_group = request.POST.get('blood_group')
        units = int(request.POST.get('units'))
        
        blood_stock, created = BloodStock.objects.get_or_create(blood_group=blood_group)
        blood_stock.units += units
        blood_stock.save()
        messages.success(request, f'Stock updated for {blood_group}. Current units: {blood_stock.units}')
        return redirect('admin-dashboard')
    
    return render(request, 'donation/update_stock.html')

@staff_member_required
def generate_reports(request):
    # Generate reports logic here
    return render(request, 'donation/reports.html')

def home(request):
    blood_stocks = BloodStock.objects.all()
    urgent_requests = BloodRequest.objects.filter(urgent=True, status='Pending')[:3]
    
    context = {
        'blood_stocks': blood_stocks,
        'urgent_requests': urgent_requests,
    }
    return render(request, 'donation/home.html', context)

# Add this view to test if Pillow is working after the update
def test_pillow(request):
    """
    A simple view to test if Pillow is working correctly
    """
    try:
        from PIL import Image
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        
        # Save it to memory
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Save to default storage
        file_name = 'test_pillow_image.png'
        default_storage.save(file_name, ContentFile(img_buffer.getvalue()))
        
        # Check if file exists
        if default_storage.exists(file_name):
            default_storage.delete(file_name)
            return HttpResponse("Pillow is working correctly! Test image created and deleted successfully.")
        else:
            return HttpResponse("Pillow test completed but file operation failed.")
            
    except ImportError:
        return HttpResponse("Pillow is not installed correctly.")
    except Exception as e:
        return HttpResponse(f"Error testing Pillow: {str(e)}")

# Create your views here.
