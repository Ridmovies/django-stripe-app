from django.db import models

from items.models import Item


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

    @property
    def total_cost(self):
        return sum(item.total_price for item in self.items.all())
