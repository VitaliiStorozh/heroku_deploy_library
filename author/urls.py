from django.urls import path
from .views import AuthorViewById

urlpatterns = [
    path('<int:pk>/', AuthorViewById.as_view(), name='author_by_id_url'),
]
