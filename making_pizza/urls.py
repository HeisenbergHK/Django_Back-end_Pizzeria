# Defining URL patterns for making_pizza

from django.urls import path

from . import views

app_name = 'making_pizza'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # A page to show all the pizzas
    path('pizzas', views.pizzas, name='pizzas'),
    # A page for all orders of a costumer
    path('orders', views.orders, name='orders'),
    # A page for details about an order
    path('orders/<int:order_id>', views.order, name='order'),
    # New pizza
    path('new_order', views.new_order, name='new_order'),
]
