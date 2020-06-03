from django.core.paginator import Paginator
from django.shortcuts import render

from listings.models import Book


def index(request):
    books = Book.objects.order_by('-created')
    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_books = paginator.get_page(page_number)
    return render(request, 'listings/listings.html', {'books': page_books})


def listing(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'listings/listing.html', {'book': book})


def search(request):
    return render(request, 'listings/search.html')
