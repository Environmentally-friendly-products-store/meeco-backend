from django.contrib import admin

from .models import Event, ProductEvent


class ProductEventInline(admin.TabularInline):
    model = ProductEvent
    min_num = 1
    max_num = 200
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = (ProductEventInline)
    list_display = ('name', 'description', 'discount',
                    'start_date', 'end_date')
    list_filter = ('name', 'discount', 'start_date', 'end_date')
    empty_value_display = '-пусто-'


admin.site.register(Event, EventAdmin)
