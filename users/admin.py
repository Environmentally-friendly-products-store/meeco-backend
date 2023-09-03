from django.contrib import admin
from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
    )
    list_editable = (
        'username',
        'first_name',
        'last_name',
    )
    search_fields = ('username',)
    empty_value_display = '-пусто-'
