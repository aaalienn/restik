from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('reserve/', views.reserve, name='reserve'),
    path('message/', views.message, name='message'),
    path('reservations/', views.reservations_list, name='reservations_list'),
    path('reservations/toggle/<int:reservation_id>/', views.toggle_reservation, name='toggle_reservation'),
    path('reservations/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
]