from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import Item, Discount, Tax, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Item.
    """
    list_display = ('name', 'price', 'currency', 'description')
    list_filter = ('currency',)
    search_fields = ('name', 'description')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Discount.
    """
    list_display = ('name', 'percent_off')
    search_fields = ('name',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Tax.
    """
    list_display = ('name', 'percentage')
    search_fields = ('name',)


class OrderAdminForm(forms.ModelForm):
    """
    Форма для валидации валюты перед сохранением заказа.
    """

    class Meta:
        model = Order
        fields = '__all__'

    def clean(self):
        """
        Проверяет, что все товары в заказе имеют одну валюту.

        Вызывает:
            ValidationError: Если у товаров в заказе разные валюты.
        """
        cleaned_data = super().clean()
        items = cleaned_data.get("items", [])

        currencies = {item.currency for item in items}

        if len(currencies) > 1:
            raise ValidationError("Все товары в заказе должны быть в одной валюте!")

        return cleaned_data


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Order.
    """
    form = OrderAdminForm
    list_display = ('id', 'created_at', 'currency', 'get_total_price')
    list_filter = ('currency', 'created_at')
    filter_horizontal = ('items',)
    readonly_fields = ('created_at', 'currency')

    def get_total_price(self, obj):
        """
        Возвращает общую сумму заказа.

        Аргументы:
            obj (Order): Объект заказа.

        Возвращает:
            Decimal: Общая стоимость заказа.
        """
        return obj.get_total_price()

    get_total_price.short_description = 'Total Price'

    def save_related(self, request, form, formsets, change):
        """
        Проверяет валюту товаров перед сохранением заказа.
        В случае ошибки выводит сообщение в админке.

        Аргументы:
            request (HttpRequest): Запрос от администратора.
            form (ModelForm): Форма заказа.
            formsets (list): Связанные формсеты.
            change (bool): Флаг изменения существующего объекта.
        """
        super().save_related(request, form, formsets, change)
        order = form.instance

        try:
            order.currency = order.clean_items_currency()
            order.save(update_fields=["currency"])
        except ValidationError as e:
            messages.error(request, str(e))
