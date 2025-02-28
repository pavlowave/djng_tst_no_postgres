import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_KEYS = settings.STRIPE_KEYS


def buy_item(request, id):
    """
    Создает сессию Stripe Checkout для покупки одного товара.

    Аргументы:
        request (HttpRequest): Запрос от клиента.
        id (int): ID товара.

    Возвращает:
        JsonResponse: JSON-ответ с идентификатором сессии Stripe.

    Вызывает:
        JsonResponse: Ошибка 404, если товар не найден.
    """
    item = get_object_or_404(Item, id=id)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.name,
                },
                "unit_amount": int(item.price * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:8000/success/",
        cancel_url="http://localhost:8000/cancel/",
    )

    return JsonResponse({"session_id": session.id})


def item_detail(request, id):
    """
    Отображает страницу с деталями товара.

    Аргументы:
        request (HttpRequest): Запрос от клиента.
        id (int): ID товара.

    Возвращает:
        HttpResponse: HTML-страница с информацией о товаре.
    """
    item = get_object_or_404(Item, id=id)
    return render(
        request,
        "products/item.html",
        {"item": item, "stripe_public_key": settings.STRIPE_PUBLIC_KEY}
    )


def buy_order(request, id):
    """
    Создает PaymentIntent в Stripe для оплаты заказа.

    Аргументы:
        request (HttpRequest): Запрос от клиента.
        id (int): ID заказа.

    Возвращает:
        JsonResponse: JSON-ответ с client_secret и валютой заказа.

    Вызывает:
        JsonResponse: Ошибка 404, если заказ не найден.
    """
    order = get_object_or_404(Order, id=id)

    stripe_secret_key = STRIPE_KEYS.get(order.currency, {}).get("secret", settings.STRIPE_SECRET_KEY)
    stripe.api_key = stripe_secret_key

    total_amount = int(order.get_total_price() * 100)

    payment_intent = stripe.PaymentIntent.create(
        amount=total_amount,
        currency=order.currency,
        payment_method_types=["card"],
    )

    return JsonResponse({
        "client_secret": payment_intent.client_secret,
        "currency": order.currency
    })


def order_detail(request, id):
    """
    Отображает страницу с деталями заказа.

    Аргументы:
        request (HttpRequest): Запрос от клиента.
        id (int): ID заказа.

    Возвращает:
        HttpResponse: HTML-страница с информацией о заказе.
    """
    order = get_object_or_404(Order, id=id)
    stripe_public_key = STRIPE_KEYS.get(order.currency, {}).get("public", settings.STRIPE_PUBLIC_KEY)

    return render(request, "products/order.html", {
        "order": order,
        "currency": order.currency,
        "stripe_public_key": stripe_public_key
    })


def success(request):
    """
    Отображает страницу успешного платежа.

    Аргументы:
        request (HttpRequest): Запрос от клиента.

    Возвращает:
        HttpResponse: HTML-страница успешного завершения оплаты.
    """
    return render(request, "products/success.html")


def cancel(request):
    """
    Отображает страницу отмененного платежа.

    Аргументы:
        request (HttpRequest): Запрос от клиента.

    Возвращает:
        HttpResponse: HTML-страница с информацией об отмене оплаты.
    """
    return render(request, "products/cancel.html")
