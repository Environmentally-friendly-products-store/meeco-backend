from django.shortcuts import get_object_or_404

from orders.models import OrderProduct, Product
from orders.serializers import DBCartSerializer
from users.models import ShoppingCart


class DBCart:
    """
    CRUD-операции для корзины в БД
    """

    def __init__(self, request):
        self.dbcart = ShoppingCart.objects.filter(user=request.user)

    def add(self, user, product_id, amount=1, overide_amount=False):
        product_ids = self.dbcart.values_list("product_id", flat=True)
        if product_id not in product_ids:
            ShoppingCart.objects.create(
                user_id=user,
                product_id=product_id,
                amount=amount,
            )
        else:
            item = self.dbcart.get(product_id=product_id)
            if overide_amount:
                item.amount = amount
            else:
                item.amount += amount
            item.save()

    def remove(self, product_id):
        get_object_or_404(self.dbcart, product=product_id).delete()

    def clear(self):
        self.dbcart.delete()

    def __iter__(self):
        serializer = DBCartSerializer(self.dbcart, many=True)
        yield from serializer.data

    def __len__(self):
        return sum([dict(item)["amount"] for item in self.__iter__()])

    def get_total_price(self):
        return sum([dict(item)["total_price"] for item in self.__iter__()])

    def build_order(self, order_instance):
        """
        Перенос корзины залогиненного пользователя в заказ и её удаление.
        """
        order_total = 0
        for item in self.dbcart:
            product_instance = Product.objects.get(id=item.product.pk)
            data = {
                "order_id": order_instance,
                "product_id": product_instance,
                "amount": item.amount,
                "purchase_price": product_instance.price_per_unit,
            }
            record = OrderProduct.objects.create(**data)
            order_total += record.item_total
        self.clear()
        return order_total
