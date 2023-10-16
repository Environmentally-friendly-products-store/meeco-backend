from celery import task
from django.core.mail import send_mail

from orders.models import Order


@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f"Заказ № {order_id} интернет-магазине EcoMe"
    message = f"Здравствуйте, {order.customer.first_name},\n\nВы успешно оформили заказ № {order_id}."
    mail_sent = send_mail(
        subject, message, "admin@myshop.com", [order.customer.email]
    )
    return mail_sent
