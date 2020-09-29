from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from .forms import RegisterForm, AuthoriseForm


def register(request, id=0):
    context = {}
    if request.POST:
        if id == 0:
            form = RegisterForm(request.POST)
        else:
            user = CustomUser.get_by_id(id)
            form = RegisterForm(request.POST, instance=user)
            context["data"] = form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            context["data"] = form
    else:
        if id == 0:
            form = RegisterForm()
        else:
            user = CustomUser.get_by_id(id)
            form = RegisterForm(instance=user)
        context["data"] = form
    return render(request, "register.html", context=context)


def authorise(request):
    context = {"email": None, "password": None}
    if request.POST:
        form = AuthoriseForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = CustomUser.get_by_email(email)
            if user.check_password(password):
                current_user = authenticate(request, email=email, password=password, role=user.role)
                login(request, current_user)
                return redirect("home")
            else:
                context["data"] = form
                context["password"] = "Incorrect password"
        except ValueError as ve:
            context["email"] = ve
            context["data"] = form
    else:
        form = AuthoriseForm()
        context["data"] = form
    return render(request, "authorise.html", context=context)


def log_out(request):
    logout(request)
    return redirect("home")


def get_all(request):
    return render(request, "get_users.html", {"users": CustomUser.get_all()})


def delete_user(request, id):
    CustomUser.delete_by_id(id)
    return redirect("get_users")


def home(request):
    return render(request, "home.html")
