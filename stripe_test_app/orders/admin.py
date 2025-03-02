from django.contrib import admin

from orders.models import Discount, Order, OrderItem, Tax


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total_cost")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "quantity", "total_price")


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "percent_off")


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("tax_id", "name", "percentage")
