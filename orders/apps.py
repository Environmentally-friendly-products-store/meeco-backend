from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
    verbose_name = "Управление заказами"

    def ready(self):
        """Подключение сигналов"""
        import orders.signals  # noqa
