from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from socket import gaierror
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
        return render(request, "accounts/home.html", {'request_path': request.path})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')

from django.core.exceptions import ValidationError
from datetime import datetime, date

def reserve(request):
    if request.method == 'POST':
        try:
            
            date_str = request.POST['datepicker']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            if date_obj < date.today():
                messages.error(request, 'Нельзя бронировать на прошедшую дату!')
                return redirect('home')
            
            
            reservation = Reservation(
                user=request.user,
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                date=date_obj,
                phone=request.POST['phone'],
                email=request.POST['email']
            )
            reservation.save()
            
            
            message = f"""
            Подтверждение бронирования:
            
            Имя: {reservation.first_name}
            Фамилия: {reservation.last_name}
            Дата: {reservation.date}
            Телефон: {reservation.phone}
            Email: {reservation.email}
            
            Спасибо за ваше бронирование!
            """
            
            try:
                send_mail(
                    'Подтверждение бронирования',
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [reservation.email],
                    fail_silently=False,
                )
                messages.success(request, 'Бронирование успешно создано! Проверьте вашу почту.')
            except (BadHeaderError, gaierror) as e:
                messages.warning(request, 'Бронирование создано, но письмо не отправлено.')
                print(f"Email error: {str(e)}")
                
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'Произошла ошибка при бронировании.')
            print(f"Error: {str(e)}")
        
        return redirect('home')
    
    return render(request, 'accounts/home.html')

def message(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            subject = request.POST['subject']
            message_text = request.POST['message']
            
            
            formatted_message = f"""
            Новое сообщение от посетителя:
            
            Имя: {name}
            Тема: {subject}
            
            Сообщение:
            {message_text}
            """
            
            
            send_mail(
                f'Жалоба/Предложение от {name}: {subject}', 
                formatted_message,  
                settings.DEFAULT_FROM_EMAIL,  
                ['akmammedovallan@gmail.com'],  
                fail_silently=False,
            )
            
            messages.success(request, 'Ваше сообщение успешно отправлено!')
        except (BadHeaderError, gaierror) as e:
            messages.error(request, 'Ошибка при отправке сообщения. Попробуйте позже.')
            print(f"Email error: {str(e)}")
        except Exception as e:
            messages.error(request, 'Произошла ошибка. Попробуйте позже.')
            print(f"Error: {str(e)}")
            
        return redirect('home')
    
    return render(request, 'accounts/home.html')

@login_required
def reservations_list(request):
    reservations = Reservation.objects.all().order_by('-created_at')
    return render(request, 'accounts/reservations.html', {'reservations': reservations})

@login_required
def toggle_reservation(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.is_confirmed = not reservation.is_confirmed
        reservation.save()
        messages.success(request, 'Статус бронирования обновлен')
    return redirect('reservations_list')

@login_required
def delete_reservation(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.delete()
        messages.success(request, 'Бронирование удалено')
    return redirect('reservations_list')


@staff_member_required
def reservations_list(request):
    reservations = Reservation.objects.all().order_by('-created_at')
    return render(request, 'accounts/reservations.html', {'reservations': reservations})