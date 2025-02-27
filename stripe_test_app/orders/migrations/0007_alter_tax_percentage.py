# Generated by Django 5.1.6 on 2025-02-26 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0006_order_tax"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tax",
            name="percentage",
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
    ]
