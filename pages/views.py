from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from listings.models import Book


def index(request):
    books = Book.objects.order_by('-created')[:3][::-1]
    return render(request, 'pages/index.html', {'books': books})


def about(request):
    return render(request, 'pages/about.html')
