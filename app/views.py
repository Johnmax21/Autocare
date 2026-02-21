import random
from django.shortcuts import render

# Create your views here.
from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

def index(request):
    
    is_logged_in = 'email' in request.session

    return render(request, "index.html", {
      
        "is_logged_in": is_logged_in
    })
def feedbacback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Here you can save the feedback to the database or send an email

        return JsonResponse({'status': 'success', 'message': 'Feedback received!'})
    else:
        return HttpResponseBadRequest("Invalid request method.")

def adminlogin(request):
            return render(request, 'adminlogin.html')
            
def admin(request):
            return render(request, 'admin.html') 

# views.py

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import  user

@csrf_exempt  # Not recommended for production. Better: use {% csrf_token %} in the template.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')
        gender = request.POST.get('gender')
        license = request.FILES.get('license')

        # Create and save user
        User = user(
            usernname=username,
            password=password,
            email=email,
            phone=phone,
            address=address,
            profile_picture=profile_picture,
            gender=gender,
            license=license

        )
        User.save()
        alert_message="<script>alert('User Created Successfully'); window.location.href='/login/';</script>"
        return HttpResponse(alert_message)
        # return redirect('success')  # redirect to a success page

    return render(request, 'register.html')
# In views.py (optional)
from django.http import HttpResponse

def success(request):
    return HttpResponse("User created successfully!")
def about(request):
        return render(request, 'about.html')


    
def adminlogin(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        password=request.POST.get('password')
        u='admin'
        p='123456'
        if uname==u:
            
            if password==p:
                return redirect('admin_dashboard')
            return render(request,'adminlogin.html')
    
        alert_message="<script>alert('INCORRECT EMAIL⚠️'); window.location.href='/adminlogin';</script>"
        return HttpResponse(alert_message)
    return render(request,'adminlogin.html')


def admin_dashboard(request):

    return render(request,'admin.html')




# views.py

def user_list(request):
    users = user.objects.all()
    return render(request, 'user_list.html', {'users': users})



from django.shortcuts import render, redirect
from .models import user  # Use lowercase if your model is actually called `user`
from django.urls import reverse

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email,"email")
        password = request.POST.get('password')

        try:
            user_obj = user.objects.get(email=email)
            if user_obj.password == password:
                # For demo purposes, we'll just redirect; implement session later
                request.session['email'] = email

                return redirect('userhome')  # You can define 'home' route separately
            else:
                return render(request, 'login.html', {'error': 'Invalid password.'})
        except Exception as w:
            print(w)
            return render(request, 'login.html', {'error': 'User does not exist.'})

    return render(request, 'login.html')
def userhome(request):
    is_logged_in = 'email' in request.session
    return render(request, 'userhome.html', {
        "is_logged_in": is_logged_in
    })




from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user_obj = user.objects.get(email=email)
            otp = random.randint(100000, 999999)

            request.session['reset_email'] = email
            request.session['reset_otp'] = str(otp)

            # Render HTML template
            html_content = render_to_string('otp_email.html', {
                'otp': otp,
                'user': user_obj
            })

            text_content = strip_tags(html_content)  # Fallback text version

            email_message = EmailMultiAlternatives(
                subject='Password Reset OTP',
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )

            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return redirect('verify_otp')

        except user.DoesNotExist:
            return render(request, 'forgotpassword.html', {'error': 'Email not found.'})

    return render(request, 'forgotpassword.html')

def verify_otp_view(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        session_otp = request.session.get('reset_otp')

        if input_otp == session_otp:
            return redirect('reset_password')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'verify_otp.html')


