# Generated by Django 3.0.8 on 2022-03-09 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("menu", "0009_auto_20220309_0030"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("customization", models.CharField(max_length=150)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "item_selected",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item_selected",
                        to="menu.MenuItem",
                    ),
                ),
                (
                    "menu",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menu",
                        to="menu.Menu",
                    ),
                ),
                (
                    "ordered_by",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("ordered_by", "menu")},
            },
        ),
    ]