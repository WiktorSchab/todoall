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
        # Creating a form based on data submitted via POST method
        form = PrivateTaskForm(request.POST)

        if form.is_valid():
            # Getting clean data from the form
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            date = form.cleaned_data.get('date')
            hour = form.cleaned_data.get('hour')
            color = form.cleaned_data.get('color')

            # Checking if the user is logged in
            if request.user.is_authenticated:
                # If the user is logged in, save the form to the database
                private_task = form.save(commit=False)
                private_task.owner = request.user
                private_task.save()
            else:
                # If the user is not logged in, save the data in the session
                if 'private_tasks' not in request.session:
                    request.session['private_tasks'] = [] 

                # Creating a dictionary containing task data
                data = {
                    'title':title,
                    'description':description,
                    'color':color,
                    'date':date.isoformat(),
                    'hour':hour.isoformat(),
                }

                # Adding task data to the session
                request.session['private_tasks'].append(data)

                # Marking the session as modified
                request.session.modified = True
   
        return redirect('mytodo')
    else:    
        form = PrivateTaskForm()

        # Checking if the user is logged in
        if request.user.is_authenticated:
            # Getting data to display from DB
            pass
        else:
            # Getting data to display from Session
            pass

    context = {
        'form': form,
    }

    return render(request, 'mytodo.html', context)