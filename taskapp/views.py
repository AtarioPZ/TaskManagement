from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login user
            login(request, user)
            # Redirect to dashboard page
            return redirect('dashboard')
        else:           
            messages.error(request, 'Invalid username or password.')
        
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def signup(request):
    return render(request, 'signup.html')

def dashboard(request):
    return render(request, 'dashboard.html')
