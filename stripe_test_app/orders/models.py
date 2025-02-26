from django.db import models

from items.models import Item

class Tax(models.Model):
    """Модель для хранения налогов"""
    tax_id = models.CharField(max_length=255, unique=True)  # ID налога в Stripe
    percentage = models.DecimalField(max_digits=3, decimal_places=1)  # Процент налога
    name = models.CharField(max_length=100)  # Название налога

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Discount(models.Model):
    """Модель для хранения скидок"""
    # Используйте Stripe API или панель управления Stripe для создания купона.
    coupon_id = models.CharField(max_length=255, unique=True)  # ID купона в Stripe
    # Percent that will be taken off the subtotal of any invoices
    # for this customer for the duration of the coupon. For example,
    # a coupon with percent_off of 50 will make a $100 invoice $50 instead.
    percent_off = models.DecimalField(max_digits=3, decimal_places=1)  # Процент скидки
    name = models.CharField(max_length=100)  # Название скидки

    def __str__(self):
        return f"{self.name} ({self.percent_off}%)"


# Model to store individual order items
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)

    @property
    def total_price(self):
        return self.item.price * self.quantity


# Model for orders
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    @property
    def total_cost(self):
        return sum(item.total_price for item in self.items.all())


