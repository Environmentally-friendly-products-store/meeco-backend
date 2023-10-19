from orders.models import OrderProduct, Product


def build_order(db_cart, order_instance):
    """
    Перенос корзины залогиненного пользователя в заказ и её удаление.
    """
    order_total = 0
    for item in db_cart:
        product_instance = Product.objects.get(id=item.product_id)
        data = {
            "order_id": order_instance,
            "product_id": product_instance,
            "amount": item.amount,
            "purchase_price": product_instance.price_per_unit,
        }
        record = OrderProduct.objects.create(**data)
        order_total += record.item_total
    db_cart.delete()
    return order_total
