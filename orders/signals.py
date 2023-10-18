from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from orders.services.cart import Cart


@receiver(user_logged_in)
def on_login(user, request, **kwargs):
    """
    Перенос корзины пользователя из сессии в БД при входе в систему.
    """
    cart = Cart(request)
    if cart:
        cart.build_cart(user)
