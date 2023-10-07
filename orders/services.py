from decimal import Decimal

from orders import appvars as VARS
from orders.models import OrderProduct, Product
from orders.serializers import ProductSerializer


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(VARS.CART_SESSION_ID, {})

    def save(self):
        self.session[VARS.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, amount=1, overide_amount=False):
        pid = str(product_id)
        price = str(Product.objects.get(id=product_id).price_per_unit)
        if pid not in self.cart:
            self.cart[pid] = {
                "amount": amount,
                "price": price,
            }
        else:
            if overide_amount:
                self.cart[pid]["amount"] = amount
                self.cart[pid]["price"] = price
            else:
                self.cart[pid]["amount"] += amount
                self.cart[pid]["price"] = price
        self.save()

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = ProductSerializer(product).data
        for item in cart.values():
            item["price"] = Decimal(item["price"])
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

    def build_order(self, order_id):
        # products = []
        for product_id, data in self.items():
            # products.append(
            OrderProduct.objects.create(
                order_id=order_id,
                product_id=product_id,
                amount=data["amount"],
                purchase_price=data["price"],
                item_total=data["total_price"],
            )
        # )
        # order.items.bulk_create(items)
        self.clear()
        # return order_id
