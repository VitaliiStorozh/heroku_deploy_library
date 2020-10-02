from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import ListView, View

from authentication.models import CustomUser
from author.forms import AuthorForm
from author.models import Author


class AuthorViewById(ListView):
    model = Author
    template_name = 'author/author.html'
    context_object_name = 'authors'
    paginate_by = 10

    def get_queryset(self):
        try:
            return Author.objects.filter(pk=self.kwargs['pk'])
        except Author.DoesNotExist:
            raise Http404("No Books matches the given query.")


class AuthorViewAll(ListView):
    model = Author
    template_name = 'author/author.html'
    context_object_name = 'authors'
    paginate_by = 10
    queryset = Author.objects.all()


class AuthorCreate(View):
    def get(self, request):
        form = AuthorForm()
        return render(request, 'author/author_create.html', context={'form': form})

    def post(self, request):
        bound_form = AuthorForm(request.POST)

        if bound_form.is_valid():
            new_author = bound_form.save()
            return redirect(f'/author/{new_author.id}/')
        return render(request, '/author/author_create.html', context={'form': bound_form})


def delete_author(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    Author.delete_by_id(id)
    return redirect("all_author")
