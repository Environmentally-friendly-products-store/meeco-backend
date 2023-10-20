from orders.serializers import DBCartSerializer
from users.models import ShoppingCart


class DBCart:
    """
    CRUD-операции для корзины в БД
    """

    def __init__(self, request):
        self.dbcart = ShoppingCart.objects.filter(user=request.user)

    def add(self, user, product_id, amount=1, overide_amount=False):
        pids = self.dbcart.values_list("product_id", flat=True)
        if product_id not in pids:
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

    # def remove(self, product_id):
    #     pid = str(product_id)
    #     if pid in self.cart:
    #         del self.cart[pid]
    #         self.save()

    def __iter__(self):
        serializer = DBCartSerializer(self.dbcart, many=True)
        yield from serializer.data

    # def __len__(self):
    #     return sum(item["amount"] for item in self.cart.values())

    def get_total_price(self):
        return sum([dict(item)["total_price"] for item in self.__iter__()])
