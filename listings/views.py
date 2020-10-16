from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from listings.models import Book, Category


def index(request):
    books = Book.objects.order_by('-created')
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_books = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'listings/search.html', {'books': page_books, 'categories': categories})


@login_required
def listing(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'listings/listing.html', {'book': book})


def search(request):
    context = {}
    keywords = request.GET.get('keywords')
    category = request.GET.get('category')
    categories = Category.objects.all()
    books = Book.objects.order_by('-created')
    if keywords:
        books = Book.objects.filter(
            Q(author__icontains=keywords) | Q(title__icontains=keywords))
        context['keyword_selected'] = keywords
    if category != 'Категорія (Усі)' and category is not None and category != '':
        context['category_selected'] = category
        category_id = Category.objects.get(title=category).id
        books = books.filter(category=category_id)
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_books = paginator.get_page(page_number)
    context['books'] = page_books
    context['categories'] = categories
    return render(request, 'listings/listings.html', context)
