from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.db import OperationalError
from .models import Task
from .forms import TaskForm
from django.contrib.auth.models import User

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