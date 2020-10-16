from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect

from contacts.models import Contact
from listings.models import Book


def contact(request):
    if request.method == 'POST':
        data = request.POST

        # Check is it the first request
        user_id = data['user_id']
        book = Book.objects.get(id=data['book_id'])
        has_contacted = Contact.objects.filter(user_id=user_id, book=book)
        if has_contacted:
            messages.error(request,
                           'Ви уже створили запит для цієї книги. \
                           Зачекайте пок з вами зв\'яжеться власник.')
            return redirect('/listings/' + str(book.id))

        Contact.objects.create(book=book,
                               name=data['name'],
                               email=data['email'],
                               phone=data['phone'],
                               message=data.get('message'),
                               user_id=user_id)

        # Send email to owner
        send_mail(
            "Новий запит для вашої книги.",
            data['message'],
            data['email'],
            [book.owner.user.email],
            fail_silently=False
        )

        messages.success(request, 'Ваш запит було відправлено')
        return redirect('/accounts/dashboard/')


def delete_contact(request):
    if request.method == 'POST':
        data = request.POST
        Contact.objects.get(book_id=data['book_id'], user_id=request.user.id).delete()
        return redirect('/accounts/dashboard/')
