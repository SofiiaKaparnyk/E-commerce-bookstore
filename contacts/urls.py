from django.urls import path

from contacts import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('delete_contact/', views.delete_contact, name='delete_contact'),
]
