from orders.serializers import DBCartSerializer
from users.models import ShoppingCart

# from products.models import Product


class DBCart:
    """
    CRUD-операции для корзины в БД
    """

    def __init__(self, request):
        self.dbcart = ShoppingCart.objects.filter(user=request.user)

    def add(self, product_id, amount=1, overide_amount=False):
        # pid = str(product_id)
        item = self.dbcart.get(product_id=product_id)
        if item:
            item.amount += amount
        else:
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

    # def clear(self):
    #     del self.session[VARS.CART_SESSION_ID]
    #     self.session.modified = True

    # def build_cart(self, user):
    #     """
    #     Перенос корзины залогиненного пользователя из гостевой сессии в
    #     таблицу БД. Если в корзине есть совпадающие товары, то их количество
    #     суммируется.
    #     Цена в таблице корзины не хранится, берется из таблицы продукта.
    #     """
    #     ids = list(
    #         ShoppingCart.objects.filter(user=user).values_list("product_id", flat=True)
    #     )
    #     for product_id, data in self.cart.items():
    #         product = Product.objects.get(id=int(product_id))
    #         if product.id in ids:
    #             item = ShoppingCart.objects.get(product=product)
    #             item.amount += data["amount"]
    #             # item.price = data["price"]
    #             item.save()
    #         else:
    #             ShoppingCart.objects.create(
    #                 user=user,
    #                 product=product,
    #                 amount=data["amount"],
    #                 # price=data["price"],
    #             )
    #     self.clear()
