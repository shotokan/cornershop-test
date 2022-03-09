from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.timezone import localdate, localtime
from django.views import View

from menu.models import Menu
from staff.forms import OrderForm

from .models import Order


class CreateOrderView(View):
    """View that display form to create and create the order for a user
    """
    def get(self, request: HttpRequest, menu_id: str):
        """Display the form to select an item and create the order

        Paramaters:
          request (HttpRequest): django object
          menu_id (str): the menu identifier
        """
        today_order = Order.objects.filter(
            menu__uuid=menu_id, ordered_by__id=request.user.id
        ).exists()
        # it is validated that the user has not selected an item for the menu
        if today_order:
            return redirect("staff:list_orders_staff")
        menu = Menu.objects.get(uuid=menu_id)
        return render(request, "staff/create_order.html", {"menu": menu})

    @method_decorator(login_required(login_url="/account/login/"))
    @transaction.atomic
    def post(self, request: HttpRequest, menu_id: str):
        """Create a new order for the user given a menu id

        Paramaters:
          request (HttpRequest): django object
          menu_id (str): the menu identifier
        """
        form = OrderForm(request.POST)
        form.instance.ordered_by = request.user
        menu = Menu.objects.get(uuid=menu_id)
        if form.is_valid():
            form.save()
            return redirect("staff:list_orders_staff")
        return render(request, "staff/create_order.html", {"form": form, "menu": menu})


class ListOrdersByStaffView(LoginRequiredMixin, View):
    """View to list orders that are created by a user"""

    login_url = "/account/login/"

    def get(self, request: HttpRequest):
        """List all options that a employee has selected
        
        parameters:
            request: django object
            render: a web page that displays the orders or option that belong to the employee
        """
        today_message = ""
        today_order = None
        orders = []
        try:
            today_order = Order.objects.get(
                menu__date=localdate(), ordered_by__id=request.user.id
            )
        except Order.DoesNotExist:
            today_message = "No order generated yet today"
        if today_order:
            orders = Order.objects.filter(ordered_by__id=request.user.id).exclude(
                pk=today_order.id
            )
        return render(
            request,
            "staff/list_orders.html",
            {
                "orders": orders,
                "today_order": today_order,
                "today_message": today_message,
            },
        )
