from mail.send_mail import gmail_send_message
from orders import appvars as VARS


def order_created(order_instance):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    subject = f"Заказ № {order_instance.id} в интернет-магазине EcoMe"
    message = f"Здравствуйте, <b>{order_instance.customer.first_name}</b>,</br>"
    f"Вы успешно оформили заказ № {order_instance.id} "
    f"на сумму {order_instance.price_total} руб."
    return gmail_send_message(order_instance.customer.email, subject, message)


def set_order_status(validated_data):
    """
    Task to set default order status when an order is successfully created.
    """
    if "status" in validated_data and validated_data["status"]:
        return validated_data["status"]
    return VARS.ORDER_STATUS_DEFAULT
