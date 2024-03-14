from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('pizzas', views.pizzas, name='pizza_type'),
    path('orders', views.orders, name='orders'),
    path('orders/<int:order_id>', views.order_detail, name='order_detail'),
    path('sizes', views.sizes, name='sizes'),
    path('sizes/<int:size_id>', views.size_detail, name='size_detail'),
    path('toppings', views.toppings, name='toppings'),
    path('toppings/<int:topping_id>', views.topping_detail, name='topping_detail'),
    path('crusts', views.crusts, name='crusts'),
    path('crusts/<int:crust_id>', views.crust_detail, name='crust_detail'),
]