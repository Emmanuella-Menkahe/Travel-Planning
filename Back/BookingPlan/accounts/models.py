from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError


class Accommodation(models.Model):
    ACCOMMODATION_TYPES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
    )
    
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    # description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/accommodations/', null=True, blank=True)  
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2) 
    phone_number = models.CharField(max_length=15)
    type_of_accommodation = models.CharField(max_length=20, choices=ACCOMMODATION_TYPES)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('accommodation_receptionist', 'Accommodation_Receptionist'),
        ('agency_receptionist', 'Agency_Receptionist'),
        ('client', 'Client'),
    ]
    roles = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True, blank=True, default='client')


class Agency(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/agency/')
    description = models.TextField()
    
    agency_receptionist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, limit_choices_to={'roles': 'agency_receptionist'},related_name='managed_agencies'
    )

    def __str__(self):
        return self.name


class TravelPlan(models.Model):
    STATUS_CHOICES = [
        ('complete', 'Complete'),
        ('active', 'Active'),
    ]
    
    departure = models.CharField(max_length=100)
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    destination = models.CharField(max_length=100)
    number_of_places = models.PositiveIntegerField()
    number_of_available_places = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.departure} to {self.destination} on {self.date}"
    
    def is_complete(self):
        return self.status == 'complete'
    
    def update_available_places(self, booked_places):
        """Update available places when bookings are made."""
        if self.number_of_available_places >= booked_places:
            self.number_of_available_places -= booked_places
            self.save()
        else:
            raise ValueError("Not enough available places.")
        

class Reservation(models.Model):
    travel_plan = models.ForeignKey('TravelPlan', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    number_of_places = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    id_card_number = models.CharField(max_length=50)
    reserved_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensure the travel plan is active
        if self.travel_plan.status != 'active':
            raise ValidationError('Reservations can only be made for active travel plans.')

        # Ensure the number of places is positive
        if self.number_of_places <= 0:
            raise ValidationError('The number of places must be greater than zero.')

        # Ensure the number of places does not exceed available places
        if self.number_of_places > self.travel_plan.number_of_available_places:
            raise ValidationError('The number of places requested exceeds the available places.')

        # Calculate the total price based on the travel plan's price  
        self.total_price = self.number_of_places * self.travel_plan.price

        # Validate ID card number (e.g., should be alphanumeric and have a certain length)
        if not self.id_card_number.isalnum() or len(self.id_card_number) < 5:
            raise ValidationError('The ID card number must be alphanumeric and at least 5 characters long.')

    def save(self, *args, **kwargs):
        # Perform validation before saving
        self.full_clean()
        # Update the number of available places in the travel plan
        self.travel_plan.number_of_available_places -= self.number_of_places
        self.travel_plan.save()
        # Save the reservation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.travel_plan.destination}"



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    travel_preferences = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.full_name

class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=100)
    popular_attractions = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/destination_img/', null= False, blank= False)

    def __str__(self):
        return f'{self.city}'


class Hotel(Accommodation):
    ROOM_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    ]

    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.room_type}"


class Booking(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.accommodation.name}'



