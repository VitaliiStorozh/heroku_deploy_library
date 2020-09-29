from django.http import Http404

from django.views.generic import ListView

from author.models import Author


class AuthorViewById(ListView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'authors'
    paginate_by = 10

    def get_queryset(self):
        try:
            return Author.objects.filter(pk=self.kwargs['pk'])
        except Author.DoesNotExist:
            raise Http404("No Books matches the given query.")
