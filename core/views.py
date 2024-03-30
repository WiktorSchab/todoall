from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import LoginForm, SignUpForm, PrivateTaskForm
from .models import PrivateTask

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
    if request.method == 'POST':
        form = PrivateTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            date = form.cleaned_data.get('date')
            hour = form.cleaned_data.get('hour')
            color = form.cleaned_data.get('color')

            """ Checking if user is logged or not
            if he is data will be stored in db
            otherwise data will be stored in session on user browser """
            if request.user.is_authenticated:
                print('zalogowany')
            else:
                if 'private_tasks' not in request.session:
                    request.session['private_tasks'] = [] 

                data = {
                    'title':title,
                    'description':description,
                    'color':color,
                    'date':date.isoformat(),
                    'hour':hour.isoformat(),
                }

                request.session['private_tasks'].append(data)

                request.session.modified = True
        return redirect('mytodo')
    else:    
        form = PrivateTaskForm()

    context = {
        'form': form,
    }
    return render(request, 'mytodo.html', context)