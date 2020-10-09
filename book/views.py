from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, View

from authentication.models import CustomUser
from author.models import Author
from book.forms import *
from book.models import Book


class BooksListViewByAuthor(ListView):
    model = Book
    template_name = 'book/books.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        self.authors = get_object_or_404(Author, name=self.kwargs['authors'])
        return Book.objects.filter(authors=self.authors)


class BooksViewById(ListView):
    model = Book
    template_name = 'book/books.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        try:
            return Book.objects.filter(pk=self.kwargs['pk'])
        except Book.DoesNotExist:
            raise Http404("No Books matches the given query.")


class BooksViewAll(ListView):
    model = Book
    template_name = 'book/books.html'
    context_object_name = 'books'
    # paginate_by = 10
    queryset = Book.objects.all()


class BookCreate(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Log in first!")
            return redirect("authorise")
        if not CustomUser.get_by_email(request.user.email).role == 1:
            messages.info(request, "You don`t have permission!")
            return redirect("home")
        form = BookForm()
        return render(request, 'book/book_create.html', context={'form': form})

    def post(self, request):
        bound_form = BookForm(request.POST)

        if bound_form.is_valid():
            new_book = bound_form.save()
            return redirect(f'/book/{new_book.id}/')
        return render(request, '/book/book_create.html', context={'form': bound_form})


class BookUpdate(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            messages.info(request, "Log in first!")
            return redirect("authorise")
        if not CustomUser.get_by_email(request.user.email).role == 1:
            messages.info(request, "You don`t have permission!")
            return redirect("home")
        try:
            book = Book.get_by_id(id)
            bound_form = BookForm(instance=book)
            return render(request, 'book/book_update_form.html', context={'form': bound_form, 'book': book})
        except Book.DoesNotExist:
            raise Http404("No Books matches to update.")

    def post(self, request, id):
        try:
            book = Book.get_by_id(id)
            bound_form = BookForm(request.POST, instance=book)
        except Book.DoesNotExist:
            raise Http404("No Books matches to update.")


        if bound_form.is_valid():
            new_book = bound_form.save()
            return redirect(f'/book/{new_book.id}/')
        return render(request, 'book/book_update_form.html', context={'form': bound_form, 'book': book})


def delete_book(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    try:
        Book.delete_by_id(id)
        return redirect("all_books")
    except Book.DoesNotExist:
        raise Http404("No Books matches to delete.")
    return redirect("all_books")
