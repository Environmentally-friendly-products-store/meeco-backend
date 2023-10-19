from users.models import ShoppingCart


class DBCart:
    """
    CRUD-операции для корзины в БД
    """

    def __init__(self, request):
        self.dbcart = ShoppingCart.objects.filter(user=request.user)
        # self.serializer = DBCartSerializer(self.dbcart, many=True)

    # def save(self):
    #     self.session[VARS.CART_SESSION_ID] = self.cart
    #     self.session.modified = True

    # def add(self, product_id, amount=1, overide_amount=False):
    #     pid = str(product_id)
    #     price = str(Product.objects.get(id=product_id).price_per_unit)
    #     if pid not in self.cart:
    #         self.cart[pid] = {
    #             "amount": amount,
    #             "price": price,
    #         }
    #     else:
    #         if overide_amount:
    #             self.cart[pid]["amount"] = amount
    #             self.cart[pid]["price"] = price
    #         else:
    #             self.cart[pid]["amount"] += amount
    #             self.cart[pid]["price"] = price
    #     self.save()

    # def remove(self, product_id):
    #     pid = str(product_id)
    #     if pid in self.cart:
    #         del self.cart[pid]
    #         self.save()

    # def get_dbcart_list(self):
    #     serializer = DBCartSerializer(self.dbcart, many=True)
    #     return serializer.data

    # def __len__(self):
    #     return sum(item["amount"] for item in self.cart.values())

    # def get_total_price(self):
    #     return sum([dict(item)["total_price"] for item in self.get_dbcart_list])

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
