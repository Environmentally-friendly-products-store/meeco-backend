from decimal import Decimal

from orders import appvars as VARS
from products.models import Product
from products.serializers import ShortProductSerializer


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(VARS.CART_SESSION_ID)
        if not cart:
            cart = self.session[VARS.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session[VARS.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product, amount=1, overide_amount=False):
        product_id = str(product["id"])
        if product_id not in self.cart:
            self.cart[product_id] = {
                "amount": 0,
                "price": str(product["price"]),
            }
        if overide_amount:
            self.cart[product_id]["amount"] = amount
        else:
            self.cart[product_id]["amount"] += amount
        self.save()

    def remove(self, product):
        product_id = str(product["id"])

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = ShortProductSerializer(
                product
            ).data
        for item in cart.values():
            item["price"] = float(item["price"])
            item["total_price"] = item["price"] * item["amount"]
            yield item

    def __len__(self):
        return sum(item["amount"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["amount"]
            for item in self.cart.values()
        )

    def clear(self):
        del self.session[VARS.CART_SESSION_ID]
        self.session.modified = True
