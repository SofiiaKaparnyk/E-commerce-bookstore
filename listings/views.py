import redis as redis
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from accounts.forms import CategoryForm
from listings.models import Book, Category
from owners.models import Owner

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


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
    categories = CategoryForm
    year_range = [i for i in range(2020, 1950, -1)]
    total_views = r.incr('book:{}:views'.format(book.id))
    return render(request, 'listings/listing.html',
                  {'book': book, 'form': categories, 'year_range': year_range, 'total_views': total_views})


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
        image_main = request.FILES.get('image_main')
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
        if image_main:
            book.image_main = image_main
        book.category.clear()
        [book.category.add(category) for category in categories]
        book.save()
        categories = CategoryForm
        year_range = [i for i in range(2020, 1950, -1)]
        return render(request, 'listings/listing.html',
                      {'book': book, 'form': categories, 'year_range': year_range})


def delete_listing(request):
    if request.method == 'POST':
        Book.objects.get(id=request.POST.get('book_id')).delete()
        books = Book.objects.filter(owner=Owner.objects.get(user=request.user))
        return redirect('/accounts/add/', {'books': books})


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
