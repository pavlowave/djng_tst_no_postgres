from django.urls import path
from modules.products.views import buy_item, item_detail, buy_order, order_detail, success, cancel

urlpatterns = [
    path('buy/<int:id>/', buy_item, name='buy_item'),
    path('item/<int:id>/', item_detail, name='item_detail'),
    path('buy/order/<int:id>/', buy_order, name='buy_order'),
    path('order/<int:id>/', order_detail, name='order_detail'),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
]
