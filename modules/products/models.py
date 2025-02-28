from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class Item(models.Model):
    """
    Модель, представляющая товар.

    Атрибуты:
        name (CharField): Название товара.
        description (TextField): Описание товара.
        price (DecimalField): Цена товара.
        currency (CharField): Валюта цены (USD или EUR).
    """

    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='usd'
    )

    def __str__(self):
        return self.name


class Discount(models.Model):
    """
    Модель, представляющая скидку.

    Атрибуты:
        name (CharField): Название скидки.
        percent_off (DecimalField): Процент скидки.
    """

    name = models.CharField(max_length=255)
    percent_off = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Скидка в процентах"
    )

    def __str__(self):
        return f"{self.name} ({self.percent_off}%)"


class Tax(models.Model):
    """
    Модель, представляющая налог.

    Атрибуты:
        name (CharField): Название налога.
        percentage (DecimalField): Процент налога.
    """

    name = models.CharField(max_length=255)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Налог в процентах"
    )

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Order(models.Model):
    """
    Модель заказа.

    Атрибуты:
        items (ManyToManyField): Список товаров в заказе.
        discount (ForeignKey): Примененная скидка (опционально).
        tax (ForeignKey): Примененный налог (опционально).
        created_at (DateTimeField): Дата и время создания заказа.
        currency (CharField): Валюта заказа (устанавливается автоматически).
    """

    items = models.ManyToManyField("Item")
    discount = models.ForeignKey(
        "Discount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tax = models.ForeignKey(
        "Tax",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(
        max_length=3,
        choices=Item.CURRENCY_CHOICES,
        editable=False,
        default="usd"
    )

    def clean_items_currency(self):
        """
        Проверяет, что все товары в заказе имеют одну валюту.

        Возвращает:
            str: Валюта заказа.

        Вызывает:
            ValidationError: Если в заказе присутствуют товары с разными валютами.
        """
        items = list(self.items.all())
        currencies = {item.currency for item in items}

        if len(currencies) > 1:
            raise ValidationError("Все товары в заказе должны быть в одной валюте!")

        return currencies.pop() if currencies else "usd"

    def save(self, *args, **kwargs):
        """
        Устанавливает валюту заказа перед сохранением.
        """
        if self.pk:
            try:
                self.currency = self.clean_items_currency()
            except ValidationError:
                pass
        super().save(*args, **kwargs)

    def get_total_price(self):
        """
        Рассчитывает общую стоимость заказа с учетом скидок и налогов.

        Возвращает:
            Decimal: Общая сумма заказа с учетом скидки и налога.
        """
        total = sum(item.price for item in self.items.all())

        if self.discount:
            total *= Decimal(1) - (self.discount.percent_off / Decimal(100))
        if self.tax:
            total *= Decimal(1) + (self.tax.percentage / Decimal(100))

        return round(total, 2)

    def __str__(self):
        return f"Order #{self.id or 'New'} ({self.currency})"
