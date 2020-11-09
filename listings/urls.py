from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:book_id>/', views.listing, name='listing'),
    path('add/', views.add_listing, name='add_book'),
    path('edit/', views.edit_listing, name='edit_book'),
    path('delete/', views.delete_listing, name='delete_book'),
    path('search/', views.search, name='search'),
]
