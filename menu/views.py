from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.forms.utils import ErrorList
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import localdate
from django.views import View
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import CreateView

from menu.forms import OPTION_FORM_SET, OPTION_FORM_SET_UPDATE, CreateMenuForm
from menu.models import Menu
from staff.models import Order

from share.notification.tasks import send_menu_notification


class MenuCreaterView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View to display the form in order to generate a new menu and its items"""

    model = Menu
    template_name = "admin/create_menu.html"
    form_class = CreateMenuForm
    login_url = "/account/login/"
    success_url = None

    def get_initial(self):
        if "date" in self.kwargs:
            return {"date": self.kwargs["date"]}
        return {"date": timezone.now().date()}

    def get_context_data(self, **kwargs):
        data = super(MenuCreaterView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["description"] = OPTION_FORM_SET(self.request.POST)
        else:
            data["description"] = OPTION_FORM_SET()
        return data

    @transaction.atomic
    def form_valid(self, form: CreateMenuForm):
        date = form.instance.date
        exist_menu_for_date = Menu.objects.filter(date=date).exists()
        if exist_menu_for_date:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(
                [f"A menu for this date was already created before: {date}"]
            )
            return self.form_invalid(form)

        context = self.get_context_data()
        description = context["description"]
        form.instance.created_by = self.request.user
        self.object = form.save()
        if description.is_valid():
            description.instance = self.object
            description.instance.created_by = self.request.user
            description.save()

        return super(MenuCreaterView, self).form_valid(form)

    def get_success_url(self):
        return reverse("menu:list_menus")

    def test_func(self):
        return self.request.user.is_superuser


class MenuListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """List all menus that have been created"""

    model = Menu
    context_object_name = "menus"
    template_name = "admin/list_menu.html"
    login_url = "/account/login/"
    ordering = [
        "-date",
    ]

    def test_func(self):
        return self.request.user.is_superuser


class MenuUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Vew to display the form in order to update a menu's items"""

    model = Menu
    template_name = "admin/create_menu.html"
    form_class = CreateMenuForm
    login_url = "/account/login/"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        data = super(MenuUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["description"] = OPTION_FORM_SET_UPDATE(
                self.request.POST, instance=self.object
            )
        else:
            data["description"] = OPTION_FORM_SET_UPDATE(instance=self.object)
        return data

    @transaction.atomic
    def form_valid(self, form: CreateMenuForm):
        date = form.instance.date
        exist_menu_for_date = (
            Menu.objects.filter(date=date).exclude(pk=form.instance.pk).exists()
        )
        if exist_menu_for_date:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(
                [f"A menu for this date was already created before: {date}"]
            )
            return self.form_invalid(form)
        context = self.get_context_data()
        item = context["description"]
        form.instance.created_by = self.request.user
        self.object = form.save()
        if item.is_valid():
            item.instance = self.object
            item.save()

        return super(MenuUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("menu:list_menus")


def menu_order(request: HttpRequest, menu_id: str):
    """View to call the logic in the staff app"""
    return redirect("staff:select", menu_id=menu_id)


class OrdersRequestedListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """View to get and list all orders that are requested by users in the current day"""

    model = Order
    context_object_name = "orders"
    template_name = "admin/view_orders_requested.html"
    login_url = "/account/login/"
    ordering = [
        "-created",
    ]

    def get_queryset(self):
        current_date = localdate()
        return Order.objects.filter(menu__date=current_date)

    def get_context_data(self, **kwargs):
        current_date = localdate()
        kwargs.update({"current_date": current_date})
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.is_superuser


def __is_superuser_check(user):
    return user.is_superuser


@login_required(login_url="/account/login/")
@user_passes_test(__is_superuser_check, login_url="/account/login/")
def send_reminder(request: HttpRequest) -> HttpResponseRedirect:
    """
    View to send slack reminder

    Parameters:
      request (HttpRequest): django request object
    """
    current_date = localdate()
    today_menu: Menu = Menu.objects.get(date=current_date)
    send_menu_notification.delay(today_menu.uuid)
    messages.success(request, "Slack Reminders are being processed")
    return redirect(reverse("menu:list_menus"))
