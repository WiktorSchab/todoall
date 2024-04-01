from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
def todoproject(request):
    return render(request, 'todoproject.html')
