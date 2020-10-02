from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from authentication.models import CustomUser
from book.models import Book
from .models import Order


def get_orders(request):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if CustomUser.get_by_email(request.user.email).role == 1:
        orders = Order.get_all()
    else:
        orders = list(Order.objects.all().filter(user_id=request.user.id))
    if len(orders) == 0:
        raise Http404("You don't have any order")
    return render(request, "get_orders.html", {"orders": orders})


def new_order(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    book = Book.get_by_id(id)
    if not book:
        raise Http404("This book doesn't exist")
    if Order.create(request.user, book, datetime.now() + timedelta(days=14)) is None:
        messages.warning(request, f"We haven't any available book with name: {book.name} ")
    else:
        messages.info(request, "Order saved!")
    return redirect("books_list_url")


def delete_order(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if not (Order.get_by_id(id).user.id == request.user.id or CustomUser.get_by_id(request.user.id).role == 1):
        raise PermissionDenied
    if not Order.delete_by_id(id):
        raise Http404("Order doesn't exist")
    return redirect("get_orders")
