from django.contrib.auth.models import User
from django.db import models

from menu.models import Menu, MenuItem


class Order(models.Model):
    ordered_by = models.OneToOneField(
        User, related_name="user", on_delete=models.CASCADE
    )
    menu = models.OneToOneField(Menu, related_name="menu", on_delete=models.CASCADE)
    item_selected = models.OneToOneField(
        MenuItem, related_name="item_selected", on_delete=models.CASCADE, null=True
    )
    customization = models.CharField(max_length=150)
    created = models.DateField(auto_now_add=True)

    class Meta:
        # Just one selection per day
        unique_together = [["ordered_by", "menu"]]

    def __str__(self):
        return str(self.id)
