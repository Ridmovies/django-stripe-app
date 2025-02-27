class OrderService:
    @staticmethod
    def get_line_items_for_order(order):
        """Получить список товаров для Stripe Checkout"""
        line_items = []
        for order_item in order.items.all():
            item = order_item.item
            line_item = {
                "price_data": {
                    "currency": item.currency,
                    "product_data": {
                        "name": item.name,
                        "description": item.description,
                    },
                    "unit_amount": int(
                        item.price * 100
                    ),  # Stripe требует сумму в центах
                },
                "quantity": order_item.quantity,
            }

            # Добавляем налоговую ставку к каждому товару, если она есть
            if order.tax:
                line_item["tax_rates"] = [
                    order.tax.tax_id
                ]  # Используем tax_id из Stripe

            line_items.append(line_item)

        return line_items
