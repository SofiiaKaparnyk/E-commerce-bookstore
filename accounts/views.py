from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already used')
                return redirect('register')
            # All OK
            user = User.objects.create(username=username, email=email, password=password)
            # Login after register
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if not user:
            user = auth.authenticate(email=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
        return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
