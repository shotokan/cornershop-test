import uuid
from django.contrib.auth.models import User
from django.db import models


class Menu(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, null=True)
    date = models.DateField()
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.pk} menu date: {self.date}"


class MenuItem(models.Model):
    description = models.TextField()
    menu = models.ForeignKey(Menu, related_name="has_items", on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ["created"]
