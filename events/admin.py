from django.contrib import admin

from products.models import ProductEvent

from .models import Event


class ProductEventInline(admin.TabularInline):
    model = ProductEvent
    min_num = 1
    max_num = 200
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = (ProductEventInline,)
    list_display = ("id", "name", "description", "discount", "date_start", "date_end")
    list_filter = ("name", "discount", "date_start", "date_end")
    list_editable = ("name", "description", "discount", "date_start", "date_end")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


admin.site.register(Event, EventAdmin)
