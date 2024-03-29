from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm, PrivateTaskForm

def home(request):
    return render(request, 'home.html')


def login_user(request):
    if request.method == 'POST':  
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have been successfully logged in.')
            return redirect('home')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'redirect_to': 'login',
    }
    return render(request, 'login_register.html', context)

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been successfully created. You have been logged in.')
            return redirect('home')
    else: 
        form = SignUpForm()    

    context = {
        'form':form,
        'redirect_to': 'register',
    }
    return render(request, 'login_register.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout was successful')
    return redirect('home')

def mytodo(request):
    form = PrivateTaskForm()
    context = {
        'form': form,
    }
    return render(request, 'mytodo.html', context)