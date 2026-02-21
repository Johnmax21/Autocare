from django.db import models

# Create your models here.
class user(models.Model):
    usernname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)  # Optional
    license = models.ImageField(upload_to='license/', null=True, blank=True)
        


from django.db import models
from multiselectfield import MultiSelectField

class workshop(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    Location = models.CharField(max_length=255,null=True, blank=True)
    description = models.CharField(max_length=255,null=True, blank=True)

    phone = models.CharField(max_length=15)
    address = models.TextField()
    workshop_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    license = models.ImageField(upload_to='license/', null=True, blank=True)
    slots = models.IntegerField(default=0)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    SERVICE_CHOICES = (
        ('Oil Change', 'Oil Change'),
        ('Engine Repair', 'Engine Repair'),
        ('AC Service', 'AC Service'),
        ('Brake Service', 'Brake Service'),
        ('Battery Service', 'Battery Service'),
        ('Tire Service', 'Tire Service'),
    )
    services = MultiSelectField(choices=SERVICE_CHOICES,null=True, blank=True)
    DAYS_OF_WEEK = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )

    available_days = MultiSelectField(
        choices=DAYS_OF_WEEK,
        max_choices=7,
        max_length=20
    )
    is_approved = models.BooleanField(default=False)
from django.db import models
from django.contrib.auth.models import User

class VehicleRegistration(models.Model):
    userd = models.ForeignKey(user, on_delete=models.CASCADE)
    vehicle_name = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    vehicle_image = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    rc = models.FileField(upload_to='rc/', null=True, blank=True)
    insurance = models.FileField(upload_to='insurance/', null=True, blank=True)
    pollution = models.FileField(upload_to='pollution/', null=True, blank=True)


class Booking(models.Model):
    userd = models.ForeignKey(user, on_delete=models.CASCADE)
    workshop = models.ForeignKey(workshop, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(VehicleRegistration, on_delete=models.CASCADE)
    SERVICE_CHOICES = (
        ('Oil Change', 'Oil Change'),
        ('Engine Repair', 'Engine Repair'),
        ('AC Service', 'AC Service'),
        ('Brake Service', 'Brake Service'),
        ('Battery Service', 'Battery Service'),
        ('Tire Service', 'Tire Service'),
    )
    services = MultiSelectField(choices=SERVICE_CHOICES,null=True, blank=True)
    booking_time = models.DateField()
    status = models.CharField(max_length=20, default='Pending')
    payment=models.IntegerField(null=True,blank=True)
    is_paid = models.BooleanField(default=False) 

class transaction(models.Model):
    userd = models.ForeignKey(user, on_delete=models.CASCADE)
    workshop = models.ForeignKey(workshop, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id= models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')



    class Feedback(models.Model):
        userd = models.ForeignKey(user, on_delete=models.CASCADE)
        workshop = models.ForeignKey(workshop, on_delete=models.CASCADE)
        booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
        rating = models.IntegerField()
        comment = models.TextField()