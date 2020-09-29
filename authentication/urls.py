from django.urls import path
import authentication.views as views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("authorise/", views.authorise, name="authorise"),
    path("update/<int:id>/", views.register, name="update"),
    path("", views.get_all, name="get_users"),
    path("log_out/", views.log_out, name="log_out"),
    path("delete/<int:id>", views.delete_user, name="delete_user")
]
