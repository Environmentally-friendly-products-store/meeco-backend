from orders.models import Order, OrderProduct, Product


def build_order(db_cart, order_id):
    """
    Перенос корзины залогиненного пользователя в заказ и её удаление.
    """
    total = 0
    for item in db_cart:
        order = Order.objects.get(id=order_id)
        product = Product.objects.get(id=item.product_id)
        data = {
            "order_id": order,
            "product_id": product,
            "amount": item.amount,
            "purchase_price": item.price,
        }
        record = OrderProduct.objects.create(**data)
        total += record.item_total
    db_cart.delete()
    return total