def reset_password_view(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match.'})

        email = request.session.get('reset_email')
        try:
            user_obj = user.objects.get(email=email)
            user_obj.password = new_password  # ⚠️ Should hash this in real apps!
            user_obj.save()

            # Clean session
            request.session.pop('reset_email', None)
            request.session.pop('reset_otp', None)

            return redirect('login')
        except user.DoesNotExist:
            return render(request, 'reset_password.html', {'error': 'User not found.'})
    return render(request, 'reset_password.html')





def profile(request):
    # Fetch user email from session
    email = request.session.get('email')
    
    # Handle the case where the email is not found in session
    if not email:
        return render(request, 'user_profile.html', {'error': 'User not logged in'})
    
    # Fetch user information from the database
    cr = get_object_or_404(user, email=email)
    
    # Prepare user information for rendering
    user_info = {
        'first_name': cr.usernname,
        'address': cr.address,
        'phone': cr.phone,
        'email': cr.email,
        'password': cr.password,
        'gender': cr.gender,

        'image': cr.profile_picture,
    }
    
    return render(request, 'profile.html', user_info)

def update_profile(request):
    email=request.session['email']
    cr =user.objects.get(email=email)
    if cr:
        user_info = {
            'first_name':cr.first_name,
            'last_name':cr.last_name,
            'age':cr.age,
            'address':cr.address,
            'phone':cr.phone,
            'email':cr.email,
            'password':cr.password,
            'image':cr.image
        }
        return render(request,'update_profile.html',user_info)
    else:
        return render(request,'update_profile.html')
    from django.shortcuts import render, redirect
from .models import workshop

def workshopregister(request):
    if request.method == "POST":

        name = request.POST.get('name')
        print(name,"name")
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        Location = request.POST.get('Location')
        description = request.POST.get('description')
        slots = request.POST.get('slots')

        opening_time = request.POST.get('opening_time')
        closing_time = request.POST.get('closing_time')

        # MultiSelect fields
        services = request.POST.getlist('services')
        available_days = request.POST.getlist('available_days')

        # File upload
        license_file = request.FILES.get('license')

        # Save to database
        workshop.objects.create(
            name=name,
            phone=phone,
            email=email,
            password=password,
            Location=Location,
            description=description,
            slots=slots,
            opening_time=opening_time,   # You currently only have one TimeField
            closing_time=closing_time,
            services=services,
            available_days=available_days,
            license=license_file
        )

        return redirect('wlogin')  # change to your success page

    return render(request, 'workshopregister.html')

def wlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email,"email")
        password = request.POST.get('password')

        try:
            user_obj = user.objects.get(email=email)
            if user_obj.password == password:
                # For demo purposes, we'll just redirect; implement session later
                request.session['email'] = email

                return redirect('workshophome')  # You can define 'home' route separately
            else:
                return render(request, 'wlogin.html', {'error': 'Invalid password.'})
        except Exception as w:
            print(w)
            return render(request, 'wlogin.html', {'error': 'User does not exist.'})

    return render(request, 'wlogin.html')


from django.shortcuts import render
from .models import workshop

