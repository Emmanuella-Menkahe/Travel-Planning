from django.contrib import admin
from .models import CustomUser, Profile, Destination, Accommodation, Hotel, Booking, Agency, Reservation
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'password', 'roles', 'is_staff']

    # This ensures only users with 'add_agency' permission (admins) can add agencies
    def has_add_permission(self, request):
        return request.user.is_superuser
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Reservation)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'address', 'travel_preferences', 'profile_picture')
    search_fields = ('full_name', 'user__username', 'phone_number')
    list_filter = ('user',)
admin.site.register(Profile, ProfileAdmin)

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'popular_attractions', 'image')
    search_fields = ('name', 'city', 'popular_attractions')
admin.site.register(Destination, DestinationAdmin)

class AccommodationAdmin(admin.ModelAdmin):
    search_fields = ('type_of_accommodation', 'name', 'town')
    list_display = ("name", "town", 'location', "price_per_night", "type_of_accommodation", "phone_number")
admin.site.register(Accommodation, AccommodationAdmin)

admin.site.register(Hotel)

class BookingAdmin(admin.ModelAdmin):
    list_filter = ("user", "accommodation", "check_in_date", "check_out_date", "total_price")
admin.site.register(Booking, BookingAdmin)

class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'agency_receptionist')
    search_fields = ('name', 'description')
admin.site.register(Agency, AgencyAdmin)