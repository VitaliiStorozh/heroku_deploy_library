from django.urls import path
from . import views
from .views import BooksListView

urlpatterns = [
    path('books_list/<author>/', BooksListView.as_view(), name='books_list_url'),

]
