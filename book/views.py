from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from author.models import Author
from book.models import Book


class BooksListView(ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        self.author = get_object_or_404(Author, name=self.kwargs['author'])
        return Book.objects.filter(author=self.author)