def workshoplist(request):
    workshops = workshop.objects.all()

    # Rating filter (if you have rating field later)
    ratings = request.GET.getlist('rating')
    if ratings:
        workshops = workshops.filter(rating__gte=min(ratings))

    # Service filter
    services = request.GET.getlist('services')
    if services:
        for service in services:
            workshops = workshops.filter(services__icontains=service)

    # Location filter
    locations = request.GET.getlist('location')
    if locations:
        workshops = workshops.filter(Location__in=locations)

    # Pass choices dynamically
    context = {
        'workshops': workshops,
        'service_choices': workshop.SERVICE_CHOICES,
        'locations': workshop.objects.values_list('Location', flat=True).distinct(),
    }

    return render(request, 'workshoplist.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import VehicleRegistration

def register_vehicle(request):
    
    if request.method == "POST":
         email=request.session['email']
         cr =user.objects.get(email=email)
         vehicle = VehicleRegistration.objects.create(
            userd=cr,  # 🔥 user from session
            vehicle_name=request.POST.get("name"),
            vehicle_model=request.POST.get("model"),
            license_plate=request.POST.get("license_plate"),
            vehicle_image=request.FILES.get("vehicle-image"),
            rc=request.FILES.get("rc-doc"),
            insurance=request.FILES.get("insurance-doc"),
            pollution=request.FILES.get("pollution-doc"),
        )
         return redirect("profile")  # change to your profile URL name

    return render(request, "vehicleregistration.html")
def yourvehicles(request):
    email=request.session['email']
    cr =user.objects.get(email=email)
    vehicles = VehicleRegistration.objects.filter(userd=cr)
    return render(request, "yourvehicles.html", {"vehicles": vehicles})
from django.shortcuts import render, redirect, get_object_or_404
from .models import workshop, user, Booking, VehicleRegistration
from django.contrib import messages
from django.utils.dateparse import parse_date

def book_service(request, id):
    # Get the workshop
    email = request.session.get('email')
    dr = get_object_or_404(workshop, id=id)
    cr = user.objects.get(email=email)
    vehicl = VehicleRegistration.objects.filter(userd=cr)
    print(vehicl,"vehicl")
    print("ggg")
    context = {
        'service': dr.services,
        'vehicles': vehicl,
        
    }
    
    if not email:
            messages.error(request, "Please login to book a service.")
            return redirect("login")
  


    # Split services string into a list if it's stored as comma-separated
    # If it's already a list in the DB, you can skip this
    

    if request.method == "POST":
        
        selected_services = request.POST.getlist('service')  # returns list

        # Booking date & time (we only have date input; you can extend to time if needed)
        booking_time = request.POST.get('bookingDate')  # optional if you have time field
        vehicle = request.POST.get('vehicle')
        gg=VehicleRegistration.objects.get(vehicle_name=vehicle)
        # Pickup info
        pickup_lat = request.POST.get('pickup_lat')
        pickup_lng = request.POST.get('pickup_lng')
        pickup_location = request.POST.get('pickupLocation')

        # Payment calculation
        distance_km = float(request.POST.get('distance-km', 0))
        pickup_charges = distance_km * 20
        extra_service = 100  # fixed extra
        total_payment = int(pickup_charges + extra_service)

        # Save booking
        booking = Booking.objects.create(
            userd=cr,
            workshop=dr,
            vehicle=gg,
            services=selected_services,  # MultiSelectField handles list
            booking_time=booking_time if booking_time else None,
            payment=total_payment,
        )

        messages.success(request, f"Booking successful! Total payment: ₹{total_payment}")
        return redirect("profile")

    return render(request, "book.html", context)
def mybookings(request):
    email = request.session.get('email')
    cr = user.objects.get(email=email)
    bookings = Booking.objects.filter(userd=cr).order_by('-id')

    return render(request, "mybookings.html", {"bookings": bookings})

def servicerequestpage(request):
    email = request.session.get('email')
    cr = workshop.objects.get(email=email)
    bookings = Booking.objects.filter(workshop=cr)
    return render(request, "servicerequestpage.html", {"bookings": bookings})

from django.shortcuts import redirect, get_object_or_404

def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = status
    booking.save()
    return redirect("servicerequestpage")

import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Booking, transaction

RAZOR_KEY_ID = "rzp_test_X5OfG2jiWrAzSj"
RAZOR_KEY_SECRET = "SsCovWWZSwB1TGd1rSoIiwF3"

def make_payment(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

    amount = booking.payment * 100   # Razorpay needs paise

    payment_order = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    })

    context = {
        'booking': booking,
        'order_id': payment_order['id'],
        'razor_key': RAZOR_KEY_ID,
        'amount': amount
    }

    return render(request, "payment.html", context)

from django.shortcuts import render
from .models import Booking, transaction

def payment_success(request):

    booking_id = request.GET.get("booking_id")

    booking = Booking.objects.get(id=booking_id)

    # mark booking paid
    booking.is_paid = True
    booking.save()

    # save transaction
    transaction.objects.create(
        userd=booking.userd,
        workshop=booking.workshop,
        booking=booking,
        amount=booking.payment,
        order_id="manual_success",   # replace with razorpay order later
        status="Paid"
    )

    return render(request, "success.html")

