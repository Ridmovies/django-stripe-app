# Generated by Django 5.1.6 on 2025-02-27 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("items", "0004_alter_item_product_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="item",
            name="product_id",
        ),
    ]
