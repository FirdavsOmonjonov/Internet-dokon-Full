from django.shortcuts import render, redirect
from main import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def log_in(request):
    """Log in to"""
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:index')
            else:
                return render(request,'dashboard/auth/error.html')
        except:
            return redirect('index')
    return render(request, 'auth/login.html')


def log_out(request):
    """Log out of"""
    logout(request)
    return redirect('auth:error')


def error1(request):
    """Login error"""
    return render(request, 'auth/error.html')