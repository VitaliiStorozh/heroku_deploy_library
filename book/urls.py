from django.urls import path
from . import views
from .views import BooksListViewByAuthor, BooksViewById

urlpatterns = [
    path('authors_book/<authors>/', BooksListViewByAuthor.as_view(), name='books_list_url'),
    path('<int:pk>/', BooksViewById.as_view(), name='book_by_id_url'),

]
