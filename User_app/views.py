#from django.shortcuts import render, redirect
from urllib import response
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login 
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.password):
            auth_login(request, user)  # Use Django's login function
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender,  # Assuming gender is a field in CustomUser
                'contact_number': user.contact_number,  # Assuming contact_number is a field in CustomUser
            }
            refresh = RefreshToken.for_user(user)
            response_data = {
                'success': True,
                'message': 'Login successful',
                'user_data': user_data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'Code': "200"}
            return render(request,'dashboard.html')
            
            return JsonResponse(response_data)
        else:
            response_data = {
                'success': False,
                'message': 'Invalid credentials',
            }
            return JsonResponse(response_data)
    else:
        response_data = {
            'message': 'Please use POST method for login',
        }
        return render(request, 'login.html')


@csrf_exempt  # Only for testing, consider CSRF protection in production
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number')  # Corrected field name
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Username Taken'}, status=400)
            elif User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email Taken'}, status=400)
            else:
                user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, gender=gender, contact_number=contact_number, username=username, password=password1)
                user.save()
                return JsonResponse({'message': 'Successfully Registered'})

        else:
            return JsonResponse({'message': 'Passwords do not match'}, status=400)

    return render(request, 'register.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def logout(request):
    logout(request)
    return redirect('login')