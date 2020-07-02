from django.shortcuts import render

from listings.models import Book, Category


def index(request):
    books = Book.objects.order_by('-created')[:12]
    categories = Category.objects.all()
    return render(request, 'pages/index.html', {'books': books, 'categories': categories})


def about(request):
    return render(request, 'pages/about.html')
