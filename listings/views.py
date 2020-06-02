from django.shortcuts import render

# Create your views here.
from listings.models import Book


def index(request):
    books = Book.objects.all().order_by('-created')
    return render(request, 'listings/listings.html', {'books': books})


def listing(request):
    return render(request, 'listings/listing.html')


def search(request):
    return render(request, 'listings/search.html')
