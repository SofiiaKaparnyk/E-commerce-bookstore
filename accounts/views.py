from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accounts.forms import CategoryForm
from contacts.models import Contact
from listings.models import Book
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
            data = request.POST
            Owner.objects.create(phone=data['phone'], city=data['city'], region=data['region'],
                                 street=data.get('street'))
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
    inquiries_from_other = Contact.objects.filter(book__owner=request.user.owner)
    return render(request, 'accounts/dashboard.html',
                  {'inquiries': inquiries, 'inquiries_from_other': inquiries_from_other})


def add_listing(request):
    if request.method == 'POST':
        data = request.POST
        form = CategoryForm(request.POST)
        categories = None
        if form.is_valid():
            categories = form.cleaned_data.get('Categories')
        image_main = request.FILES['image_main']
        is_new = True if data.get('is_new') else False
        can_be_exchanged = True if data.get('can_be_exchanged') else False
        book = Book.objects.create(title=data['title'], is_new=is_new, author=data['author'],
                                   price=data['price'], description=data.get('description'),
                                   owner=request.user.owner,
                                   publisher=data['publisher'], language=data['language'],
                                   year_of_publishing=data['year_of_publishing'],
                                   number_of_pages=data['number_of_pages'],
                                   translator=data['translator'], book_cover=data['book_cover'],
                                   can_be_exchanged=can_be_exchanged, rate=data['rate'],
                                   image_main=image_main)
        [book.category.add(category) for category in categories]
    categories = CategoryForm
    books = Book.objects.filter(owner=Owner.objects.get(user=request.user))
    year_range = [i for i in range(2020, 1950, -1)]
    return render(request, 'accounts/add_listing.html',
                  {'books': books, 'form': categories, 'year_range': year_range})


def edit_listing(request):
    if request.method == 'POST':
        book = Book.objects.get(id=request.POST.get('book_id'))
        data = request.POST
        form = CategoryForm(request.POST)
        categories = None
        if form.is_valid():
            categories = form.cleaned_data.get('Categories')
        image_main = request.FILES['image_main']
        is_new = True if data.get('is_new') else False
        can_be_exchanged = True if data.get('can_be_exchanged') else False
        book.title = data['title']
        book.is_new = is_new
        book.author = data['author']
        book.price = data['price']
        book.description = data['description']
        book.owner = request.user.owner
        book.publisher = data['publisher']
        book.language = data['language']
        book.year_of_publishing = data['year_of_publishing']
        book.number_of_pages = data['number_of_pages']
        book.translator = data['translator']
        book.book_cover = data['book_cover']
        book.can_be_exchanged = can_be_exchanged
        book.rate = data['rate']
        book.image_main = image_main
        [book.category.add(category) for category in categories]
        books = Book.objects.filter(owner=Owner.objects.get(user=request.user))
        return redirect('/accounts/add/', {'books': books})


def delete_listing(request):
    if request.method == 'POST':
        Book.objects.get(id=request.POST.get('book_id')).delete()
        books = Book.objects.filter(owner=Owner.objects.get(user=request.user))
        return redirect('/accounts/add/', {'books': books})


def account_settings(request):
    owner = request.user.owner
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        if User.objects.exclude(id=request.user.id).filter(username=username).exists():
            messages.error(request, "Ім'я юзера уже існує, виберіть інакше.")
            return render(request, 'accounts/settings.html', {'owner': owner})
        owner.user.username = username
        owner.user.save()
        owner.phone = data['phone']
        owner.city = data['city']
        owner.region = data['region']
        owner.street = data.get('street')
        owner.save()
        messages.success(request, "Дані було оновлено.")
        return render(request, 'accounts/settings.html', {'owner': owner})
    return render(request, 'accounts/settings.html', {'owner': owner})
