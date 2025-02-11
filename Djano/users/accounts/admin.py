from django.contrib import admin
from .models import Reservation
from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date', 'phone', 'email', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')