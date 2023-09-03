from django.contrib import admin
from orders.models import DeliveryAddress, OrderProducts, Orders

admin.site.register(DeliveryAddress)
admin.site.register(OrderProducts)
admin.site.register(Orders)
