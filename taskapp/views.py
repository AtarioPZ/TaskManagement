from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.db import OperationalError
from .models import Task
from .forms import TaskForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


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
           try:                
                login(request, user)                
                return redirect('dashboard')
           except OperationalError:
                error_message = 'Failed to connect. Please try again after some minutes.'
                return render(request, 'login.html', {'error_message': error_message})
        else:           
            messages.error(request, 'Invalid username or password.')
        
    return render(request, 'login.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.instance)  # Update session to prevent log out
            messages.success(request, 'Profile information successfully updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session to prevent log out
            messages.success(request, 'Password successfully changed.')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect("/")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        confirm_email = request.POST['confirm_email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate email and password
        if email != confirm_email:
            return render(request, 'signup.html', {'error': 'Emails do not match.'})
        
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})

        # Create the user and save to the database
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Redirect to the login page or any other desired page
        return redirect('user_login')
    else:
        return render(request, 'signup.html')
    
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('dashboard')

def profile(request):
    return render(request, 'profile.html')