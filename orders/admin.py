from django.contrib import admin
from orders.models import DeliveryAddress, OrderProducts, Orders

admin.site.register(DeliveryAddress, OrderProducts, Orders)
