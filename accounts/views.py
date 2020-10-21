from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from contacts.models import Contact
from listings.models import Book, Category
from owners.models import Owner


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
            next = request.POST.get('next')
            return redirect(next) if next != '' else redirect('dashboard')
        messages.error(request, 'Invalid credentials')
        return redirect('login')
    next = request.GET.get('next')
    if next:
        return render(request, 'accounts/login.html', {'next': next})
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'pages/index.html')


def dashboard(request):
    inquiries = Contact.objects.filter(user_id=request.user.id)
    return render(request, 'accounts/dashboard.html', {'inquiries': inquiries})


def add_listing(request):
    if request.method == 'POST':
        data = request.POST
        # category
        image_main = request.FILES['image_main']
        is_new = True if data.get('is_new') else False
        can_be_exchanged = True if data.get('can_be_exchanged') else False
        Book.objects.create(title=data['title'], is_new=is_new, author=data['author'],
                            price=data['price'], description=data.get('description'),
                            owner=request.user.owner,
                            publisher=data['publisher'], language=data['language'],
                            year_of_publishing=data['year_of_publishing'],
                            number_of_pages=data['number_of_pages'],
                            translator=data['translator'], book_cover=data['book_cover'],
                            can_be_exchanged=can_be_exchanged, rate=data['rate'],
                            image_main=image_main)
    categories = Category.objects.all()
    books = Book.objects.filter(owner=Owner.objects.get(user=request.user))
    return render(request, 'accounts/add_listing.html', {'books': books, 'categories': categories})


def delete_listing(request):
    if request.method == 'POST':
        Book.objects.get(id=request.POST.get('book_id')).delete()
        books = Book.objects.filter(owner=Owner.objects.get(user=request.user))
        return redirect('/accounts/add/', {'books': books})


def account_settings(request):
    return render(request, 'accounts/settings.html')
