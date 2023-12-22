# Generated by Django 4.2.4 on 2023-11-18 16:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_alter_sellingproduct_color_variant_and_more"),
        ("customer", "0002_alter_cart_products"),
        ("seller", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SellHistory",
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
                ("total_price", models.PositiveIntegerField()),
                ("count", models.PositiveIntegerField()),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customer.customer",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.sellingproduct",
                    ),
                ),
            ],
        ),
    ]
