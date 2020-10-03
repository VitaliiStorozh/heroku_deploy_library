from django.urls import path
from .views import *

urlpatterns = [
    path('authors_book/<authors>/', BooksListViewByAuthor.as_view(), name='books_list_url'),
    path('<int:pk>/', BooksViewById.as_view(), name='book_by_id_url'),
    path('book_create/', BookCreate.as_view(), name='book_create_url'),
    path('<int:id>/book_update/', BookUpdate.as_view(), name='book_update_url'),
    path('', BooksViewAll.as_view(), name='all_books'),
    path("delete/<int:id>/", delete_book, name="delete_book"),
]
