from django import forms
from django.utils import timezone

from menu.models import Menu
from .models import Order


class OrderForm(forms.ModelForm):
    """Form to create a new order"""

    def __init__(self, *args, **kwargs):
        self.item_selected = args[0].get("item_selected")
        self.menu = args[0].get("menu")
        self.customization = args[0].get("customization")
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields["customization"].required = False

    def unique_selection_validation(self):
        """Check that the user has not selected an option for this current menu (today)"""
        order = Order.objects.filter(
            ordered_by=self.instance.ordered_by, menu=self.menu
        )
        if order.exists():
            raise forms.ValidationError("User already chose an item for this menu")

    def time_validation(self):
        """Validation to check if request is before 11 am in current day"""
        menu_date = Menu.objects.get(pk=self.menu).date
        now = timezone.localtime(timezone.now())
        cut_off_time = timezone.localtime(timezone.now()).replace(
            hour=11, minute=0, second=0, microsecond=0
        )
        now_date = now.date()
        if menu_date < now_date:
            raise forms.ValidationError("This is a past menu")
        if now_date == menu_date and now > cut_off_time:
            raise forms.ValidationError("You are too late")

    def clean(self):
        """Verify that user have not created a new order and that he is on time"""
        try:
            self.unique_selection_validation()
            self.time_validation()
        except forms.ValidationError as errors:
            for error in errors:
                self.add_error(None, error)

    class Meta:
        model = Order
        fields = ["item_selected", "menu", "customization"]
