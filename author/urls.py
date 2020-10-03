from django.urls import path

from .views import *

urlpatterns = [
    path('', AuthorViewAll.as_view(), name='all_author'),
    path('<int:pk>/', AuthorViewById.as_view(), name='author_by_id_url'),
    path('author_create/', AuthorCreate.as_view(), name='author_create_url'),
    path('<int:id>/author_update/', AuthorUpdate.as_view(), name='author_update_url'),
    path("delete/<int:id>/", delete_author, name="delete_author"),
]
