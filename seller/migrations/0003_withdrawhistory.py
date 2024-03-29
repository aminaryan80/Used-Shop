# Generated by Django 4.2.4 on 2024-02-04 21:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("seller", "0002_sellhistory"),
    ]

    operations = [
        migrations.CreateModel(
            name="WithdrawHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.PositiveIntegerField()),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="seller.seller"
                    ),
                ),
            ],
        ),
    ]
