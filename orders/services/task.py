from pathlib import Path

from django.conf import settings
from django.template.loader import render_to_string

from core.mail_api.sendmail import send_email
from orders import appvars as VARS
from orders.models import OrderProduct

INVOICE_TEMPLATE = Path(settings.BASE_DIR) / "core/mail_api/invoice.html"


def order_created(order_instance):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order_id = order_instance.id
    created_at = order_instance.created_at.strftime("%d.%m.%Y")
    customer_email = order_instance.customer.email
    customer_name = (
        order_instance.customer.first_name + " " + order_instance.customer.last_name
    )
    subject = f"Заказ № {order_id} от {created_at} в интернет-магазине EcoMe"
    context = {
        "order_id": order_id,
        "created_at": created_at,
        "customer_name": order_instance.customer.first_name,
        "order_total": order_instance.price_total,
        "products": OrderProduct.objects.filter(order_id=order_id),
    }
    message = render_to_string(INVOICE_TEMPLATE, context)
    return send_email(customer_email, customer_name, subject, message)


def set_order_status(validated_data):
    """
    Task to set default order status when an order is successfully created.
    """
    if "status" in validated_data and validated_data["status"]:
        return validated_data["status"]
    return VARS.ORDER_STATUS_DEFAULT
