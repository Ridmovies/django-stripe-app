from django.db import models

class Item(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[('usd', 'USD'), ('eur', 'EUR')])  # Добавляем поле валюты

    def __str__(self):
        return self.name
