# Generated by Django 4.2.4 on 2024-02-04 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_alter_sellingproduct_color_variant_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sellingproduct",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]