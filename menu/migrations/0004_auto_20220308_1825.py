# Generated by Django 3.0.8 on 2022-03-08 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0003_auto_20220308_1722"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="date",
            field=models.DateField(),
        ),
    ]
