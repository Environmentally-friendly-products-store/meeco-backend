from django.contrib import admin
from orders.models import DeliveryAddress, OrderProduct, Order

admin.site.register(DeliveryAddress)
admin.site.register(OrderProduct)
admin.site.register(Order)
